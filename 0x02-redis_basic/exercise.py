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

    @property
    def redis_instance(self):
        return self._redis

    def call_history(method: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            inputs = str(args)
            outputs = method(self, inputs)
            self._redis.rpush(
                "{}:outputs".format(method.__qualname__),
                outputs)
            self._redis.rpush("{}:inputs".format(method.__qualname__), inputs)
            return outputs

        return wrapper

    def count_calls(method: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            self._redis.incr(method.__qualname__, 1)
            return method(self, *args, **kwargs)

        return wrapper

    @count_calls
    @call_history
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


def replay(method: Callable[..., Any]) -> None:
    """Tells you all the transaction that has been going on for a method

    Args:
        method (Callable[..., Any]): The method

    Returns:
        None
    """
    redis_instance = redis.Redis()
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)
    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)
    class_method = "Cache.store"
    print("{} was called {} times:".format(class_method, len(inputs)))
    for elements in zip(inputs, outputs):
        new_input = elements[0].decode("utf-8")
        new_output = elements[1].decode("utf-8")
        print("{}(*{}) -> {}".format(class_method, new_input, new_output))
