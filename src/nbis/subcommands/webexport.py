"""
nbis-admin webexport: sync webexport folders

All contents of folder reports/webexport will be synced to the url
defined by the 'webexport.url' configuration property.

"""
import logging
import subprocess

from nbis.config import Config

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument("--sync", action="store_true", help="sync webexport folders")
    parser.add_argument("--dry-run", "-n", action="store_true", help="dry run")
    parser.add_argument(
        "--backend",
        action="store",
        default="rsync",
        choices=["rsync"],
        help="sync backend tool",
    )
    parser.add_argument(
        "rsync_options",
        nargs="*",
        default=[],
        help="Additional options to pass to rsync.",
    )


def sync(args):
    config = Config(f"{args.prog}.yaml")
    arguments = [args.backend] + args.extra_options + args.rsync_options
    if args.dry_run:
        arguments.append("-n")
    arguments += [f"{config.webexport.builddir}/", f"{config.webexport.url}/"]
    try:
        subprocess.run(arguments, check=True)
    except Exception:
        raise


def main(args):
    logger.info("Running nbis-admin webexport")

    if args.sync:
        sync(args)
