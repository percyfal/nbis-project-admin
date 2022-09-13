"""Documentation administration utilities


"""
import logging
import os
import pathlib

import click
import pkg_resources
from nbis.config import Config
from nbis.config import load_config
from nbis.templates import env

__shortname__ = __name__.split(".")[-1]


logger = logging.getLogger(__name__)


@click.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.debug(f"Running {__shortname__} subcommand.")


@main.command()
@click.option(
    "--template", "-t", help="documentation template", default="running-slides"
)
@click.option("--title", help="title", default="title")
@click.option("--subtitle", help="subtitle", default="subtitle")
@click.option("--author", help="author")
@click.option(
    "--bibliography", help="bibliography", default="../resources/bibliography.bib"
)
@click.option(
    "--csl",
    help="csl",
    default="https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl",  # noqa
)
@click.option("--path", help="work on path")
@click.option("--css", help="css template")
@click.option(
    "--scss",
    help="scss template",
    default=pkg_resources.resource_filename("nbis", "resources/nbis.scss"),
)
@click.option("--config-file", help="configuration file")
@click.pass_context
def add(ctx, template, **kw):
    """Add documentation template"""
    logger.info("Adding documentation template.")
    config = load_config(file=kw["config_file"])
    if config.is_empty:
        config = Config({"docs": {"src": pathlib.Path(os.curdir) / "docs"}})

    outdir = pathlib.Path(config.docs.src)
    if not outdir.exists():
        outdir.mkdir()
    if template == "running-slides":
        path = (
            pathlib.Path(kw["path"])
            if kw["path"] is not None
            else outdir / "running-slides.qmd"
        )
        if path.exists():
            logger.error(f"{path} exists; not overwriting")
            raise FileExistsError(f"{path} exists; skipping!")
        template = env.get_template("running-slides.qmd.j2")
        options = dict(filename=os.path.basename(path))
        options.update(kw)
        with open(path, "w") as fh:
            fh.write(template.render(**options))
    else:
        logger.error(f"Unknown template '{template}'")
