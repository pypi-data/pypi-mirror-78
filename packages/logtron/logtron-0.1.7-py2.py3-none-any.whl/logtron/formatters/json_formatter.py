import json
import traceback
from logging import Formatter, LogRecord


class JsonFormatter(Formatter):
    def __init__(self, context=None):
        super(JsonFormatter, self).__init__()
        self.context = context
        self.dummy = LogRecord(None, None, None, None, None, None, None)

    def format(self, record):
        data = {
            "timestamp": int(record.created * 1000),
            "message": record.msg,
            "name": record.name,
            "level": record.levelno,
            "context": self.context,
        }

        data["extra"] = {}
        for k, v in record.__dict__.items():
            if k not in self.dummy.__dict__ and k not in ["message"]:
                data["extra"][k] = v

        if record.exc_info is not None:
            data["exception"] = "".join(traceback.format_exception(*record.exc_info))

        return json.dumps(data)
