"""This module provides a class for authentication related calls to the CC API"""

from typing import Any

from currencycloud.http import Http


class Auth(Http):
    """This class provides an interface to the Authentication endpoints of the CC API"""

    async def authenticate(self) -> dict[str, Any]:
        """Exchange Login ID and Api Key for a temporary Auth Token"""
        return await self.post(
            "/v2/authenticate/api",
            {"login_id": self.config.login_id, "api_key": self.config.api_key},
            authenticated=False,
            retry=False,
            disable_on_behalf_of=True,
        )

    async def close_session(self) -> dict[str, Any]:
        """Invalidate the Auth Token"""
        return await self.post("/v2/authenticate/close_session", {})
