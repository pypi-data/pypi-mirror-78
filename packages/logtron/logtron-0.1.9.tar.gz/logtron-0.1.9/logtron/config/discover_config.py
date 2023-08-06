import os

import yaml

from logtron.util import parse_env

ENV_PREFIX = "LOGTRON_"
DEFAULT_CONFIG_FILE = "logtron.yaml"
DEFAULT_CONFIG = {
    "handlers": [
        "logtron.handlers.ConsoleHandler",
    ],
}


def read_config_file(path):
    if os.path.isfile(path):
        with open(path, "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)
    return {}


def discover_config(existing=None):
    config = DEFAULT_CONFIG.copy()
    if existing is None:
        existing = {}

    # Read default config file
    config.update(read_config_file(DEFAULT_CONFIG_FILE))

    # Read env vars
    config.update(parse_env(ENV_PREFIX))

    # Read explicit config
    if isinstance(existing, str):
        config.update(read_config_file(existing))
    else:
        config.update(existing)

    return config
