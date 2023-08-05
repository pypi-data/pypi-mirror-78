import click

from ..decorators import loses_interactivity, require_bins, require_login
from ..helpers.boto import host_to_instance
from ..helpers.ssh import ensure_ssh_key, start_tunnel
from . import GlobalOptions
from .sym import sym


@sym.command(hidden=True, short_help="Start a SSH session")
@click.argument("resource")
@click.option("--host", required=True)
@click.option("--port", default=22, type=int, show_default=True)
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("aws", "session-manager-plugin")
@require_login
def ssh_session_with_key(
    options: GlobalOptions, resource: str, host: str, port: int
) -> None:
    """
      Use approved creds for RESOURCE to start a SSH session to an EC2 instance,
      uploading a public key if necessary.
    """
    client = options.create_saml_client(resource)
    instance = host_to_instance(client, host)
    ensure_ssh_key(client, instance, port)
    start_tunnel(client, instance, port)
