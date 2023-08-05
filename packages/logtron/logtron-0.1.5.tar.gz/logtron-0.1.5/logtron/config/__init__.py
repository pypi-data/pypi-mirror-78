import os

import yaml

DEFAULT_CONFIG = {
    "handlers": [
        "logtron.handlers.ConsoleHandler",
    ],
}


def _parse_value(value):
    if type(value) == list:
        return [_parse_value(i) for i in value]

    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _parse_nested_env(key, value):
    split = key.split("_")
    if len(split) == 1:
        if "," in value:
            value = value.split(",")
        return {key: _parse_value(value)}
    return {
        split[0]: _parse_nested_env("_".join(split[1:]), value),
    }


def _parse_env():
    env_config = dict(
        [
            (i.lower().split("logtron_")[-1], os.environ.get(i))
            for i in os.environ.keys()
            if i.lower().startswith("logtron_")
        ]
    )
    env_config_parsed = {}
    for k, v in env_config.items():
        nested = _parse_nested_env(k, v)
        env_config_parsed.update(nested)

    return env_config_parsed


def discover_config(existing=None):
    config = DEFAULT_CONFIG.copy()
    config_file = "logtron.yaml"

    if existing is not None:
        if type(existing) == dict:
            config.update(existing)
        elif type(existing) == str:
            config_file = existing

    # Read config file
    if os.path.isfile(config_file):
        f = open(config_file, "r")
        file_config = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
        config.update(file_config)

    # Read env vars
    env_config = _parse_env()

    config.update(env_config)

    return config
