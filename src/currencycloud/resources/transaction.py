"""This module provides the object representation of a CurrencyCloud Transaction"""

from typing import Literal

from currencycloud.resources.resource import Resource


class Transaction(Resource):
    """This class represents a CurrencyCloud Transaction"""

    id: str
    balance_id: str
    account_id: str
    currency: str
    amount: str
    balance_amount: str
    type: Literal["credit", "debit"]
    related_entity_type: str
    related_entity_id: str
    related_entity_short_reference: str
    status: str
    reason: str
    settles_at: str
    created_at: str
    updated_at: str
    completed_at: str | None
    action: str
