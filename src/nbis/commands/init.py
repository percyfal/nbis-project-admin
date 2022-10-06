"""Initialize python project skeleton with a CLI.

Initialize a python project with a CLI in PROJECT_DIRECTORY.
Initialization will add a bare minimum of files needed to setup a
python project, including pyproject.toml, setup.cfg and src directory
containing module to run a CLI.

To activate the CLI, after initialization the newly created project
must be put under version control and installed:

    cd PROJECT_DIRECTORY
    git init
    git add -f .
    python -m pip install -e .

The CLI can then be accessed through the PROJECT_NAME comand, which by
default is equal to the PROJECT_DIRECTORY name:

    PROJECT_NAME

nbis-admin subcommands are available via the subcommand 'admin':

    PROJECT_NAME admin

which allows for easy access to administration commands for adding
templates to the project. The advantage of accessing the admin
commands here is that they will automatically apply the project
settings and context to execution.

"""
import logging
import pathlib

import click
from nbis import decorators
from nbis import templates


__shortname__ = __name__.split(".")[-1]


logger = logging.getLogger(__name__)


@click.command(help=__doc__, name=__shortname__)
@click.argument("project_directory", type=click.Path(exists=False))
@click.option(
    "--description",
    help="short description of the project",
    default="A short description of the project.",
)
@click.option(
    "--project-name",
    help=(
        "project name if different from project directory. "
        "Defaults to PROJECT_DIRECTORY."
    ),
)
@click.option(
    "--repo-name",
    help="repo name if different from project name. Defaults to PROJECT_NAME.",
)
@click.option(
    "--open-source-license",
    help="open source licencse.",
    type=click.Choice(["MIT", "BSD-3-Clause"]),
    default=None,
)
@click.option("--author", help="author name")
@decorators.dry_run_option
@click.pass_context
def main(
    ctx,
    project_directory,
    description,
    project_name,
    repo_name,
    open_source_license,
    author,
    dry_run,
):
    logger.debug(f"Running {__shortname__} subcommand.")
    p = pathlib.Path(project_directory).absolute()
    if project_name is None:
        project_name = p.name
    if repo_name is None:
        repo_name = project_name
    python_module = repo_name
    data = {
        "project_directory": str(p),
        "repo_name": repo_name,
        "project_name": project_name,
        "python_module": python_module,
        "description": description,
        "version": ctx.obj.version,
        "open_source_license": open_source_license,
        "author": author,
    }
    pdir = pathlib.Path(project_directory)
    if not pdir.exists():
        pdir.mkdir()
    setup = pdir / "setup.cfg"
    setup.touch()
    templates.add_template(pdir / "README.md", "project/README.md.j2", **data)
    templates.add_template(pdir / "pyproject.toml", "project/pyproject.toml.j2", **data)
    templates.add_template(
        pdir / ".pre-commit-config.yaml",
        "project/.pre-commit-config.yaml.j2",
        **data,
    )
    templates.add_template(
        pdir / "src" / python_module / "__init__.py",
        "project/src/python_module/__init__.py.j2",
        **data,
    )
    templates.add_template(
        pdir / "src" / python_module / "cli.py",
        "project/src/python_module/cli.py.j2",
        **data,
    )
    command_dir = pdir / "src" / python_module / "commands"
    command_dir.mkdir(exist_ok=True, parents=True)
    command_init = command_dir / "__init__.py"
    command_init.touch()
    templates.add_template(
        command_dir / "admin.py",
        "project/src/python_module/commands/admin.py.j2",
        **data,
    )
