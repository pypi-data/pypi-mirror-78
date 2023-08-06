import importlib
import logging

from logtron.config import discover_config as discover_config_base
from logtron.formatters import JsonFormatter
from logtron.util import flatten_dict

is_configured = False


def __get_handlers(config, formatter):
    handlers = [(i,) + tuple(i.rsplit(".", 1)) for i in config["handlers"]]
    classes = [i[2] for i in handlers]

    for handler, module_name, class_name in handlers:
        HandlerClass = getattr(importlib.import_module(module_name), class_name)
        instance = None
        args = {}
        if config.get(handler.lower()) is not None:
            args.update(config[handler.lower()])
        if classes.count(class_name) == 1 and config.get(class_name.lower()) is not None:
            args.update(config[class_name.lower()])
        instance = HandlerClass(**args)
        instance.setFormatter(formatter)
        yield instance


def autodiscover(name=None, level=logging.INFO, **kwargs):
    global is_configured

    refresh = kwargs.get("refresh", False)
    if not refresh and is_configured:
        return logging.getLogger(name)

    config = kwargs.get("config")

    discover_config = kwargs.get("discover_config", discover_config_base)
    config = discover_config(config)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    existing_handlers = root_logger.handlers
    [root_logger.removeHandler(i) for i in existing_handlers]

    config = {k.lower(): v for k, v in config.items()}

    discover_context = kwargs.get("discover_context", lambda: config.get("context", {}))
    flatten = kwargs.get("flatten", False)
    formatter = JsonFormatter(discover_context=discover_context, flatten=flatten)
    handlers = __get_handlers(config, formatter)
    for i in handlers:
        root_logger.addHandler(i)

    is_configured = True

    return logging.getLogger(name)
