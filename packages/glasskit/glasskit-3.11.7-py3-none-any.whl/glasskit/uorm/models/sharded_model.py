from typing import Dict, Any, Union, List
from functools import partial
from pymongo.cursor import Cursor
from .storable_model import StorableModel
from ..errors import MissingShardId
from glasskit.errors import NotFound
from ..db import db, Shard, ObjectsCursor
from ..utils import resolve_id, ObjectId


class ShardedModel(StorableModel):

    def __init__(self, attrs: Dict[str, Any], shard_id: str = None):
        super().__init__(attrs)
        self._shard_id = shard_id
        if not self.is_new and self._shard_id is None:
            from traceback import print_stack
            print_stack()
            raise MissingShardId(
                "ShardedModel from database with missing shard_id - this must be a bug")

    @classmethod
    def create(cls, shard_id=None, **attrs) -> 'ShardedModel':
        return cls(attrs, shard_id)

    @property
    def _db(self) -> Shard:
        return db.shards[self._shard_id]

    def save(self, skip_callback=False, invalidate_cache=True) -> None:
        if self._shard_id is None:
            raise MissingShardId(
                "ShardedModel must have shard_id set before save")
        super().save(skip_callback, invalidate_cache)

    def _refetch_from_db(self) -> 'ShardedModel':
        return self.find_one(self._shard_id, {"_id": self._id})

    @classmethod
    def _get_possible_databases(cls):
        return list(db.shards.values())

    @classmethod
    def find(cls, shard_id: str, query: Dict = None, **kwargs) -> ObjectsCursor:
        if not query:
            query = {}
        return db.get_shard(shard_id).get_objs(
            cls._ctor,
            cls.collection,
            cls._preprocess_query(query),
            **kwargs
        )

    @classmethod
    def aggregate(cls, shard_id: str, pipeline: List, query: Dict = None, **kwargs) -> Cursor:
        if not query:
            query = {}
        pipeline = [{"$match": cls._preprocess_query(query)}] + pipeline
        return db.get_shard(shard_id).get_aggregated(cls.collection, pipeline, **kwargs)

    @classmethod
    def find_projected(cls, shard_id: str, query: Dict = None, projection=('_id',), **kwargs) -> Cursor:
        if not query:
            query = {}
        return db.get_shard(shard_id).get_objs_projected(
            cls.collection,
            cls._preprocess_query(query),
            projection=projection,
            **kwargs
        )

    @classmethod
    def find_one(cls, shard_id: str, query: Dict, **kwargs) -> 'ShardedModel':
        return db.get_shard(shard_id).get_obj(
            cls._ctor,
            cls.collection,
            cls._preprocess_query(query),
            **kwargs
        )

    @classmethod
    def get(cls, shard_id: str, expression: Any, raise_if_none=None) -> Union['ShardedModel', None]:
        if expression is None:
            return None
        expression = resolve_id(expression)
        if isinstance(expression, ObjectId):
            query = {"_id": expression}
        else:
            expression = str(expression)
            query = {cls.KEY_FIELD: expression}
        res = cls.find_one(shard_id, query)
        if res is None and raise_if_none is not None:
            if isinstance(raise_if_none, Exception):
                raise raise_if_none
            else:
                raise NotFound(f"{cls.__name__} not found")
        return res

    @classmethod
    def cache_get(cls, shard_id: str, expression: Any, raise_if_none=None) -> Union['ShardedModel', None]:
        if expression is None:
            return None
        cache_key = f"{cls.collection}.{shard_id}.{expression}"
        getter = partial(cls.get, shard_id, expression, raise_if_none)
        constructor = partial(cls, shard_id=shard_id)
        obj = cls._cache_get(cache_key, getter, constructor)
        obj.shard_id = shard_id
        return obj

    def invalidate(self, _id=None) -> None:
        if _id is None:
            _id = self._id
        cache_key_id = f"{self.collection}.{self._shard_id}.{_id}"
        self._invalidate(cache_key_id)
        if self.KEY_FIELD is not None and self.KEY_FIELD != "_id":
            cache_key_keyfield = f"{self.collection}.{self._shard_id}.{getattr(self, self.KEY_FIELD)}"
            self._invalidate(cache_key_keyfield)

    @classmethod
    def destroy_all(cls, shard_id: str) -> None:
        # warning: being a faster method than traditional model manipulation,
        # this method doesn't provide any lifecycle callback for independent
        # objects
        db.get_shard(shard_id).delete_query(
            cls.collection, cls._preprocess_query({}))

    @classmethod
    def destroy_many(cls, shard_id: str, query: Dict) -> None:
        # warning: being a faster method than traditional model manipulation,
        # this method doesn't provide any lifecycle callback for independent
        # objects
        db.get_shard(shard_id).delete_query(
            cls.collection, cls._preprocess_query(query))

    @classmethod
    def update_many(cls, shard_id: str, query: Dict, attrs: Dict) -> None:
        # warning: being a faster method than traditional model manipulation,
        # this method doesn't provide any lifecycle callback for independent
        # objects
        db.get_shard(shard_id).update_query(
            cls.collection, cls._preprocess_query(query), attrs)

    def __repr__(self) -> str:
        attributes = [f"_shard_id=%r" % self._shard_id]
        attributes += ["%s=%r" % (a, getattr(self, a))
                      for a in self.__fields__]
        return '%s(\n    %s\n)' % (self.__class__.__name__, ',\n    '.join(attributes))
