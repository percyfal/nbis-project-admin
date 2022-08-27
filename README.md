[![CI](https://github.com/percyfal/nbis-project-admin/actions/workflows/ci.yml/badge.svg)](https://github.com/percyfal/nbis-project-admin/actions/workflows/ci.yml)


# NBIS project admin

A small collection of tools to administrate [NBIS](https://nbis.se/)
projects. It serves as the backbone for the cookiecutter
[cookiecutter-nbis-project](
https://github.com/percyfal/cookiecutter-nbis-project).

## Features

Tool interaction is hidden behind a CLI. Tools include

- documentation templates for diaries, running slides and more (TODO)
- configuration interface for uploading documents to webexport and
  confluence (TODO)
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

