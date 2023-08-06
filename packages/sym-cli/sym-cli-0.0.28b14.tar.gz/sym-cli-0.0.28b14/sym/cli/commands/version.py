from typing import Tuple

import click

from ..version import __version__
from .sym import sym


@sym.command(short_help="print the version")
def version() -> None:
    click.echo(__version__)
