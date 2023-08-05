import click

from . import config as cmd
from .sym import sym


def key_callback(ctx, key: str):
    return cmd.key_callback(ctx, key=f"default_{key}")


@sym.command(short_help="get a default value")
@click.argument("key", callback=key_callback)
@click.argument("value", callback=cmd.value_callback, required=False)
@click.pass_context
def defaults(ctx, key: str, value: str) -> None:
    """Get a Sym default value."""
    ctx.forward(cmd.config)


@sym.command(name="defaults:set", short_help="set a default value")
@click.argument("key", callback=key_callback)
@click.argument("value", callback=cmd.value_callback)
@click.pass_context
def defaults_set(ctx, key: str, value: str) -> None:
    """Set a Sym default value."""
    ctx.forward(cmd.config_set)


@sym.command(name="defaults:unset", short_help="unset a default value")
@click.argument("key", callback=key_callback)
@click.pass_context
def defaults_unset(ctx, key: str) -> None:
    """Unset a Sym default value."""
    ctx.forward(cmd.config_unset)
