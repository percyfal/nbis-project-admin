"""Command wrappers"""

import logging
import os
import shutil
import subprocess

import pypandoc

logger = logging.getLogger(__name__)


class Wrapper:  # pylint: disable=too-few-public-methods
    """Documentation wrapper base class."""

    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        """Run wrapper using subprocess.run"""
        raise NotImplementedError


def snakemake(*, targets=None, options=None, snakefile=None):
    """Run snakemake workflows."""
    if isinstance(options, list):
        options = " ".join(options)
    cmdlist = [
        "snakemake",
        f"{'-s ' + str(snakefile) if snakefile else ''}",
        f"{str(options) or ''}",
        f"{str(targets) or ''}",
    ]
    cmd = " ".join(cmdlist)
    if shutil.which("snakemake") is None:
        logger.info("snakemake not installed; cannot run command:")
        logger.info("  %s", cmd)
        return

    try:
        logger.debug("running %s", cmd)
        subprocess.run(cmd, check=True, shell=True)
    except subprocess.CalledProcessError:
        logger.error("%s failed", cmd)
        raise


def rmarkdown(path, output_dir=None):
    """Render Rmarkdown files"""
    render_args = [f'"{str(path)}"']
    if output_dir is not None:
        render_args += [f'output_dir="{str(output_dir)}"']
    render = ",".join(render_args)
    cmdlist = ["R", "-e", f"'library(rmarkdown); rmarkdown::render({str(render)})'"]
    cmd = " ".join(cmdlist)
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        logger.error("%s failed", cmd)
        raise


def jupyter_book(path, output_format="html"):
    """Build jupyter book"""
    reportdir = f"_build/{output_format}/reports"
    cmdlist = ["jupyter-book", "build", "-W", "-n", "--keep-going", path]
    cmd = " ".join(cmdlist)
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        logger.error("%s failed", cmd)
        if os.path.exists(reportdir):
            logger.info("Error occured; showing saved reports")
            subprocess.run(["cat", f"{reportdir}/*"], check=True)
        raise


def pandoc(path, output, output_format="html", **kwargs):
    """Convert single markdown files"""
    output = pypandoc.convert_file(path, outputfile=output, to=output_format, **kwargs)
