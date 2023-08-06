from typing import Type

import pytest

from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.saml_clients.aws_profile import AwsProfile
from sym.cli.saml_clients.chooser import SAMLClientName, choose_saml_client
from sym.cli.saml_clients.saml2aws import Saml2Aws
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.mark.parametrize(
    argnames=("saml_client_name", "make_saml2aws", "expected"),
    argvalues=[
        ("auto", False, AwsProfile),
        ("auto", True, Saml2Aws),
        ("aws-okta", False, AwsOkta),
        ("aws-okta", True, AwsOkta),
        ("saml2aws", False, Saml2Aws),
        ("saml2aws", True, Saml2Aws),
    ],
)
def test_chooser(
    sandbox: Sandbox,
    saml_client_name: SAMLClientName,
    make_saml2aws: bool,
    expected: Type[SAMLClient],
) -> None:
    if make_saml2aws:
        sandbox.create_file("bin/saml2aws", 0o755)
    with sandbox.push_exec_path():
        assert choose_saml_client(saml_client_name) == expected
