"""Console script for nbis."""
import ast
import importlib
import logging
import pkgutil
import sys
from argparse import ArgumentDefaultsHelpFormatter
from argparse import ArgumentParser

from . import __version__
from . import subcommands

# Code initially by Marcel Martin, with minor modifications by author
__author__ = "Per Unneberg"


logger = logging.getLogger(__name__)


class RawDescriptionDefaultsHelpFormatter(ArgumentDefaultsHelpFormatter):
    """Help message formatter which retains any formatting in
    descriptions and adds default values."""

    def _fill_text(self, text, width, indent):
        return "".join(indent + line for line in text.splitlines(keepends=True))


class DescriptionArgumentParser(ArgumentParser):
    """An ArgumentParser that prints correctly formatted description
    and epilog help strings"""

    def __init__(self, *args, **kwargs):
        if "formatter_class" not in kwargs:
            kwargs["formatter_class"] = RawDescriptionDefaultsHelpFormatter
        super().__init__(*args, **kwargs)

    def error(self, message):
        self.print_help(sys.stderr)
        args = {"prog": self.prog, "message": message}
        self.exit(2, "%(prog)s: error: %(message)s\n" % args)


def get_top_parser(prog):
    # fmt: off
    top_parser = DescriptionArgumentParser(
        description=__doc__,
        prog=prog,
    )
    top_parser.add_argument(
        '--config-file',
        action='store',
        default=None,
        help='configuration file'
    )
    top_parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + __version__
    )
    top_parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='Print debug messages'
    )
    # fmt: on
    return top_parser


def main(arg_list=None):
    if arg_list is None:
        arg_list = sys.argv[1:]
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    top_parser = get_top_parser("nbis")
    minimal_parser, _ = make_minimal_parser(top_parser, subcommands)
    logger.info(dir(minimal_parser))
    subcommand_name = get_subcommand_name(minimal_parser, arg_list)
    top_parser = get_top_parser("nbis")
    parser = make_subcommand_parser(top_parser, subcommand_name)

    args, extra = parser.parse_known_args(arg_list)

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    del args.debug

    args.project_name = "nbis"
    args.prog = parser.prog
    args.extra_options = extra
    if args.config_file is None:
        args.config_file = f"{args.project_name}.yaml"
    args.runner(args)

    return 0


def get_subcommand_name(parser, arg_list) -> str:
    """Parse arg_list to get name of subcommand"""
    args, _ = parser.parse_known_args(arg_list)
    module_name = getattr(args, "module_name", None)
    if module_name is None:
        parser.error("Please provide the name of a subcommand to run")
    return module_name


def make_subcommand_parser(parser, subcommand_name, package=subcommands):
    """
    Make parser and load module whilst adding subparser documentation.
    """
    subparsers = parser.add_subparsers()
    module = importlib.import_module("." + subcommand_name, package.__name__)
    # fmt: off
    subparser = subparsers.add_parser(
        subcommand_name,
        help=module.__doc__.split("\n", maxsplit=2)[1],
        description=module.__doc__
    )
    # fmt: on
    subparser.set_defaults(module_name=subcommand_name, runner=module.main)
    module.add_arguments(subparser)
    return parser


# We need the minimal parser just to get the actual subcommand name
def make_minimal_parser(parser, package_list):
    """
    Make minimal parser including subcommands from package_list
    """
    subparsers = parser.add_subparsers()
    subcommands_map = dict()

    if not isinstance(package_list, list):
        package_list = [package_list]
    for pkg in package_list:
        for module_name, docstring in subcommands_modules(pkg):
            subcommands_map[module_name] = pkg
            help_str = docstring.split("\n", maxsplit=2)[1].replace("%", "%%")
            # fmt: off
            subparser = subparsers.add_parser(
                module_name, help=help_str,
                description=docstring, add_help=False
            )
            # fmt: on
            subparser.set_defaults(module_name=module_name)
    return parser, subcommands_map


def subcommands_modules(package):
    """
    Yield (module_name, docstring) tuples for all modules in the given package.
    """
    modules = pkgutil.iter_modules(package.__path__)
    for module in modules:
        spec = importlib.util.find_spec(package.__name__ + "." + module.name)
        with open(spec.origin) as f:
            mod_ast = ast.parse(f.read())
        docstring = ast.get_docstring(mod_ast, clean=False)
        yield module.name, docstring
