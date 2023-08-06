import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from signal import SIGPIPE, signal
from subprocess import CalledProcessError
from textwrap import dedent
from typing import Sequence

from ..decorators import intercept_errors, retry, run_subprocess
from ..errors import (
    AccessDenied,
    FailedSubprocessError,
    SuppressedError,
    TargetNotConnected,
    WrappedSubprocessError,
)
from ..helpers.boto import send_ssh_key
from ..helpers.config import Config, SymConfigFile
from ..helpers.params import get_ssh_user

MissingPublicKeyPattern = re.compile(r"Permission denied \(.*publickey.*\)")
TargetNotConnectedPattern = re.compile("TargetNotConnected")
AccessDeniedPattern = re.compile("AccessDeniedException")
ConnectionClosedPattern = re.compile(r"Connection to .* closed")

SSHConfigPath = "ssh/config"
SSHKeyPath = "ssh/key"


def ssh_key_and_config(client: "SAMLClient"):
    ssh_key = SymConfigFile(file_name=SSHKeyPath)
    ssh_config = client.subconfig(SSHConfigPath, ssh_key=str(ssh_key))
    return (ssh_key, ssh_config)


@intercept_errors()
@run_subprocess
def _gen_ssh_key(dest: SymConfigFile):
    with dest.exclusive_create() as f:
        Path(f.name).unlink(missing_ok=True)
        yield "ssh-keygen", {"t": "rsa", "f": f.name, "N": ""}


def gen_ssh_key(dest: SymConfigFile):
    try:
        _gen_ssh_key(dest, capture_output_=True, input_="n\n")
    except FailedSubprocessError:
        if not dest.path.exists():
            raise


def ssh_args(client, instance, port) -> tuple:
    _, ssh_config = ssh_key_and_config(client)
    return (
        "ssh",
        instance,
        {"p": str(port), "F": str(ssh_config), "l": get_ssh_user(), "v": client.debug},
    )


@run_subprocess
def _start_background_ssh_session(
    client: "SAMLClient", instance: str, port: int, *command
):
    yield (
        *ssh_args(client, instance, port),
        {"f": True},
        "-o BatchMode=yes",
        *command,
    )


@run_subprocess
def _start_ssh_session(client: "SAMLClient", instance: str, port: int, *command: str):
    yield (*ssh_args(client, instance, port), *command)


@retry(TargetNotConnected, delay=1)
def start_ssh_session(
    client: "SAMLClient",
    instance: str,
    port: int,
    command: Sequence[str] = [],
    retry=True,
):
    ensure_ssh_key(client, instance, port)
    try:
        _start_ssh_session(client, instance, port, *command)
    except CalledProcessError as err:
        if MissingPublicKeyPattern.search(err.stderr):
            Config.touch_instance(instance, error=True)
            if retry:
                start_ssh_session(client, instance, port, command, retry=False)
            else:
                raise WrappedSubprocessError(
                    err, f"Does the user ({get_ssh_user()}) exist on the instance?"
                ) from err
        # If the ssh key path is cached then this doesn't get intercepted in ensure_ssh_key
        elif TargetNotConnectedPattern.search(err.stderr):
            raise TargetNotConnected() from err
        elif AccessDeniedPattern.search(err.stderr):
            raise AccessDenied() from err
        elif ConnectionClosedPattern.search(err.stderr):
            raise SuppressedError(err, echo=True) from err
        else:
            raise WrappedSubprocessError(
                err, f"Contact your Sym administrator.", report=True
            ) from err
    else:
        Config.touch_instance(instance)


@retry(TargetNotConnected, delay=2, count=4)
@intercept_errors({TargetNotConnectedPattern: TargetNotConnected}, suppress=True)
def ensure_ssh_key(client, instance: str, port: int):
    ssh_key, ssh_config = ssh_key_and_config(client)

    sym_cmd = (
        f"sym {client.cli_options} ssh-session {client.resource} --instance %h --port %p"
    )
    # fmt: off
    ssh_config.put(dedent(  # Ensure the SSH Config first, always
        f"""
        Host *
            IdentityFile {str(ssh_key)}
            PreferredAuthentications publickey
            PubkeyAuthentication yes
            StrictHostKeyChecking no
            PasswordAuthentication no
            ChallengeResponseAuthentication no
            GSSAPIAuthentication no
            ProxyCommand sh -c "{sym_cmd} || exit $?"
        """
    ))
    # fmt: on

    instance_config = Config.get_instance(instance)

    if not ssh_key.path.exists():
        gen_ssh_key(ssh_key)

    last_connect = instance_config.get("last_connection")
    if last_connect and datetime.now() - last_connect < timedelta(days=1):
        client.dprint(f"Skipping remote SSH key check for {instance}")
        return

    try:
        _start_background_ssh_session(
            client, instance, port, "exit", capture_output_=True
        )
    except CalledProcessError as err:
        if not MissingPublicKeyPattern.search(err.stderr):
            raise
        send_ssh_key(client, instance, ssh_key)

    Config.touch_instance(instance)


def start_tunnel(client, instance: str, port: int):
    def handler(signum, frame):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        # Set error state on session end.
        # If the connection was actually successful,
        # the parent thread will re-set a success state.
        # This is the only reliable way to avoid error
        # loops with Ansible due to missing SSH public keys.
        Config.touch_instance(instance, error=True)

    signal(SIGPIPE, handler)

    client.exec(
        "aws",
        "ssm",
        "start-session",
        target=instance,
        document_name="AWS-StartSSHSession",
        parameters=f"portNumber={port}",
    )

    Config.touch_instance(instance)
