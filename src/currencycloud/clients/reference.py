"""This module provides a class for Reference calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import (
    BankDetails,
    BeneficiaryRequiredDetails,
    ConversionDates,
    Currency,
    PayerRequiredDetails,
    PaymentFeeRule,
    PaymentPurposeCode,
    SettlementAccount,
)


class Reference(Http):
    """This class provides an interface to the Reference endpoints of the CC API"""

    async def beneficiary_required_details(self, **kwargs: Any) -> list[BeneficiaryRequiredDetails]:
        """Returns required beneficiary details and their basic validation formats."""
        response = (await self.get("/v2/reference/beneficiary_required_details", query=kwargs))["details"]
        return [BeneficiaryRequiredDetails(**c) for c in response]

    async def conversion_dates(self, **kwargs: Any) -> ConversionDates:
        """Returns dates for which dates this currency pair can not be traded."""
        return ConversionDates(**await self.get("/v2/reference/conversion_dates", query=kwargs))

    async def currencies(self) -> list[Currency]:
        """Returns a list of all the currencies that are tradeable."""
        response = (await self.get("/v2/reference/currencies"))["currencies"]
        return [Currency(**c) for c in response]

    async def payment_dates(self, **kwargs: Any) -> dict[str, Any]:
        """
        This call returns a list of dates that are invalid when making payments of a specific
        currency.
        """
        return await self.get("/v2/reference/payment_dates", query=kwargs)

    async def settlement_accounts(self, **kwargs: Any) -> list[SettlementAccount]:
        """Returns settlement account information, detailing where funds need to be sent to."""
        response = (await self.get("/v2/reference/settlement_accounts", query=kwargs))["settlement_accounts"]
        return [SettlementAccount(**c) for c in response]

    async def payer_required_details(self, **kwargs: Any) -> list[PayerRequiredDetails]:
        """Returns required payer details and their basic validation formats."""
        response = (await self.get("/v2/reference/payer_required_details", query=kwargs))["details"]
        return [PayerRequiredDetails(**c) for c in response]

    async def payment_purpose_codes(self, **kwargs: Any) -> list[PaymentPurposeCode]:
        """Returns a list of valid purpose codes for the specified currency."""
        response = (await self.get("/v2/reference/payment_purpose_codes", query=kwargs))["purpose_codes"]
        return [PaymentPurposeCode(**c) for c in response]

    async def bank_details(self, **kwargs: Any) -> BankDetails:
        """Returns the details of the bank related to the specified identifier."""
        response = await self.post("/v2/reference/bank_details/find", kwargs)
        return BankDetails(**response)

    async def payment_fee_rules(self, **kwargs: Any) -> list[PaymentFeeRule]:
        """Returns a list of payment fee rules."""
        response = (await self.get("/v2/reference/payment_fee_rules", query=kwargs))["payment_fee_rules"]
        return [PaymentFeeRule(**c) for c in response]
