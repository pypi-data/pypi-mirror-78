from typing import Optional, Tuple

import click

from ..decorators import loses_interactivity, require_bins, require_login
from ..helpers.ansible import run_ansible
from ..helpers.options import aws_profile_options
from . import GlobalOptions
from .sym import sym


@sym.command(
    short_help="Run an Ansible command",
    context_settings={"ignore_unknown_options": True},
)
@click.argument("resource")
@click.argument("command", nargs=-1)
@aws_profile_options
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("ansible", "aws", "session-manager-plugin")
@require_login
def ansible(
    options: GlobalOptions,
    resource: str,
    command: Tuple[str, ...],
    ansible_aws_profile: Optional[str],
    ansible_sym_resource: Optional[str],
) -> None:
    """Use approved creds for RESOURCE to run an Ansible command."""
    client = options.create_saml_client(resource)
    run_ansible(
        client,
        command,
        ansible_aws_profile=ansible_aws_profile,
        ansible_sym_resource=ansible_sym_resource,
    )
