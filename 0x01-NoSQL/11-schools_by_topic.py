#!/usr/bin/env python3

""" This module contains function that updates"""


def schools_by_topic(mongo_collection, topic):
    """The function that

    Args:
        mongo_collection (_type_): _description_
        topic (_type_): _description_
    """
    return mongo_collection.find({"topics": {"$in": [topic]}})
