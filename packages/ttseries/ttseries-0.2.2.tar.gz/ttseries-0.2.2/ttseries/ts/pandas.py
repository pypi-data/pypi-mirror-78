# encoding:utf-8
import itertools
from datetime import datetime

import numpy
import pandas as pd

import ttseries.utils
from ttseries.exceptions import RedisTimeSeriesError
from ttseries.ts.sample import RedisSampleTimeSeries


class RedisPandasTimeSeries(RedisSampleTimeSeries):
    """
    Base on Pandas DataFrame to store time series data into redis sorted set.
    """

    def __init__(self, redis_client, columns,
                 index_name="timestamp", dtypes=None,
                 max_length=100000, *args, **kwargs):
        """
        :param redis_client: redis client instance, only test with redis-py client.
        :param timezone: datetime timezone
        :param columns: pandas DataFrame columns names' list
        :param dtypes: pandas columns data type, example: {"value":"int64","value2":"float64"}
        :param max_length: int, max length of data to store the time-series data.
        :param args:
        :param kwargs:
        """
        super(RedisPandasTimeSeries, self).__init__(redis_client=redis_client,
                                                    max_length=max_length, *args, **kwargs)

        if index_name in columns:
            raise RedisTimeSeriesError("columns name can't contain index name")

        self.columns = columns
        self.dtypes = dtypes
        self.index_name = index_name

    def _timestamp_exist(self, name, data_frame):
        """
        sorted timestamp and check exist repeated timestamp
        :param name:
        :param data_frame:
        :return:
        """
        date_index = data_frame.index

        start_timestamp = data_frame.idxmin()
        start_timestamp = start_timestamp[0].to_pydatetime().timestamp()

        end_timestamp = data_frame.idxmax()
        end_timestamp = end_timestamp[0].to_pydatetime().timestamp()

        exist_length = self.count(name, start_timestamp, end_timestamp)

        if exist_length > 0:

            filter_data_frame = self.get_slice(name, start_timestamp, end_timestamp)

            filter_timestamps_index = filter_data_frame.index

            # check repeated data
            duplicated = numpy.intersect1d(filter_timestamps_index.to_pydatetime(), date_index.to_pydatetime())

            if duplicated.size > 0:
                raise RedisTimeSeriesError("add duplicated timestamp into redis -> timestamp:")

    def _validate_append_data(self, data_frame):
        """
        validate repeated index
        :return:
        """
        date_index = data_frame.index
        unique_date = date_index[date_index.duplicated()].unique()
        if not unique_date.empty:
            raise RedisTimeSeriesError("DataFrame index can't contains duplicated index data")

    def _auto_trim_array(self, name, array_data):
        """
        auto to trim the redis sorted set base on the max length.

        before to insert the data into redis, check the current stored array length and
        trim the insert data array with max length
        :param name:
        :param array_data:
        :return:
        """
        length = array_data.size
        # auto trim array
        if length + self.length(name) >= self.max_length:
            trim_length = length + self.length(name) - self.max_length
            self.trim(name, trim_length)

        if length > self.max_length:
            array_data = array_data.iloc[length - self.max_length:]
        return array_data

    def add_many(self, name, data_frame, chunks_size=2000):
        """
        add large amount of pandas.DataFrame, the dataframe index type should be the pandas.DateTimeIndex.
        or a kind of timestamp index.
        :param name: redis key
        :param data_frame: pandas.DataFrame
        :param chunks_size: int, split data into chunk, optimize for redis pipeline
        """
        self._validate_key(name)
        if not isinstance(data_frame, pd.DataFrame):
            raise TypeError("data parameter's type must be a pandas.DataFrame")
        if not isinstance(data_frame.index, pd.DatetimeIndex):
            raise TypeError("DataFrame index must be pandas.DateTimeIndex type")
        data_frame = data_frame.sort_index()

        # check timestamp repeated
        self._validate_append_data(data_frame)

        # auto trim timestamps
        array = self._auto_trim_array(name, data_frame)
        # validate timestamp exist
        self._timestamp_exist(name, array)
        for chunk_array in ttseries.utils.chunks_np_or_pd_array(array, chunks_size):
            # To preserve dtypes while iterating over the rows, it is better
            # to use :meth:`itertuples` which returns namedtuples of the values
            # and which is generally faster than ``iterrows``

            data_pairs = {self._serializer.dumps(row[1:]): row[0].to_pydatetime().timestamp()
                          for row in chunk_array.itertuples()}

            def pipe_func(_pipe):
                _pipe.zadd(name, data_pairs)

            self.transaction_pipe(pipe_func, watch_keys=name)

    def add(self, name, series):
        """
        :param name: redis key
        :param series: pandas.Series
        :return: bool
        """
        self._validate_key(name)

        if isinstance(series, pd.Series) and hasattr(series.name, "timestamp"): # validate datetime

            series_time = series.name.to_pydatetime()
            timestamp = series_time.timestamp()

            with self._lock:
                if not self.exist_timestamp(name, timestamp):
                    values = series.tolist()
                    data = self._serializer.dumps(values)
                    if self.length(name) == self.max_length:
                        self.client.zpopmin(name)
                    return self.client.zadd(name, {data: timestamp})
        else:
            raise RedisTimeSeriesError("Please check series Type or "
                                       "series name value is not pandas.DateTimeIndex type")

    def get(self, name: str, timestamp: float):
        """
        get one item by timestamp
        :param name:
        :param timestamp:
        :return: pandas.Series
        """
        data = super(RedisPandasTimeSeries, self).get(name, timestamp)
        if data:
            date = datetime.fromtimestamp(timestamp)
            return pd.Series(data=data, index=self.columns, name=date)

    def iter(self, name, count=None):
        """
        iterable all data with count values
        :param name: redis key
        :param count: the count length of records
        :return: yield pandas.Series
        """
        for timestamp, data in super(RedisPandasTimeSeries, self).iter(name, count):
            date = datetime.fromtimestamp(timestamp)
            yield pd.Series(data=data, index=self.columns, name=date)

    def get_slice(self, name, start_timestamp=None,
                  end_timestamp=None, limit=None, asc=True):
        """
        return a slice pandas.DataFrame from start timestamp to end timestamps,
        if start timestamp is None, and end timestamp is None, will retrieve all records from
        redis sorted set.

        :param name: redis key
        :param start_timestamp: float, start timestamp
        :param end_timestamp: float, end timestamp
        :param limit: int,
        :param asc: bool, sorted as the timestamp values
        :return: pandas.DataFrame
        """

        results = self._get_slice_mixin(name, start_timestamp,
                                        end_timestamp, limit, asc)

        if results:
            # [(b'\x81\xa5value\x00', 1526008483.331131),...]

            data = list(itertools.starmap(lambda serializer, timestamp:
                                          [datetime.fromtimestamp(timestamp)] +
                                          self._serializer.loads(serializer),
                                          results))

            data_frame = pd.DataFrame.from_records(data, columns=[self.index_name] + self.columns)
            data_frame = data_frame.set_index(self.index_name)
            if self.dtypes:
                data_frame = data_frame.astype(dtype=self.dtypes)
            return data_frame
