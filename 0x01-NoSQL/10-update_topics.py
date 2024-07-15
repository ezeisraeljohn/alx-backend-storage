#!/usr/bin/env python3

""" This module contains a function that updates documents"""


def update_topics(mongo_collection, name, topics):
    """Updates documents

    Args:
        mongo_collection (_type_): The collection instance
        name (_type_): name to filter and update document
        topics (_type_): The topics
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
