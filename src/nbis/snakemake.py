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
