import configparser
from pathlib import Path

from config import read_config, try_to_read_config


def parser(build):
    parser = build('init', help='Initialize jira client')
    parser.add_argument('-s', '--show', action="store_true", help='Show jira initilization data')
    return parser


def execute(show, *args, **kwargs):
    if show:
        config = read_config()
        for section, data in config.items():
            for key, value in data.items():
                print(f"{section}.{key}={value}")
    else:
        url = input("Jira URL: ")
        username = input("Username: ")
        password = input("Password: ")

        try:
            config = try_to_read_config()
        except:
            config = configparser.ConfigParser()

        config['rest'] = { 'url': url, 'username': username, 'password': password }
        with open(Path(Path.home(), '.jirarc'), 'w') as f:
            config.write(f)
