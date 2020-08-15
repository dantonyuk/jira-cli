import configparser
from pathlib import Path

from config import read_config, try_to_read_config, write_config
from utils import not_implemented


def parser(build):
    parser = build('alias', help='Manage aliases')
    subparsers = parser.add_subparsers(title='alias commands', dest='alias command')

    list_parser = subparsers.add_parser('list', help='Show current aliases')
    list_parser.set_defaults(func=execute_list)

    get_parser = subparsers.add_parser('get', help='Show value of specified alias')
    get_parser.add_argument('alias')
    get_parser.set_defaults(func=execute_get)

    set_parser = subparsers.add_parser('set', help='Set value of specified alias')
    set_parser.add_argument('alias')
    set_parser.add_argument('value')
    set_parser.set_defaults(func=execute_set)

    delete_parser = subparsers.add_parser('delete', help='Delete specified alias')
    delete_parser.add_argument('alias')
    delete_parser.set_defaults(func=execute_delete)

    return parser


def execute(list, get, set, *args, **kwargs):
    not_implemented()


def execute_list(*args, **kwargs):
    config = read_config()
    if 'alias' in config:
        for key, value in config['alias'].items():
                print(f"{key} = {value}")


def execute_get(alias, *args, **kwargs):
    config = read_config()
    if 'alias' in config:
        if alias in config['alias']:
            print(config['alias'][alias])


def execute_set(alias, value, *args, **kwargs):
    config = read_config()
    if not 'alias' in config:
        config.add_section('alias')
    config['alias'][alias] = value
    write_config(config)


def execute_delete(alias, *args, **kwargs):
    config = read_config()
    if 'alias' in config:
        if alias in config['alias']:
            del config['alias'][alias]
            write_config(config)
