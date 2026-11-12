"""Test that add/smk commands render imports with the python module."""

import ast

import pytest

from nbis.cli import cli


def _imported_roots(path):
    """Yield the top-level module name of every absolute import in a file."""
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module.split(".")[0]
        elif isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name.split(".")[0]


@pytest.mark.parametrize(
    "name,module",
    [("my_project", "my_project"), ("my-project", "my_project")],
)
def test_admin_flow_uses_python_module(runner, tmp_path, monkeypatch, name, module):
    """Imports in generated code must use the python module name."""
    out = tmp_path / name
    steps = [
        ["init", str(out)],
        ["config", "init"],
        ["smk", "init"],
        ["smk", "add", "main"],
        ["add", "tool", "my_tool"],
        ["add", "command-group", "grp"],
        ["add", "command", "cmd", "--group", "grp"],
    ]
    for step in steps:
        if step[0] != "init":
            monkeypatch.chdir(out)
        result = runner.invoke(cli, step)
        assert not result.exception, (step, result.output)

    pkg = out / "src" / module
    assert pkg.is_dir()
    roots = set()
    for f in pkg.rglob("*.py"):
        roots.update(_imported_roots(f))  # SyntaxError here means an empty module
    assert module in roots
    assert name == module or name not in roots


def test_config_file_named_after_project(runner, tmp_path, monkeypatch):
    """The config file is named after the project, not the directory."""
    out = tmp_path / "some_directory"
    result = runner.invoke(cli, ["init", str(out), "--project-name", "my-project"])
    assert not result.exception
    monkeypatch.chdir(out)
    result = runner.invoke(cli, ["config", "init"])
    assert not result.exception
    assert (out / "my-project.yaml").exists()
    assert not (out / "some_directory.yaml").exists()
    # Fails (placeholder project name) unless the config file is found
    result = runner.invoke(cli, ["smk", "init"])
    assert not result.exception
    assert (out / "src" / "my_project" / "smk" / "config.py").exists()


def test_no_config_file_uses_pyproject_name(runner, tmp_path, monkeypatch):
    """Without a config file, the project name is read from pyproject.toml."""
    out = tmp_path / "some_directory"
    result = runner.invoke(cli, ["init", str(out), "--project-name", "my-project"])
    assert not result.exception
    monkeypatch.chdir(out)
    assert not (out / "my-project.yaml").exists()  # no config file
    result = runner.invoke(cli, ["smk", "init"])
    assert not result.exception
    assert (out / "src" / "my_project" / "smk" / "config.py").exists()
    assert not (out / "src" / "nbis_admin").exists()
