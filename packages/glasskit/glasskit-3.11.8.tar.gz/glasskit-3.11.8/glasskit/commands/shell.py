from . import Command
import os


class Shell(Command):

    DESCRIPTION = 'Run shell (using IPython if available)'

    def run(self):
        if os.path.isfile(".shellrc.py"):
            with open(".shellrc.py") as rcf:
                try:
                    exec(rcf.read())
                except:
                    from traceback import print_exc
                    print("Error running .shellrc.py script!")
                    print_exc()
        try:
            # trying IPython if installed...
            from IPython import embed
            embed(using=False)
        except ImportError:
            # ... or python default console if not
            try:
                # optional readline interface for history if installed
                import readline  # pylint: disable=possibly-unused-variable
            except ImportError:
                pass
            import code
            variables = globals().copy()
            variables.update(locals())
            shell = code.InteractiveConsole(variables)
            shell.interact()
