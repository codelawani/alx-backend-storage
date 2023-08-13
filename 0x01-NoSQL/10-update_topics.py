#!/usr/bin/env python3
"""changes all topics of a school document based on the name"""


from typing import List
from pymongo import collection


def update_topics(mongo_collection: collection, name: str, topics: List[str]) -> None:
    mongo_collection.update_one({'name': name}, {'$set': {
        'topics': topics
    }})
