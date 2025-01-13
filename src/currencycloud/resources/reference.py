from typing import Literal

from currencycloud.resources.resource import Resource


class Currency(Resource):
    pass


class ConversionDates(Resource):
    pass


class SettlementAccount(Resource):
    pass


class BeneficiaryRequiredDetails(Resource):
    pass


class PayerRequiredDetails(Resource):
    pass


class PaymentPurposeCode(Resource):
    pass


class BankDetails(Resource):
    pass


class PaymentFeeRule(Resource):
    payment_type: Literal["regular", "priority"]
    charge_type: Literal["ours", "shared"] | None
    fee_amount: str
    fee_currency: str
    payment_fee_id: str
    payment_fee_name: str
