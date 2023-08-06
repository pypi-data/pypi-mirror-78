from ..uorm.db import db
from ..uorm.models.sharded_model import ShardedModel
from ..uorm.errors import MissingShardId
from ..uorm.models.fields import StringField, Field
from .mongo_mock_test import MongoMockTest

CALLABLE_DEFAULT_VALUE = 4


def callable_default():
    return CALLABLE_DEFAULT_VALUE


class TestModel(ShardedModel):
    field1: StringField(rejected=True, index=True, default="default_value")
    field2: Field(required=True)
    field3: Field(required=True, default="required_default_value")
    callable_default_field: Field(default=callable_default)


class TestShardedModel(MongoMockTest):

    def setUp(self) -> None:
        super().setUp()
        for shard_id in db.shards:
            TestModel.destroy_all(shard_id)

    def tearDown(self) -> None:
        for shard_id in db.shards:
            TestModel.destroy_all(shard_id)
        super().tearDown()

    def test_init(self):
        model = TestModel({"field1": "value"})
        self.assertEqual(model.field1, "value")
        model._before_save()
        model._before_delete()

    def test_shard(self):
        model = TestModel({"field2": "value"})
        self.assertIsNone(model._shard_id)
        self.assertRaises(MissingShardId, model.save)

        shard_id = db.rw_shards[0]
        model = TestModel(shard_id=shard_id, attrs={"field2": "value"})
        self.assertEqual(model._shard_id, shard_id)
        model.save()
