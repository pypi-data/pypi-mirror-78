import click

from ..decorators import loses_interactivity, require_bins, require_login
from ..helpers.ssh import start_tunnel
from . import GlobalOptions
from .sym import sym


@sym.command(hidden=True, short_help="starts a SSH session over SSM")
@click.argument("resource")
@click.option("--instance", required=True)
@click.option("--port", default=22, type=int, show_default=True)
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("aws", "session-manager-plugin")
@require_login
def ssh_session(options: GlobalOptions, resource: str, instance: str, port: int):
    """Use approved creds for RESOURCE to tunnel a SSH session through an SSM session"""
    client = options.create_saml_client(resource)
    start_tunnel(client, instance, port)
