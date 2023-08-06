from typing import Optional, Tuple

from ..decorators import intercept_errors, run_subprocess
from ..helpers.config import SymConfigFile
from ..helpers.params import get_ssh_user
from ..helpers.ssh import SSHKeyPath
from ..saml_clients.aws_profile import AwsProfile


def run_ansible(
    client: "SAMLClient",
    command: Tuple[str, ...],
    ansible_aws_profile: Optional[str],
    ansible_sym_resource: Optional[str],
    binary: str = "ansible",
):
    sym_cmd = (
        f"sym {client.cli_options} ssh-session-with-key {client.resource} --host %h"
        " --port %p"
    )
    ssh_args = " ".join(
        [
            "-o StrictHostKeyChecking=no",
            "-o LogLevel=DEBUG1",
            f'-o ProxyCommand="sh -c \\"{sym_cmd} || exit $?\\""',
        ]
    )

    if ansible_aws_profile:
        client = client.clone(klass=AwsProfile, resource=ansible_aws_profile)
    elif ansible_sym_resource:
        client = client.clone(resource=ansible_sym_resource)

    client.exec(
        binary,
        *command,
        f"--ssh-common-args={ssh_args}",
        f"--user={get_ssh_user()}",
        f"--private-key={str(SymConfigFile(file_name=SSHKeyPath))}",
        suppress_=True,
    )
