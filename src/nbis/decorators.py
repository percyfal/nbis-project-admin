import typing as t

import click
from click.core import Command
from click.core import Context
from click.core import Parameter
from click.decorators import option

F = t.TypeVar("F", bound=t.Callable[..., t.Any])
FC = t.TypeVar("FC", t.Callable[..., t.Any], Command)


def debug_option(*param_decls: str, **kwargs: t.Any) -> t.Callable[[FC], FC]:
    """Add a ``--debug`` option which turns on debugging.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--debug"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """

    def callback(ctx: Context, param: Parameter, value: bool) -> None:
        ctx.obj["DEBUG"] = value
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


# FIXME: parametrize some of these to allow for other defaults
dry_run = click.option("--dry-run", "-n", is_flag=True, help="dry run")
opt_output_file = click.option("--output-file", "-o", help="output file name")
