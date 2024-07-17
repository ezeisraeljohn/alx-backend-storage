#!/usr/bin/env python3

""" This contains a redis class known as Cache"""


import redis
from typing import Union, Callable, Any
import uuid


class Cache:
    """The Cache class to store all cached data"""

    def __init__(self) -> None:
        """The Init Method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Returns a the key of a stored value

        Args:
            data (Union[str, bytes, int, float]): The data to store in the db

        Returns:
            str: Returns the key representing the value stored in the db
        """
        key = uuid.uuid4()
        self._redis.set(str(key), data)
        return str(key)

    def get(self, key: str, fn: Union[Callable] = None) -> Any:
        """Returns a value to its original type

        Args:
            key (_type_): _description_
            fn (Union[Callable], optional): The original callable. Defaults
            to None.

            Returns:
                Any: Returns the original rep of the data
        """

        value = self._redis.get(key)

        if value and not fn:
            return value

        if fn:
            return fn(value)
