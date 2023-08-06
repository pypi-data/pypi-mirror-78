import pytest
from botocore.exceptions import ClientError
from botocore.paginate import Paginator

from sym.cli.errors import BotoError
from sym.cli.helpers.boto import boto_client, host_to_instance, send_ssh_key
from sym.cli.helpers.config import SymConfigFile
from sym.cli.helpers.ssh import SSHKeyPath
from sym.cli.saml_clients.aws_profile import AwsProfile
from sym.cli.tests.saml_clients.conftest import TestContextFixture

pytestmark = pytest.mark.usefixtures("click_context")


def test_error_handling_unauthorized(monkeypatch, boto_stub, click_context, saml_client):
    def paginate(*args, **kwargs):
        raise ClientError(
            {
                "Error": {
                    "Code": "UnauthorizedOperation",
                    "Message": "You are not authorized to perform this operation.",
                }
            },
            "DescribeInstances",
        )

    monkeypatch.setattr(Paginator, "paginate", paginate)

    with click_context:
        with pytest.raises(
            BotoError, match="Does your user role have permission to DescribeInstances?"
        ):
            host_to_instance(saml_client, "localhost")


def test_error_handling_expired(monkeypatch, boto_stub, click_context, saml_client):
    def paginate(*args, **kwargs):
        raise ClientError(
            {"Error": {"Code": "RequestExpired", "Message": "Request has expired.",}},
            "DescribeInstances",
        )

    monkeypatch.setattr(Paginator, "paginate", paginate)

    with click_context:
        with pytest.raises(BotoError, match="Your AWS credentials have expired."):
            host_to_instance(saml_client, "localhost")


def test_wait_for_invocation(saml_client, boto_stub, monkeypatch) -> None:
    send_command_response = {
        "Command": {
            "Status": "Pending",
            "CommandId": "1925e603-4f3f-4e1a-9f29-29fb7dcb4d47",
        }
    }
    get_command_invocation_response = {
        "Status": "Success",
        "CommandId": "1925e603-4f3f-4e1a-9f29-29fb7dcb4d47",
    }

    ssm = boto_stub("ssm")
    ssm.add_response("send_command", send_command_response)
    ssm.add_response("get_command_invocation", get_command_invocation_response)

    ssh_key = SymConfigFile(file_name=f"{SSHKeyPath}.pub")
    ssh_key.put("==")

    send_ssh_key(saml_client, "foo", ssh_key)

    ssm.assert_no_pending_responses()
