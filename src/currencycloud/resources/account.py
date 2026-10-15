"""This module provides the object representation of a CurrencyCloud Account"""

from typing import Literal

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


class ComplianceSettings(Resource):
    account_id: str
    industry_type: str | None
    country_of_incorporation: str | None
    date_of_incorporation: str | None
    business_website_url: str | None
    expected_transaction_countries: list[str] | None
    expected_transaction_currencies: list[str] | None
    expected_monthly_activity_volume: int | None
    expected_monthly_activity_value: float | None
    tax_identification: str | None
    national_identification: str | None
    country_of_citizenship: str | None
    trading_address_street: str | None
    trading_address_city: str | None
    trading_address_state: str | None
    trading_address_postalcode: str | None
    trading_address_country: str | None
    customer_risk: Literal["LOW", "MEDIUM", "HIGH"] | None
