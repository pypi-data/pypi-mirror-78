from . import Command
from glasskit.uorm.models.base_model import BaseModel
from glasskit.uorm.models.storable_model import StorableModel
from glasskit.uorm.models.sharded_model import ShardedModel
from glasskit.uorm.models.submodel import ShardedSubmodel, StorableSubmodel
from glasskit import ctx
import os
import inspect
import importlib


class Index(Command):
    def find_model_classes(self):
        classes = set()
        model_dir = os.path.join(self.app.app_dir, "models")
        for filename in os.listdir(model_dir):
            if filename.endswith(".py"):
                mod_name = os.path.basename(filename)[:-3]
                mod_name = f"{self.app.app_name}.models.{mod_name}"
                module = importlib.import_module(mod_name)
                for key in dir(module):
                    obj = getattr(module, key)
                    if inspect.isclass(obj) and issubclass(obj, BaseModel):
                        if obj not in [
                            BaseModel,
                            StorableSubmodel,
                            ShardedSubmodel,
                            StorableModel,
                            ShardedModel,
                        ]:
                            classes.add(obj)
        return classes

    def run(self):
        model_classes = self.find_model_classes()
        for cls in model_classes:
            ctx.log.info("generating indexes for model %s", cls.__name__)
            cls.ensure_indexes()
