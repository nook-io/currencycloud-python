"""This module provides the object representation of a CurrencyCloud Beneficiary"""

from currencycloud.resources.resource import Resource


class Beneficiary(Resource):
    """This class represents a CurrencyCloud Beneficiary"""

    id: str
    name: str | None
    email: str | None
    payment_types: list[str]
    beneficiary_address: list[str] | None
    beneficiary_country: str | None
    beneficiary_entity_type: str
    beneficiary_company_name: str | None
    beneficiary_first_name: str | None
    beneficiary_last_name: str | None
    beneficiary_city: str | None
    beneficiary_postcode: str | None
    beneficiary_state_or_province: str | None
    beneficiary_date_of_birth: str | None
    beneficiary_identification_type: str | None
    beneficiary_identification_value: str | None
    bank_country: str
    bank_account_holder_name: str
    bank_name: str | None
    bank_account_type: str | None
    currency: str
    account_number: str | None
    routing_code_type_1: str | None
    routing_code_value_1: str | None
    routing_code_type_2: str | None
    routing_code_value_2: str | None
    bic_swift: str | None
    iban: str | None
    default_beneficiary: str
    creator_contact_id: str
    bank_address: list[str] | None
    created_at: str
    updated_at: str
    beneficiary_external_reference: str | None
    business_nature: str | None
    company_website: str | None
