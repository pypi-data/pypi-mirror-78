from glasskit.base import Base


class App(Base):

    def setup_controllers(self):
        pass

    def after_setup(self):
        pass


def force_init_app():
    # touch Proxy object
    _ = app.__doc__


app = App()
