#!/usr/bin/env python3
"""Redis Cache Class"""
from typing import Callable, Any, Optional, Union
from functools import wraps
import redis
from uuid import uuid4


def count_calls(f: Callable) -> Callable:
    """
    Decorator that counts the number of times a function is called
    and increments the count in Redis.

    Args:
        f (Callable): The function to be wrapped.

    Returns:
        Callable: The wrapper function.
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count
        and calls the original function.

        Args:
            self: Instance of the class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: Result of the original function call.
        """
        self._redis.incr(f.__qualname__)
        return f(self, *args, **kwargs)
    return wrapper


def call_history(f: Callable) -> Callable:
    """
    Decorator that records the inputs and outputs
    of a function call in Redis.

    Args:
        f (Callable): The function to be wrapped.

    Returns:
        Callable: The wrapper function.
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that records function inputs
        and outputs in Redis and calls the original function.

        Args:
            self: Instance of the class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any: Result of the original function call.
        """
        in_key = f'{f.__qualname__}:inputs'
        out_key = f'{f.__qualname__}:outputs'
        self._redis.rpush(in_key, str(*args))
        output = f(self, *args)
        self._redis.rpush(out_key, output)
        return output
    return wrapper


class Cache:
    """
    A class that provides caching functionality
    using Redis and decorators.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache instance.

        Returns:
            None
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, float, int, bytes]) -> str:
        """
        Stores data in the cache and returns a unique key.

        Args:
            data (Union[str, float, int, bytes]): The data to be stored.

        Returns:
            str: The unique key associated with the stored data.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        Retrieves data from the cache using the given key.

        Args:
            key (str): The key associated with the cached data.
            fn (Callable, optional): A function to transform
            the retrieved value. Defaults to None.

        Returns:
            Union[str, float, int, bytes]: The retrieved data.
        """
        value = self._redis.get(key)
        return fn(value) if fn else value

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from the cache using the given key.

        Args:
            key (str): The key associated with the cached string.

        Returns:
            str: The retrieved string value.
        """
        return self.get(key, fn=lambda v: v.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from the cache using the given key.

        Args:
            key (str): The key associated with the cached integer.

        Returns:
            int: The retrieved integer value.
        """
        return self.get(key, fn=lambda v: int(v))


def replay(f: Callable):
    """
    Replays the history of a function's calls
    and their inputs and outputs.

    Args:
        f: The function whose history will be replayed.

    Returns:
        None
    """
    key = f.__qualname__
    in_key = key + ':inputs'
    out_key = key + ':outputs'
    count = f.__self__.get_int(key)
    redis = f.__self__._redis
    inputs = redis.lrange(in_key, 0, -1)
    outputs = redis.lrange(out_key, 0, -1)
    print(f'Cache.store was called {count} times')
    for input, output in zip(inputs, outputs):
        output = output.decode('utf-8')
        input = input.decode('utf-8')
        print(f"Cache.store(*({input},)) -> {output}")
