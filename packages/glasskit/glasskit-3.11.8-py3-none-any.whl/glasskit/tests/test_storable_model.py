from unittest.mock import patch
from ..uorm.models.storable_model import StorableModel
from ..uorm.models.fields import StringField, Field
from .mongo_mock_test import MongoMockTest

CALLABLE_DEFAULT_VALUE = 4


def callable_default():
    return CALLABLE_DEFAULT_VALUE


class TestModel(StorableModel):
    field1: StringField(rejected=True, index=True, default="default_value")
    field2: Field(required=True)
    field3: Field(required=True, default="required_default_value")
    callable_default_field: Field(default=callable_default)


class TestStorableModel(MongoMockTest):
    def setUp(self) -> None:
        super().setUp()
        TestModel.destroy_all()

    def tearDown(self) -> None:
        TestModel.destroy_all()
        super().tearDown()

    def test_defaults(self):
        model = TestModel()
        self.assertEqual(model.field1, "default_value")
        self.assertEqual(model.field3, "required_default_value")
        self.assertEqual(model.callable_default_field, CALLABLE_DEFAULT_VALUE)

    def test_eq(self):
        model = TestModel({"field2": "mymodel"})
        model.save()
        model2 = TestModel.find_one({"field2": "mymodel"})
        self.assertEqual(model, model2)

    def test_reject_on_update(self):
        model = TestModel.create(field1="original_value", field2="mymodel_reject_test")
        model.save()
        id_ = model._id
        model.update({"field1": "new_value"})
        model = TestModel.find_one({"_id": id_})
        self.assertEqual(model.field1, "original_value")

    def test_update(self):
        model = TestModel.create(field1="original_value", field2="mymodel_update_test")
        model.save()
        id_ = model._id
        model.update({"field2": "mymodel_updated"})
        model = TestModel.find_one({"_id": id_})
        self.assertEqual(model.field2, "mymodel_updated")

    def test_update_many(self):
        model1 = TestModel.create(field1="original_value", field2="mymodel_update_test")
        model1.save()
        model2 = TestModel.create(field1="original_value", field2="mymodel_update_test")
        model2.save()
        model3 = TestModel.create(field1="do_not_modify", field2="mymodel_update_test")
        model3.save()

        TestModel.update_many(
            {"field1": "original_value"}, {"$set": {"field2": "mymodel_updated"}}
        )
        model1.reload()
        model2.reload()
        model3.reload()

        self.assertEqual(model1.field2, "mymodel_updated")
        self.assertEqual(model2.field2, "mymodel_updated")
        self.assertEqual(model3.field2, "mymodel_update_test")

    @patch("glasskit.uorm.models.storable_model.db.l2c", spec=True)
    @patch("glasskit.uorm.models.storable_model.db.l1c", spec=True)
    def test_invalidate(self, l1c, l2c):
        class Model(StorableModel):

            field1: StringField()

            KEY_FIELD = "field1"

            def setup_initial_state(self):
                state = super().setup_initial_state()
                state["field1"] = self.field1
                return state

        model = Model({"field1": "value"})
        model.save()

        l1c.delete.assert_called_once_with("model.value")
        l2c.delete.assert_called_once_with("model.value")

        model.save()
        l1c.delete.assert_any_call(f"model.{model._id}")
        l1c.delete.assert_any_call("model.value")
        l2c.delete.assert_any_call(f"model.{model._id}")
        l2c.delete.assert_any_call("model.value")
