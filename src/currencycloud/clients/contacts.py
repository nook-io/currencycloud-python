"""This module provides a class for Contacts calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import Contact, PaginatedCollection
from currencycloud.resources.contact import HMACKey


class Contacts(Http):
    """This class provides an interface to the Contacts endpoints of the CC API"""

    async def create(self, **kwargs: Any) -> Contact:
        """
        Creates a new contact which is added to the logged in account and returns a hash containing
        the details of the new contact.
        """
        return Contact(**await self.post("/v2/contacts/create", kwargs))

    async def current(self) -> Contact:
        """
        Returns a json structure containing the details of the contact that is currently logged in.
        """
        return Contact(**await self.get("/v2/contacts/current"))

    async def find(self, **kwargs: Any) -> PaginatedCollection[Contact]:
        """
        A paged response of an array containing hashes of details of the contacts matching the
        search criteria for the active user.
        """
        response = await self.post("/v2/contacts/find", kwargs)
        data = [Contact(**fields) for fields in response["contacts"]]
        return PaginatedCollection(data, response["pagination"])

    async def first(self, **params: Any) -> Contact:
        params["per_page"] = 1
        return (await self.find(**params))[0]

    async def retrieve(self, resource_id: str, **kwargs: Any) -> Contact:
        """Returns a json structure containing the details of the requested contact."""
        return Contact(**await self.get("/v2/contacts/" + resource_id, query=kwargs))

    async def update(self, resource_id: str, **kwargs: Any) -> Contact:
        """
        Updates an existing contact and returns a hash containing the details of the requested
        contact.
        """
        return Contact(**await self.post("/v2/contacts/" + resource_id, kwargs))

    async def generate_hmac_key(self) -> HMACKey:
        return HMACKey(**await self.post("/v2/contacts/generate_hmac_key", None))
