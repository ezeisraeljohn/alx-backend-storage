#!/usr/bin/env python3

""" Returns all students sorted by average score"""


def top_students(mongo_collection):
    """
    Return a list of students sorted by their average score.
    Args:
        mongo_collection: The MongoDB collection.
    """
    pipeline = [
        {"$unwind": "$topics"},
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$topics.score"},
            }
        },
        {"$sort": {"averageScore": -1}},
    ]

    return list(mongo_collection.aggregate(pipeline))
