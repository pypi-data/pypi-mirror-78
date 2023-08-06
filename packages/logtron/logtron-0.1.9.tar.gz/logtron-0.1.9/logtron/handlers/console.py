import json
from logging import StreamHandler


class ConsoleHandler(StreamHandler):
    def __init__(self, **kwargs):
        super(ConsoleHandler, self).__init__()
