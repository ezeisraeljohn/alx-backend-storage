#!/usr/bin/env python3
""" This module contains a function to list all the docs in a collection"""


def list_all(mongo_collection) -> list:
    """_summary_

    Args:
        mongo_collection: This a mongo collection

    Returns:
        list: Returns a list of documents in the mongo_collection
    """
    if mongo_collection is None:
        return []
    return mongo_collection.find()
