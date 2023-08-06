from contextlib import contextmanager
from pathlib import Path
from typing import Callable, ContextManager, Iterator
from uuid import UUID, uuid4

import boto3
import click
import pytest
from _pytest.monkeypatch import MonkeyPatch
from botocore.stub import Stubber
from click.testing import CliRunner

from sym.cli.commands import GlobalOptions
from sym.cli.helpers import boto
from sym.cli.helpers.config import Config
from sym.cli.saml_clients.aws_okta import AwsOkta
from sym.cli.saml_clients.saml_client import SAMLClient
from sym.cli.sym import sym as click_command
from sym.cli.tests.helpers.capture import CaptureCommand
from sym.cli.tests.helpers.sandbox import Sandbox


@pytest.fixture(autouse=True)
def patch_is_setup(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(SAMLClient, "check_is_setup", lambda self: ...)


@pytest.fixture
def sandbox(tmp_path: Path) -> Sandbox:
    return Sandbox(tmp_path)


@pytest.fixture
def uuid() -> UUID:
    return uuid4()


@pytest.fixture
def uuid_factory() -> Callable[[], UUID]:
    return uuid4


CustomOrgFixture = Callable[[str], ContextManager[None]]


@pytest.fixture
def custom_org(monkeypatch: MonkeyPatch) -> CustomOrgFixture:
    @contextmanager
    def custom_org(org: str) -> Iterator[None]:
        with monkeypatch.context() as mp:
            mp.setattr(Config, "get_org", classmethod(lambda cls: org))
            yield

    return custom_org


@pytest.fixture
def capture_command(monkeypatch: MonkeyPatch) -> CaptureCommand:
    return CaptureCommand(monkeypatch)


@pytest.fixture
def click_context(sandbox):
    with sandbox.push_xdg_config_home():
        Config.instance()["org"] = "sym"
        with click.Context(click_command) as ctx:
            ctx.ensure_object(GlobalOptions)
            yield ctx


@pytest.fixture
def click_setup(sandbox: Sandbox):
    @contextmanager
    def context(set_org=True):
        runner = CliRunner()
        with runner.isolated_filesystem():
            with sandbox.push_xdg_config_home():
                sandbox.create_binary(f"bin/{AwsOkta.binary}")
                with sandbox.push_exec_path():
                    if set_org:
                        Config.instance()["org"] = "sym"
                    yield runner

    return context


@pytest.fixture
def saml_client(sandbox: Sandbox, monkeypatch: MonkeyPatch):
    def get_creds(self):
        return {
            "AWS_REGION": "us-east-2",
            "AWS_ACCESS_KEY_ID": "ASIA4GNNUMIHHBPSAQC3",
            "AWS_SECRET_ACCESS_KEY": "xxx",
            "AWS_SESSION_TOKEN": "xxx",
        }

    monkeypatch.setattr(AwsOkta, "get_creds", get_creds)

    sandbox.create_binary(f"bin/{AwsOkta.binary}")
    return AwsOkta("test", debug=False)


@pytest.fixture
def boto_stub(monkeypatch: MonkeyPatch):
    stubs = {}

    def boto_client(_saml_client, service):
        if service in stubs:
            return stubs[service][0]

        client = boto3.client(service)
        stubber = Stubber(client)
        stubber.activate()

        stubs[service] = (client, stubber)
        return client

    monkeypatch.setattr(boto, "boto_client", boto_client)

    def get_stub(service):
        boto_client(None, service)
        return stubs[service][1]

    return get_stub


@contextmanager
def setup_context():
    with click.Context(click_command) as ctx:
        ctx.ensure_object(GlobalOptions)
        yield
