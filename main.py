import argparse
from os.path import dirname, basename, isfile
import glob
from importlib import import_module

from rest import enable_debug


def parse_args():
    parser = argparse.ArgumentParser(description="Jira CLI")
    parser.add_argument('-d', '--debug', type=bool, default=False, help='Enable debug mode')
    subparsers = parser.add_subparsers(title='commands', dest='command')
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')

    def build(*args, **kwargs):
        return subparsers.add_parser(parents=[parent_parser], *args, **kwargs)

    def add_parser(module_name):
        module = import_module(module_name)
        parser = module.parser(build)
        parser.set_defaults(func=module.execute)

    module_files = glob.glob(dirname(__file__) + "command/*.py")
    module_names = ['command.' + basename(f)[:-3] for f in module_files if isfile(f) and not f.endswith('__init__.py')]

    for module_name in module_names:
        add_parser(module_name)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.debug:
        enable_debug()
    args.func(**vars(args))
