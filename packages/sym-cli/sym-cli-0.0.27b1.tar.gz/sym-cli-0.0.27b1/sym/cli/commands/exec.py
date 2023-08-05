from typing import Tuple

import click

from ..decorators import loses_interactivity, require_login
from . import GlobalOptions
from .sym import sym


@sym.command("exec", short_help="execute a command")
@click.argument("resource")
@click.argument("command", nargs=-1)
@loses_interactivity
@click.make_pass_decorator(GlobalOptions)
@require_login
def sym_exec(options: GlobalOptions, resource: str, command: Tuple[str, ...]) -> None:
    """Use approved creds for RESOURCE to execute COMMAND"""
    options.create_saml_client(resource).exec(*command)
