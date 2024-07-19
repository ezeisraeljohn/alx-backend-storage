#!/usr/bin/env python3
""" The Module that caches a website's url"""
import requests
import redis
from typing import Callable, Any
import functools


def my_decorator(method: Callable) -> Any:
    """Decorates a function to store a cache.

    Args:
        method (Callable): The method.

    Returns:
        Any: Any
    """

    @functools.wraps(method)
    def wrapper(url):
        """Function that really does the decoration

        Args:
            url (_type_): The url

        Returns:
            _type_: return the method
        """
        redis_instance = redis.Redis()
        redis_instance.incr("count:{}".format(url), 1)
        redis_instance.expire("count:{}".format(url), 10)
        return method(url)

    return wrapper


@my_decorator
def get_page(url: str) -> str:
    """This will return the html of a url and cache the url

    Args:
        url (str): The url
    Returns:
        str: The return value
    """
    response = requests.get(url=url)
    return response.text
