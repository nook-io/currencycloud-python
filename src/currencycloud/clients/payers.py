"""This module provides a class for Payers calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import Payer


class Payers(Http):
    """This class provides an interface to the Payers endpoints of the CC API"""

    async def retrieve(self, resource_id: str, **kwargs: Any) -> Payer:
        """Returns a hash containing the details of the requested payer."""
        return Payer(**await self.get("/v2/payers/" + resource_id, query=kwargs))
