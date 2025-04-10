"""Test initialization of project."""

from nbis.cli import cli

expected = [
    "project_foo/.gitignore",
    "project_foo/.markdownlint.yaml",
    "project_foo/.pre-commit-config.yaml",
    "project_foo/.pylintrc",
    "project_foo/README.md",
    "project_foo/setup.cfg",
    "project_foo/pyproject.toml",
    "project_foo/src/project_foo/__init__.py",
    "project_foo/src/project_foo/cli.py",
    "project_foo/src/project_foo/config.py",
    "project_foo/src/project_foo/core/__init__.py",
    "project_foo/src/project_foo/core/options.py",
    "project_foo/src/project_foo/core/snakemake.py",
    "project_foo/src/project_foo/core/wrappers.py",
    "project_foo/src/project_foo/commands/__init__.py",
    "project_foo/src/project_foo/env.py",
    "project_foo/src/project_foo/schemas/config.schema.yaml",
    "project_foo/src/project_foo/schemas/profile.schema.yaml",
]


def test_init_relative(runner, cd_tmp_path):
    """Test initialization of project with relative path."""
    out = cd_tmp_path / "project_foo"
    result = runner.invoke(cli, ["init", out.name])
    assert not result.exception
    files = [str(p.relative_to(out.parent)) for p in out.rglob("*") if p.is_file()]
    assert sorted(files) == sorted(expected)


def test_init_absolute(runner, tmp_path):
    """Test initialization of project with absolute path."""
    out = tmp_path / "project_foo"
    result = runner.invoke(cli, ["init", str(out)])
    assert not result.exception
    files = [str(p.relative_to(out.parent)) for p in out.rglob("*") if p.is_file()]
    assert sorted(files) == sorted(expected)


def test_init_curdir(runner, project_foo):
    """Test initialization of project."""
    out = project_foo
    result = runner.invoke(cli, ["init", "."])
    assert not result.exception
    files = [str(p.relative_to(out.parent)) for p in out.rglob("*") if p.is_file()]
    assert sorted(files) == sorted(expected)
