"""This module provides a class for Conversions calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import Conversion, PaginatedCollection, ProfitAndLoss


class Conversions(Http):
    """This class provides an interface to the Conversions endpoints of the CC API"""

    async def create(self, **kwargs: Any) -> Conversion:
        """Returns a json structure containing the details of the requested conversion."""
        return Conversion(**await self.post("/v2/conversions/create", kwargs))

    async def find(self, **kwargs: Any) -> PaginatedCollection[Conversion]:
        """
        Return an array containing json structures of details of the conversions matching the
        search criteria for the logged in user.
        """
        response = await self.get("/v2/conversions/find", query=kwargs)
        data = [Conversion(**fields) for fields in response["conversions"]]
        return PaginatedCollection(data, response["pagination"])

    async def first(self, **params: Any) -> Conversion:
        params["per_page"] = 1
        return (await self.find(**params))[0]

    async def retrieve(self, resource_id: str, **kwargs: Any) -> Conversion:
        """Returns a json structure containing the details of the requested conversion."""
        return Conversion(
            **await self.get("/v2/conversions/" + resource_id, query=kwargs)
        )

    async def cancel(self, resource_id: str, **kwargs: Any) -> Conversion:
        """Returns a json structure containing the details of the conversion cancellation."""
        return Conversion(
            **await self.post("/v2/conversions/" + resource_id + "/cancel", kwargs),
        )

    async def date_change(self, resource_id: str, **kwargs: Any) -> Conversion:
        """Returns a json structure containing the details of the conversion date change rate."""
        return Conversion(
            **await self.post(
                "/v2/conversions/" + resource_id + "/date_change", kwargs
            ),
        )

    async def split(self, resource_id: str, **kwargs: Any) -> Conversion:
        """Returns a json structure containing split results as parent and child conversions."""
        return Conversion(
            **await self.post("/v2/conversions/" + resource_id + "/split", kwargs)
        )

    async def split_preview(self, resource_id: str, **kwargs: Any) -> Conversion:
        """Returns a json structure containing split results as parent and child conversions."""
        return Conversion(
            **await self.get(
                "/v2/conversions/" + resource_id + "/split_preview", kwargs
            ),
        )

    async def split_history(self, resource_id: str, **kwargs: Any) -> Conversion:
        """Returns a json structure containing split results as parent, origin and child conversions."""
        return Conversion(
            **await self.get(
                "/v2/conversions/" + resource_id + "/split_history", kwargs
            ),
        )

    async def date_change_quote(self, resource_id: str, **kwargs: Any) -> Conversion:
        """
        Returns a JSON structure containing the quote for changing the date of the specified conversion.
        """
        return Conversion(
            **await self.get(
                "/v2/conversions/" + resource_id + "/date_change_quote", kwargs
            ),
        )

    async def cancellation_quote(self, resource_id: str, **kwargs: Any) -> Conversion:
        """
        Returns a JSON structure containing the quote for cancelling the specified conversion.
        """
        return Conversion(
            **await self.get(
                "/v2/conversions/" + resource_id + "/cancellation_quote", kwargs
            ),
        )

    async def profit_and_loss(
        self, **kwargs: Any
    ) -> PaginatedCollection[ProfitAndLoss]:
        """
        Return an array containing json structures of details of the conversions profit and loss matching the
        search criteria for the logged in user.
        """
        response = await self.get("/v2/conversions/profit_and_loss", query=kwargs)
        data = [
            ProfitAndLoss(**fields)
            for fields in response["conversion_profit_and_losses"]
        ]
        return PaginatedCollection(data, response["pagination"])
