"""This module provides a class for beneficiaries calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import (
    AccountVerification,
    Beneficiary,
    PaginatedCollection,
)


class Beneficiaries(Http):
    """This class provides an interface to the Beneficiaries endpoints of the CC API"""

    async def create(self, **kwargs: Any) -> Beneficiary:
        """
        Creates a new beneficiary and returns a hash containing the details of the new beneficiary.
        Some of the optional parameters may be required depending on the requirements of the
        currency and the country.

        Please use the /v2/reference/beneficiary_required_details call to know which fields are
        required.

        Information that is required for your payment depends on the payment type (local or
        standard/SWIFT payment), originating country, payer country, payer legal entity type,
        beneficiary country, beneficiary entity type and payment destination country.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        """
        return Beneficiary(**await self.post("/v2/beneficiaries/create", kwargs))

    async def delete(self, resource_id: str, **kwargs: Any) -> Beneficiary:
        """
        Delete a previously created beneficiary and returns a hash containing the details of the
        deleted beneficiary.
        """
        return Beneficiary(
            **await self.post("/v2/beneficiaries/" + resource_id + "/delete", kwargs),
        )

    async def find(self, **kwargs: Any) -> PaginatedCollection[Beneficiary]:
        """
        Return an array containing json structures of details of the accounts matching the search
        criteria for the logged in user.
        """
        response = await self.post("/v2/beneficiaries/find", kwargs)
        data = [Beneficiary(**fields) for fields in response["beneficiaries"]]
        return PaginatedCollection(data, response["pagination"])

    async def first(self, **params: Any):
        params["per_page"] = 1
        return (await self.find(**params))[0]

    async def retrieve(self, resource_id: str, **kwargs: Any) -> Beneficiary:
        """Returns a json structure containing the details of the requested beneficiary."""
        return Beneficiary(
            **await self.get("/v2/beneficiaries/" + resource_id, query=kwargs)
        )

    async def update(self, resource_id: str, **kwargs: Any) -> Beneficiary:
        """
        Updates an existing beneficiary and returns a json structure containing the details of the
        beneficiary.

        The same rules for parameters apply as for the create request.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        """
        return Beneficiary(
            **await self.post("/v2/beneficiaries/" + resource_id, kwargs)
        )

    async def validate(self, **kwargs: Any) -> Beneficiary:
        """
        Validates Beneficiary details without creating one. Some of the optional parameters may be
        required depending on the requirements of the currency and the country.

        Please use the /v2/reference/beneficiary_required_details call to know which fields are
        required.
        """
        return Beneficiary(**await self.post("/v2/beneficiaries/validate", kwargs))

    async def account_verification(self, **kwargs: Any) -> AccountVerification:
        """
        Validates Bank account details.
        """
        return AccountVerification(
            **await self.post("/v2/beneficiaries/account_verification", kwargs)
        )
