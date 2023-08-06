from pickle import dumps, loads
from typing import MutableMapping, Tuple
from uuid import uuid4

from redis import Redis

from pyreo.transactional import ReObjectTransaction


class _RedisMapper_(MutableMapping):
    def __init__(self) -> None:
        self.redis_stack = [Redis(host="localhost", port=6379, db=0)]
        self.hash = uuid4()

    @property
    def connection(self):
        return self.redis_stack[-1]

    def push_pipeline(self) -> Tuple[Redis]:
        self.redis_stack.append(self.redis_stack[-1].pipeline())
        return tuple(self.redis_stack)

    def pop_pipeline(self):
        popped = self.redis_stack[-1]
        self.redis_stack = self.redis_stack[:-1]
        results = popped.execute()
        popped.reset()
        return results

    def __setitem__(self, k, v) -> None:
        pickled_value = dumps(v)
        self.connection.hset(self.hash.hex, k, pickled_value)

    def __getitem__(self, k) -> None:
        with ReObjectTransaction(self) as redis_get:
            self.connection.hget(self.hash.hex, k)
            self.connection.hexists(self.hash.hex, k)

        got_value, had_value = redis_get
        if not had_value:
            raise KeyError(f"{self.__class__.__name__} has no attribute {k}")
        return loads(got_value)

    def __delitem__(self, k) -> None:
        self.connection.hdel(self.hash.hex, k)

    def __contains__(self, __x: object) -> bool:
        return self.connection.hexists(self.hash.hex, __x)

    def __iter__(self):
        return self.connection.hkeys(self.hash.hex)

    def __len__(self):
        return self.connection.hlen(self.hash.hex)

    def update(self, *args, **kwargs) -> None:
        super().update(*args, **kwargs)

    def setdefault(self, *args, **kwargs):
        return super().setdefault(*args, **kwargs)