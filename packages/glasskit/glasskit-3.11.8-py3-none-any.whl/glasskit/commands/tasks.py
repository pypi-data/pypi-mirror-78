from . import Command
from glasskit.queue.worker import BaseWorker
import importlib
import inspect


class Tasks(Command):
    def find_worker_class(self):
        wrk_module = importlib.import_module(f"{self.app.app_name}.tasks.worker")
        for objname in dir(wrk_module):
            obj = getattr(wrk_module, objname)
            if (
                inspect.isclass(obj)
                and issubclass(obj, BaseWorker)
                and obj is not BaseWorker
            ):
                return obj
        return None

    def run(self):
        wrk_cls = self.find_worker_class()
        if wrk_cls is None:
            raise RuntimeError(
                f"Worker class not found in {self.app.app_name}.tasks.worker"
            )
        wrk = wrk_cls()
        wrk.process_tasks()

