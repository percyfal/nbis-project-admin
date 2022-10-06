"""Diary administration utilities


"""
import logging
import pathlib
import sys
from datetime import date

import click
from nbis import decorators
from nbis.exceptions import CommandError
from nbis.templates import env


__shortname__ = __name__.split(".")[-1]


logger = logging.getLogger(__name__)


@click.group(help=__doc__, name=__shortname__)
@click.pass_context
def main(ctx):
    logger.debug(f"Running {__shortname__} subcommand.")


@main.command()
@click.option(
    "diary",
    "--diary-file",
    "-d",
    help="diary file name",
    default=pathlib.Path("docs/diary.md"),
)
@decorators.dry_run_option
@click.pass_context
def init(ctx, diary, dry_run):
    """Initialize diary.

    Add a template diary.
    """
    diary = pathlib.Path(diary)
    logger.info(f"Initializing diary file {diary}")
    if diary.exists():
        logger.warning(f"{diary} already exists; skipping init")
        if not dry_run:
            raise CommandError
    if dry_run:
        click.echo("(DRY RUN)")
        return
    try:
        with open(diary, "w") as fh:
            sysargs = " ".join(sys.argv[1:])
            template = env.get_template("diary.md.j2")
            fh.write(
                template.render(
                    project_name=ctx.find_root().info_name,
                    args=sysargs,
                    date=date.today(),
                )
            )
    except FileNotFoundError:
        logger.error(f"Make sure parent directory exists: {diary}")
        raise
