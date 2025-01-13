from currencycloud import Client, Config
from tests.integration.conftest import my_vcr


class TestAuthentication:
    def setup_method(self, method) -> None:
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = "development@currencycloud.com"
        api_key = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    def test_authentication_happens_lazily(self) -> None:
        with my_vcr.use_cassette("authentication/happens_lazily.json"):
            assert self.client.config.auth_token is None
            assert self.client.config.auth_token is not None

    async def test_authentication_can_reuse_an_auth_token(self) -> None:
        special_client = Client("dummy", "dummy", Config.ENV_DEMO)
        special_client.config.auth_token = "deadbeefdeadbeefdeadbeefdeadbeef"

        with my_vcr.use_cassette("authentication/can_use_just_a_token.json"):
            response = await special_client.beneficiaries.find()
            assert response is not None

    async def test_authentication_can_be_closed(self) -> None:
        with my_vcr.use_cassette("authentication/can_be_closed.json"):
            assert self.client.config.auth_token is not None
            assert await self.client.close_session() is True
            assert self.client.config.auth_token is None

    async def test_authentication_handles_session_timeout(self) -> None:
        # Set the token to an invalid one
        self.client.config.auth_token = "deadbeefdeadbeefdeadbeefdeadbeef"

        with my_vcr.use_cassette("authentication/handles_session_timeout", match_requests_on=["uri", "method"]):
            response = await self.client.beneficiaries.find()

            assert response is not None
