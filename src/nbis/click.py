"""Console script for nbis based on click."""
import logging
import click
import pkgutil
import importlib
#import nbis.commands.smkcli
from nbis import commands
from . import __version__


__author__ = "Per Unneberg"


logger = logging.getLogger(__name__)



@click.group(help=__doc__)
@click.option("--debug", help="print debugging messages", default=False, is_flag=True)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx, debug):
    """Cli help"""
    ctx.ensure_object(dict)
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s [%(name)s:%(funcName)s]: %(message)s"
    )
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    ctx.obj['DEBUG'] = debug


def main():
    package = commands
    module = importlib.import_module(".", package.__name__)
    add_subcommands(package)
    cli(obj={})


def add_subcommands(package):
    """Iterate subpackages to add subcommands. NB: this will probably
    take time and we would like to quickly generate the help message."""
    for mod in iter_modules(package):
        imod = importlib.import_module(package.__name__ + "." + mod.name, mod.name)
    for pkg in iter_packages(package):
        ipkg = importlib.import_module(package.__name__ + "." + pkg.name, pkg.name)
        add_subcommands(ipkg)



def iter_modules(package):
    """Iter modules in a package"""
    for mod in iter_pkgmod(package, ispkg=False):
        yield mod


def iter_packages(package):
    """Iter packages in a package"""
    for pkg in iter_pkgmod(package):
        yield pkg


def iter_pkgmod(package, ispkg=True):
    """
    Yield module for all modules or packages in the given package
    """
    modules = pkgutil.iter_modules(package.__path__)
    for mod in modules:
        if mod.ispkg == ispkg:
            yield mod
