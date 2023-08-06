import unittest
import logging
import inspect
import sys
from types import ModuleType
from . import Command

MODULE_NAME = "_all_tests"


class Test(Command):

    def run(self):
        logging.disable(logging.CRITICAL)
        all_tests_module = ModuleType(MODULE_NAME)

        glasskit_test_mod = __import__("glasskit.tests").tests
        app_test_mod = __import__(f"{self.app.app_name}.tests").tests

        for module in [glasskit_test_mod, app_test_mod]:
            for objname in dir(module):
                obj = getattr(module, objname)
                if inspect.isclass(obj) and issubclass(obj, unittest.TestCase) and obj != unittest.TestCase:
                    setattr(all_tests_module, objname, obj)

        sys.modules[MODULE_NAME] = all_tests_module
        unittest.main(argv=["glass.py test", "-b"], module=MODULE_NAME)
