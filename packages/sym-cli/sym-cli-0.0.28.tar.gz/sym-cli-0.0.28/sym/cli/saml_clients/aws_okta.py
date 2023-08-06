import sys
from configparser import ConfigParser, NoOptionError, NoSectionError
from pathlib import Path
from typing import Final, Iterator, Optional, Tuple
from urllib.parse import urlsplit

from ..decorators import intercept_errors, require_bins, run_subprocess
from ..errors import (
    FailedSubprocessError,
    ResourceNotSetup,
    SamlClientNotSetup,
    UnavailableResourceError,
)
from ..helpers.config import Config, SymConfigFile, xdg_config_home
from ..helpers.constants import AwsOktaNoCreds, AwsOktaNoRoles, AwsOktaNotSetup
from ..helpers.contexts import push_env
from ..helpers.keywords_to_options import Argument
from ..helpers.params import Profile, get_aws_okta_params
from .saml_client import SAMLClient

ErrorPatterns = {
    AwsOktaNoRoles: UnavailableResourceError,
    AwsOktaNotSetup: ResourceNotSetup,
    AwsOktaNoCreds: SamlClientNotSetup,
}


class AwsOkta(SAMLClient):
    __slots__ = ["config_file", "resource", "debug", "_config"]
    binary = "aws-okta"
    option_value = "aws-okta"
    priority = 5
    setup_help = "Run `aws-okta add`."

    resource: str
    debug: bool
    config_file: Final[SymConfigFile]
    _config: Optional[ConfigParser]

    def __init__(self, resource: str, *, debug: bool) -> None:
        super().__init__(resource, debug=debug)
        self.config_file = SymConfigFile(resource=resource, file_name="aws-okta.cfg")

    def is_setup(self) -> bool:
        path = Path.home() / ".aws" / "config"
        config = ConfigParser()
        config.read(path)
        return "okta" in config.sections()

    @intercept_errors(ErrorPatterns)
    @run_subprocess
    @require_bins(binary)
    def _exec(self, *args: str, **opts: str) -> Iterator[Tuple[Argument, ...]]:
        self.log_subprocess_event(args)
        self.ensure_config()
        with push_env("AWS_CONFIG_FILE", str(self.config_file)):
            yield ("aws-okta", {"debug": self.debug}, "exec", "sym", "--", *args, opts)

    @intercept_errors(ErrorPatterns)
    @run_subprocess
    @require_bins(binary)
    def _login(self) -> Iterator[Tuple[Argument, ...]]:
        self.ensure_config()
        with push_env("AWS_CONFIG_FILE", str(self.config_file)):
            yield (
                "aws-okta",
                {"debug": self.debug},
                "add",
                {"domain": self.okta_domain, "username": Config.get_email()},
                {
                    k: v
                    for k, v in get_aws_okta_params().items()
                    if k in ["mfa_provider", "mfa_factor_type"]
                },
            )

    def _ensure_session(self):
        # aws-okta fails in mysterious ways if your
        # keychain credentials are deleted after setup.
        # This logic handles that case cleanly.
        try:
            super()._ensure_session()
        except FailedSubprocessError:
            print("Logging in to Okta...", file=sys.stderr)
            self._login(silence_stderr_=False)
            print("Fetching SAML assertion...", file=sys.stderr)
            super()._ensure_session()

    @property
    def okta_domain(self) -> str:
        url = self.get_aws_saml_url(bare=False)
        return urlsplit(url).netloc

    def _ensure_config(self, profile: Profile) -> ConfigParser:
        config = ConfigParser(default_section="okta")
        config.read_dict(
            {
                "okta": get_aws_okta_params(),
                "profile sym": {
                    "aws_saml_url": self.get_aws_saml_url(bare=True),
                    "region": profile.region,
                    "role_arn": profile.arn,
                },
            }
        )
        return config
