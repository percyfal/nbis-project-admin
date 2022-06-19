import argparse
from importlib.machinery import SourceFileLoader

import pytest
from nbis.cli import get_top_parser
from nbis.cli import make_minimal_parser
from nbis.cli import make_subcommand_parser
from nbis.cli import subcommands_modules


def add_module(p, pkg, modules):
    pout = p / pkg
    pout.mkdir()
    for mod in modules:
        fn = f"__{mod}__.py" if mod == "init" else f"{mod}.py"
        out = pout / fn
        out.write_text(f'"""\n{mod}\n"""')
    return pout


@pytest.fixture
def package(tmp_path):
    pout = add_module(tmp_path, "package", ["init"])
    add_module(pout, "commands", ["init", "foo", "bar"])
    add_module(pout, "utils", ["init", "foobar", "barfoo"])
    package = SourceFileLoader(
        fullname="package", path=str(pout / "__init__.py")
    ).load_module()
    return package


@pytest.fixture
def commands(package):
    from package import commands

    return commands


@pytest.fixture
def utils(package):
    from package import utils

    return utils


@pytest.fixture
def webexport(monkeypatch):
    from nbis.subcommands import webexport

    def mockreturn(cls):
        return "Mock webexport runner"

    monkeypatch.setattr(webexport, "main", mockreturn)


def test_subcommands_modules(commands):
    modules = {
        mod: docstring.strip() for mod, docstring in subcommands_modules(commands)
    }
    assert sorted(modules.keys()) == ["bar", "foo"]
    assert sorted(modules.values()) == ["bar", "foo"]


def test_make_minimal_parser(commands, utils):
    top_parser = get_top_parser("nbis")
    parser, _ = make_minimal_parser(top_parser, [commands, utils])
    subcommands = []
    for action in parser._action_groups:
        for act in action._actions:
            if isinstance(act, argparse._SubParsersAction):
                subcommands.extend(act.choices.keys())
    assert set(subcommands) == {"bar", "foo", "barfoo", "foobar"}


def test_webexport_subcommand(webexport):
    top_parser = get_top_parser("nbis")
    parser = make_subcommand_parser(top_parser, "webexport")
    args = parser.parse_args(["webexport"])
    results = args.runner(args)
    assert results == "Mock webexport runner"
