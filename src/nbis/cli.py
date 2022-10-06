"""Console script for nbis based on click."""
import logging
import os

import click
from nbis import decorators
from nbis.env import Environment

from . import __version__

__author__ = "Per Unneberg"


logger = logging.getLogger(__name__)


CONTEXT_SETTINGS = dict(auto_envvar_prefix="NBIS_ADMIN", show_default=True)

pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class NbisCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and not filename.startswith("__"):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            mod = __import__(f"nbis.commands.{name}", None, None, ["main"])
        except ImportError:
            return
        return mod.main


@click.command(
    cls=NbisCLI, context_settings=CONTEXT_SETTINGS, help=__doc__, name="nbis-admin"
)
@click.version_option(version=__version__)
@decorators.debug_option()
@pass_environment
def cli(env):
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s [%(name)s:%(funcName)s]: %(message)s"
    )
    if env.debug:
        logging.getLogger().setLevel(logging.DEBUG)
