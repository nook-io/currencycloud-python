"""This module provides a class for Transfers calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Transfer


class Transfers(Http):
    """This class provides an interface to the Transfers endpoints of the CC API"""

    async def create(self, **kwargs: Any) -> Transfer:
        """
        Creates a transfer of funds from a cash manager balance of an account to the same currency
        cash manager balance of another account.
        """
        return Transfer(**await self.post("/v2/transfers/create", kwargs))

    async def find(self, **kwargs: Any) -> PaginatedCollection[Transfer]:
        """Returns an array of Transfer objects for the given search criteria."""
        response = await self.get("/v2/transfers/find", query=kwargs)
        data = [Transfer(**fields) for fields in response["transfers"]]
        return PaginatedCollection(data, response["pagination"])

    async def first(self, **params: Any) -> Transfer:
        params["per_page"] = 1
        return (await self.find(**params))[0]

    async def retrieve(self, resource_id: str, **kwargs: Any) -> Transfer:
        """Returns an array of Transfer objects for the given search criteria."""
        return Transfer(**await self.get("/v2/transfers/" + resource_id, query=kwargs))

    async def cancel(self, resource_id: str, **kwargs: Any) -> Transfer:
        """Request a transfer to be cancelled. Returns the Transfer object."""
        return Transfer(**await self.get("/v2/transfers/" + resource_id + "/cancel", query=kwargs))
