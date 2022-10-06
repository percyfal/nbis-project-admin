import os
import pathlib
import sys

import click

from . import __version__


class Environment:
    def __init__(self):
        self.verbose = False
        self.home = pathlib.Path(os.getcwd())
        self.debug = False
        self.dry_run = False
        self.version = __version__

    def log(self, msg, *args):
        """Logs a message"""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr"""
        if self.verbose:
            self.log(msg, *args)