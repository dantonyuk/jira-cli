import configparser
from pathlib import Path


_config = None


def rest_config():
    return read_config()['rest']


def try_to_read_config():
    global _config
    if _config is not None:
        return _config

    config_file = Path(Path.home(), '.jirarc')
    if not config_file.is_file():
        raise IOError(f"Cannot find configuration file {config_file}", "Run jira init first")

    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except:
        raise IOError("Cannot read configuration file {config_file}")

    _config = config
    return config


def read_config():
    try:
        return try_to_read_config()
    except IOError as ex:
        for msg in ex.args:
            print(msg)
        exit(1)


def write_config(config):
    config_file = Path(Path.home(), '.jirarc')
    try:
        with open(config_file, 'w') as f:
            config.write(f)
            _config = config
    except IOError as ex:
        for msg in ex.args:
            print(msg)
        exit(1)
