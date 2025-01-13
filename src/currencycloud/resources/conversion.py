"""This module provides the object representation of a CurrencyCloud Conversion"""

from typing import Literal

from currencycloud.resources.resource import Resource


class Conversion(Resource):
    """This class represents a CurrencyCloud Conversion"""

    id: str
    settlement_date: str
    conversion_date: str
    short_reference: str
    creator_contact_id: str
    account_id: str
    currency_pair: str
    status: Literal[
        "awaiting_funds",
        "funds_sent",
        "funds_arrived",
        "funds_being_processed",
        "trade_settling",
        "trade_settled",
        "closed",
        "awaiting_authorisation",
    ]
    buy_currency: str
    sell_currency: str
    client_buy_amount: str
    client_sell_amount: str
    fixed_side: Literal["buy", "sell"]
    core_rate: str
    partner_rate: str
    partner_buy_amount: str
    partner_sell_amount: str
    client_rate: str
    deposit_required: bool
    deposit_amount: str
    deposit_currency: str | None
    deposit_status: str
    deposit_required_at: str | None
    payment_ids: list[str]
    unallocated_funds: str
    unique_request_id: str | None
    created_at: str
    updated_at: str
    mid_market_rate: str


class ProfitAndLoss(Resource):
    account_id: str
    contact_id: str
    event_account_id: str | None
    event_contact_id: str | None
    conversion_id: str
    event_type: str
    amount: str
    currency: str
    notes: str
    event_date_time: str
