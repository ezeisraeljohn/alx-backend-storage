#!/usr/bin/env python3

""" Contains a function that adds a new document"""


def insert_school(mongo_collection, **kwargs):
    """This function creates a new mongodb document and return the _id

    Args:
        mongo_collection (_type_): The mongodb collection instance

    Returns: The _id of the newly created document
    """
    new_document = {key: value for key, value in kwargs.items()}
    document_id = mongo_collection.insert_one(new_document).inserted_id

    return document_id
