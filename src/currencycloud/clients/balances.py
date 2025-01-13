"""This module provides a class for Balances calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import Balance, MarginBalanceTopUp, PaginatedCollection


class Balances(Http):
    """This class provides an interface to the Balances endpoints of the CC API"""

    async def for_currency(self, currency: str, **kwargs: Any) -> Balance:
        """
        Provides the balance for a currency and shows the date that the balance was last updated.
        """
        return Balance(**await self.get("/v2/balances/" + currency, query=kwargs))

    async def find(self, **kwargs: Any) -> PaginatedCollection[Balance]:
        """
        Search for a range of balances and receive a paged response. This is useful if you want to
        see historic balances.
        """
        response = await self.get("/v2/balances/find", query=kwargs)
        data = [Balance(**fields) for fields in response["balances"]]
        return PaginatedCollection(data, response["pagination"])

    async def top_up_margin(self, **kwargs: Any) -> MarginBalanceTopUp:
        """
        Provides the balance for a currency and shows the date that the balance was last updated.
        """
        return MarginBalanceTopUp(**await self.post("/v2/balances/top_up_margin", kwargs))

    async def first(self, **params: Any) -> Balance:
        params["per_page"] = 1
        return (await self.find(**params))[0]
