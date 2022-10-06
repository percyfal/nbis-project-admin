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
    logger.info(f"Installing {filename}")
    if filename.exists():
        logger.warning(f"{filename} already exists; skipping")
        return
    try:
        if not filename.parent.exists():
            filename.parent.mkdir(exist_ok=True, parents=True)
        with open(filename, "w") as fh:
            template = env.get_template(template)
            fh.write(template.render(**kwargs))
    except FileNotFoundError:
        logger.error(f"Make sure parent directory exists: {filename}")
        raise


def render_template(template, **kw):
    template = env.get_template(template)
    return template.render(**kw)
