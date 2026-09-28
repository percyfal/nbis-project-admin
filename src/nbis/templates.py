"""Module to render templates to files"""

import logging
from pathlib import Path

from jinja2 import Environment, PackageLoader, TemplateNotFound

logger = logging.getLogger(__name__)

_loader = PackageLoader("nbis", "templates")
env = Environment(
    loader=_loader,
    keep_trailing_newline=True,
    trim_blocks=False,
    lstrip_blocks=False,
)

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
    logger.info("Installing %s to %s", template, filename)
    if filename.exists():
        logger.warning("%s already exists; skipping", filename)
        return
    filename.parent.mkdir(exist_ok=True, parents=True)

    try:
        if template.endswith(".j2"):
            content = env.get_template(template).render(**kwargs)
        else:
            content, _, _ = _loader.get_source(env, template)
    except TemplateNotFound:
        logger.error("Template not found: %s", template)
        raise

    content = content.rstrip() + "\n"
    filename.write_text(content, encoding="utf-8")


def render_template(template, **kw):
    """Generic function to render template"""
    template = env.get_template(template)
    return template.render(**kw).rstrip() + "\n"


def multi_add(pdir, *, subdir=None, files=None, **kwargs):
    """Add multiple templates to directory"""
    if files is None:
        raise ValueError("files must be provided")
    if subdir is not None:
        pdir = pdir / subdir
    logger.info("Adding %s to %s", files, pdir)
    if not pdir.exists():
        pdir.mkdir(exist_ok=True, parents=True)
    for f in files:
        tpl = Path(subdir) / f if subdir else f
        add_template(pdir / f, f"{tpl}.j2", **kwargs)


def init_py_module(pdir, *, module, submodule=None, files=None, init=True, **kwargs):
    """Initialize python module directory"""
    if submodule is not None:
        module = Path(module) / submodule
    module_dir = pdir / "src" / module
    logger.info("Initializing %s in %s", module, pdir)
    if module_dir.exists():
        logger.info("%s exists; skipping", module)
        return
    module_dir.mkdir(exist_ok=True, parents=True)
    if init:
        if files is None or "__init__.py" not in files:
            module_init = module_dir / "__init__.py"
            module_init.touch()
    if files is not None:
        for f in files:
            tpl = Path(submodule) / f if submodule else f
            add_template(
                module_dir / f,
                f"src/python_module/{tpl}.j2",
                **kwargs,
            )
