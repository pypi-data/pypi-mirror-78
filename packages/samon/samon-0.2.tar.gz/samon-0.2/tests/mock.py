from pathlib import Path

from doculabs.samon.environment import Environment
from doculabs.samon.loaders import FileSystemLoader


def get_base_environment():
    loader = FileSystemLoader(Path(__file__).parent / 'assets/base')
    env = Environment(loader=loader)
    return env
