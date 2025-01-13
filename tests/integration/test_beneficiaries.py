import pytest

from currencycloud import Client, Config
from currencycloud.errors import BadRequestError
from currencycloud.resources import Beneficiary
from tests.integration.conftest import my_vcr


class TestBeneficiaries:
    def setup_method(self, method) -> None:
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = "development@currencycloud.com"
        api_key = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    async def test_beneficiaries_can_create(self) -> None:
        with my_vcr.use_cassette("beneficiaries/create.json"):
            beneficiary = await self.client.beneficiaries.create(
                bank_account_holder_name="Test User",
                bank_country="GB",
                currency="GBP",
                name="Test User",
                account_number="12345678",
                routing_code_type_1="sort_code",
                routing_code_value_1="123456",
            )

            assert beneficiary is not None
            assert isinstance(beneficiary, Beneficiary)

            assert beneficiary.id is not None
            assert beneficiary.bank_country == "GB"

    async def test_beneficiaries_can_find(self) -> None:
        with my_vcr.use_cassette("beneficiaries/find.json"):
            beneficiaries = await self.client.beneficiaries.find(account_number="12345678", per_page=1)

            assert beneficiaries
            assert len(beneficiaries) == 1

            beneficiary = beneficiaries[0]

            assert beneficiary is not None
            assert isinstance(beneficiary, Beneficiary)

            assert beneficiary.account_number == "12345678"

    async def test_beneficiaries_can_retrieve(self) -> None:
        with my_vcr.use_cassette("beneficiaries/retrieve.json"):
            beneficiary = await self.client.beneficiaries.retrieve("a0bd2d78-3621-4c29-932f-a39d6b34d5e7")

            assert beneficiary is not None
            assert isinstance(beneficiary, Beneficiary)

            assert beneficiary.id == "a0bd2d78-3621-4c29-932f-a39d6b34d5e7"

    async def test_beneficiaries_can_update(self) -> None:
        with my_vcr.use_cassette("beneficiaries/update.json"):
            beneficiary = await self.client.beneficiaries.retrieve("a0bd2d78-3621-4c29-932f-a39d6b34d5e7")
            assert beneficiary is not None
            beneficiary.account_number = "87654321"

    async def test_beneficiaries_can_validate(self):
        with my_vcr.use_cassette("beneficiaries/validate.json"):
            beneficiary = await self.client.beneficiaries.validate(
                bank_country="GB",
                currency="GBP",
                beneficiary_country="GB",
                account_number="12345678",
                routing_code_type_1="sort_code",
                routing_code_value_1="123456",
            )

            assert beneficiary is not None
            assert isinstance(beneficiary, Beneficiary)

            assert beneficiary.bank_country == "GB"

    async def test_beneficiaries_validate_raises_on_missing_details(self) -> None:
        with my_vcr.use_cassette("beneficiaries/validate_error.json"):
            with pytest.raises(BadRequestError):
                await self.client.beneficiaries.validate(bank_country="GB", currency="GBP", beneficiary_country="GB")
                raise Exception("Should raise exception")
