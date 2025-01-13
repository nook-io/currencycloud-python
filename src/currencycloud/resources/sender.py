from currencycloud.resources.resource import Resource


class Sender(Resource):
    """This class represents a CurrencyCloud Sender"""

    id: str
    amount: str
    currency: str
    additional_information: str
    value_date: str
    sender: str
    receiving_account_number: str | None
    receiving_account_iban: str | None
    created_at: str
    updated_at: str
