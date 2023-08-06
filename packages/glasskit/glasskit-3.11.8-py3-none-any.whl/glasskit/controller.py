from flask import Blueprint, g
from inspect import isclass
from .errors import AuthenticationError


class Controller(Blueprint):

    auth_error = AuthenticationError

    def __init__(self, name, import_name, require_auth=True, **kwargs):
        super().__init__(name, import_name, **kwargs)

        if not isclass(self.auth_error) or not issubclass(self.auth_error, Exception):
            raise TypeError(
                f"{self.__class__.__name__}.auth_error must be a subclass of Exception"
            )

        self.before_request(self.__set_auth_data)
        if require_auth:
            self.before_request(self.check_auth)

    def get_current_user(self) -> object:
        return None

    def __set_auth_data(self):
        g.user = self.get_current_user()

    def check_auth(self):
        if g.user is None:
            raise self.auth_error()
