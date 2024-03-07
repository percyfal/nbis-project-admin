"""This module contains custom exceptions for the command line interface."""


class CommandError(Exception):
    """CommandError is raised when a command fails for any reason."""


class CommandLineError(Exception):
    """CommandLineError is raised when a command line is malformed."""
