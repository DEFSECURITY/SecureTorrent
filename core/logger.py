import sys
class logger:
    def __init__(self, name):
        self.name = name
    def log(self, *msgs):
        print(self.name, '| log |', *msgs)
    def error(self, *msgs):
        print(self.name, '| error |', *msgs, file=sys.stderr)