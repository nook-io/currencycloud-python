"""This module provides the object representation of a CurrencyCloud Transfer"""

from typing import Literal

from currencycloud.resources.resource import Resource


class Transfer(Resource):
    """This class represents a CurrencyCloud Transfer"""

    id: str
    short_reference: str
    source_account_id: str
    destination_account_id: str
    currency: str
    amount: str
    status: Literal["pending", "completed", "cancelled"]
    reason: str
    created_at: str
    updated_at: str
    completed_at: str
    creator_account_id: str
    creator_contact_id: str
    unique_request_id: str
