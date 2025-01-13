from currencycloud import Client, Config
from currencycloud.resources import Conversion

from tests.integration.conftest import my_vcr


class TestConversions:
    def setup_method(self, method) -> None:
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = "development@currencycloud.com"
        api_key = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    async def test_conversions_can_create(self) -> None:
        with my_vcr.use_cassette("conversions/create.json"):
            conversion = await self.client.conversions.create(
                buy_currency="EUR",
                sell_currency="GBP",
                fixed_side="buy",
                amount="1000",
                term_agreement="true",
            )

            assert conversion is not None
            assert isinstance(conversion, Conversion)

            assert conversion.id is not None
            assert conversion.client_buy_amount == "1000.00"

    async def test_actions_can_find(self) -> None:
        with my_vcr.use_cassette("conversions/find.json"):
            conversions = await self.client.conversions.find(per_page=1)

            assert conversions
            assert len(conversions) == 1

            conversion = conversions[0]

            assert conversion is not None
            assert isinstance(conversion, Conversion)

            assert conversion.client_buy_amount == "1000.00"

    async def test_actions_can_retrieve(self) -> None:
        with my_vcr.use_cassette("conversions/retrieve.json"):
            conversion = await self.client.conversions.retrieve(
                "a26ffc86-c0f6-45d8-8c1c-6a3e579ce974"
            )

            assert conversion is not None
            assert isinstance(conversion, Conversion)

            assert conversion.id == "a26ffc86-c0f6-45d8-8c1c-6a3e579ce974"
            assert conversion.client_buy_amount == "1000.00"

    async def test_actions_can_cancel(self) -> None:
        with my_vcr.use_cassette("conversions/cancel.json"):
            response = await self.client.conversions.cancel(
                "84033366-2135-4fc9-8016-41a7adba463e"
            )

            assert response is not None
            assert response.conversion_id == "84033366-2135-4fc9-8016-41a7adba463e"

    async def test_actions_can_date_change(self) -> None:
        with my_vcr.use_cassette("conversions/date_change.json"):
            response = await self.client.conversions.date_change(
                "d3c7d733-7c2f-443d-a082-4c728157b99f",
                new_settlement_date="2019-04-02T13:00:00+00:00",
            )

            assert response is not None
            assert response.conversion_id == "d3c7d733-7c2f-443d-a082-4c728157b99f"
            assert response.new_settlement_date == "2019-04-02T13:00:00+00:00"

    async def test_actions_can_split(self) -> None:
        with my_vcr.use_cassette("conversions/split.json"):
            response = await self.client.conversions.split(
                "d3c7d733-7c2f-443d-a082-4c728157b99f", amount="100"
            )

            assert response is not None
            assert (
                response.parent_conversion.get("id")
                == "d3c7d733-7c2f-443d-a082-4c728157b99f"
            )
            assert response.child_conversion.get("id") is not None

    async def test_actions_can_split_preview(self) -> None:
        with my_vcr.use_cassette("conversions/split_preview.json"):
            response = await self.client.conversions.split_preview(
                "c805aa35-9bd3-4afe-ade2-d341e551aa16", amount="100"
            )

            assert response is not None
            assert (
                response.parent_conversion.get("id")
                == "c805aa35-9bd3-4afe-ade2-d341e551aa16"
            )
            assert response.child_conversion.get("sell_amount") == "100.00"

    async def test_actions_can_split_history(self) -> None:
        with my_vcr.use_cassette("conversions/split_history.json"):
            response = await self.client.conversions.split_history(
                "c805aa35-9bd3-4afe-ade2-d341e551aa16"
            )

            assert response is not None
            for element in response.child_conversions:
                assert element.get("id") is not None
                assert element.get("sell_amount") == "100.00"
                assert element.get("short_reference") is not None

    async def test_actions_can_quote_date_change(self) -> None:
        with my_vcr.use_cassette("conversions/quote_date_change.json"):
            response = await self.client.conversions.date_change_quote(
                "2b436517-619b-4abe-a591-821dd31b264f",
                new_settlement_date="2018-10-29T16:30:00+00:00",
            )
            assert response is not None
            assert response.conversion_id == "2b436517-619b-4abe-a591-821dd31b264f"
            assert response.new_settlement_date == "2018-10-29T16:30:00+00:00"

    async def test_actions_can_quote_cancellation(self) -> None:
        with my_vcr.use_cassette("conversions/cancellation_quote.json"):
            response = await self.client.conversions.cancellation_quote(
                "63298593-bd8d-455d-8ee8-2f85dd390f2f"
            )

            assert response is not None
            assert response.amount is not None
            assert response.currency is not None
            assert response.event_date_time is not None

    async def test_action_can_retrieve_profit_and_loss(self) -> None:
        with my_vcr.use_cassette("conversions/profit_and_loss.json"):
            response = await self.client.conversions.profit_and_loss()

            assert response is not None
            for element in response:
                assert element.account_id is not None
                assert element.contact_id is not None
                assert element.conversion_id is not None
                assert element.event_type is not None
                assert element.amount is not None
                assert element.currency is not None
                assert element.event_date_time is not None
