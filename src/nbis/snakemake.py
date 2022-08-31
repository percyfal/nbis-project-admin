"""Snakemake utilities"""
import logging

logger = logging.getLogger(__name__)


def profile(uri, config):
    """Retrieve snakemake profile from config"""
    try:
        uri = config["snakemake_profiles"][uri]
    except TypeError as e:
        logger.debug(f"TypeError: '{e}'")
    except KeyError as e:
        logger.debug(f"KeyError: no such snakemake-profiles key {e}")
    finally:
        logger.debug(f"trying snakemake profile at uri '{uri}'")
    return uri


def add_arguments(parser, profile=True, no_profile=True, jobs=True, test=True):
    """Utility function to add some standard arguments to snakemake parser"""
    if profile:
        parser.add_argument(
            "--profile",
            action="store",
            default="rackham",
            help=(
                "snakemake profile, either defined as key:value pair in config"
                " or a URI pointing to profile directory"
            ),
        )
    if no_profile:
        parser.add_argument(
            "--no-profile",
            action="store_true",
            default=False,
            help="disable snakemake profile",
        )
    if jobs:
        parser.add_argument(
            "-j", "--jobs", action="store", default=1, help="snakemake jobs"
        )
    if test:
        parser.add_argument(
            "--test",
            action="store_true",
            default=False,
            help="run workflow on small test data set",
        )
