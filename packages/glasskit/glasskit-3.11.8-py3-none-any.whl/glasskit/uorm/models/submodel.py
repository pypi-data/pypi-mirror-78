"""
- Make the base class first. Set COLLECTION explicitly - it is not
  generated automatically from the class name but inherited instead.
- Subclass your base class to define submodels. Set SUBMODEL to a string
  that will identify your submodel in the DB.
- You can further subclass your submodels. To avoid saving such abstract
  intermediate models do not set SUBMODEL.
- Register the submodel with the base model

It is possible to register an arbitrary function instead of a proper class.
It may be particularly useful if the correct class depends on something
other than `submodel` field. The function will get **data from the DB and
should return an model object.

If you decide to do it you will likely have to override _preprocess_query()
on your submodels to keep the expected find/destroy/update behaviour

"""
from .fields import StringField
from .storable_model import StorableModel
from .sharded_model import ShardedModel
from ..errors import IntegrityError, MissingSubmodel, WrongSubmodel, UnknownSubmodel


class BaseSubmodelMixin:

    SUBMODEL = None

    submodel: StringField(required=True)

    __submodel_loaders__ = None

    def __init__(self, attrs, **kwargs):
        super().__init__(attrs, **kwargs)
        if self.is_new:
            if not self.SUBMODEL:
                raise IntegrityError(
                    f"Attempted to create an object of abstract model {self.__class__.__name__}")
            if "submodel" in attrs:
                raise IntegrityError(
                    "Attempt to override submodel for a new object")
            self.submodel = self.SUBMODEL
        else:
            if not self.submodel:
                raise MissingSubmodel(f"{self.__class__.__name__} has no submodel in the DB. Bug?")
            self._check_submodel()

    def _check_submodel(self):
        if self.submodel != self.SUBMODEL:
            raise WrongSubmodel(f"Attempted to load {self.submodel} as"
                                f" {self.__class__.__name__}. Correct submodel"
                                f" would be {self.SUBMODEL}. Bug?")

    def validate(self):
        super().validate()
        self._check_submodel()

    @classmethod
    def register_submodel(cls, name, ctor):
        if cls.SUBMODEL:
            raise IntegrityError("Attempted to register submodel with another submodel")
        if not cls.__submodel_loaders__:
            cls.__submodel_loaders__ = {}
        if name in cls.__submodel_loaders__:
            raise IntegrityError(f"Submodel {name} already registered")
        cls.__submodel_loaders__[name] = ctor

    @classmethod
    def _preprocess_query(cls, query):
        if not cls.SUBMODEL:
            return query
        return {
            "submodel": cls.SUBMODEL,
            **query
        }

    @classmethod
    def _ctor(cls, attrs, **kwargs):
        if "submodel" not in attrs:
            raise MissingSubmodel(f"{cls.__name__} has no submodel in the DB. Bug?")
        if not cls.__submodel_loaders__:
            return cls(attrs, **kwargs)
        submodel_name = attrs["submodel"]
        if submodel_name not in cls.__submodel_loaders__:
            raise UnknownSubmodel(f"Submodel {submodel_name} is not registered with {cls.__name__}")
        return cls.__submodel_loaders__[submodel_name](attrs, **kwargs)


class StorableSubmodel(BaseSubmodelMixin, StorableModel):
    pass


class ShardedSubmodel(BaseSubmodelMixin, ShardedModel):
    pass
