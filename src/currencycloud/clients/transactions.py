"""This module provides a class for Transactions calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Transaction


class Transactions(Http):
    """This class provides an interface to the Transactions endpoints of the CC API"""

    async def find(self, **kwargs: Any) -> PaginatedCollection[Transaction]:
        """Search for transactions that meet a number of criteria and receive a paged response."""
        response = await self.get("/v2/transactions/find", query=kwargs)
        data = [Transaction(**fields) for fields in response["transactions"]]
        return PaginatedCollection(data, response["pagination"])

    async def first(self, **params: Any) -> Transaction:
        params["per_page"] = 1
        return (await self.find(**params))[0]

    async def retrieve(self, resource_id: str, **kwargs: Any) -> Transaction:
        """Find the details of a specific transaction."""
        return Transaction(**await self.get("/v2/transactions/" + resource_id, query=kwargs))
