import itertools
from bson import ObjectId
from .mongo_mock_test import MongoMockTest
from ..uorm.db import db
from ..uorm.models.fields import Field
from ..uorm.models.submodel import StorableSubmodel, ShardedSubmodel
from ..uorm.errors import WrongSubmodel, MissingSubmodel, IntegrityError


class TestStorableSubmodel(MongoMockTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class TestBaseModel(StorableSubmodel):
            COLLECTION = "test"
            field1: Field()
            field2: Field()

        class Submodel1(TestBaseModel):

            SUBMODEL = "submodel1"
            field3: Field()

        class Submodel2(TestBaseModel):

            SUBMODEL = "submodel2"
            field4: Field()

        TestBaseModel.register_submodel(Submodel1.SUBMODEL, Submodel1)
        TestBaseModel.register_submodel(Submodel2.SUBMODEL, Submodel2)

        cls.base_model = TestBaseModel
        cls.submodel1 = Submodel1
        cls.submodel2 = Submodel2

    def setUp(self) -> None:
        super().setUp()
        self.base_model.destroy_all()

    def test_wrong_input(self):
        with self.assertRaises(WrongSubmodel):
            self.submodel1({"_id": ObjectId(), "field1": "value", "submodel": "wrong"})
        with self.assertRaises(MissingSubmodel):
            self.submodel1({"_id": ObjectId(), "field1": "value"})
        with self.assertRaises(IntegrityError):
            self.submodel1({"field1": "value", "submodel": "my_submodel"})
        with self.assertRaises(WrongSubmodel):
            obj = self.submodel1({"field1": "value"})
            obj.submodel = "wrong"
            obj.save()

    def test_submodel_field(self):
        obj = self.submodel1({})
        self.assertTrue(hasattr(obj, "submodel"))
        self.assertEqual(obj.submodel, self.submodel1.SUBMODEL)
        obj.save()
        obj.reload()
        self.assertEqual(obj.submodel, self.submodel1.SUBMODEL)
        db_obj = self.submodel1.get(obj._id)
        self.assertEqual(db_obj.submodel, self.submodel1.SUBMODEL)

    def test_inheritance(self):

        class Submodel1(self.base_model):
            SUBMODEL = "submodel1"

        class Submodel1_1(Submodel1):
            pass

        self.assertEqual(self.base_model.collection, Submodel1.collection)
        self.assertEqual(Submodel1.collection, Submodel1_1.collection)
        self.assertEqual(Submodel1.SUBMODEL, Submodel1_1.SUBMODEL)

    def test_abstract(self):
        with self.assertRaises(IntegrityError):
            self.base_model({})

        with self.assertRaises(IntegrityError):
            class C(self.base_model):
                pass  # no SUBMODEL
            C({})

        with self.assertRaises(IntegrityError):
            class C(self.submodel1):
                SUBMODEL = "c"
            self.submodel1.register_submodel("c", C)

    def test_fields_inheritance(self):
        m1 = self.submodel1({})
        m2 = self.submodel2({})

        self.assertCountEqual(m1.__fields__, ["_id", "submodel", "field1", "field2", "field3"])
        self.assertCountEqual(m2.__fields__, ["_id", "submodel", "field1", "field2", "field4"])

    def _create_objs(self):
        """Returns two lists of objects. Objects in the same positions only differ in their submodel"""
        values = [1, 2, 3]
        objs1 = [self.submodel1({"field1": v, "field2": v}) for v in values]
        objs2 = [self.submodel2({"field1": v, "field2": v}) for v in values]
        for obj in itertools.chain(objs1, objs2):
            obj.save()
        return objs1, objs2

    def test_isolation_find(self):
        objs1, objs2 = self._create_objs()
        self.assertCountEqual(
            self.submodel1.find().all(),
            objs1,
        )
        self.assertCountEqual(
            self.submodel2.find().all(),
            objs2,
        )
        self.assertCountEqual(
            self.base_model.find().all(),
            objs1 + objs2,
        )

        self.assertCountEqual(
            self.submodel1.find({"field1": objs1[0].field1}).all(),
            [objs1[0]],
        )
        self.assertCountEqual(
            self.base_model.find({"field1": objs1[0].field1}).all(),
            [objs1[0], objs2[0]],
        )

    def test_isolation_update(self):
        objs1, objs2 = self._create_objs()
        obj1 = objs2[0]
        obj1.field2 = "new_value"
        self.submodel2.update_many(
            {"field1": obj1.field1},
            {"$set": {"field2": obj1.field2}}
        )
        self.assertCountEqual(
            self.base_model.find({"field2": obj1.field2}),
            [obj1]
        )

        obj1 = objs1[1]
        obj2 = objs2[1]
        obj1.field2 = "newer_value"
        obj2.field2 = "newer_value"
        self.base_model.update_many(
            {"field1": obj1.field1},
            {"$set": {"field2": obj1.field2}}
        )
        self.assertCountEqual(
            self.base_model.find({"field2": obj1.field2}),
            [obj1, obj2]
        )

    def test_isolation_destroy(self):
        objs1, objs2 = self._create_objs()
        to_destroy = objs2.pop()
        to_keep = objs1[-1]
        self.submodel2.destroy_many({"field1": to_destroy.field1})
        self.assertListEqual(
            self.submodel2.find({
                "field1": to_destroy.field1
            }).all(),
            []
        )
        self.assertListEqual(
            self.base_model.find({
                "field1": to_destroy.field1
            }).all(),
            [to_keep]
        )

        to_destroy = objs1[0]
        objs1 = objs1[1:]
        objs2 = objs2[1:]
        self.base_model.destroy_many({"field1": to_destroy.field1})
        self.assertCountEqual(
            self.base_model.find().all(),
            objs1 + objs2,
        )

    def test_double_register(self):
        with self.assertRaises(IntegrityError):
            class NewSubmodel(self.base_model):
                SUBMODEL = self.submodel2.SUBMODEL
            self.base_model.register_submodel(
                NewSubmodel.SUBMODEL, NewSubmodel)


class TestShardedSubmodel(MongoMockTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        class TestBaseModel(ShardedSubmodel):
            COLLECTION = "test"
            field1: Field()
            field2: Field()

        class Submodel1(TestBaseModel):

            SUBMODEL = "submodel1"

        class Submodel2(TestBaseModel):

            SUBMODEL = "submodel2"

        TestBaseModel.register_submodel(Submodel1.SUBMODEL, Submodel1)
        TestBaseModel.register_submodel(Submodel2.SUBMODEL, Submodel2)

        cls.base_model = TestBaseModel
        cls.submodel1 = Submodel1
        cls.submodel2 = Submodel2

    def setUp(self) -> None:
        super().setUp()
        for shard in db.shards:
            self.base_model.destroy_all(shard)

    def test_wrong_input(self):
        with self.assertRaises(WrongSubmodel):
            self.submodel1({"_id": ObjectId(), "field1": "value", "submodel": "wrong"}, shard_id="s1")
        with self.assertRaises(MissingSubmodel):
            self.submodel1({"_id": ObjectId(), "field1": "value"}, shard_id="s1")
        with self.assertRaises(IntegrityError):
            self.submodel1({"field1": "value", "submodel": "my_submodel"}, shard_id="s1")
        with self.assertRaises(WrongSubmodel):
            obj = self.submodel1({"field1": "value"}, shard_id="s1")
            obj.submodel = "wrong"
            obj.save()

    def test_submodel_field(self):
        obj = self.submodel1({}, shard_id="s1")
        self.assertTrue(hasattr(obj, "submodel"))
        self.assertEqual(obj.submodel, self.submodel1.SUBMODEL)
        obj.save()
        obj.reload()
        self.assertEqual(obj.submodel, self.submodel1.SUBMODEL)
        db_obj = self.submodel1.get("s1", obj._id)
        self.assertEqual(db_obj.submodel, self.submodel1.SUBMODEL)

    def test_inheritance(self):

        class Submodel1(self.base_model):
            SUBMODEL = "submodel1"

        class Submodel1_1(Submodel1):
            pass

        self.assertEqual(self.base_model.collection, Submodel1.collection)
        self.assertEqual(Submodel1.collection, Submodel1_1.collection)
        self.assertEqual(Submodel1.SUBMODEL, Submodel1_1.SUBMODEL)

    def test_abstract(self):
        with self.assertRaises(IntegrityError):
            self.base_model({}, shard_id="s1")

        with self.assertRaises(IntegrityError):
            class C(self.base_model):
                pass  # no SUBMODEL
            C({}, shard_id="s1")

        with self.assertRaises(IntegrityError):
            class C(self.submodel1):
                SUBMODEL = "c"
            self.submodel1.register_submodel("c", C)

    def _create_objs(self):
        """Returns two lists of objects. Objects in the same positions only differ in their submodel"""
        values = [1, 2, 3]
        objs1 = [self.submodel1({"field1": v, "field2": v}, shard_id="s1") for v in values]
        objs2 = [self.submodel2({"field1": v, "field2": v}, shard_id="s1") for v in values]
        for obj in itertools.chain(objs1, objs2):
            obj.save()
        return objs1, objs2

    def test_isolation_find(self):
        objs1, objs2 = self._create_objs()
        self.assertCountEqual(
            self.submodel1.find("s1").all(),
            objs1,
        )
        self.assertCountEqual(
            self.submodel2.find("s1").all(),
            objs2,
        )
        self.assertCountEqual(
            self.base_model.find("s1").all(),
            objs1 + objs2,
        )

        self.assertCountEqual(
            self.submodel1.find("s1", {"field1": objs1[0].field1}).all(),
            [objs1[0]],
        )
        self.assertCountEqual(
            self.base_model.find("s1", {"field1": objs1[0].field1}).all(),
            [objs1[0], objs2[0]],
        )

    def test_isolation_update(self):
        objs1, objs2 = self._create_objs()
        obj1 = objs2[0]
        obj1.field2 = "new_value"
        self.submodel2.update_many(
            "s1",
            {"field1": obj1.field1},
            {"$set": {"field2": obj1.field2}}
        )
        self.assertCountEqual(
            self.base_model.find("s1", {"field2": obj1.field2}),
            [obj1]
        )

        obj1 = objs1[1]
        obj2 = objs2[1]
        obj1.field2 = "newer_value"
        obj2.field2 = "newer_value"
        self.base_model.update_many(
            "s1",
            {"field1": obj1.field1},
            {"$set": {"field2": obj1.field2}}
        )
        self.assertCountEqual(
            self.base_model.find("s1", {"field2": obj1.field2}),
            [obj1, obj2]
        )

    def test_isolation_destroy(self):
        objs1, objs2 = self._create_objs()
        to_destroy = objs2.pop()
        to_keep = objs1[-1]
        self.submodel2.destroy_many("s1", {"field1": to_destroy.field1})
        self.assertListEqual(
            self.submodel2.find("s1", {
                "field1": to_destroy.field1
            }).all(),
            []
        )
        self.assertListEqual(
            self.base_model.find("s1", {
                "field1": to_destroy.field1
            }).all(),
            [to_keep]
        )

        to_destroy = objs1[0]
        objs1 = objs1[1:]
        objs2 = objs2[1:]
        self.base_model.destroy_many("s1", {"field1": to_destroy.field1})
        self.assertCountEqual(
            self.base_model.find("s1").all(),
            objs1 + objs2,
        )

    def test_double_register(self):
        with self.assertRaises(IntegrityError):
            class NewSubmodel(self.base_model):
                SUBMODEL = self.submodel2.SUBMODEL
            self.base_model.register_submodel(
                NewSubmodel.SUBMODEL, NewSubmodel)
