"""This module provides the object representation of a CurrencyCloud Account"""

from currencycloud.resources.resource import Resource


class Account(Resource):
    """This class represents a CurrencyCloud Account"""

    id: str
    account_name: str
    brand: str
    your_reference: str | None
    status: str
    street: str
    city: str
    state_or_province: str | None
    country: str
    postal_code: str
    spread_table: str
    legal_entity_type: str
    created_at: str
    updated_at: str
    identification_type: str | None
    identification_value: str | None
    short_reference: str
    api_trading: bool
    online_trading: bool
    phone_trading: bool
    process_third_party_funds: bool
    settlement_type: str
    agent_or_reliance: bool
    terms_and_conditions_accepted: bool | None
    bank_account_verified: str


class PaymentChargesSettings(Resource):
    pass
