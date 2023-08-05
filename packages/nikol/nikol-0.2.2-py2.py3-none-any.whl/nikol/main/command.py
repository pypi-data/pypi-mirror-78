class Command(object):
    def __init__(self, cli):
        self.cli = cli
    
class HelpCommand(Command):
    def __call__(self, args):
        self.cli.parser.print_help()

