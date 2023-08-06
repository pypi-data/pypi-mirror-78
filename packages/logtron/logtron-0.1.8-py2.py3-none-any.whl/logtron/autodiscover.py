import importlib
import logging

from logtron.config import discover_config
from logtron.formatters import JsonFormatter

is_configured = False


def autodiscover(name=None, level=logging.INFO, config=None, refresh=False, discover_context=None):
    global is_configured

    if not refresh and is_configured:
        return logging.getLogger(name)

    config = discover_config(config)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    existing_handlers = root_logger.handlers
    [root_logger.removeHandler(i) for i in existing_handlers]

    context = {}
    if "context" in config:
        context = config["context"]
    elif discover_context is not None:
        context = discover_context()

    handlers = [(i,) + tuple(i.rsplit(".", 1)) for i in config["handlers"]]
    classes = [i[2] for i in handlers]

    for handler, module_name, class_name in handlers:
        HandlerClass = getattr(importlib.import_module(module_name), class_name)
        instance = None
        if handler in config and config[handler] is not None:
            instance = HandlerClass(context, **config[handler])
        elif classes.count(class_name) == 1 and (class_name in config and config[class_name] is not None):
            instance = HandlerClass(context, **config[class_name])
        else:
            instance = HandlerClass(context)
        instance.setFormatter(JsonFormatter(context))
        root_logger.addHandler(instance)

    is_configured = True

    return logging.getLogger(name)
