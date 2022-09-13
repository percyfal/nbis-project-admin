"""Snakemake administration utilities


"""
import logging
import pathlib

import click
from nbis.templates import add_template
from nbis.templates import render_template

from .config import add_config_py


__shortname__ = __name__.split(".")[-1]

logger = logging.getLogger(__name__)


def project_name(ctx):
    return ctx.find_root().info_name


def add_group_smk_py(ctx, group, **kw):
    pyfile = pathlib.Path("src") / project_name(ctx) / "commands" / f"{group}.py"
    add_template(
        pyfile,
        "src/project/commands/group.smk.py.j2",
        project_name=project_name(ctx),
        command=group,
        test=kw["test"],
    )


def add_command_smk_py(ctx, group, **kw):
    pyfile = pathlib.Path("src") / project_name(ctx) / "commands" / f"{group}.py"
    assert (
        f"def {kw['command']}(" not in pyfile.read_text()
    ), f"{kw['command']} already defined"
    with open(pyfile, "a") as fh:
        fh.write(render_template("src/project/commands/command.smk.py.j2", **kw))


def add_command_smk(ctx, command, **kw):
    smkfile = pathlib.Path("src") / "snakemake" / "rules" / f"{command}.smk"
    add_template(
        smkfile,
        "src/snakemake/rules/command.smk.j2",
        project_name=project_name(ctx),
        command=command,
        test=kw["test"],
        validation=kw["validation"],
    )


def add_test_config(command):
    smkfile = pathlib.Path("src") / "snakemake" / "rules" / f"test-{command}-config.smk"
    add_template(
        smkfile,
        "src/snakemake/rules/test-config.smk.j2",
    )


def add_test_smk_setup(command):
    smkfile = pathlib.Path("src") / "snakemake" / "rules" / f"test-{command}-setup.smk"
    add_template(smkfile, "src/snakemake/rules/test-setup.smk.j2", command=command)


def add_config_yaml():
    yamlconf = pathlib.Path("config") / "config.yaml"
    add_template(yamlconf, "config/config.yaml.j2")


def add_config_schema_yaml():
    confschema = pathlib.Path("schemas") / "config.schema.yaml"
    add_template(confschema, "schemas/config.schema.yaml.j2")


def add_samples_schema_yaml():
    sampleschema = pathlib.Path("schemas") / "samples.schema.yaml"
    add_template(sampleschema, "schemas/samples.schema.yaml.j2")


def add_samples_tsv():
    samplestsv = pathlib.Path("resources") / "samples.tsv"
    add_template(samplestsv, "resources/samples.tsv.j2")


def add_local_profile():
    localprofile = pathlib.Path("config") / "local" / "config.yaml"
    add_template(localprofile, "profile.yaml.j2")


@click.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.debug(f"Running command {__shortname__}")


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
@click.pass_context
def add(ctx, group, **kw):
    """Add snakefile and python helper code.

    Add snakefile and possibly a command CLI. There are options to
    add tests and validation.

    """
    add_group_smk_py(ctx, group, **kw)
    add_command_smk_py(ctx, group, **kw)
    command = kw.pop("command")
    add_command_smk(ctx, command, **kw)
    if kw["test"]:
        add_test_config(command)
        add_test_smk_setup(command)


@main.command()
@click.pass_context
def init(ctx):
    """Initialize configuration files.

    Install minimal config, sample and schema files. Will install
    config/config.yaml, resources/samples.tsv,
    schemas/config.schema.yaml and schemas/samples.schema.yaml.
    """
    # FIXME: move to config?
    add_config_py(ctx)
    add_local_profile()
    add_config_yaml()
    add_config_schema_yaml()
    add_samples_schema_yaml()
    add_samples_tsv()
