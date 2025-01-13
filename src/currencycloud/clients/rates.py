"""This module provides a class for Rates calls to the CC API"""

from typing import Any

from currencycloud import resources
from currencycloud.http import Http
from currencycloud.resources import Rate


class Rates(Http):
    """This class provides an interface to the Rates endpoints of the CC API"""

    async def detailed(self, **kwargs: Any) -> Rate:
        """
        Returns a hash containing a full quote for the requested currency based on the spread table
        of the currently logged in contact. If delivery date is not supplied it will default to a
        deal which settles in 2 working days.
        """
        return Rate(**await self.get("/v2/rates/detailed", query=kwargs))

    async def find(self, **kwargs: Any) -> resources.Rates:
        """
        Returns core rate information for multiple pairs. The first number in each pair in the
        response is the bid rate and the second is the offer rate.
        """
        response = await self.get("/v2/rates/find", query=kwargs)

        rates = []
        for currency_pair, bid_offer in response["rates"].items():
            rate = {
                "currency_pair": currency_pair,
                "bid": bid_offer[0],
                "offer": bid_offer[1],
            }
            rates.append(Rate(**rate))

        return resources.Rates(currencies=rates, unavailable=response["unavailable"])
