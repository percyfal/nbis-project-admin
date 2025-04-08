"""Decorators for command-line interfaces."""

import os
import pathlib
import typing as t

import click
from click.core import Command, Context, Parameter
from click.decorators import option

from nbis.config import load_config
from nbis.env import Environment

F = t.TypeVar("F", bound=t.Callable[..., t.Any])
FC = t.TypeVar("FC", t.Callable[..., t.Any], Command)


def debug_option(*param_decls: str, **kwargs: t.Any) -> t.Callable[[FC], FC]:
    """Add a ``--debug`` option which turns on debugging.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--debug"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """

    def callback(
        ctx: Context,
        param: Parameter,  # pylint: disable=unused-argument
        value: bool,  # pylint: disable=unused-argument
    ) -> None:
        if not value or ctx.resilient_parsing:
            return
        ctx.ensure_object(Environment)
        ctx.obj.debug = value
        if ctx.resilient_parsing:
            return

    if not param_decls:
        param_decls = ("--debug",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", ("Print debugging information."))
    kwargs["callback"] = callback
    return option(*param_decls, **kwargs)


def config_file_option(*param_decls: str, **kwargs: t.Any) -> t.Callable[[FC], FC]:
    """Add a ``--config-file`` option.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--debug"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """

    def callback(
        ctx: Context,
        param: Parameter,  # pylint: disable=unused-argument
        value: bool,  # pylint: disable=unused-argument
    ) -> None:
        ctx.ensure_object(Environment)
        ctx.obj.config = load_config(data={"project_name": "nbis-admin"})
        if not value or ctx.resilient_parsing:
            ctx.obj.home = pathlib.Path(os.curdir).absolute()
            config_file = ctx.obj.home / f"{ctx.obj.home.name}.yaml"
            if config_file.exists():
                ctx.obj.config = load_config(file=config_file)
            return
        ctx.obj.home = pathlib.Path(value).absolute().parent
        ctx.obj.config = load_config(file=value)
        if ctx.resilient_parsing:
            return

    if not param_decls:
        param_decls = ("--config-file",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault(
        "help", ("Path to project configuration file. Defaults to <DIRNAME>.yaml.")
    )
    kwargs["callback"] = callback
    return option(*param_decls, **kwargs)


dry_run_option = click.option("--dry-run", "-n", is_flag=True, help="dry run")
output_file_option = click.option("--output-file", "-o", help="output file name")
