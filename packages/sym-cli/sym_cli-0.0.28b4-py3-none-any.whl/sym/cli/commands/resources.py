import click

from ..decorators import require_login
from ..helpers.config import Config
from ..helpers.params import get_profiles
from .sym import sym


@sym.command(short_help="list available resource groups")
@require_login
def resources() -> None:
    """List resource groups available for use"""
    default = Config.instance().get("default_resource")
    for (slug, profile) in get_profiles().items():
        star = "* " if default == slug else ""
        click.echo(f"{star}{slug} ({profile.display_name})")
