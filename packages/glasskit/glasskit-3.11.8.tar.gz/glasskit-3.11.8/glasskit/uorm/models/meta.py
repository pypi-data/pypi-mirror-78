from typing import Dict, Callable, Any, Set, List
from .fields import Field


def snake_case(name):
    result = ""
    for i, l in enumerate(name):
        if 65 <= ord(l) <= 90:
            if i != 0:
                result += "_"
            result += l.lower()
        else:
            result += l
    return result


class MetaModel:

    __fields__: Set = None
    __rejected_fields__: Set = None
    __restricted_fields__: Set = None
    __validators__: Dict[str, Callable[[Any], None]] = None
    __def_values__: Dict[str, Any] = None
    __def_indexes__: List = None
    __cache_key_fields__: Set = None

    COLLECTION = None
    INDEXES = None
    KEY_FIELD = "_id"
    CACHE_KEY_FIELDS = None

    collection = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__fields__ = set() if cls.__fields__ is None else cls.__fields__.copy()

        cls.__def_values__ = (
            {} if cls.__def_values__ is None else cls.__def_values__.copy()
        )

        cls.__validators__ = (
            {} if cls.__validators__ is None else cls.__validators__.copy()
        )

        cls.__rejected_fields__ = (
            set() if cls.__rejected_fields__ is None else cls.__rejected_fields__.copy()
        )

        cls.__restricted_fields__ = (
            set()
            if cls.__restricted_fields__ is None
            else cls.__restricted_fields__.copy()
        )

        cls.__def_indexes__ = (
            [] if cls.__def_indexes__ is None else cls.__def_indexes__[:]
        )

        cls.__cache_key_fields__ = (
            {"_id"}
            if cls.__cache_key_fields__ is None
            else cls.__cache_key_fields__.copy()
        )

        for name, value in cls.__annotations__.items():
            if not isinstance(value, Field):
                continue
            value.set_name(name)
            field = value.descriptor()
            field.__set_name__(cls, name)
            setattr(cls, name, field)
            cls.__fields__.add(name)
            cls.__validators__[name] = value.validate
            if value.def_value is not None:
                cls.__def_values__[name] = value.def_value
            if value.rejected:
                cls.__rejected_fields__.add(name)
            if value.restricted:
                cls.__restricted_fields__.add(name)
            if value.index is not None:
                cls.__def_indexes__.append([[(name, value.index)], value.index_options])

        if cls.INDEXES is not None:
            for idx in cls.INDEXES:
                cls.__def_indexes__.append(idx)

        cls.__cache_key_fields__.add(cls.KEY_FIELD)
        if cls.CACHE_KEY_FIELDS:
            for field in cls.CACHE_KEY_FIELDS:
                cls.__cache_key_fields__.add(field)

        if cls.COLLECTION:
            cls.collection = cls.COLLECTION
        else:
            cls.collection = snake_case(cls.__name__)
