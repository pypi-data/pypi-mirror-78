from typing import Sequence

import click

from ..decorators import loses_interactivity, require_bins, require_login
from ..helpers.boto import host_to_instance
from ..helpers.ssh import start_ssh_session
from . import GlobalOptions
from .sym import sym


@sym.command(
    short_help="Start a SSH session", context_settings={"ignore_unknown_options": True}
)
@click.argument("resource")
@click.argument("host")
@click.option("--port", default=22, type=int, show_default=True)
@click.argument("cmd", nargs=-1, required=False)
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("aws", "session-manager-plugin")
@require_login
def ssh(
    options: GlobalOptions, resource: str, host: str, port: int, cmd: Sequence[str]
) -> None:
    """Use approved creds for RESOURCE to start a SSH session to an EC2 instance."""
    client = options.create_saml_client(resource)
    instance = host_to_instance(client, host)
    start_ssh_session(client, instance, port, cmd)
