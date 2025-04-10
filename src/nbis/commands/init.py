"""Initialize python project skeleton with a CLI.

Initialize a python project with a CLI in PROJECT_DIRECTORY.
Initialization will add a bare minimum of files needed to setup a
python project, including pyproject.toml, setup.cfg and src directory
containing module to run a CLI.

To activate the CLI, after initialization the newly created project
must be put under version control and installed:

\b
    cd PROJECT_DIRECTORY
    git init
    git add -f .
    python -m pip install -e .

The CLI can then be accessed through the PROJECT_NAME command, which
by default is equal to the PROJECT_DIRECTORY name:

    PROJECT_NAME
"""

import logging
import pathlib

import click

from nbis import templates

__shortname__ = __name__.rsplit(".", maxsplit=1)[-1]


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
@click.pass_context
def main(
    ctx,
    project_directory,
    description,
    project_name,
    repo_name,
    **kw,
):
    """Main init command"""
    logger.debug("Running %s subcommand.", __shortname__)
    p = pathlib.Path(project_directory).absolute()
    if project_name is None:
        project_name = p.name
    if repo_name is None:
        repo_name = project_name
    python_module = repo_name
    data = {
        "project_directory": str(p.name),
        "repo_name": repo_name,
        "project_name": project_name,
        "python_module": python_module,
        "description": description,
        "version": ctx.obj.version,
        "open_source_license": kw.get("open_source_license"),
        "config_file": ctx.obj.config.get("config_file", p / f"{python_module}.yaml"),
        "author": kw.get("author"),
    }

    pdir = pathlib.Path(project_directory)
    if not pdir.exists():
        pdir.mkdir()

    setup = pdir / "setup.cfg"
    setup.touch()
    templates.multi_add(
        pdir,
        files=[
            "README.md",
            "pyproject.toml",
            ".gitignore",
            ".pre-commit-config.yaml",
            ".markdownlint.yaml",
        ],
        **data,
    )
    templates.init_py_module(
        pdir,
        module=python_module,
        files=["__init__.py", "cli.py", "env.py", "config.py"],
        **data,
    )
    templates.init_py_module(
        pdir,
        module=python_module,
        submodule="schemas",
        init=False,
        files=["config.schema.yaml", "profile.schema.yaml"],
        **data,
    )
    templates.init_py_module(pdir, module=python_module, submodule="commands", **data)
    templates.init_py_module(
        pdir,
        module=python_module,
        submodule="core",
        files=["options.py", "snakemake.py", "wrappers.py"],
        **data,
    )
