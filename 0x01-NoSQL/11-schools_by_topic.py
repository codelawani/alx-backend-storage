#!/usr/bin/env python3
"""returns the list of school having a specific topic"""

from pymongo import collection
from typing import List


def schools_by_topic(mongo_collection: collection, topic: str) -> List:
    return list(mongo_collection.find({'topics': topic}))
