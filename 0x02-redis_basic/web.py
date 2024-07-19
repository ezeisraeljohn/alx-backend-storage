#!/usr/bin/env python3

import requests
import redis


def get_page(url: str) -> str:
    """This will return the html of a url and cache the url

    Args:
        url (str): The url
    Returns:
        str: The return value
    """
    response = requests.get(url=url)
    redis_instance = redis.Redis()
    redis_instance.incr(f"count:{url}", 1)
    redis_instance.expire(f"count:{url}", 10)
    return response.text
