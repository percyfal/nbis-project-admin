"""Snakemake administration utilities


"""
import logging

import click
from nbis.cli import pass_environment
from nbis.templates import add_template
from nbis.templates import render_template


__shortname__ = __name__.split(".")[-1]

logger = logging.getLogger(__name__)


def add_group_smk_py(env, group, **kw):
    pyfile = env.home / "src" / env.config.project_name / "commands" / f"{group}.py"
    add_template(
        pyfile,
        "src/python_module/commands/group.smk.py.j2",
        project_name=env.config.project_name,
        command=group,
        test=kw["test"],
    )


def add_command_smk_py(env, group, **kw):
    pyfile = env.home / "src" / env.config.project_name / "commands" / f"{group}.py"
    assert (
        f"def {kw['command']}(" not in pyfile.read_text()
    ), f"{kw['command']} already defined"
    kw["group"] = group
    with open(pyfile, "a") as fh:
        fh.write(render_template("src/python_module/commands/command.smk.py.j2", **kw))


def add_command_smk(env, group, command, **kw):
    smkfile = env.home / "src" / "snakemake" / "commands" / f"{group}-{command}.smk"
    add_template(
        smkfile,
        "src/snakemake/commands/command.smk.j2",
        project_name=env.config.project_name,
        command=command,
        test=kw["test"],
        validation=kw["validation"],
        group=group,
    )


def add_test_config(env, group, command):
    smkfile = (
        env.home
        / "src"
        / "snakemake"
        / "commands"
        / f"test-{group}-{command}-config.smk"
    )
    add_template(
        smkfile,
        "src/snakemake/commands/test-config.smk.j2",
    )


def add_test_smk_setup(env, group, command):
    smkfile = (
        env.home
        / "src"
        / "snakemake"
        / "commands"
        / f"test-{group}-{command}-setup.smk"
    )
    add_template(smkfile, "src/snakemake/commands/test-setup.smk.j2", command=command)


def add_config_yaml(env):
    yamlconf = env.home / "config" / "config.yaml"
    add_template(yamlconf, "config/config.yaml.j2")


def add_config_schema_yaml(env):
    confschema = env.home / "schemas" / "config.schema.yaml"
    add_template(confschema, "schemas/config.schema.yaml.j2")


def add_samples_schema_yaml(env):
    sampleschema = env.home / "schemas" / "samples.schema.yaml"
    add_template(sampleschema, "schemas/samples.schema.yaml.j2")


def add_samples_tsv(env):
    samplestsv = env.home / "resources" / "samples.tsv"
    add_template(samplestsv, "resources/samples.tsv.j2")


def add_local_profile(env):
    localprofile = env.home / "config" / "local" / "config.yaml"
    add_template(localprofile, "config/local/profile.yaml.j2")


def add_config_py(env):
    """Add python configuration module"""
    configfile = env.home / "src" / env.config.project_name / "snakemake" / "config.py"
    add_template(
        configfile,
        "src/python_module/snakemake/config.py.j2",
        project_name=env.config.project_name,
    )


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
@pass_environment
def add(env, group, **kw):
    """Add snakefile and python helper code.

    Add snakefile and possibly a command CLI. There are options to
    add tests and validation.

    """
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
    config/config.yaml, resources/samples.tsv, src/project_name/snakemake/config.py,
    schemas/config.schema.yaml and schemas/samples.schema.yaml.
    """
    add_config_py(env)
    add_local_profile(env)
    add_config_yaml(env)
    add_config_schema_yaml(env)
    add_samples_schema_yaml(env)
    add_samples_tsv(env)
