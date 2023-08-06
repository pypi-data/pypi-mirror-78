from unittest import TestCase
from ..uorm.db import db
from ..context import ctx, ContextError
from ..queue import DummyQueue


class MongoMockTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        db.configure(
            {
                "meta": {"uri": "mongodb://fake_server:27017/unittest_meta"},
                "shards": {
                    "s1": {"uri": "mongodb://fake_server:27017/unittest_s1"},
                    "s2": {"uri": "mongodb://fake_server:27017/unittest_s2"},
                    "s3": {"uri": "mongodb://fake_server:27017/unittest_s3"},
                    "s4": {"uri": "mongodb://fake_server:27017/unittest_s4"},
                },
            },
            mock=True,
        )
        try:
            _ = ctx.queue
            del ctx.queue
        except ContextError:
            pass
        ctx.queue = DummyQueue({})

