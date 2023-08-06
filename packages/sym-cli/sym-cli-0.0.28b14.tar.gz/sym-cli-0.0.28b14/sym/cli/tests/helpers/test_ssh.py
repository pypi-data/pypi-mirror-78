from multiprocessing import Pool
from uuid import UUID

import click
import pytest

from sym.cli.helpers.config import SymConfigFile
from sym.cli.helpers.ssh import SSHKeyPath, gen_ssh_key
from sym.cli.sym import sym as click_command
from sym.cli.tests.conftest import setup_context
from sym.cli.tests.helpers.sandbox import Sandbox


def _gen_ssh_key_fn(_i):
    with setup_context():
        ssh_key = SymConfigFile(file_name=SSHKeyPath)
        gen_ssh_key(ssh_key)


def test_gen_ssh_key(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        with Pool(processes=4) as pool:
            pool.map(_gen_ssh_key_fn, range(10))

        with SymConfigFile(file_name=SSHKeyPath) as f:
            assert "BEGIN OPENSSH PRIVATE KEY" in f.read()


def test_gen_ssh_key_exists(sandbox: Sandbox):
    with sandbox.push_xdg_config_home():
        _gen_ssh_key_fn(0)

        with SymConfigFile(file_name=SSHKeyPath) as f:
            key = f.read()

        with Pool(processes=4) as pool:
            pool.map(_gen_ssh_key_fn, range(10))

        with SymConfigFile(file_name=SSHKeyPath) as f:
            assert key == f.read()
