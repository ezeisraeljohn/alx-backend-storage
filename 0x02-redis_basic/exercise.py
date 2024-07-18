#!/usr/bin/env python3

""" This contains a redis class known as Cache"""


import redis
import uuid
from functools import wraps
from typing import Union, Callable, Any


class Cache:
    """The Cache class to store all cached data"""

    def __init__(self) -> None:
        """The Init Method"""
        self._redis = redis.Redis()
        self._redis.flushdb()
        self.store = self.count_calls(self.store)

    def count_calls(self, method: Callable) -> Callable:
        @wraps(method)
        def wrapper(*args, **kwargs):
            self._redis.incr(method.__qualname__, 1)
            return method(*args, **kwargs)

        return wrapper

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

    def get_str(self, key: str, fn) -> str:
        """This will return the string rep of the value

        Args:
            key (str): The key used to save the value
            fn (function): The Callable

        Returns:
            str: The string to return
        """
        value = self.get(key, fn)
        return str(value)

    def get_int(self, key: str, fn: Union[Callable] = None) -> int:
        """Returns a value for this function

        Args:
            key (str): The key
            fn (Union[Callable], optional): The callable. Defaults to None.

        Returns:
            int: returns an int
        """
        value = self.get(self, key, fn)
        return int(value)
