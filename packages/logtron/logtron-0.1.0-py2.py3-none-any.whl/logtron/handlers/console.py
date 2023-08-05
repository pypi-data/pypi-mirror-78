import json
from logging import StreamHandler


class ConsoleHandler(StreamHandler):
    def __init__(self, context):
        super(ConsoleHandler, self).__init__()
        self.context = context
