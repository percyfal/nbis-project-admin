import os

import nbis.wrappers as wrappers
import pkg_resources
import pytest
from nbis.templates import env


if os.getenv("TOX_ENV_NAME") is not None:
    pytest.skip(allow_module_level=True, reason="disable test in tox environment")


def test_running_slides_template(tmp_path):
    fn = "running-slides.Rmd"
    p = tmp_path / fn
    template = env.get_template("running-slides.Rmd.j2")
    p.write_text(
        template.render(
            title="Running slides",
            subtitle="Awesome stuff",
            author="John Doe",
            filename=fn,
            css=[pkg_resources.resource_filename("nbis", "resources/nbis.css")],
            csl="https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl",  # noqa
            in_header=pkg_resources.resource_filename(
                "nbis", "resources/nbisfooter.html"
            ),
            libraries=[],
        )
    )
    wrappers.rmarkdown(p)
