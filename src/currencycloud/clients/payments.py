"""This module provides a class for payments related calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import (
    PaginatedCollection,
    Payment,
    PaymentDeliveryDate,
    PaymentTrackingInfo,
    PaymentValidation,
    QuotePaymentFee,
)
from currencycloud.resources.payment import PaymentFee


class Payments(Http):
    """This class provides an interface to the Payment endpoints of the CC API"""

    async def create(self, **kwargs: Any) -> Payment:
        """
        Creates a new payment and returns a hash containing the details of the created payment.

        Information that is required for your payment depends on the payment type (local or
        standard/SWIFT payment), originating country, payer country, payer legal entity type,
        beneficiary country, beneficiary entity type and payment destination country.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        """
        return Payment(**await self.post("/v2/payments/create", kwargs, headers=kwargs.pop("headers", {})))

    async def delete(self, resource_id: str, **kwargs: Any) -> Payment:
        """
        Delete a previously created payment and returns a hash containing the details of the
        deleted payment.
        """
        return Payment(**await self.post("/v2/payments/" + resource_id + "/delete", kwargs))

    async def find(self, **kwargs: Any) -> PaginatedCollection[Payment]:
        """Returns an Array of Payment objects matching the search criteria."""
        response = await self.get("/v2/payments/find", query=kwargs)
        data = [Payment(**fields) for fields in response["payments"]]
        return PaginatedCollection(data, response["pagination"])

    async def first(self, **params: Any) -> Payment:
        params["per_page"] = 1
        return (await self.find(**params))[0]

    async def retrieve(self, resource_id: str, **kwargs: Any) -> Payment:
        """Returns a hash containing the details of the requested payment."""
        return Payment(**await self.get("/v2/payments/" + resource_id, query=kwargs))

        """
        Returns a hash containing the details of MT103 information for a SWIFT submitted payment.
        """
        return await self.get("/v2/payments/" + resource_id + "/submission", query=kwargs)

    async def update(self, resource_id: str, **kwargs: Any) -> Payment:
        """
        Edits a previously created payment and returns a hash containing the details of the edited
        payment.

        Information that is required for your payment depends on the payment type (local or
        standard/SWIFT payment), originating country, payer country, payer legal entity type,
        beneficiary country, beneficiary entity type and payment destination country.

        For more detailed information please see our payment guide:
            http://help.currencycloud.com/world/faq/#mandatory-payment-information
        """
        return Payment(**await self.post("/v2/payments/" + resource_id, kwargs))

    async def payment_confirmation(self, resource_id: str, **kwargs: Any) -> Payment:
        """
        Get confirmation for a payment.
        """
        return Payment(**await self.get("/v2/payments/" + resource_id + "/confirmation", kwargs))

    async def authorise(self, **kwargs: Any) -> Payment:
        """
        Authorise pending payment(s) and returns a hash containing the details of the payment authorisation.
        """
        return Payment(**await self.post("/v2/payments/authorise", kwargs))

    async def payment_delivery_date(self, **kwargs: Any) -> PaymentDeliveryDate:
        """
        Retrieves Payment Delivery Date.
        """
        return PaymentDeliveryDate(**await self.get("/v2/payments/payment_delivery_date", query=kwargs))

    async def quote_payment_fee(self, **kwargs: Any) -> QuotePaymentFee:
        """
        Retrieves Quote Payment Fee.
        """
        return QuotePaymentFee(**await self.get("/v2/payments/quote_payment_fee", query=kwargs))

    async def tracking_info(self, resource_id: str, **kwargs: Any) -> PaymentTrackingInfo:
        """
        Retrieves Payment Tracking Info.
        """
        return PaymentTrackingInfo(**await self.get("/v2/payments/" + resource_id + "/tracking_info", query=kwargs))

    async def validate(self, **kwargs: Any) -> PaymentValidation:
        """Validate Payment"""
        response, headers = await self.post(
            "/v2/payments/validate", data=kwargs, headers=kwargs.pop("headers", {}), return_headers=True
        )
        sca_header_names = ("x-sca-id", "x-sca-type", "x-sca-required")
        headers = {
            header_name: header_value for header_name in sca_header_names if (header_value := headers.get(header_name))
        }
        return PaymentValidation(**response, headers=headers)

    async def payment_fees(self, **kwargs: Any) -> PaymentFee:
        return PaymentFee(**await self.get("/v2/payments/payment_fees", query=kwargs))

    async def assign_payment_fees(self, **kwargs: Any) -> PaymentFee:
        return PaymentFee(**await self.post("/v2/payments/assign_payment_fee", data=kwargs))
