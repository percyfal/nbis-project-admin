"""
nbis-admin doc: manage documentation
"""
import logging
import os
import pathlib

import nbis.wrappers as wrappers
import pkg_resources
from nbis.config import Config
from nbis.config import get_schema
from nbis.templates import env

logger = logging.getLogger(__name__)


def add_arguments(parser):
    parser.add_argument(
        "--path", help="work on path only", action="store", default=None
    )
    parser.add_argument(
        "--template",
        help="which template to add",
        action="store",
        default="running-slides",
        choices=["running-slides", "jupyterbook", "diary"],
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--build", help="build documentation", action="store_true")
    group.add_argument("--add", help="add documentation", action="store_true")


def build(args, sourcedir):
    """Build documentation folders"""
    if args.path is not None:
        sources = [pathlib.Path(args.path)]
    else:
        sources = []
        for fn in os.listdir(sourcedir):
            fn = pathlib.Path(os.path.join(sourcedir, fn))
            if fn.is_dir:
                sources.append(fn)
    for src in sources:
        if os.path.splitext(src)[1] == ".Rmd":
            wrappers.rmarkdown(src)


def add(args, outdir):
    """Initialize documentation folders"""
    if args.template == "running-slides":
        path = args.path if args.path is not None else outdir / "running-slides.Rmd"
        template = env.get_template("running-slides.Rmd.j2")
        with open(path, "w") as fh:
            fh.write(
                template.render(
                    title="Running slides",
                    subtitle="Subtitle",
                    author="",
                    filename=os.path.basename(path),
                    css=[pkg_resources.resource_filename("nbis", "resources/nbis.css")],
                    csl="https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl",  # noqa
                    in_header=pkg_resources.resource_filename(
                        "nbis", "resources/nbisfooter.html"
                    ),
                    libraries=[],
                )
            )


def main(args):
    logger.info("Running nbis-admin docs")

    schema = get_schema()
    config = Config(file=args.config_file)
    if config.is_empty:
        config = Config({"docs": {"src": os.curdir}})
    schema.validate(config)

    if args.build:
        build(args, sourcedir=pathlib.Path(config.docs.src))

    if args.add:
        add(args, outdir=pathlib.Path(config.docs.src))
