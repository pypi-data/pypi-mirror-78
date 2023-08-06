import json
import traceback
from logging import Formatter, LogRecord

from logtron.util import flatten_dict


class JsonFormatter(Formatter):
    def __init__(self, **kwargs):
        super(JsonFormatter, self).__init__()
        self.reserved = ["message", "asctime"] + [
            k for k, v in LogRecord(None, None, None, None, None, None, None).__dict__.items()
        ]
        self.flatten = kwargs.get("flatten", False)
        self.discover_context = kwargs.get("discover_context", lambda: {})

    def format(self, record):
        data = {
            "timestamp": int(record.created * 1000),
            "message": record.msg,
            "name": record.name,
            "level": record.levelno,
        }

        if record.exc_info is not None:
            data["exception"] = "".join(traceback.format_exception(*record.exc_info))

        if self.flatten:
            items = {
                k: v
                for d in [record.__dict__, self.discover_context()]
                for k, v in d.items()
                if k not in self.reserved and k not in data
            }
            data.update(flatten_dict(items))
        else:
            items = {k: v for k, v in record.__dict__.items() if k not in self.reserved and k not in data}
            data.update({"extra": items, "context": self.discover_context()})

        return json.dumps(data)
