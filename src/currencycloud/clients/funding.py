"""This module provides a class for Funding calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import FundingAccount, PaginatedCollection


class Funding(Http):
    """This class provides an interface to the Funding endpoints of the CC API"""

    async def find_funding_accounts(self, **kwargs: Any) -> PaginatedCollection[FundingAccount]:
        """
        Return an array containing json structures of details of the funding accounts matching the
        search criteria for the logged in user.
        """
        response = await self.get("/v2/funding_accounts/find", query=kwargs)
        data = [FundingAccount(**fields) for fields in response["funding_accounts"]]
        return PaginatedCollection(data, response["pagination"])
