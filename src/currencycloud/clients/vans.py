"""This module provides a class for VANs calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Van


class Vans(Http):
    """This class provides an interface to the VANs endpoints of the CC API"""

    async def find(self, **kwargs: Any):
        """Search for VANs that meet a number of criteria and receive a paged response."""
        response = await self.get("/v2/virtual_accounts/find", query=kwargs)
        data = [Van(**fields) for fields in response["virtual_accounts"]]
        return PaginatedCollection(data, response["pagination"])

    async def first(self, **params: Any):
        params["per_page"] = 1
        return (await self.find(**params))[0]
