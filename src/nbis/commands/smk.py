"""Snakemake administration utilities

The smk command group adds support for adding snakemake subcommands.
To enable, first run the command

    PROJECT_NAME admin smk init

Thereafter, snakemake commands or command groups can be added as

    PROJECT_NAME admin smk add --group smk --command run

which will add a snakefile src/snakemake/commands/smk-run.smk and a
CLI command file src/PROJECT_NAME/commands/smk.py. Once installed, the
snakemake file can be run as

    PROJECT_NAME smk run

Edit the CLI command file to add specific settings for a given
command. For instance, one may want to set a default directory in
which to run a snakemake command, which could be achieved by adding a
click option:

\b
    @click.option("--directory/-d", default="some/path")
    @click.pass_context
    def run(ctx, profile, jobs, snakemake_args, directory):
        options = list(snakemake_args) +
            ['-j', str(jobs), '--directory', directory]

The option --quarto will add a rule to run quarto based on a
specialized template.

"""

import logging

import click

from nbis.cli import pass_environment
from nbis.templates import add_template, render_template

__shortname__ = __name__.rsplit(".", maxsplit=1)[-1]

logger = logging.getLogger(__name__)


def add_group_smk_py(env, group, **kw):
    """Add snakemake python command group file"""
    pyfile = env.home / "src" / env.config.project_name / "commands" / f"{group}.py"
    add_template(
        pyfile,
        "src/python_module/commands/group.smk.py.j2",
        project_name=env.config.project_name,
        command=group,
        test=kw["test"],
    )


def add_command_smk_py(env, group, **kw):
    """Add snakemake python command file"""
    pyfile = env.home / "src" / env.config.project_name / "commands" / f"{group}.py"
    assert f"def {kw['command']}(" not in pyfile.read_text(), (
        f"{kw['command']} already defined"
    )
    kw["group"] = group
    command = "quarto" if kw["quarto"] else "command"
    with open(pyfile, "a", encoding="utf-8") as fh:
        fh.write(
            render_template(f"src/python_module/commands/{command}.smk.py.j2", **kw)
        )
        fh.write("\n")


def add_command_smk(env, group, command, **kw):
    """Add snakemake command file"""
    smkfile = (
        env.home
        / "src"
        / env.config.project_name
        / "workflow"
        / "snakemake"
        / "commands"
        / f"{group}-{command}.smk"
    )
    command_template = "quarto" if kw["quarto"] else "command"
    add_template(
        smkfile,
        f"src/python_module/workflow/snakemake/commands/{command_template}.smk.j2",
        project_name=env.config.project_name,
        command=command,
        test=kw["test"],
        validation=kw["validation"],
        group=group,
    )


def add_test_config(env, group, command):
    """Add snakemake test config file"""
    smkfile = (
        env.home
        / "src"
        / env.config.project_name
        / "workflow"
        / "snakemake"
        / "commands"
        / f"test-{group}-{command}-config.smk"
    )
    add_template(
        smkfile,
        "src/python_module/workflow/snakemake/commands/test-config.smk.j2",
    )


def add_test_smk_setup(env, group, command):
    """Add snakemake test setup file"""
    smkfile = (
        env.home
        / "src"
        / env.config.project_name
        / "workflow"
        / "snakemake"
        / "commands"
        / f"test-{group}-{command}-setup.smk"
    )
    add_template(
        smkfile,
        "src/python_module/workflow/snakemake/commands/test-setup.smk.j2",
        command=command,
    )


def add_config_yaml(env):
    """Add config.yaml file"""
    yamlconf = env.home / "config" / "config.yaml"
    add_template(yamlconf, "config/config.yaml.j2")


def add_config_schema_yaml(env):
    """Add config.schema.yaml file"""
    confschema = (
        env.home
        / "src"
        / env.config.project_name
        / "workflow"
        / "schemas"
        / "config.schema.yaml"
    )
    add_template(confschema, "src/python_module/workflow/schemas/config.schema.yaml.j2")


def add_samples_schema_yaml(env):
    """Add samples.schema.yaml file"""
    sampleschema = (
        env.home
        / "src"
        / env.config.project_name
        / "workflow"
        / "schemas"
        / "samples.schema.yaml"
    )
    add_template(
        sampleschema,
        "src/python_module/workflow/schemas/samples.schema.yaml.j2",
    )


def add_samples_tsv(env):
    """Add samples.tsv file"""
    samplestsv = env.home / "resources" / "samples.tsv"
    add_template(samplestsv, "resources/samples.tsv.j2")


def add_local_profile(env):
    """Add local snakemake profile"""
    localprofile = env.home / "config" / "local" / "config.yaml"
    add_template(localprofile, "config/local/profile.yaml.j2")


def add_config_py(env, wf="snakemake"):
    """Add python configuration module"""
    configfile = env.home / "src" / env.config.project_name / wf / "config.py"
    add_template(
        configfile,
        f"src/python_module/{wf}/config.py.j2",
        project_name=env.config.project_name,
    )


@click.group(help=__doc__, name=__shortname__)
def main():
    """Snakemake administration utilities."""
    logger.debug("Running command %s", __shortname__)


@main.command()
@click.option(
    "test",
    "--add-test",
    "-t",
    is_flag=True,
    help=("Add code to deal with tests and add simple snakemake test files"),
)
@click.option(
    "validation",
    "--add-validation",
    "-V",
    is_flag=True,
    help=("Add code to deal with validation and add schemas"),
)
@click.option(
    "profile",
    "--add-profile",
    "-p",
    is_flag=True,
    help=("Add local snakemake profile"),
)
@click.option("group", "--group", default="smk", help="snakemake command group name")
@click.option("command", "--command", default="run", help="snakemake command to add")
@click.option(
    "quarto",
    "--quarto",
    is_flag=True,
    help="add quarto snakeamake code and command",
)
@click.pass_context
def add(ctx, group, **kw):
    """Add snakefile and python helper code.

    Add snakefile and possibly a command CLI. There are options to
    add tests and validation.

    """
    env = ctx.obj
    configfile = env.home / "src" / env.config.project_name / "snakemake" / "config.py"
    if not configfile.exists():
        logger.error(
            "No snakemake configuration module available. "
            "Make sure to first run '%s smk init.'",
            ctx.find_root().info_name,
        )
        return
    if kw["quarto"]:
        kw["command"] = "quarto"
    add_group_smk_py(env, group, **kw)
    add_command_smk_py(env, group, **kw)
    command = kw.pop("command")
    add_command_smk(env, group, command, **kw)
    if kw["test"]:
        add_test_config(env, group, command)
        add_test_smk_setup(env, group, command)


@main.command()
@pass_environment
def init(env):
    """Initialize configuration files.

    Install minimal config, sample and schema files. Will install
    config/config.yaml, resources/samples.tsv,
    src/project_name/snakemake/config.py,
    schemas/config.schema.yaml and schemas/samples.schema.yaml.
    """
    add_config_py(env)
    add_local_profile(env)
    add_config_yaml(env)
    add_config_schema_yaml(env)
    add_samples_schema_yaml(env)
    add_samples_tsv(env)
