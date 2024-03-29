"""Environment for nbis-admin"""

import os
import pathlib
import sys

import click

from nbis.config import Config

try:
    from dotenv import dotenv_values
except ImportError:
    pass

from . import __version__


class Environment:
    """Environment for nbis-admin"""

    def __init__(self):
        self.verbose = False
        self.home = pathlib.Path(os.getcwd())
        self.debug = False
        self.dry_run = False
        self.version = __version__
        self.config = Config(data={"project_name": "nbis-admin"})
        try:
            self.dotenv = dotenv_values(self.home / ".env")
        except NameError:
            self.dotenv = {}

    def log(self, msg, *args):
        """Logs a message"""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr"""
        if self.verbose:
            self.log(msg, *args)
