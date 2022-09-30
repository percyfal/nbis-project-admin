"""Console script for nbis based on click."""
import importlib
import logging
import os
import pathlib
import pkgutil

import click
from nbis import commands
from nbis import decorators

from . import __version__

__author__ = "Per Unneberg"


logger = logging.getLogger(__name__)


@click.group(help=__doc__)
@click.version_option(version=__version__)
@decorators.debug_option()
@click.pass_context
def cli(ctx):
    """Cli help"""
    ctx.ensure_object(dict)
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s [%(name)s:%(funcName)s]: %(message)s"
    )
    if ctx.obj["DEBUG"]:
        logging.getLogger().setLevel(logging.DEBUG)
    ctx.obj["ROOT"] = pathlib.Path(os.curdir)


def main():
    setup_commands()
    cli(obj={})


def setup_commands(commands=commands, cli=cli):
    add_subcommands(commands, cli)


def add_subcommands(package, cli=cli):
    """Iterate subpackages to add subcommands. NB: this will probably
    take time and we would like to quickly generate the help message."""
    for mod in iter_modules(package):
        imod = importlib.import_module(package.__name__ + "." + mod.name, mod.name)
        cli.add_command(imod.main)
    for pkg in iter_packages(package):
        ipkg = importlib.import_module(package.__name__ + "." + pkg.name, pkg.name)
        add_subcommands(ipkg, cli)


def iter_modules(package):
    """Iter modules in a package"""
    yield from iter_pkgmod(package, ispkg=False)


def iter_packages(package):
    """Iter packages in a package"""
    yield from iter_pkgmod(package)


def iter_pkgmod(package, ispkg=True):
    """
    Yield module for all modules or packages in the given package
    """
    modules = pkgutil.iter_modules(package.__path__)
    for mod in modules:
        if mod.ispkg == ispkg:
            yield mod
