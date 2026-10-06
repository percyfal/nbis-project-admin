# Contributing to nbis-admin

## Development setup

Dependency resolution is handled by `uv`. Install project with all
extra dependencies:

    uv sync --all-extras --dev

## pytest

Run tests with pytest:

    uv run pytest

## tox

tox is used to test multiple python versions:

    uv run tox -p -e ALL

## Code linting

Code linting is done with pre-commit:

    uv run pre-commit
