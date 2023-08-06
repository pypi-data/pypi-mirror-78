import re
from bson import ObjectId
from datetime import datetime
from glasskit.uorm.errors import ValidationError
from pymongo import ASCENDING


class BaseFieldDescriptor:
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class AutotrimFieldDescriptor(BaseFieldDescriptor):
    def __set__(self, instance, value):
        if hasattr(value, "strip"):
            value = value.strip()
        super().__set__(instance, value)


class Field:

    descriptor = BaseFieldDescriptor

    def __init__(
        self,
        required=False,
        rejected=False,
        restricted=False,
        default=None,
        index=None,
        unique=False,
        choices=None,
    ):
        self.required = required
        self.rejected = rejected
        self.restricted = restricted
        if choices:
            self.choices = set(choices)
        else:
            self.choices = None
        self.def_value = default
        self.index, self.index_options = self.__generate_index(index, unique)
        self.name = None

    @staticmethod
    def __generate_index(index, unique):
        if unique:
            if index is None or index is True:
                return ASCENDING, {"unique": True}
            else:
                return index, {"unique": True}
        else:
            if index is None:
                return None, {}
            elif index is True:
                return ASCENDING, {}
            else:
                return index, {}

    def set_name(self, name):
        self.name = name

    def validate(self, value):
        if self.required and value is None:
            raise ValidationError(f"field {self.name} is required")

        if self.choices and value not in self.choices:
            if value is None:
                # at this point the value can be None only if it's not required
                # thus, if it's not required, it's ok to be None even if choices are defined
                return

            raise ValidationError(f"field {self.name} must be one of {self.choices}")


class TypedField(Field):

    TYPE = None

    def validate(self, value):
        super().validate(value)
        if value is None and not self.required:
            return
        if not isinstance(value, self.TYPE):
            raise ValidationError(
                f"field {self.name} must be an instance of type {self.TYPE.__name__}"
            )


class ObjectIdField(TypedField):

    TYPE = ObjectId


class StringField(TypedField):

    TYPE = str

    def __init__(
        self, min_length=None, max_length=None, re_match=None, auto_trim=True, **kwargs
    ):
        super().__init__(**kwargs)
        if auto_trim:
            self.__class__.descriptor = AutotrimFieldDescriptor

        if min_length is not None:
            assert isinstance(min_length, int)
        if max_length is not None:
            assert isinstance(max_length, int)

        self.min_length = min_length
        self.max_length = max_length
        if re_match:
            self.re_match = re.compile(re_match)
        else:
            self.re_match = None

    def validate(self, value):
        super().validate(value)
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(
                f"field {self.name} must be at least {self.min_length} characters long"
            )

        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(
                f"field {self.name} must be at most {self.max_length} characters long"
            )

        if self.re_match is not None and not self.re_match.match(value):
            raise ValidationError(
                f'field {self.name} must match pattern "{self.re_match.pattern}"'
            )


class IntField(TypedField):

    TYPE = int

    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)
        if min_value is not None:
            assert isinstance(min_value, int)
        if max_value is not None:
            assert isinstance(max_value, int)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        super().validate(value)
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"field {self.name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"field {self.name} must be <= {self.max_value}")


class FloatField(TypedField):

    TYPE = float

    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)
        if min_value is not None:
            assert isinstance(min_value, float) or isinstance(min_value, int)
        if max_value is not None:
            assert isinstance(max_value, float) or isinstance(max_value, int)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        super().validate(value)
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"field {self.name} must be >= {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"field {self.name} must be <= {self.max_value}")


class ListField(TypedField):

    TYPE = list

    def __init__(self, min_length=None, max_length=None, **kwargs):
        super().__init__(**kwargs)
        if min_length is not None:
            assert isinstance(min_length, int)
        if max_length is not None:
            assert isinstance(max_length, int)
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        super().validate(value)
        if self.min_length is not None and len(value) < self.min_length:
            raise ValidationError(
                f"field {self.name} must be at least {self.min_length} items long"
            )

        if self.max_length is not None and len(value) > self.max_length:
            raise ValidationError(
                f"field {self.name} must be at most {self.max_length} items long"
            )


class DatetimeField(TypedField):

    TYPE = datetime


class DictField(TypedField):

    TYPE = dict


class BoolField(TypedField):

    TYPE = bool
