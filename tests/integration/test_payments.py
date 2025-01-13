import pytest
from currencycloud import Client, Config
from currencycloud.errors import BadRequestError
from currencycloud.resources import (
    Payment,
    PaymentTrackingInfo,
    PaymentValidation,
    QuotePaymentFee,
)

from tests.integration.conftest import my_vcr


class TestPayments:
    paymentId = None

    def setup_method(self, method) -> None:
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = "development@currencycloud.com"
        api_key = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    async def test_payments_can_create(self) -> None:
        with my_vcr.use_cassette("payments/create.json"):
            payment = await self.client.payments.create(
                currency="GBP",
                beneficiary_id="a0bd2d78-3621-4c29-932f-a39d6b34d5e7",
                amount="1000",
                reason="Testing payments",
                reference="Testing payments",
                payment_type="regular",
            )

            assert payment is not None
            assert isinstance(payment, Payment)

            assert payment.id is not None
            assert payment.currency == "GBP"

            TestPayments.paymentId = payment.id

    async def test_payments_can_validate(self) -> None:
        with my_vcr.use_cassette("payments/validate.json"):
            payment = await self.client.payments.validate(
                currency="GBP",
                beneficiary_id="a0bd2d78-3621-4c29-932f-a39d6b34d5e7",
                amount="1000",
                reason="Testing payments",
                reference="Testing payments",
                payment_type="regular",
            )

            assert payment is not None
            assert isinstance(payment, PaymentValidation)

            assert payment.validation_result == "success"

    async def test_payments_validate_raises_on_missing_details(self) -> None:
        with my_vcr.use_cassette("payments/validate_error.json"):
            with pytest.raises(BadRequestError):
                await self.client.payments.validate(
                    currency="GBP",
                    beneficiary_id="a0bd2d78-3621-4c29-932f-a39d6b34d5e7",
                    reason="Testing payments",
                    reference="Testing payments",
                    payment_type="regular",
                )
                raise Exception("Should raise exception")

            assert True

    async def test_payments_can_find(self) -> None:
        with my_vcr.use_cassette("payments/find.json"):
            payments = await self.client.payments.find(currency="GBP", per_page=1)

            assert payments
            assert len(payments) == 1

            payment = payments[0]

            assert payment is not None
            assert isinstance(payment, Payment)

            assert payment.currency == "GBP"

    async def test_payments_can_retrieve(self) -> None:
        with my_vcr.use_cassette("payments/retrieve.json"):
            payment = await self.client.payments.retrieve(TestPayments.paymentId)

            assert payment is not None
            assert isinstance(payment, Payment)

            assert payment.id == TestPayments.paymentId

    async def test_payments_can_update(self) -> None:
        with my_vcr.use_cassette("payments/update.json"):
            payment = await self.client.payments.retrieve(TestPayments.paymentId)
            assert payment is not None

            payment.amount = "1200"

    async def test_payments_can_delete(self) -> None:
        with my_vcr.use_cassette("payments/delete.json"):
            payment = await self.client.payments.retrieve(TestPayments.paymentId)
            assert payment is not None

    async def test_payments_can_confirm(self) -> None:
        with my_vcr.use_cassette("payments/payments_confirmation.json"):
            payment = await self.client.payments.payment_confirmation(
                "a739b199-8260-4ffa-a404-b4b58345332e"
            )

            assert payment is not None
            assert payment.id is not None
            assert payment.payment_id == "a739b199-8260-4ffa-a404-b4b58345332e"
            assert payment.account_id is not None

    async def test_payments_can_authorise(self) -> None:
        with my_vcr.use_cassette("payments/authorise.json"):
            beneficiary = await self.client.beneficiaries.create(
                bank_account_holder_name="Test User",
                bank_country="GB",
                currency="GBP",
                name="Test User",
                account_number="12345678",
                routing_code_type_1="sort_code",
                routing_code_value_1="123456",
            )
            payment = await self.client.payments.create(
                currency="GBP",
                beneficiary_id=beneficiary.id,
                amount="1000",
                reason="Testing payments",
                reference="Testing payments",
                payment_type="regular",
            )
            self.client.config.login_id = "development2@currencycloud.demo"
            self.client.config.api_key = (
                "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
            )
            await self.client.config.reauthenticate()
            payment = await self.client.payments.authorise(
                payment_ids=[TestPayments.paymentId]
            )
            assert payment is not None
            self.client.config.login_id = "development@currencycloud.demo"
            self.client.config.api_key = (
                "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
            )
            await self.client.config.reauthenticate()

    async def test_payments_delivery_date(self) -> None:
        with my_vcr.use_cassette("payments/delivery_date.json"):
            payment = await self.client.payments.payment_delivery_date(
                payment_date="2018-01-01",
                payment_type="regular",
                currency="EUR",
                bank_country="IT",
            )

            assert payment is not None
            assert isinstance(payment, Payment)

    async def test_quote_payment_fee(self) -> None:
        with my_vcr.use_cassette("payments/quote_payment_fee.json"):
            quote_payment_fee = await self.client.payments.quote_payment_fee(
                payment_currency="USD",
                payment_destination_country="US",
                payment_type="regular",
            )

            assert quote_payment_fee is not None
            assert isinstance(quote_payment_fee, QuotePaymentFee)
            assert (
                quote_payment_fee.account_id == "0534aaf2-2egg-0134-2f36-10b11cd33cfb"
            )
            assert quote_payment_fee.fee_amount == "10.00"
            assert quote_payment_fee.fee_currency == "EUR"
            assert quote_payment_fee.payment_currency == "USD"
            assert quote_payment_fee.payment_destination_country == "US"
            assert quote_payment_fee.payment_type == "regular"
            assert quote_payment_fee.charge_type is None

    async def test_payments_delivery_date_error_response(self) -> None:
        with my_vcr.use_cassette("payments/delivery_date_error.json"):
            with pytest.raises(BadRequestError):
                await self.client.payments.payment_delivery_date(
                    payment_date="2020-08-02",
                    payment_type="priority",
                    currency="USD",
                    bank_country="CA",
                )

    async def test_payments_delivery_date_error_response2(self) -> None:
        with my_vcr.use_cassette("payments/delivery_date_error2.json"):
            with pytest.raises(BadRequestError):
                await self.client.payments.payment_delivery_date(
                    payment_date="2020-08-02",
                    payment_type="priority",
                    currency="USD",
                    bank_country="abc",
                )

    async def test_tracking_info(self) -> None:
        with my_vcr.use_cassette("payments/tracking_info.json"):
            tracking_info = await self.client.payments.tracking_info(
                "46ed4827-7b6f-4491-a06f-b548d5a7512d"
            )

            assert tracking_info is not None
            assert isinstance(tracking_info, PaymentTrackingInfo)
            assert tracking_info.uetr == "46ed4827-7b6f-4491-a06f-b548d5a7512d"
            assert tracking_info.transaction_status["status"] == "processing"
            assert len(tracking_info.payment_events) == 7
