from pathlib import Path

import click

from ..decorators import loses_interactivity, require_bins, require_login
from ..saml_clients.aws_profile import AwsCredentialsPath
from . import GlobalOptions
from .sym import sym


@sym.command(short_help="Write out AWS credentials")
@click.argument("resource")
@click.option(
    "--path",
    help="credentials file path",
    default=str(AwsCredentialsPath),
    type=click.Path(exists=True, dir_okay=False, writable=True),
)
@click.option("--profile", help="profile name", default="sym")
@click.make_pass_decorator(GlobalOptions)
@loses_interactivity
@require_bins("aws", "session-manager-plugin")
@require_login
def write_creds(options: GlobalOptions, resource: str, path: str, profile: str) -> None:
    """Write AWS credentials to a profile"""
    options.create_saml_client(resource).write_creds(path=path, profile=profile)
