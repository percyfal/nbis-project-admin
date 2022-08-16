<!-- 
[![PyPI](https://img.shields.io/pypi/v/nbis.svg)](https://pypi.python.org/pypi/nbis_project_admin)
-->
<!--
[![CI](https://github.com/NBISweden/nbis/actions/workflows/ci.yml/badge.svg)](https://github.com/NBISweden/nbis_project_admin/actions/workflows/ci.yml)
-->
<!--
[![BioConda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg)](http://bioconda.github.io/recipes/nbis/README.html)
-->

# NBIS project admin

A small collection of tools to administrate [NBIS](https://nbis.se/).
It serves as the backbone for the cookiecutter
[cookiecutter-nbis-project](
https://github.com/percyfal/cookiecutter-nbis-project).

## Features

Tool interaction is hidden behind a CLI. Tools include

- documentation templates for diaries, running slides and more (TODO)
- configuration interface for uploading documents to webexport and
  confluence
- wrappers for workflow managers
- adding python modules to a subcommands directory will make the
  module available via the CLI. Intended for use with
  [cookiecutter-nbis-project](
  https://github.com/percyfal/cookiecutter-nbis-project).

## Installation

Either install via pip

	python -m pip install git+https://github.com/percyfal/nbis-admin@main
	
Alternatively grab a copy of the source distribution and make a local
install:

	git clone https://github.com/percyfal/nbis-admin.git
	cd nbis-admin
	python -m pip install -e .
	
After installation, you can access the tool with the command 

	nbis-admin

