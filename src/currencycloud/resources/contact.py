"""This module provides the object representation of a CurrencyCloud Contact"""

from currencycloud.resources.resource import Resource


class Contact(Resource):
    """This class represents a CurrencyCloud Contact"""

    login_id: str
    id: str
    first_name: str
    last_name: str
    account_id: str
    account_name: str
    status: str
    locale: str
    timezone: str
    email_address: str
    mobile_phone_number: str | None
    phone_number: str | None
    your_reference: str | None
    date_of_birth: str | None
    created_at: str
    updated_at: str


class HMACKey(Resource):
    pass
