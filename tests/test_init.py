"""Test initialization of project."""
import ast

import pytest
import toml

from nbis.cli import cli

expected = [
    "project_foo/.gitignore",
    "project_foo/.markdownlint.yaml",
    "project_foo/.pre-commit-config.yaml",
    "project_foo/.pylintrc",
    "project_foo/README.md",
    "project_foo/CONTRIBUTING.md",
    "project_foo/pyproject.toml",
    "project_foo/docs/architecture.md",
    "project_foo/docs/_quarto.yml",
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

def _imported_roots(path):
    """Yield the top-level module name of every absolute import in a a file."""
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module.split(".")[0]
        elif isinstance(node, ast.Import):
            for alias in node.names:
                yield alias.name.split(".")[0]

@pytest.mark.parametrize(
    "project_name,repo_name,module",
    [
        ("my_project", "my_repo", "my_project"),
        ("my-project", "my-repo", "my_project"),
    ],
)
def test_init_repo_name_differs(runner, tmp_path, project_name, repo_name, module):
    """The python module derives from the project name, not the repo name."""
    out = tmp_path / project_name
    result = runner.invoke(
        cli,
        [
            "init",
            str(out),
            "--project-name",
            project_name,
            "--repo-name",
            repo_name
        ],
    )
    assert not result.exception
    pkg = out / "src" / module
    assert pkg.is_dir()

    roots = set()
    for f in pkg.rglob("*.py"):
        roots.update(_imported_roots(f))
    assert module in roots
    assert repo_name not in roots
    assert repo_name.replace("-", "_") not in roots


def test_init_console_script_named_after_project(runner, tmp_path):
    """The console script is named after the project, pointing at the module."""
    out = tmp_path / "project_foo"
    result = runner.invoke(cli, ["init", str(out), "--project-name", "my-project"])
    assert not result.exception
    pyproject = toml.load(out / "pyproject.toml")
    assert pyproject["project"]["name"] == "my-project"
    assert pyproject["project"]["scripts"] == {"my-project": "my_project.cli:cli"}


def test_init_env_var_names_are_valid(runner, tmp_path):
    """Environment variable names derive from the python module name."""
    out = tmp_path / "project_foo"
    result = runner.invoke(cli, ["init", str(out), "--project-name", "my-project"])
    assert not result.exception
    pkg = out / "src" / "my_project"
    options = (pkg / "core" / "options.py").read_text()
    assert '"MY_PROJECT_CONFIG_FILE"' in options
    assert '"MY_PROJECT_SNAKEMAKE_DIRECTORY"' in (pkg / "core" / "snakemake.py").read_text()
    assert '"auto_envvar_prefix": "MY_PROJECT"' in (pkg / "cli.py").read_text()
    for f in (pkg / "cli.py", pkg / "core" / "options.py", pkg / "core" / "snakemake.py"):
        assert "MY-PROJECT" not in f.read_text()
