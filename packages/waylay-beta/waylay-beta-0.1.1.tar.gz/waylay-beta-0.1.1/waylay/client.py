"""REST client for the Waylay Platform"""

from typing import (
    Optional, TypeVar, List, Mapping
)

from .service import (
    AnalyticsService,
    ByomlService,
    WaylayService
)
from .config import (
    WaylayConfig,
    DEFAULT_PROFILE
)
from .auth import (
    WaylayCredentials,
    ClientCredentials,
    TokenCredentials,
    DEFAULT_ACCOUNTS_URL
)

S = TypeVar('S', bound=WaylayService)


class WaylayClient():
    """REST client for the Waylay Platform"""
    analytics: AnalyticsService
    config: WaylayConfig
    _services: List[WaylayService]

    @classmethod
    def from_profile(
        cls, profile: str = DEFAULT_PROFILE,
        interactive=True, accounts_url=DEFAULT_ACCOUNTS_URL
    ):
        """
        Creates a WaylayClient using credentials from environment variables or
        locally stored configuration.
        """
        return cls(WaylayConfig.load(profile, interactive=interactive, accounts_url=accounts_url))

    @classmethod
    def from_client_credentials(
        cls, api_key: str, api_secret: str, accounts_url: str = DEFAULT_ACCOUNTS_URL
    ):
        """
        Creates a WaylayClient using the given client credentials
        """
        return cls.from_credentials(ClientCredentials(api_key, api_secret, accounts_url))

    @classmethod
    def from_token(
        cls, token_string: str, accounts_url: str = DEFAULT_ACCOUNTS_URL
    ):
        """
        Creates a WaylayClient using a waylay token
        """
        return cls.from_credentials(TokenCredentials(token_string, accounts_url))

    @classmethod
    def from_credentials(
        cls, credentials: WaylayCredentials
    ):
        """
        Creates a WaylayClient using the given client credentials
        """
        return cls(WaylayConfig(credentials))

    def __init__(self, config: WaylayConfig):
        self._services: List[WaylayService] = []

        def register(srv: S) -> S:
            self._services.append(srv)
            return srv
        self.analytics = register(AnalyticsService())
        self.byoml = register(ByomlService())
        self.configure(config)

    def configure(self, config: WaylayConfig):
        """update this client with the given configuration"""
        self.config = config
        for srv in self._services:
            srv.configure(self.config)

    def list_root_urls(self) -> Mapping[str, Optional[str]]:
        """List the currently configured root url for each of the registered services."""
        return {srv.config_key: srv.get_root_url() for srv in self._services}

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"services=[{','.join(srv.config_key for srv in self._services)}],"
            f"config={self.config}"
            ")>"
        )
