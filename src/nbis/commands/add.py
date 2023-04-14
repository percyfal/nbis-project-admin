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


__shortname__ = __name__.split(".")[-1]


def _add_doc_and_assets(outdir, assets, ext, template="running-slides", **kw):
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
    templates.add_template(path, f"docs/{template}.{ext}.j2", **kw)
    templates.add_template(www / "title-slide.html", "docs/assets/www/title-slide.html")
    templates.add_template(www / "tikzfig.tex", "docs/assets/www/tikzfig.tex")
    templates.add_template(
        logos / "nbis-scilifelab.svg", "docs/assets/logos/nbis-scilifelab.svg"
    )
    templates.add_template(css / "nbis.scss", "docs/assets/css/nbis.scss")


@click.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.debug(f"Running {__shortname__} subcommand.")


@main.command()
@click.option(
    "slide_type", "--type", type=click.Choice(["quarto", "rmarkdown"]), default="quarto"
)
@click.option("--show", is_flag=True, help="show template")
@click.option("--title", help="title", default="title")
@click.option("--subtitle", help="subtitle", default="subtitle")
@click.option("--author", help="author")
@click.option(
    "--assets", help="assets location relative to document", default="../assets"
)
@click.option(
    "--bibliography", help="bibliography", default="../../resources/bibliography.bib"
)
@click.option(
    "--csl",
    help="csl",
    default="https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl",  # noqa
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
    assets = outdir / kw["assets"]
    ext = "qmd"
    if slide_type == "rmarkdown":
        ext = "Rmd"
    if show:
        t = templates.render_template(f"docs/running-slides.{ext}.j2", **kw)
        click.echo(t)
    else:
        _add_doc_and_assets(outdir, assets, ext)


@main.command()
@click.option(
    "doc_type",
    "--doc-type",
    type=click.Choice(["quarto", "markdown"]),
    default="quarto",
)
@click.option("--show", is_flag=True, help="show template")
@click.option("--title", help="title", default="title")
@click.option("--subtitle", help="subtitle", default="subtitle")
@click.option("--author", help="author")
@click.option(
    "--assets", help="assets location relative to document", default="../assets"
)
@click.option(
    "--bibliography", help="bibliography", default="../../resources/bibliography.bib"
)
@click.option(
    "--csl",
    help="csl",
    default="https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl",  # noqa
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
    logger.info(f"Initializing diary file {diary}")
    if "docs" not in env.config.keys():
        env.config["docs"] = Config({"src": env.home / "docs"})

    outdir = pathlib.Path(env.config.docs.src) / kw["name"]
    assets = outdir / kw["assets"]
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
        _add_doc_and_assets(outdir, assets, ext, template="diary", **kw)


@main.command
@click.argument("command_group")
@click.option("--path", help="output template to path", type=click.Path(exists=False))
@click.option("--show", is_flag=True, help="show rendered template")
@pass_environment
def command_group(env, command_group, path, show):
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


@main.command
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
def command(env, command, group, path, show, standalone):
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
        data = path.read_text()
        data = data + t
        if not re.search(rf"def {command}\(", data):
            path.write_text(data)
        else:
            logger.warning(f"Command {command} already defined in {path}; skipping")
