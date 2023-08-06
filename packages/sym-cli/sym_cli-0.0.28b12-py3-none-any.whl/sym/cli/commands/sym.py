import click

from ..decorators import setup_segment, setup_sentry
from ..helpers import segment
from ..helpers.constants import SegmentWriteKey, SentryDSN
from ..helpers.envvar_option import EnvvarOption
from ..helpers.options import resource_option
from ..helpers.sym_group import SymGroup
from ..saml_clients.chooser import SAMLClientName, choose_saml_client, option_values
from ..version import __version__
from . import GlobalOptions


@click.group(cls=SymGroup)
@click.option(
    "--saml-client",
    "saml_client_name",
    default="auto",
    type=click.Choice(option_values()),
    help="the SAML client type to use",
    envvar="SYM_SAML_CLIENT",
    cls=EnvvarOption,
)
@click.option(
    "--debug", is_flag=True, help="enable verbose debugging", envvar="SYM_DEBUG"
)
@click.option("--log-file", type=click.Path(), hidden=True, envvar="SYM_LOG_FILE")
@resource_option
@click.make_pass_decorator(GlobalOptions, ensure=True)
@setup_segment(write_key=SegmentWriteKey)
@setup_sentry(dsn=SentryDSN, release=f"sym-cli@{__version__}")
def sym(
    options: GlobalOptions,
    saml_client_name: SAMLClientName,
    debug: bool,
    resource: str,
    log_file: str,
) -> None:
    """Access resources managed by Sym workflows.

    Use these tools to work with your resources once you've gotten approval in
    Slack.
    """
    options.saml_client_type = choose_saml_client(saml_client_name)
    options.debug = debug
