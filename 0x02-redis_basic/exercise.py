#!/usr/bin/env python3

""" This contains a redis class known as Cache"""


import redis
from typing import Union
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
