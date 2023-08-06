from typing import TypeVar, Generic, Callable, Optional, List, Iterator, Any, Union, Dict
from time import sleep
from datetime import datetime
from bson.objectid import ObjectId, InvalidId
from pymongo import MongoClient, ReturnDocument
from pymongo.cursor import Cursor
from pymongo.database import Database
from mongomock import MongoClient as MockMongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.uri_parser import parse_uri
from contextlib import contextmanager
from glasskit.uorm.errors import AbortTransaction, InvalidShardId, ConfigurationError
from glasskit import ctx

MONGO_RETRY_MAX = 6
MONGO_RETRY_SLEEP = 3  # 3 seconds
T = TypeVar("T")


class NoCache:

    NAME = "NoCache"

    @staticmethod
    def has(_key: str) -> bool:
        return False

    @staticmethod
    def set(*_args, **_kwargs) -> bool:
        return False

    @staticmethod
    def get(_key: str) -> Any:
        return None

    @staticmethod
    def delete(_key: str) -> bool:
        return False


def intercept_pymongo_errors(func):
    def wrapper(*args, **kwargs):
        retries = MONGO_RETRY_MAX
        while True:
            retries -= 1
            try:
                return func(*args, **kwargs)
            except ServerSelectionTimeoutError:
                ctx.log.error(
                    "ServerSelectionTimeoutError in db module, retries left = %d",
                    retries,
                )
                if retries == MONGO_RETRY_MAX // 2:
                    ctx.log.error("trying to reinstantiate connection")
                    db_inst = args[0]  # self
                    db_inst.reset_conn()
                elif retries == 0:
                    ctx.log.error(
                        "ServerSelectionTimeoutError max retries exceeded, giving up"
                    )
                    raise
                sleep(MONGO_RETRY_SLEEP)

    return wrapper


class ObjectsCursor(Generic[T]):
    def __init__(self, cursor: Cursor, ctor: Callable[..., T], shard_id: Optional[str] = None):
        self.ctor = ctor
        self.cursor = cursor
        self._shard_id = shard_id

    def all(self) -> List[T]:
        return list(self)

    def limit(self, *args, **kwargs) -> 'ObjectsCursor[T]':
        self.cursor.limit(*args, **kwargs)
        return self

    def skip(self, *args, **kwargs) -> 'ObjectsCursor[T]':
        self.cursor.skip(*args, **kwargs)
        return self

    def sort(self, *args, **kwargs) -> 'ObjectsCursor[T]':
        self.cursor.sort(*args, **kwargs)
        return self

    def __iter__(self) -> Iterator[T]:
        for item in self.cursor:
            if self._shard_id:
                yield self.ctor(shard_id=self._shard_id, attrs=item)
            else:
                yield self.ctor(attrs=item)

    def __getitem__(self, item) -> T:
        attrs = self.cursor.__getitem__(item)
        if self._shard_id:
            return self.ctor(shard_id=self._shard_id, attrs=attrs)
        return self.ctor(attrs)

    def __getattr__(self, item):
        return getattr(self.cursor, item)


class Shard:
    @contextmanager
    def transaction(self):
        client = self.get_client()
        try:
            self._session = client.start_session()
            self._session.start_transaction()
            yield self._session
            self._session.commit_transaction()
        except Exception as e:
            self._session.abort_transaction()
            if not isinstance(e, AbortTransaction):
                raise
        finally:
            self._session.end_session()
            self._session = None

    def __init__(self, dbconf, shard_id=None, mock=False):
        self._config = dbconf
        self._client = None
        self._conn = None
        self._ro_conn = None
        self._shard_id = shard_id
        self._session = None
        self._mock = mock
        self.readonly = self._config.get("readonly", False)

    @property
    def _dbname(self) -> str:
        return parse_uri(self._config["uri"]).get("database")

    def get_client(self) -> Union[MongoClient, MockMongoClient]:
        if not self._client:
            client_kwargs = self._config.get("pymongo_extra", {})
            if self._mock:
                self._client = MockMongoClient(self._config["uri"], **client_kwargs)
            else:
                self._client = MongoClient(self._config["uri"], **client_kwargs)
        return self._client

    def reset_conn(self) -> None:
        self._client = None
        self._conn = None

    def init_conn(self) -> None:
        ctx.log.info("creating a new mongo connection")
        client = self.get_client()
        self._conn = client[self._dbname]

    @property
    def conn(self) -> 'Database':
        if self._conn is None:
            self.init_conn()
        return self._conn

    @intercept_pymongo_errors
    def get_obj(self,
                ctor: Callable[..., 'StorableModel'],
                collection: str,
                query: Union[str, Dict]) -> Union['StorableModel', None]:
        if not isinstance(query, dict):
            try:
                query = {"_id": ObjectId(query)}
            except InvalidId:
                pass
        data = self.conn[collection].find_one(query, session=self._session)
        if data:
            if self._shard_id:
                return ctor(shard_id=self._shard_id, attrs=data)
            else:
                return ctor(attrs=data)

        return None

    @intercept_pymongo_errors
    def get_obj_id(self, collection: str, query: Dict) -> Union[ObjectId, None]:
        obj = self.conn[collection].find_one(
            query, projection=(), session=self._session
        )
        if obj:
            return obj["_id"]
        return None

    @intercept_pymongo_errors
    def get_objs(self,
                 ctor: Callable[..., 'StorableModel'],
                 collection: str,
                 query: Dict,
                 **kwargs) -> ObjectsCursor:
        if self._session:
            kwargs["session"] = self._session
        cursor = self.conn[collection].find(query, **kwargs)
        return ObjectsCursor(cursor, ctor, shard_id=self._shard_id)

    @intercept_pymongo_errors
    def get_objs_projected(self,
                           collection: str,
                           query: Dict,
                           projection: Dict, **kwargs) -> Cursor:
        if self._session:
            kwargs["session"] = self._session
        cursor = self.conn[collection].find(query, projection=projection, **kwargs)
        return cursor

    @intercept_pymongo_errors
    def get_aggregated(self, collection: str, pipeline: List[Dict], **kwargs) -> Cursor:
        if self._session:
            kwargs["session"] = self._session
        cursor = self.conn[collection].aggregate(pipeline, **kwargs)
        return cursor

    @intercept_pymongo_errors
    def count_docs(self, collection: str, query: dict, **kwargs) -> int:
        return self.conn[collection].count_documents(query, **kwargs)

    def get_objs_by_field_in(self,
                             ctor: Callable[..., 'StorableModel'],
                             collection: str,
                             field: str,
                             values: List[Any],
                             **kwargs) -> ObjectsCursor:
        return self.get_objs(ctor, collection, {field: {"$in": values}}, **kwargs)

    @intercept_pymongo_errors
    def save_obj(self, obj: 'StorableModel') -> None:
        if obj.is_new:
            # object to_dict() method should always return all fields
            data = obj.to_dict(include_restricted=True)
            # although with the new object we shouldn't pass _id=null to mongo
            del data["_id"]
            inserted_id = (
                self.conn[obj.collection]
                .insert_one(data, session=self._session)
                .inserted_id
            )
            obj._id = inserted_id
        else:
            self.conn[obj.collection].replace_one(
                {"_id": obj._id},
                obj.to_dict(include_restricted=True),
                upsert=True,
                session=self._session,
            )

    @intercept_pymongo_errors
    def delete_obj(self, obj: 'StorableModel') -> None:
        if obj.is_new:
            return
        self.conn[obj.collection].delete_one({"_id": obj._id}, session=self._session)

    @intercept_pymongo_errors
    def find_and_update_obj(self, obj: 'StorableModel', update: Dict, when: Union[Dict, None] = None) -> None:
        query = {"_id": obj._id}
        if when:
            assert "_id" not in when
            query.update(when)

        new_data = self.conn[obj.collection].find_one_and_update(
            query, update, return_document=ReturnDocument.AFTER, session=self._session
        )
        if new_data and self._shard_id:
            new_data["shard_id"] = self._shard_id
        return new_data

    @intercept_pymongo_errors
    def delete_query(self, collection: str, query: Dict):
        return self.conn[collection].delete_many(query, session=self._session)

    @intercept_pymongo_errors
    def update_query(self, collection: str, query: Dict, update: Dict):
        return self.conn[collection].update_many(query, update, session=self._session)

    # SESSIONS
    @intercept_pymongo_errors
    def get_session(self, sid: str, collection: str = "sessions"):
        return self.conn[collection].find_one({"sid": sid})

    @intercept_pymongo_errors
    def update_session(self, sid: str, data: Dict, expiration, collection="sessions"):
        self.conn[collection].update(
            {"sid": sid}, {"sid": sid, "data": data, "expiration": expiration}, True
        )

    @intercept_pymongo_errors
    def cleanup_sessions(self, collection="sessions"):
        return self.conn[collection].remove({"expiration": {"$lt": datetime.now()}})[
            "n"
        ]


class DB:

    MONGODB_INFO_FIELDS = (
        "allocator",
        "bits",
        "debug",
        "gitVersion",
        "javascriptEngine",
        "maxBsonObjectSize",
        "modules",
        "ok",
        "openssl",
        "storageEngines",
        "sysInfo",
        "version",
        "versionArray",
    )

    @staticmethod
    def parse_shard_cfg(shard_name: str, shardcfg: Dict, extra: Dict) -> Dict:
        if "uri" not in shardcfg:
            raise ConfigurationError(f"uri is missing for shard {shard_name}")
        local_extra = shardcfg.get("pymongo_extra", {})
        return {"uri": shardcfg["uri"], "pymongo_extra": {**extra, **local_extra}}

    def parse_cfg(self, dbconf: Dict) -> Dict:
        config = {"shards": {}}
        global_extra = dbconf.get("pymongo_extra", {})
        if "meta" not in dbconf:
            raise ConfigurationError("meta section is missing from config")
        config["meta"] = self.parse_shard_cfg("meta", dbconf["meta"], global_extra)
        if "shards" in dbconf:
            for shard_id, shardcfg in dbconf["shards"].items():
                config["shards"][shard_id] = self.parse_shard_cfg(
                    shard_id, shardcfg, global_extra
                )
        return config

    def configure(self, dbconf: Dict, mock=False) -> None:
        config = self.parse_cfg(dbconf)
        self.__meta = Shard(config["meta"], mock=mock)
        self.__shards = {}
        if "shards" in config:
            for shard_id, config in config["shards"].items():
                self.__shards[shard_id] = Shard(config, shard_id=shard_id, mock=mock)
        self.initialized = True

    def __init__(self):
        self.__meta = None
        self.__shards = {}
        self.initialized = False
        self.l1c = NoCache()
        self.l2c = NoCache()

    @property
    def rw_shards(self) -> List[str]:
        return [
            shard_id for shard_id, shard in self.shards.items() if not shard.readonly
        ]

    @property
    def meta(self) -> Shard:
        if not self.initialized:
            raise RuntimeError("attempted to use uninitialized DB")
        return self.__meta

    @property
    def shards(self) -> Dict[str, Shard]:
        if not self.initialized:
            raise RuntimeError("attempted to use uninitialized DB")
        return self.__shards

    def get_shard(self, shard_id: str) -> Shard:
        if shard_id not in self.shards:
            raise InvalidShardId(shard_id)
        return self.shards[shard_id]

    def mongodb_info(self):
        def sys_info(raw_info):
            return {k: v for k, v in raw_info.items() if k in self.MONGODB_INFO_FIELDS}

        return dict(
            meta=sys_info(self.meta.conn.client.server_info()),
            shards={
                shard_id: sys_info(self.shards[shard_id].conn.client.server_info())
                for shard_id in self.shards
            },
        )

    def setup_cache(self, cache, level):
        if level not in (1, 2):
            raise ValueError("cache level must be either 1 or 2")
        attrs = ["has", "get", "set", "delete"]
        if not all(hasattr(cache, attr) for attr in attrs):
            raise TypeError(
                "a cache instance must have set, get, delete" " and has methods defined"
            )
        if level == 1:
            self.l1c = cache
        else:
            self.l2c = cache


db = DB()

from .models.storable_model import StorableModel
