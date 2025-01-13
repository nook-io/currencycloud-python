"""This module provides a class for Accounts calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import Account, PaginatedCollection, PaymentChargesSettings


class Accounts(Http):
    """This class provides an interface to the Accounts endpoints of the CC API"""

    async def create(self, **kwargs: Any) -> Account:
        """
        Creates a new account and returns a json structure containing the details of the requested
        account.
        """
        return Account(**await self.post("/v2/accounts/create", kwargs))

    async def current(self) -> Account:
        """Returns a json structure containing the details of the active account."""
        return Account(**await self.get("/v2/accounts/current"))

    async def find(self, **kwargs: Any) -> PaginatedCollection[Account]:
        """
        Return an array containing json structures of details of the accounts matching the
        search criteria for the logged in user.
        """
        response = await self.post("/v2/accounts/find", kwargs)
        data = [Account(**fields) for fields in response["accounts"]]
        return PaginatedCollection(data, response["pagination"])

    async def first(self, **params: Any) -> Account:
        params["per_page"] = 1
        return (await self.find(**params))[0]

    async def retrieve(self, resource_id: str, **kwargs: Any) -> Account:
        """Returns a json structure containing the details of the requested account."""
        return Account(**await self.get("/v2/accounts/" + resource_id, query=kwargs))

    async def update(self, resource_id: str, **kwargs: Any) -> Account:
        """
        Updates an existing account and returns a json structure containing the details of the
        requested account.
        """
        return Account(**await self.post("/v2/accounts/" + resource_id, kwargs))

    async def payment_charges_settings(
        self, account_id: str, resource_id: str, **kwargs: Any
    ) -> PaymentChargesSettings:
        """
        Manage given Account's Payment Charge Settings (enable, disable, set default).
        """
        return PaymentChargesSettings(
            **await self.post("/v2/accounts/" + account_id + "/payment_charges_settings/" + resource_id, kwargs)
        )

    async def retrieve_payment_charges_settings(self, resource_id: str, **kwargs: Any) -> list[PaymentChargesSettings]:
        """Retrieve payment charges settings for given account."""
        response = (await self.get("/v2/accounts/" + resource_id + "/payment_charges_settings", query=kwargs))[
            "payment_charges_settings"
        ]
        return [PaymentChargesSettings(**c) for c in response]
