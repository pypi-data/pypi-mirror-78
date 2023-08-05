import sys
from argparse import ArgumentParser

import yaml
from miniscule.base import read_config, load_config
from miniscule.logs import init_logging


def _create_parser():
    parser = ArgumentParser()
    parser.add_argument("path", metavar="PATH", nargs="?")
    parser.add_argument("-c", "--command", metavar="STR")
    return parser


def main():
    init_logging()
    parser = _create_parser()
    (settings, _) = parser.parse_known_args()
    if settings.command:
        obj = load_config(settings.command)
    else:
        obj = read_config(settings.path)

    if isinstance(obj, str):
        print(obj)
    else:
        yaml.dump(obj, sys.stdout)
