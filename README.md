[![CI](https://github.com/percyfal/nbis-project-admin/actions/workflows/ci.yml/badge.svg)](https://github.com/percyfal/nbis-project-admin/actions/workflows/ci.yml)


# NBIS project admin

A small collection of tools to administrate [NBIS](https://nbis.se/)
projects.

## Features

Tool interaction is hidden behind a CLI. Features include

- documentation templates for diaries, running slides and more (TODO)
- configuration interface for uploading documents to webexport and
  confluence (TODO)
- wrappers for workflow managers
- adding python modules to a subcommands directory will make the
  module available via the CLI

## Installation

Either install via pip

	python -m pip install git+https://github.com/percyfal/nbis-admin@main

or alternatively grab a copy of the source distribution and make a
local install:

	git clone https://github.com/percyfal/nbis-admin.git
	cd nbis-admin
	python -m pip install -e .

After installation, you can access the tool with the command

	nbis-admin

## Usage example

The main point of `nbis-admin` is to help setting up project analysis
directories that are easily installable as python packages and provide
a command-line interface (CLI) to scripts and workflows. Templates can
be added that add subcommands and workflow commands to the CLI.

To start setting up a project issue

	nbis-admin init project_name

This will install templates with the following structure:

	project_name/
	├── README.md
	├── pyproject.toml
	├── setup.cfg
	└── src
		└── project_name
			├── __init__.py
			├── cli.py
			└── commands
				├── __init__.py
				└── admin.py

To activate the CLI, cd to the project directory, add it to version
control, and install in editable mode:

	cd project_name
	git init
	git add -f .
	python -m pip install -e .

Executing the command `project_name` will expose the available
commands:

	Usage: project_name [OPTIONS] COMMAND [ARGS]...

	  Console script for project_name

	Options:
	  --version           Show the version and exit.
	  --config-file PATH  configuration file
	  --debug             Print debugging information.
	  --help              Show this message and exit.

	Commands:
	  admin  Administration utilities.

The `admin` subcommand consists of the same commands as `nbis-admin`
but will be executed in the context of the project directory, such
that new templates automatically will be installed relative to
`project_name`.


### Adding snakemake commands

The following command will initialize support for snakemake commands
(`smk` subcommand) and add a command called `run`:

	project_name admin smk init
	project_name admin smk add --command run

The `smk` subcommand provides wrappers to run template snakemake files
that were installed above (`run` in this case). The help to
`project_name smk run --help` is

	Usage: project_foo smk run [OPTIONS] [SNAKEMAKE_ARGS]...

	  run help

	Options:
	  --profile TEXT      snakemake profile, either defined as key:value pair in
						  config or a URI pointing to profile directory  [default:
						  local]
	  -j, --jobs INTEGER  snakemake jobs  [default: 1]
	  --help              Show this message and exit.

Any additional options will be passed along to the snakemake workflow
that resides in the directory `src/snakemake`, relative to the project
home.
