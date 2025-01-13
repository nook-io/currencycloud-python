"""This module provides the object representation of a CurrencyCloud Funding"""

from typing import Literal

from currencycloud.resources.resource import Resource


class FundingAccount(Resource):
    """This class represents a CurrencyCloud Funding Account"""

    id: str
    account_id: str
    account_number: str
    account_number_type: str
    account_holder_name: str
    bank_name: str
    bank_address: str
    bank_country: str
    currency: str
    payment_type: Literal["regular", "priority"]
    routing_code: str
    routing_code_type: str
    created_at: str
    updated_at: str
