#!/usr/bin/env python3
"""Redis Cache Class"""
from typing import Any, Callable, Union
import redis
from uuid import uuid4
from functools import wraps


def count_calls(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        self._redis.incrby(f.__qualname__, 1)
        return f(self, *args, **kwargs)
    return wrapper


def call_history(f: Callable[..., Any]) -> callable[..., Any]:
    @wraps(f)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        in_key = f'{f.__qualname__}:inputs'
        out_key = f'{f.__qualname__}:outputs'
        self._redis.rpush(in_key, str(*args))
        output = f(self, *args)
        self._redis.rpush(out_key, output)
    return wrapper


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, float, int, bytes]) -> str:
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, float, int, bytes]:
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        return self.get(key, fn=lambda v: v.decode('utf-8'))

    def get_int(self, key: str) -> int:
        return self.get(key, fn=lambda v: int(v))
