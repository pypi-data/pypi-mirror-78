from functools import wraps
from typing import Any

from pyreo.transactional import ReObjectTransaction


def pipelined(func):
    @wraps(func)
    def inner(instance, *args: Any, **kwargs: Any) -> Any:
        with ReObjectTransaction(instance._rdict_):
            return func(instance, *args, **kwargs)

    return inner