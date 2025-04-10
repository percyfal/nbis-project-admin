"""Add template to a project.

Render various templates to a project. This includes documentation
templates, such as running-slides, commands and command groups,

"""

import logging
import pathlib
import re
import sys
from datetime import date

import click

from nbis import templates
from nbis.cli import pass_environment
from nbis.config import Config

logger = logging.getLogger(__name__)


__shortname__ = __name__.rsplit(".", maxsplit=1)[-1]


def _add_doc_and_assets(outdir, ext, template_name="running-slides", **kw):
    assets = outdir / kw["assets"]
    path = outdir / f"index.{ext}"
    www = assets / "www"
    css = assets / "css"
    logos = assets / "logos"
    if not outdir.exists():
        outdir.mkdir(parents=True)
    if not www.exists():
        www.mkdir(parents=True)
        css.mkdir()
        logos.mkdir()
    templates.add_template(path, f"docs/{template_name}.{ext}.j2", **kw)
    templates.add_template(www / "title-slide.html", "docs/assets/www/title-slide.html")
    templates.add_template(www / "tikzfig.tex", "docs/assets/www/tikzfig.tex")
    templates.add_template(
        logos / "nbis-scilifelab.svg", "docs/assets/logos/nbis-scilifelab.svg"
    )
    templates.add_template(css / "nbis.scss", "docs/assets/css/nbis.scss")


def _snake_to_caml(value):
    return "".join(word.capitalize() for word in value.split("_"))


@click.group(help=__doc__, name=__shortname__)
def main():
    """Add template to a project."""
    logger.debug("Running %s subcommand.", __shortname__)


@main.command()
@click.option(
    "slide_type",
    "--type",
    type=click.Choice(["quarto", "rmarkdown"]),
    default="quarto",
)
@click.option("--show", is_flag=True, help="show rendered template")
@click.option("--title", help="title", default="title")
@click.option("--subtitle", help="subtitle", default="subtitle")
@click.option("--author", help="author")
@click.option(
    "--assets",
    help="assets location relative to document",
    default="../assets",
)
@click.option(
    "--bibliography",
    help="bibliography",
    default="../../resources/bibliography.bib",
)
@click.option(
    "--csl",
    help="csl",
    default=(
        "https://raw.githubusercontent.com/citation-style-language/"
        "styles/master/apa.csl"
    ),
)
@click.option(
    "--name",
    help="output template to named directory",
    type=click.Path(exists=False),
    default="running_slides",
)
@pass_environment
def running_slides(env, slide_type, show, **kw):
    """Add running slides template"""
    logger.info("Adding documentation template.")
    if "docs" not in env.config.keys():
        env.config["docs"] = Config({"src": env.home / "docs"})

    outdir = pathlib.Path(env.config.docs.src) / kw["name"]
    ext = "qmd"
    if slide_type == "rmarkdown":
        ext = "Rmd"
    if show:
        t = templates.render_template(f"docs/running-slides.{ext}.j2", **kw)
        click.echo(t)
    else:
        _add_doc_and_assets(outdir, ext, **kw)


@main.command()
@click.option(
    "doc_type",
    "--doc-type",
    type=click.Choice(["quarto", "markdown"]),
    default="quarto",
)
@click.option("--show", is_flag=True, help="show rendered template")
@click.option("--title", help="title", default="title")
@click.option("--subtitle", help="subtitle", default="subtitle")
@click.option("--author", help="author")
@click.option(
    "--assets",
    help="assets location relative to document",
    default="../assets",
)
@click.option(
    "--bibliography",
    help="bibliography",
    default="../../resources/bibliography.bib",
)
@click.option(
    "--csl",
    help="csl",
    default=(
        "https://raw.githubusercontent.com/"
        "citation-style-language/styles/master/apa.csl"
    ),
)
@click.option(
    "--name",
    help="output template to named directory",
    type=click.Path(exists=False),
    default="diary",
)
@pass_environment
def diary(env, doc_type, show, **kw):
    """Add diary template"""
    logger.info("Initializing diary file %s", diary)
    if "docs" not in env.config.keys():
        env.config["docs"] = Config({"src": env.home / "docs"})

    outdir = pathlib.Path(env.config.docs.src) / kw["name"]
    ext = "qmd"
    if doc_type == "markdown":
        ext = "md"
    sysargs = " ".join(sys.argv[1:])
    kw.update(
        **{
            "project_name": env.config.project_name,
            "args": sysargs,
            "date": date.today(),
        }
    )

    if show:
        t = templates.render_template(
            f"docs/diary.{ext}.j2",
            **kw,
        )
        click.echo(t)
    else:
        _add_doc_and_assets(outdir, ext, template_name="diary", **kw)


@main.command()
@click.option(
    "template_name",
    "--template",
    "-t",
    type=click.Choice(templates.INDIVIDUAL_TEMPLATES.keys()),
)
@click.option("--show", is_flag=True, help="show rendered template")
@click.option(
    "--name",
    help="output template to named directory",
    type=click.Path(exists=False),
)
@pass_environment
def template(env, template_name, show, **kw):
    """Add individual template"""
    logger.info("Adding template %s", template_name)
    if template_name is None:
        click.echo("No template specified; exiting.")
        return
    if kw["name"] is None:
        kw["name"] = env.home
    outdir = pathlib.Path(kw["name"])
    tpl = templates.INDIVIDUAL_TEMPLATES[template_name]
    path = outdir / pathlib.Path(tpl).with_suffix("").name
    if show:
        t = templates.render_template(tpl, **kw)
        click.echo(t)
    else:
        templates.add_template(path, tpl, **kw)


@main.command()
@click.argument("tool_name", type=str)
@click.option("--show", is_flag=True, help="show rendered template")
@click.option(
    "--name",
    help="output template to named directory",
    type=click.Path(exists=False),
)
@pass_environment
def tool(env, tool_name, show, **kw):
    """Add individual tool"""
    logger.info("Adding tool %s", tool_name)
    if kw["name"] is None:
        kw["name"] = pathlib.Path("src") / env.config.project_name / "tools"
    kw["tool_name"] = tool_name
    kw["project_name"] = env.config.project_name
    outdir = pathlib.Path(kw["name"])
    tpl = "src/python_module/tools/tool.py.j2"
    tools_tpl = "src/python_module/commands/tools.py.j2"
    path = outdir / f"{tool_name}.py"
    if show:
        t = templates.render_template(tpl, **kw)
        click.echo(t)
    else:
        templates.add_template(path, tpl, **kw)
        cmd_path = (
            pathlib.Path("src") / env.config.project_name / "commands" / "tools.py"
        )
        templates.add_template(cmd_path, tools_tpl, **kw)
        click.echo(
            f"Add {env.config.project_name}-{tool_name} = "
            f'"{env.config.project_name}.tools.{tool_name}:cli" to '
            "pyproject.toml and reinstall"
        )


@main.command(name="command-group")
@click.argument("command_group")
@click.option("--path", help="output template to path", type=click.Path(exists=False))
@click.option("--show", is_flag=True, help="show rendered template")
@pass_environment
def pcommand_group(env, command_group, path, show):
    """Add project CLI COMMAND_GROUP

    Add a subcommand group. This will only add the main entry point
    for a subcommand. To add commands to the group, use the `add
    command` command.

    """
    tpl = "src/python_module/commands/command.group.py.j2"
    kw = {"command": command_group}
    if path is None:
        path = (
            env.home
            / "src"
            / env.config.project_name
            / "commands"
            / f"{command_group}.py"
        )
    else:
        path = pathlib.Path(path)
    if show:
        t = templates.render_template(tpl, **kw)
        click.echo(t)
    else:
        templates.add_template(path, tpl, **kw)


@main.command(name="command")
@click.argument("command")
@click.option(
    "--group",
    help=(
        "output to group command file. WARNING: this will"
        "append the command to the group file"
    ),
)
@click.option("--path", help="append template to path", type=click.Path(exists=True))
@click.option("--show", is_flag=True, help="show rendered template")
@click.option("--standalone", is_flag=True, help="make standalone command file")
@pass_environment
def pcommand(env, command, group, path, show, standalone):  # pylint: disable=too-many-arguments
    """Render COMMAND to project CLI command group

    Add a subcommand to a command group or make standalone command
    file.
    """
    if standalone:
        tpl = "src/python_module/commands/command.standalone.py.j2"
    else:
        tpl = "src/python_module/commands/command.py.j2"
    kw = {"command": command}
    mod = group if group is not None else command
    if path is None:
        path = env.home / "src" / env.config.project_name / "commands" / f"{mod}.py"
    else:
        path = pathlib.Path(path)
    t = templates.render_template(tpl, **kw)
    if show:
        click.echo(t)
    else:
        data = path.read_text(encoding="utf-8")
        data = data + t
        if not re.search(rf"def {command}\(", data):
            path.write_text(data, encoding="utf-8")
        else:
            logger.warning("Command %s already defined in %s; skipping", command, path)
