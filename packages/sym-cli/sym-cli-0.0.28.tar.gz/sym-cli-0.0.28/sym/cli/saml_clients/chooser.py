from typing import Literal, Type

from ..helpers.os import has_command
from . import import_all
from .aws_profile import AwsProfile
from .saml_client import SAMLClient

SAMLClientName = Literal["auto", "aws-okta", "saml2aws", "aws-profile"]

import_all()


def option_values():
    return ["auto"] + [x.option_value for x in SAMLClient.sorted_subclasses()]


def choose_saml_client(saml_client_name: SAMLClientName) -> Type[SAMLClient]:
    if saml_client_name == "auto":
        for client in SAMLClient.sorted_subclasses():
            if has_command(client.binary):
                return client
    else:
        for client in SAMLClient.sorted_subclasses():
            if client.option_value == saml_client_name:
                return client
    return AwsProfile
