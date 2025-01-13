"""This module provides the object representation of a CurrencyCloud Rate"""

from typing import Literal

from currencycloud.resources.resource import Resource


class Rate(Resource):
    """This class represents a CurrencyCloud Rate"""

    settlement_cut_off_time: str
    currency_pair: str
    client_buy_currency: str
    client_sell_currency: str
    client_buy_amount: str
    client_sell_amount: str
    fixed_side: Literal["buy", "sell"]
    client_rate: str
    partner_rate: str
    core_rate: str
    deposit_required: bool
    deposit_amount: str
    deposit_currency: str
    mid_market_rate: str


class Rates(Resource):
    """This class represents a CurrencyCloud Rate"""

    pass
