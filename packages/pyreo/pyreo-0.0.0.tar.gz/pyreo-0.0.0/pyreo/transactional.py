from pyreo.mapper import _RedisMapper_


class ReObjectTransaction:
    def __init__(self, redis_mapper: _RedisMapper_) -> None:
        self.redis_mapper = redis_mapper
        self._results = None

    def __enter__(self) -> None:
        self.redis_mapper.push_pipeline()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self._results = self.redis_mapper.pop_pipeline()

    class TransactionNotDone(Exception):
        pass

    @property
    def results(self):
        if self._results is None:
            raise self.TransactionNotDone
        return self._results

    def __getitem__(self, idx: int):
        return self.results[idx]
