import json
import logging
import os
import tempfile
import time

from azure.core.credentials import AccessToken
from azure.identity import (
    AzureCliCredential,
    ChainedTokenCredential,
    EnvironmentCredential,
    SharedTokenCacheCredential,
    WorkloadIdentityCredential,
)

AZURE_TENANT_ID = "d23844a4-14b7-4e42-9e3a-be7fcb83625b"

# Acquire the logger for azure identity
logger = logging.getLogger("azure.identity")

# Increase the logging level to remove redundant auth logs
logger.setLevel(logging.WARNING)


class AzureAuth:
    def __init__(self):
        self.__tokens = {}
        self._credentials = None
        self.token_file = os.path.join(tempfile.gettempdir(), "azure_auth_python.cache")

    def _get_token_from_azure(self, uri):
        try:
            token = WorkloadIdentityCredential().get_token(uri)
        except Exception:
            credential_chain = (
                SharedTokenCacheCredential(),
                EnvironmentCredential(),
                AzureCliCredential(tenant_id=AZURE_TENANT_ID),
            )
            token = ChainedTokenCredential(*credential_chain).get_token(uri)
        return token

    def get_token(self, uri, output=None):
        token = self.__tokens.get(uri, None)
        if not token:
            # Token doesn't exist in memory, check the shared disk cache
            try:
                with open(self.token_file, "r") as fh:
                    token_strs = json.loads(fh.read())
                    self.__tokens = {k: AccessToken(v[0], v[1]) for (k, v) in token_strs.items()}
                token = self.__tokens.get(uri, None)
            except FileNotFoundError:
                pass

        if token:
            if token.expires_on > time.time():
                # Used the cached token
                return token[0]

        # No cached token available (or it's expired).  Get a new token.
        # Store the token in both in-memory cache and on shared-disk cache
        self.__tokens[uri] = self._get_token_from_azure(uri)
        with open(self.token_file, "w") as fh:
            fh.write(json.dumps(self.__tokens))

        return self.__tokens[uri][0]
