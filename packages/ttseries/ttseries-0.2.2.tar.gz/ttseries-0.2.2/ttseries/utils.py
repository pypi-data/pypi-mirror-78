# encoding:utf-8
import itertools

import numpy as np

from .exceptions import RepeatedValueError


def check_array_repeated(array):
    """
    check array repeated keys, if exist repeated keys will raise RepeatedValueError
    :param array: [(key,value),....]
    :raise RepeatedValueError
    """
    keys, _ = itertools.zip_longest(*array)
    keys_dict = {}
    for key in keys:
        if key in keys_dict:
            raise RepeatedValueError("repeated value:", key)
        else:
            keys_dict.setdefault(key)


def chunks_np_or_pd_array(array, chunk_size: int = 2000):
    """
    split numpy array into chunk array
    :param array: numpy array
    :param chunk_size: int, split data as the length of chunks
    :return: yield numpy.ndarray
    """
    length = array.shape[0]
    if length > chunk_size:
        chunk = int(length / chunk_size)
        for item in np.array_split(array, chunk):
            yield item
    else:
        yield array


def chunks(iterable, chunk_size: int = 1000):
    """
    split iterable array into chunks

    >>> chunks(range(6),chunk_size=2)
    ... [(0,1),(2,3),(4,5)]
    :param iterable: list, iter
    :param chunk_size: chunk split size
    :return: yield iterable values
    """
    iter_data = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(iter_data, chunk_size))
        if not chunk:
            return
        yield chunk
