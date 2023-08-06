import os


def _parse_value(value):
    if isinstance(value, list):
        return [_parse_value(i) for i in value]

    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _parse_nested_env(key, value, level_sep="_", list_sep=","):
    split = key.split(level_sep)
    if len(split) == 1:
        if list_sep in value:
            value = value.split(list_sep)
        return {key: _parse_value(value)}
    return {
        split[0]: _parse_nested_env(level_sep.join(split[1:]), value),
    }


def parse_env(prefix=None, env=os.environ):
    env_config = None
    if prefix is not None:
        prefix = prefix.lower()
        env_config = {k.lower().split(prefix)[-1]: v for k, v in env.items() if k.lower().startswith(prefix)}
    else:
        env_config = env

    env_config_parsed = {}
    for k, v in env_config.items():
        nested = _parse_nested_env(k, v)
        env_config_parsed.update(nested)

    return env_config_parsed
