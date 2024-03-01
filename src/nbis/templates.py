"""Module to render templates to files"""

import logging

import pkg_resources
from jinja2 import Environment
from jinja2 import FileSystemLoader

logger = logging.getLogger(__name__)


template_path = pkg_resources.resource_filename("nbis", "templates")
file_loader = FileSystemLoader(template_path)
env = Environment(loader=file_loader)


def add_template(filename, template, **kwargs):
    """Generic function to render template to filename"""
    logger.info("Installing %s", filename)
    if filename.exists():
        logger.warning("%s already exists; skipping", filename)
        return
    try:
        if not filename.parent.exists():
            filename.parent.mkdir(exist_ok=True, parents=True)
        with open(filename, "w", encoding="utf-8") as fh:
            template = env.get_template(template)
            fh.write(template.render(**kwargs))
            fh.write("\n")
    except FileNotFoundError:
        logger.error("Make sure parent directory exists: %s", filename)
        raise


def render_template(template, **kw):
    """Generic function to render template"""
    template = env.get_template(template)
    return template.render(**kw)
