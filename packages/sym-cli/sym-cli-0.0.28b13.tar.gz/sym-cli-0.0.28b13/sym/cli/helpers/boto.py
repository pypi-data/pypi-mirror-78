import re
from functools import wraps
from textwrap import dedent
from typing import Optional

import time

import boto3
import validators
from botocore.config import Config as BotoConfig
from botocore.exceptions import ClientError

from ..errors import (
    BotoError,
    CliError,
    ErrorPatterns,
    InstanceNotFound,
    raise_if_match,
)
from .config import SymConfigFile
from .params import get_ssh_user

InstanceIDPattern = re.compile("^i-[a-f0-9]+$")
UnauthorizedError = re.compile(r"UnauthorizedOperation")
RequestExpired = re.compile(r"RequestExpired")


def intercept_boto_errors(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ClientError as err:
            if UnauthorizedError.search(str(err)):
                raise BotoError(
                    err, f"Does your user role have permission to {err.operation_name}?"
                )
            if RequestExpired.search(str(err)):
                raise BotoError(
                    err,
                    f"Your AWS credentials have expired. Try running `sym write-creds` again.",
                )

            raise CliError(str(err)) from err

    return wrapped


def boto_client(saml_client, service):
    creds = saml_client.get_creds()
    return boto3.client(
        service,
        config=BotoConfig(region_name=creds["AWS_REGION"]),
        aws_access_key_id=creds["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=creds["AWS_SECRET_ACCESS_KEY"],
        aws_session_token=creds["AWS_SESSION_TOKEN"],
    )


@intercept_boto_errors
def send_ssh_key(saml_client: "SAMLClient", instance: str, ssh_key: SymConfigFile):
    user = get_ssh_user()
    ssm_client = boto_client(saml_client, "ssm")
    # fmt: off
    command = dedent(
        f"""
        #!/bin/bash
        mkdir -p "$(echo ~{user})/.ssh"
        echo "{ssh_key.path.with_suffix('.pub').read_text()}" >> "$(echo ~{user})/.ssh/authorized_keys"
        chown -R {user}:{user} "$(echo ~{user})/.ssh"
        """
    ).strip()
    # fmt: on

    response = ssm_client.send_command(
        InstanceIds=[instance],
        DocumentName="AWS-RunShellScript",
        Comment="SSH Key for Sym",
        Parameters={"commands": command.splitlines()},
    )

    status = response["Command"]["Status"]
    if _is_pending_invocation(status):
        command_id = response["Command"]["CommandId"]
        _wait_for_invocation(ssm_client, command_id, instance)


def _is_pending_invocation(status):
    return status in ["Pending", "InProgress"]


# When you send an SSM command, it can take some time for invocation to complete.
# Using the built-in waiter seems to fail if the invocation hasn't started yet, so its kind of
# useless.
def _wait_for_invocation(ssm_client, command_id, instance_id, count=5, delay=2):
    tries = 0
    while tries < count:
        tries += 1
        try:
            response = ssm_client.get_command_invocation(
                CommandId=command_id, InstanceId=instance_id
            )
            status = response["Status"]
            if not _is_pending_invocation(status):
                if status != "Success":
                    raise BotoError(
                        None,
                        f'Unable to set up SSH public key. Status: "{status}" Command ID: "{command_id}"',
                    )
                break
            time.sleep(delay)
        except ClientError as error:
            # There can be a lag between when you send a command and when the
            # invocation exists
            if error.response["Error"]["Code"] == "InvocationDoesNotExist":
                time.sleep(delay)
            else:
                raise error


@intercept_boto_errors
def find_instance(saml_client, keys, value) -> Optional[str]:
    ec2_client = boto_client(saml_client, "ec2")
    for key in keys:
        paginator = ec2_client.get_paginator("describe_instances")
        for response in paginator.paginate(
            Filters=[
                {"Name": "instance-state-name", "Values": ["running"]},
                {"Name": key, "Values": [value]},
            ],
        ):
            if response["Reservations"]:
                return response["Reservations"][0]["Instances"][0]["InstanceId"]


@intercept_boto_errors
def get_identity(saml_client) -> dict:
    sts_client = boto_client(saml_client, "sts")
    return sts_client.get_caller_identity()


def host_to_instance(saml_client, host: str) -> str:
    if InstanceIDPattern.match(host):
        target = host
    elif validators.ip_address.ipv4(host):
        target = find_instance(saml_client, ("ip-address", "private-ip-address"), host)
    else:
        target = find_instance(saml_client, ("dns-name", "private-dns-name"), host)

    if not target:
        raise InstanceNotFound(host)

    return target
