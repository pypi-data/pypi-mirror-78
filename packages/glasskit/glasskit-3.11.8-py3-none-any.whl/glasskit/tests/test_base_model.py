from pymongo import ASCENDING, DESCENDING
from unittest import TestCase
from ..uorm.models.fields import StringField
from ..uorm.models.base_model import BaseModel


class TestBaseModel(TestCase):
    def test_empty(self):
        model = BaseModel()
        self.assertIsNone(model._id)
        self.assertCountEqual(model.__fields__, ["_id"])

    def test_not_empty(self):
        class Model(BaseModel):
            field: StringField()

        model = Model({"field": "value"})
        self.assertEqual(model.field, "value")

    def test_collection_name(self):
        class Model(BaseModel):
            COLLECTION = "model"

        model = BaseModel()
        self.assertEqual(model.collection, "base_model")
        model = Model()
        self.assertEqual(model.collection, "model")

    def test_fields(self):
        class Model(BaseModel):
            string_f: StringField()

        model = Model()
        self.assertCountEqual(model.__fields__, ["_id", "string_f"])

    def test_rejected_fields(self):
        class Model(BaseModel):
            string_f: StringField()
            string_rf: StringField(rejected=True)

        model = Model()
        self.assertCountEqual(model.__fields__, ["_id", "string_f", "string_rf"])
        self.assertCountEqual(model.__rejected_fields__, ["string_rf"])

    def test_restricted_fields(self):
        class Model(BaseModel):
            string_f: StringField()
            string_rf: StringField(restricted=True)

        model = Model()
        self.assertCountEqual(model.__fields__, ["_id", "string_f", "string_rf"])
        self.assertCountEqual(model.__restricted_fields__, ["string_rf"])

    def test_indexes(self):
        class Model(BaseModel):
            string_f: StringField()
            string_if: StringField(index=True)
            string_uf: StringField(unique=True)
            string_duf: StringField(index=DESCENDING, unique=True)

        model = Model()

        self.assertCountEqual(
            model.__def_indexes__,
            [
                [[("string_if", ASCENDING)], {}],
                [[("string_uf", ASCENDING)], {"unique": True}],
                [[("string_duf", DESCENDING)], {"unique": True}],
            ],
        )

    def test_to_dict(self):
        class Model(BaseModel):
            field1: StringField()
            field2: StringField()
            field3: StringField(restricted=True)

        model = Model({"field1": "value1", "field2": "value2", "field3": "value3",})

        self.assertDictEqual(
            model.to_dict(), {"_id": None, "field1": "value1", "field2": "value2"}
        )

        self.assertDictEqual(
            model.to_dict(fields=["field1", "field2", "field3"]),
            {"field1": "value1", "field2": "value2"},
        )

        self.assertDictEqual(
            model.to_dict(include_restricted=True),
            {"_id": None, "field1": "value1", "field2": "value2", "field3": "value3"},
        )

        self.assertDictEqual(
            model.to_dict(fields=["field1", "field3"], include_restricted=True),
            {"field1": "value1", "field3": "value3"},
        )

        self.assertDictEqual(
            model.to_dict(
                fields=["field1", "field3", "bizzare"], include_restricted=True
            ),
            {"field1": "value1", "field3": "value3"},
        )

