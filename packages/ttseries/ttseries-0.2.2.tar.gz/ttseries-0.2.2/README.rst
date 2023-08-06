=========
TT-series
=========

High performance engine to store Time series data in Redis.

|travis| |appveyor| |codecov| |codacy| |requirements| |docs| |pypi| |status| |pyversion| |download|

Redis Version required: >=5.0

TT-series is based on redis sorted sets to store the time-series data, `Sorted set`_ store scores with
unique numbers under a single key, but it has a weakness to store records, only unique members are allowed
and trying to record a time-series entry with the same value as a previous will result in only updating the score.
So TT-series provide a solution to solve that problem.

TT series normally can support redis version > 3.0, and will support **redis 5.0** in the future.

Tips
====

- **Max Store series length**

    For 32 bit Redis on a 32 bit platform redis sorted sets can support maximum 2**32-1 members,
    and for 64 bit redis on a 64 bit platform can support maximum 2**64-1 members.
    But large amount of data would cause more CPU activity, so better keep a balance with length of records is
    very important.

- **Only Support Python 3.6**

    Because python 3.6 changed the dictionary implementation for better performance,
    so in Python 3.6 dictionaries are insertion ordered.
    links: https://stackoverflow.com/questions/39980323/are-dictionaries-ordered-in-python-3-6

- **Performance Tips**

    With hiredis-py which it's targeted at speeding up parsing multi bulk replies from redis-server.
    So with a large amount of bulk data insertion or getting from redis-server, it can improve a great performance improvement.

Install
=======

Install python package from pip release::

    pip install ttseries


Documentation
=============

Features
--------

1. Quick inserts 100,000 records (1-2 sec) and get slice of 100,000 records (0.4-0.5 sec).

2. Support Data Serializer, Default Enable with MessagePack.

3. Support Data Compression.

4. In-order to void update previous records, Support Redis Hashes Time-Series storage format.

5. Support Numpy ndarray data type.

5. Support max length to auto to trim records.


Usage
-----


TT-series provide three implementation to support different kinds of time-series data type.

- ``RedisSimpleTimeSeries`` : Normally only base on Sorted sets to store records, previous records will impact the new inserting records which are **NOT** unique numbers.

- ``RedisHashTimeSeries``: Use Redis Sorted sets with Hashes to store time-series data, User don't need to consider the data repeatability with records, but sorted sets with hashes would take some extra memories to store the keys.

- ``RedisNumpyTimeSeries``: Support ``numpy.ndarray`` to store time-series records in redis sorted set.

- ``RedisPandasTimeSeries``: Support ``pandas.DataFrame`` to store time-series records in redis sorted set.

Serializer Data
---------------

TT-series use `MsgPack`_ to serializer data, because compare with other data serializer's solutions,
MsgPack provide a better performance solution to serialize data. If user don't want to use MsgPack to
serializer data, just inherit from ``ttseries.BaseSerializer`` class to implement the supported
serializer class methods.

Examples
--------

``RedisSimpleTimeSeries`` && ``RedisHashTimeSeries`` && ``RedisNumpyTimeSeries`` && ``RedisPandasTimeSeries``

Three series data implementation provide the same functions and methods, in the usage will
provide the difference in the methods.

Prepare data records:
^^^^^^^^^^^^^^^^^^^^^

.. sourcecode:: python

    from datetime import datetime
    from redis import StrictRedis

    now = datetime.now()
    timestamp = now.timestamp()

    series_data = []

    for i in range(1000):
        series_data.append((timestamp+i,i))

    client = StrictRedis() # redis client


Add records
^^^^^^^^^^^

.. sourcecode:: python

    from ttseries import RedisSimpleTimeSeries

    simple_series = RedisSimpleTimeSeries(client=client)

    key = "TEST:SIMPLE"

    simple_series.add_many(key, series_data)



Count records length
^^^^^^^^^^^^^^^^^^^^

Get the length of the records or need just get the length from timestamp span.

.. sourcecode:: python

    # get the records length
    simple_series.length(key)

    # result: ...: 1000

    # get the records length from start timestamp and end timestamp
    simple_series.count(key, from_timestamp=timestamp, end_timestamp=timestamp+10)

    # result: ...: 11


trim records
^^^^^^^^^^^^

Trim the records as the ASC.

.. sourcecode:: python

    simple_series.trim(key,10) # trim 10 length of records


delete timestamp span
^^^^^^^^^^^^^^^^^^^^^

Delete timestamp provide delete key or delete records from start timestamp to end timestamp.

.. sourcecode:: python

    simple_series.delete(key) # delete key with all records

    simple_series.delete(key, start_timestamp=timestamp) # delete key form start timestamp


Get Slice
^^^^^^^^^

Get slice form records provide start timestamp and end timestamp with **ASC** or **DESC** ordered.

Default Order: **ASC**

If user want to get the timestamp great than (>) or less than (<) which not including the timestamp record.
just use ``(timestamp`` which support ``<timestamp`` or ``>timestamp`` sign format like this.

.. sourcecode:: python

    # get series data from start timestamp ordered as ASC.

    simple_series.get_slice(key, start_timestamp=timestamp, acs=True)

    # get series data from great than start timestamp order as ASC
    simple_series.get_slice(key, start_timestamp="("+str(timestamp), asc=True)

    # get series data from start timestamp and limit the numbers with 500
    time_series.get_slice(key,start_timestamp=timestamp,limit=500)


iter
^^^^

yield item from records.

.. sourcecode:: python

    for item in simple_series.iter(key):
        print(item)



RedisNumpyTimeSeries
^^^^^^^^^^^^^^^^^^^^

Numpy array support provide ``numpy.dtype`` or just arrays with data.

Use ``numpy.dtype`` to create records. must provide ``timestamp_column_name`` and ``dtype`` parameters.

.. sourcecode:: python

    import numpy as np
    from ttseries import RedisNumpyTimeSeries

    dtype = [("timestamp","float64"),("value","i")]

    array = np.array(series_data, dtype=dtype)

    np_series = RedisNumpyTimeSeries(client=client, dtype=dtype, timestamp_column_name="timestamp")


Or just numpy array without dtype, but must provide ``timestamp_column_index`` parameter.

.. sourcecode:: python

    array = np.array(series_data)

    np_series = RedisNumpyTimeSeries(client=client,timestamp_column_index=0)


RedisPandasTimeSeries
^^^^^^^^^^^^^^^^^^^^^

Pandas TimeSeries use ``pandas.DataFrame`` to store time-series in redis.
To initialize the class must provide ``columns`` and ``dtypes`` parameters.

1. ``columns`` parameter indicates the column names of the ``pandas.DataFrame``.

2. ``dtypes`` indicates the dtype of each column in DataFrame, for example: ``{ "value1":"int64","value2":"float32"}``
   reference link: http://pbpython.com/pandas_dtypes.html

.. sourcecode:: python

    from datetime import datetime

    key = "AA:MIN"
    now = datetime.now()
    columns = ["value"]
    date_range = pandas.date_range(now, periods=10, freq="1min")

    data_frame = pandas.DataFrame([i + 1 for i in range(len(date_range))],
                                index=date_range, columns=columns)


    dtypes = {"value":"int64"}
    pandas_ts = RedisPandasTimeSeries(client=client, columns=columns, dtypes=dtypes)

Add
^^^

Add a time-series record to redis, ``series`` parameter indicates ``pandas.Series`` data type.
and especial the ``series`` name value data type must be the ``pandas.DatetimeIndex``.

.. sourcecode:: python

    series_item = data_frame.iloc[0]
    pandas_ts.add(key, series_item)


add_many
^^^^^^^^

Add large amount of ``pandas.DataFrame`` into redis, with the ``dataframe`` index data type must be
the ``pandas.DatetimeIndex``.
For better insert performance, just use ``chunks_size`` to split the dataframe into fixed ``chunks_size``
rows of dataframes.

.. sourcecode:: python

    pandas_ts.add_many(key, data_frame)


iter & Get
^^^^^^^^^^

retrieve records from redis sorted set, both of methods return ``pandas.Series``.

.. sourcecode:: python

    # yield all records data from redis
    for item in pandas_ts.iter(key):
        print(item)
    # return one record with specific timestamp
    pandas_ts.get(key, 1536157765.464465)

get_slice
^^^^^^^^^

retrieve records to slice with ``start timestamp`` or ``end timestamp``, with ``limit`` length.
return ``pandas.DataFrame``

.. sourcecode:: python

    # return records from start timestamp 1536157765.464465
    result_frame = pandas_ts.get_slice(key, start_timestamp=1536157765.464465)

    # return records from start timestamp 1536157765.464465 to end timestamp 1536157780.464465
    result2_frame = padas_ts.get_slice(key, start_timestamp=1536157765.464465, end_timestamp=1536157780.464465)


Benchmark
=========

just run ``make benchmark-init``, after then start ``make benchmark-test``.

Go to the benchmark directory there exist an example of the benchmark test reports.


TODO
====

1. Support Redis 5.0

3. Support Redis cluster.


Author
======

- Winton Wang


Donate
======


Contact
=======

Email: 365504029@qq.com


Reference
=========

links: https://www.infoq.com/articles/redis-time-series


.. _Sorted set: https://redis.io/commands#sorted_set
.. _MsgPack: http://msgpack.org

.. |travis| image:: https://travis-ci.org/nooperpudd/ttseries.svg?branch=master
    :target: https://travis-ci.org/nooperpudd/ttseries

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/ntlhwaagr5dqh341/branch/master?svg=true
    :target: https://ci.appveyor.com/project/nooperpudd/ttseries

.. |codecov| image:: https://codecov.io/gh/nooperpudd/ttseries/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nooperpudd/ttseries

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/154fe60c6d2b4e59b8ee18baa56ad0a9
    :target: https://www.codacy.com/app/nooperpudd/ttseries?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=nooperpudd/ttseries&amp;utm_campaign=Badge_Grade

.. |pypi| image:: https://img.shields.io/pypi/v/ttseries.svg
    :target: https://pypi.python.org/pypi/ttseries

.. |status| image:: https://img.shields.io/pypi/status/ttseries.svg
    :target: https://pypi.python.org/pypi/ttseries

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/ttseries.svg
    :target: https://pypi.python.org/pypi/ttseries

.. |requirements| image:: https://requires.io/github/nooperpudd/ttseries/requirements.svg?branch=master
    :target: https://requires.io/github/nooperpudd/ttseries/requirements/?branch=master

.. |docs| image:: https://readthedocs.org/projects/ttseries/badge/?version=latest
    :target: http://ttseries.readthedocs.io/en/latest/?badge=latest

.. |download| image:: https://pepy.tech/badge/ttseries
    :target: https://pepy.tech/project/ttseries



