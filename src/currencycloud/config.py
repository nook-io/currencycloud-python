"""This module provides a Client class for authentication related calls to the CC API"""

from typing import Awaitable, Callable, Literal

import httpx

from currencycloud.clients.auth import Auth


class Config:
    """API Configuration Object. Keeps track of Credentials, Auth Token and API Environment"""

    auth_token: str | None = None

    ENV_PROD = "prod"
    ENV_DEMO = "demo"

    ENVIRONMENT_URLS = {
        ENV_PROD: "https://api.currencycloud.com",
        ENV_DEMO: "https://devapi.currencycloud.com",
    }
    _session: httpx.AsyncClient | None = None

    def __init__(
        self,
        login_id: str,
        api_key: str,
        environment: Literal["prod", "demo"] = ENV_DEMO,
        token_getter: Callable[[], Awaitable[str]] | None = None,
        client: httpx.AsyncClient | None = None,
    ):
        self.login_id = login_id
        self.api_key = api_key
        self.environment = environment
        self.on_behalf_of: str | None = None
        self.token_getter = token_getter
        self.auth_token: str | None = None
        if client is not None:
            self._session = client

        super(Config, self).__init__()
    
    @property
    def session(self) -> httpx.AsyncClient:
        if self._session is None:
            Config._session = httpx.AsyncClient()
        assert self._session is not None
        return self._session
        

    async def get_auth_token(self) -> str:
        """Getter for the Auth Token. Generates one if there is None."""
        if self.auth_token is None:
            if self.login_id is None:
                raise RuntimeError("login_id must be set")
            if self.api_key is None:
                raise RuntimeError("api_key must be set")

            if self.token_getter is not None:
                self.auth_token = await self.token_getter()
            else:
                await self.reauthenticate()

        assert self.auth_token is not None
        return self.auth_token

    async def reauthenticate(self) -> None:
        """Force generation of a new auth token"""

        if self.login_id is None:
            raise RuntimeError("login_id must be set")
        if self.api_key is None:
            raise RuntimeError("api_key must be set")

        self.auth_token = (await Auth(self).authenticate())["auth_token"]

    def environment_url(self) -> str:
        if self.environment not in self.ENVIRONMENT_URLS:
            raise RuntimeError("%s is not a valid environment name" % self.environment)

        return self.ENVIRONMENT_URLS[self.environment]
