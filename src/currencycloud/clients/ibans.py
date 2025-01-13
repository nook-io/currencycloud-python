"""This module provides a class for IBANs calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import Iban, PaginatedCollection


class Ibans(Http):
    """This class provides an interface to the IBANs endpoints of the CC API"""

    async def find(self, **kwargs: Any) -> PaginatedCollection[Iban]:
        """Search for IBANs that meet a number of criteria and receive a paged response."""
        response = await self.get("/v2/ibans/find", query=kwargs)
        data = [Iban(**fields) for fields in response["ibans"]]
        return PaginatedCollection(data, response["pagination"])
