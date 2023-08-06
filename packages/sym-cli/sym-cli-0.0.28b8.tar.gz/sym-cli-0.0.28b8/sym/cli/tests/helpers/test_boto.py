import pytest
from botocore.exceptions import ClientError
from botocore.paginate import Paginator

from sym.cli.errors import BotoError
from sym.cli.helpers.boto import host_to_instance


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
