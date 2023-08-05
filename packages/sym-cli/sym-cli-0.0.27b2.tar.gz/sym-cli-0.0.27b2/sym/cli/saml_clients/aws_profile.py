import os
from configparser import ConfigParser
from pathlib import Path
from typing import Final, Iterator, Tuple

from ..decorators import intercept_errors, require_bins, run_subprocess
from ..helpers.boto import get_identity
from ..helpers.contexts import push_env
from ..helpers.keywords_to_options import Argument
from ..helpers.params import Profile
from .saml_client import SAMLClient

AwsCredentialsPath = Path(os.getenv('AWS_CREDENTIAL_FILE', Path.home() / '.aws' / 'credentials'))

class AwsProfile(SAMLClient):
    binary = "aws"
    option_value = "aws-profile"
    priority = 0
    setup_help = f"Set up your profile in `{str(AwsCredentialsPath)}`."

    resource: str
    debug: bool

    @classmethod
    def validate_resource(cls, resource: str):
        config = ConfigParser()
        config.read(AwsCredentialsPath)
        return config.has_section(resource)

    def get_creds(self):
        config = ConfigParser()
        config.read(AwsCredentialsPath)
        creds = {k.upper():v for k,v in config[self.resource].items() if k.startswith('aws')}
        creds['AWS_REGION'] = config[self.resource].get('REGION')
        return creds


    @intercept_errors()
    @run_subprocess
    @require_bins(binary)
    def _exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        self.log_subprocess_event(args)
        with push_env("AWS_PROFILE", self.resource):
            yield *args, opts

    def is_setup(self) -> bool:
        return AwsCredentialsPath.exists()

    def _ensure_config(self, profile: Profile) -> ConfigParser:
        return ConfigParser()

    def _ensure_session(self):
        get_identity(self)
