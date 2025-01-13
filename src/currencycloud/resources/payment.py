"""This module provides the object representation of a CurrencyCloud Payment"""

from typing import Literal

from currencycloud.resources.resource import Resource


class Payment(Resource):
    """This class represents a CurrencyCloud Payment"""

    id: str
    amount: str
    beneficiary_id: str
    currency: str
    reference: str
    reason: str
    status: Literal[
        "new",
        "ready_to_send",
        "completed",
        "failed",
        "released",
        "suspended",
        "awaiting_authorisation",
        "submitted",
        "authorised",
        "deleted",
    ]
    creator_contact_id: str
    payment_type: Literal["regular", "priority"]
    payment_date: str
    transferred_at: str | None
    authorisation_steps_required: str
    last_updater_contact_id: str
    short_reference: str
    conversion_id: str | None
    failure_reason: str | None
    payer_id: str
    payer_details_source: str
    created_at: str
    updated_at: str
    payment_group_id: str | None
    unique_request_id: str | None
    failure_returned_amount: str | None
    ultimate_beneficiary_name: str | None
    purpose_code: str | None
    charge_type: str | None
    fee_amount: str | None
    fee_currency: str | None
    review_status: str


class QuotePaymentFee(Resource):
    """This class represents a quoted fee for a CurrencyCloud Payment"""

    pass


class PaymentTrackingInfo(Resource):
    """This class represents the tracking info for a CurrencyCloud Payment"""

    pass


class PaymentValidation(Resource):
    """This class represents a validation for a CurrencyCloud Payment"""

    pass


class PaymentDeliveryDate(Resource):
    payment_date: str
    payment_delivery_date: str
    payment_cutoff_time: str
    payment_type: Literal["regular", "priority"]
    currency: str
    bank_country: str


class PaymentFee(Resource):
    pass
