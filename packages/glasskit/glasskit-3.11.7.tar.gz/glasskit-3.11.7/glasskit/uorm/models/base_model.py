from typing import Dict, Any, Set, Type, List
from pymongo.errors import OperationFailure

from glasskit import ctx
from glasskit.uorm.errors import DoNotSave
from ..db import db, Shard
from .fields import ObjectIdField
from .meta import MetaModel
from .hooks import BaseModelHook


class BaseModel(MetaModel):

    __hooks_classes__: Set[Type[BaseModelHook]] = None

    _id: ObjectIdField()

    def __init__(self, attrs: Dict[str, Any] = None, **kwargs):
        if attrs is None:
            attrs = {}

        for field in self.__fields__:
            value = attrs.get(field, self.__def_values__.get(field, None))
            if callable(value):
                value = value()
            self.__dict__[field] = value
        self._initial_state = None
        self.__set_initial_state()
        self.__hooks__ = []
        if self.__hooks_classes__:
            for hook_class in self.__hooks_classes__:
                hook_inst = hook_class.on_model_init(self)
                if hook_inst:
                    self.__hooks__.append(hook_inst)

    def validate(self) -> None:
        for name, func in self.__validators__.items():
            value = self.__dict__[name]
            func(value)

    @property
    def is_new(self) -> bool:
        return self._id is None

    def __set_initial_state(self) -> None:
        """
        The default initial state contains only _id and [KEY_FIELD] fields
        to perform cache invalidation. To have more fields in _initial_state
        dict, return the entire initial_state from setup_initial_state() 
        method.
        """
        self.__dict__["_initial_state"] = self.setup_initial_state()

    def setup_initial_state(self) -> Dict[str, Any]:
        """
        This method is supposed to be overriden in case you want use other
        fields besides _id and [KEY_FIELD]. Use super() call to create those
        and add other fields you need afterwards.
        """
        initial_state = {"_id": self._id}
        if self.KEY_FIELD:
            initial_state[self.KEY_FIELD] = getattr(self, self.KEY_FIELD)
        return initial_state

    @classmethod
    def register_model_hook(cls, model_hook_class: Type[BaseModelHook], *args, **kwargs) -> None:
        if not issubclass(model_hook_class, BaseModelHook):
            raise TypeError("Invalid hook class")
        if cls.__hooks_classes__ is None:
            cls.__hooks_classes__ = set()
        if model_hook_class not in cls.__hooks_classes__:
            cls.__hooks_classes__.add(model_hook_class)
            model_hook_class.on_hook_register(cls, *args, **kwargs)
            ctx.log.debug(
                "Registered hook %s for model %s",
                model_hook_class.__name__,
                cls.__name__,
            )

    @classmethod
    def unregister_model_hook(cls, model_hook_class: Type[BaseModelHook]):
        if cls.__hooks_classes__ is None:
            return
        if model_hook_class in cls.__hooks_classes__:
            cls.__hooks_classes__.remove(model_hook_class)
            model_hook_class.on_hook_unregister(cls)

    @classmethod
    def clear_hooks(cls) -> None:
        if cls.__hooks_classes__ is None:
            return
        for hook_class in cls.__hooks_classes__.copy():
            cls.unregister_model_hook(hook_class)

    def _before_save(self) -> None:
        pass

    def _before_validation(self) -> None:
        pass

    def _before_delete(self) -> None:
        pass

    def _after_save(self, is_new) -> None:
        pass

    def _after_delete(self) -> None:
        pass

    def _save_to_db(self) -> None:
        pass

    def _delete_from_db(self) -> None:
        pass

    def invalidate(self, **kwargs) -> None:
        pass

    def destroy(self, skip_callback=False, invalidate_cache=True) -> 'BaseModel':
        if self.is_new:
            return self
        if not skip_callback:
            self._before_delete()

        if invalidate_cache:
            self.invalidate()

        self._delete_from_db()
        if not skip_callback:
            self._after_delete()

        self._id = None
        for hook in self.__hooks__:
            try:
                hook.on_model_destroy(self)
            except Exception as e:
                ctx.log.error(
                    "error executing destroy hook %s on model %s(%s): %s",
                    hook.__class__.__name__,
                    self.__class__.__name__,
                    self._id,
                    e,
                )

    def save(self, skip_callback=False, invalidate_cache=True) -> 'BaseModel':
        is_new = self.is_new

        if not skip_callback:
            try:
                self._before_validation()
            except DoNotSave:
                return
        self.validate()

        if not skip_callback:
            try:
                self._before_save()
            except DoNotSave:
                return self

        if invalidate_cache:
            self.invalidate()

        self._save_to_db()

        for hook in self.__hooks__:
            try:
                hook.on_model_save(self, is_new)
            except Exception as e:
                ctx.log.error(
                    "error executing save hook %s on model %s(%s): %s",
                    hook.__class__.__name__,
                    self.__class__.__name__,
                    self._id,
                    e,
                )

        self.__set_initial_state()
        if not skip_callback:
            self._after_save(is_new)

        return self

    def __repr__(self) -> str:
        attributes = ["%s=%r" % (a, getattr(self, a)) for a in self.__fields__]
        return "%s(\n    %s\n)" % (self.__class__.__name__, ",\n    ".join(attributes))

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        for field in self.__fields__:
            if hasattr(self, field):
                if not hasattr(other, field):
                    return False
                if getattr(self, field) != getattr(other, field):
                    return False
            elif hasattr(other, field):
                return False
        return True

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def to_dict(self, fields=None, include_restricted=False) -> Dict[str, Any]:
        if fields is None:
            fields = self.__fields__

        result = {}
        for field in fields:
            if field in self.__restricted_fields__ and not include_restricted:
                continue
            if not hasattr(self, field):
                continue
            value = getattr(self, field)
            if callable(value):
                continue
            result[field] = value
        return result

    @classmethod
    def create(cls, **attrs) -> 'BaseModel':
        return cls(attrs)

    @classmethod
    def _ctor(cls, attrs, **kwargs) -> 'BaseModel':
        return cls(attrs, **kwargs)

    @classmethod
    def __get_possible_databases(cls) -> List['Shard']:
        return [db.meta]

    @classmethod
    def ensure_indexes(cls, loud=False, overwrite=False) -> None:
        for keys, options in cls.__def_indexes__:
            for db in cls.__get_possible_databases():
                try:
                    db.conn[cls.collection].create_index(keys, **options)
                except OperationFailure as e:
                    if (
                        e.details.get("codeName") == "IndexOptionsConflict"
                        or e.details.get("code") == 85
                    ):
                        if overwrite:
                            if loud:
                                ctx.log.debug("Dropping index %s as conflicting", keys)
                            db.conn[cls.collection].drop_index(keys)
                            if loud:
                                ctx.log.debug(
                                    "Creating index with options: %s, %s", keys, options
                                )
                            db.conn[cls.collection].create_index(keys, **options)
                        else:
                            ctx.log.error(
                                "Index %s conflicts with an existing one, use overwrite param to fix it",
                                keys,
                            )

    def _reload_from_obj(self, obj) -> None:
        for field in self.__fields__:
            if field == "_id":
                continue
            value = getattr(obj, field)
            self.__dict__[field] = value
