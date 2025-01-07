"""Module to render templates to files"""

import logging

try:
    import pkg_resources
except ImportError:
    from importlib import resources as pkg_resources
from jinja2 import Environment
from jinja2 import FileSystemLoader

logger = logging.getLogger(__name__)

try:
    template_path = pkg_resources.resource_filename("nbis", "templates")
except AttributeError:
    template_path = pkg_resources.files("nbis") / "templates"

file_loader = FileSystemLoader(template_path)
env = Environment(loader=file_loader)

INDIVIDUAL_TEMPLATES = {
    "pyproject.toml": "pyproject.toml.j2",
    "gitignore": ".gitignore.j2",
    "prettierignore": ".prettierignore.j2",
    "markdownlint": ".markdownlint.yaml.j2",
    "prettierrc": ".prettierrc.yml.j2",
    "editorconfig": ".editorconfig.j2",
    "readme": "README.md.j2",
    "pre-commit-config": ".pre-commit-config.yaml.j2",
    "quarto": "docs/_quarto.yml.j2",
}


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
