import click

from ..helpers.options import config_option
from ..helpers.params import set_login_fields
from .sym import sym


@sym.command(short_help="login to your sym account")
@config_option("org", help="Your organizations's slug. Contact support if you need this.")
@config_option(
    "email",
    help="The email you use to log into your identity provider (e.g. Okta or GSuite).",
)
def login(**kwargs) -> None:
    """Link your Sym account"""
    set_login_fields(**kwargs)
    click.echo("Sym successfully initalized!")
