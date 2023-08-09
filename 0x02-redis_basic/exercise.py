#!/usr/bin/env python3
"""Redis Cache Class"""
from typing import Union
import redis
from uuid import uuid4


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, float, int, bytes]) -> str:
        key = str(uuid4())
        self._redis.set(key, data)
        return key
