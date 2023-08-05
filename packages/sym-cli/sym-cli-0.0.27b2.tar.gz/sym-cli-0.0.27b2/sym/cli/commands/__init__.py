from typing import ClassVar, Mapping, Type

import click

from ..helpers import segment, util
from ..saml_clients.saml_client import SAMLClient


class GlobalOptions:
    saml_clients: Mapping[str, SAMLClient] = {}
    saml_client_type: Type[SAMLClient]
    debug: bool = False

    def create_saml_client(self, resource: str) -> SAMLClient:
        segment.track("Resource Requested", resource=resource)
        if resource not in self.saml_clients:
            self.saml_clients[resource] = self.saml_client_type(
                resource, debug=self.debug
            )
        return self.saml_clients[resource]

    def to_dict(self):
        return {"debug": self.debug, "saml_client": self.saml_client_type.__name__}


def import_all():
    util.import_all(__file__, __name__)
