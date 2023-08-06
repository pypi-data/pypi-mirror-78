from . import Command


class Run(Command):
    def init_argument_parser(self, parser):
        parser.add_argument("-H", "--host", default="127.0.0.1")
        parser.add_argument("-P", "--port", type=int, default=5000)

    def run(self):
        self.app.run(debug=True, host=self.args.host, port=self.args.port)
