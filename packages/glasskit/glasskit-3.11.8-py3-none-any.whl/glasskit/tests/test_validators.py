from unittest import TestCase
from datetime import datetime
from ..uorm.models.fields import (
    StringField,
    IntField,
    FloatField,
    ListField,
    DictField,
    BoolField,
    DatetimeField,
)
from ..uorm.models.base_model import BaseModel
from ..uorm.errors import ValidationError


class TestValidators(TestCase):
    def test_required(self):
        class Model(BaseModel):
            field: StringField(required=True)

        model = Model()
        self.assertRaises(ValidationError, model.validate)
        model.field = "string"
        model.validate()

    def test_string_field(self):
        class Model(BaseModel):
            field: StringField()

        model = Model({"field": 1})
        self.assertRaises(ValidationError, model.validate)
        model.field = "string"
        model.validate()

        model.field = "   auto-trimmed   "
        self.assertEqual(model.field, "auto-trimmed")

        class Model(BaseModel):
            field: StringField(auto_trim=False)

        model = Model({"field": "    no-auto-trim    "})
        self.assertEqual(model.field, "    no-auto-trim    ")

        class Model(BaseModel):
            field: StringField(min_length=3, max_length=5, re_match="^\d+$")

        model = Model({"field": "1"})
        self.assertRaises(ValidationError, model.validate)
        model.field = "123456"
        self.assertRaises(ValidationError, model.validate)
        model.field = "1234a"
        self.assertRaises(ValidationError, model.validate)
        model.field = "1234"
        model.validate()

    def test_list_field(self):
        class Model(BaseModel):
            field: ListField()

        model = Model({"field": 1})
        self.assertRaises(ValidationError, model.validate)
        model.field = [1, 2, 3]
        model.validate()

        class Model(BaseModel):
            field: ListField(min_length=3, max_length=5)

        model = Model({"field": [1]})
        self.assertRaises(ValidationError, model.validate)
        model.field = [1, 2, 3, 4, 5, 6]
        self.assertRaises(ValidationError, model.validate)
        model.field = [1, 2, 3, 4]
        model.validate()

    def test_bool_field(self):
        class Model(BaseModel):
            field: BoolField()

        model = Model({"field": 1})
        self.assertRaises(ValidationError, model.validate)
        model.field = False
        model.validate()

    def test_int_field(self):
        class Model(BaseModel):
            field: IntField()

        model = Model({"field": "string"})
        self.assertRaises(ValidationError, model.validate)
        model.field = -34
        model.validate()

        class Model(BaseModel):
            field: IntField(min_value=0, max_value=10)

        model = Model({"field": -34})
        self.assertRaises(ValidationError, model.validate)
        model.field = 34
        self.assertRaises(ValidationError, model.validate)
        model.field = 5
        model.validate()

    def test_float_field(self):
        class Model(BaseModel):
            field: FloatField()

        model = Model({"field": "string"})
        self.assertRaises(ValidationError, model.validate)
        model.field = -34
        self.assertRaises(ValidationError, model.validate)
        model.field = 28.0
        model.validate()

        class Model(BaseModel):
            field: FloatField(min_value=0, max_value=10)

        model = Model({"field": -15.5})
        self.assertRaises(ValidationError, model.validate)
        model.field = 15.5
        self.assertRaises(ValidationError, model.validate)
        model.field = 5.3
        model.validate()

    def test_dict_field(self):
        class Model(BaseModel):
            field: DictField()

        model = Model({"field": 1})
        self.assertRaises(ValidationError, model.validate)
        model.field = {}
        model.validate()

    def test_datetime_field(self):
        class Model(BaseModel):
            field: DatetimeField()

        model = Model({"field": 1})
        self.assertRaises(ValidationError, model.validate)
        model.field = datetime.now()
        model.validate()

    def test_choices(self):
        class Model(BaseModel):
            field: StringField(required=True, choices=["a", "b", "c"])

        class ModelNotRequired(BaseModel):
            field: StringField(required=False, choices=["a", "b", "c"])

        model = Model({"field": "a"})
        model.validate()
        model.field = "b"
        model.validate()
        model.field = "c"
        model.validate()
        model.field = "d"
        self.assertRaises(ValidationError, model.validate)
        model.field = None
        self.assertRaises(ValidationError, model.validate)

        model = ModelNotRequired({"field": "a"})
        model.validate()
        model.field = "b"
        model.validate()
        model.field = "c"
        model.validate()
        model.field = "d"
        self.assertRaises(ValidationError, model.validate)
        model.field = None
        model.validate()
