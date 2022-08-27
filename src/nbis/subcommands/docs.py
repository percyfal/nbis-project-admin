"""nbis-admin doc: manage documentation


"""
import logging
import os
import pathlib

import nbis.wrappers as wrappers
import pkg_resources
from nbis.config import Config
from nbis.config import load_config
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
        choices=["running-slides", "jupyterbook", "diary", "scss"],
    )
    parser.add_argument(
        "--css",
        help="css template",
        action="store",
        default=None,  # pkg_resources.resource_filename("nbis", "resources/nbis.css"),
    )
    parser.add_argument(
        "--scss",
        help="scss template",
        action="store",
        default=pkg_resources.resource_filename("nbis", "resources/nbis.scss"),
    )
    parser.add_argument("--title", help="title", action="store", default="title")
    parser.add_argument(
        "--subtitle", help="subtitle", action="store", default="subtitle"
    )
    parser.add_argument("--author", help="author", action="store", default=None)
    parser.add_argument(
        "--csl",
        help="csl",
        action="store",
        default="https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl",  # noqa
    )
    parser.add_argument(
        "--bibliography",
        help="bibliography",
        action="store",
        default="../resources/bibliography.bib",
    )
    parser.add_argument(
        "--footer", help="footer", action="store", default="running slides"
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
    if not outdir.exists():
        outdir.mkdir()
    if args.template == "running-slides":
        path = args.path if args.path is not None else outdir / "running-slides.qmd"
        if path.exists():
            logger.error(f"{path} exists; not overwriting")
            raise FileExistsError(f"{path} exists; skipping!")
        template = env.get_template("running-slides.qmd.j2")
        options = dict(filename=os.path.basename(path))
        options.update(vars(args))
        with open(path, "w") as fh:
            fh.write(template.render(**options))


def main(args):
    logger.info("Running nbis-admin docs")

    config = load_config(file=args.config_file)

    if config.is_empty:
        config = Config({"docs": {"src": pathlib.Path(os.curdir) / "docs"}})

    if args.build:
        build(args, sourcedir=pathlib.Path(config.docs.src))

    if args.add:
        add(args, outdir=pathlib.Path(config.docs.src))
