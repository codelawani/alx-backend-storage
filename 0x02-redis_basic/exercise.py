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


def call_history(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(self, *args: Any, **kwargs: Any) -> Any:
        in_key = f'{f.__qualname__}:inputs'
        out_key = f'{f.__qualname__}:outputs'
        self._redis.rpush(in_key, str(*args))
        output = f(self, *args)
        self._redis.rpush(out_key, output)
        return output
    return wrapper


class Cache:
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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


def replay(f):
    key = f.__qualname__
    in_key = key + ':inputs'
    out_key = key + ':outputs'
    count = cache._redis.get(key)
    inputs = cache._redis.lrange(in_key, 0, -1)
    outputs = cache._redis.lrange(out_key, 0, -1)
    print(f'Cache.store was called {count} times')
    for input, output in zip(inputs, outputs):
        print(f"Cache.store(*('{input}',)) -> {str(output)}")

# cache = Cache()

# s1 = cache.store("first")
# print(s1)
# s2 = cache.store("secont")
# print(s2)
# s3 = cache.store("third")
# print(s3)

# inputs = cache._redis.lrange(
#     "{}:inputs".format(cache.store.__qualname__), 0, -1)
# outputs = cache._redis.lrange(
#     "{}:outputs".format(cache.store.__qualname__), 0, -1)


# print("inputs: {}".format(inputs))
# print("outputs: {}".format(outputs))


cache = Cache()
cache.store('foo')
cache.store('bar')
cache.store(42)
replay(cache.store)
