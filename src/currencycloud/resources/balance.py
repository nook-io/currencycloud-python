"""This module provides the object representation of a CurrencyCloud Balance"""

from currencycloud.resources.resource import Resource


class Balance(Resource):
    """This class represents a CurrencyCloud Balance"""

    id: str
    account_id: str
    currency: str
    amount: str
    created_at: str
    updated_at: str


class MarginBalanceTopUp(Resource):
    """This class represents a CurrencyCloud MarginBalance Top Up"""

    pass
