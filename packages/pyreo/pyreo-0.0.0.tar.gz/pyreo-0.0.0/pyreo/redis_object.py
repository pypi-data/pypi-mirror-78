"""
https://en.wikipedia.org/wiki/Pointer_machine
"""
from typing import Any, FrozenSet

from pyreo.mapper import _RedisMapper_


class ReObject:
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        r_mapper = _RedisMapper_()
        obj._excl_ = set(dir(obj))
        obj._rdict_ = r_mapper
        return obj

    def __setattr__(self, name: str, value: Any) -> None:
        if not excl(name, self):
            self._rdict_[name] = value
        super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        if not excl(name, self):
            del self._rdict_[name]

    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)

        if not excl(name, self):
            try:
                return self._rdict_[name]
            except KeyError as ke:
                raise AttributeError(str(ke))
        return value


def excl(
    name,
    re_obj: ReObject,
    _cls_excl_: FrozenSet[str] = frozenset(
        # Statically, anything that is need for the `dir` function to work and
        # also the ReObject things
        ("__class__", "__dir__", "_excl_", "_rdict_")
    ),
):
    return name in _cls_excl_ or name in re_obj._excl_
