import datetime
from json import JSONDecodeError

from httpx import Response

from currencycloud import Client, Config
from currencycloud.errors import (
    ApiError,
    AuthenticationError,
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    TooManyRequestsError,
)
from currencycloud.errors.api import REDACTED_STRING
from tests.integration.conftest import my_vcr


class TestError:
    def setup_method(self, method) -> None:
        # TODO: To run against real server please delete ../fixtures/vcr_cassettes/* and replace
        # login_id and api_key with valid credentials before running the tests
        login_id = "development@currencycloud.com"
        api_key = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        environment = Config.ENV_DEMO

        self.client = Client(login_id, api_key, environment)

    async def test_error_contains_full_details_for_api_error(self) -> None:
        login_id = "non-existent-login-id"
        api_key = "deadbeefdeadbeefdeadbeefdeadbeef"
        tmp_client = Client(login_id, api_key, Config.ENV_DEMO)

        with my_vcr.use_cassette("errors/contains_full_details_for_api_error.json"):
            error = None
            try:
                await tmp_client.auth.authenticate()
                raise Exception("Should have failed")
            except BadRequestError as e:
                error = e

        assert error is not None

        expected_error_fields = [
            "login_id: non-existent-login-id",
            "api_key: '" + REDACTED_STRING + "'",
            "verb: post",
            "url: https://devapi.currencycloud.com/v2/authenticate/api",
            "status_code: 400",
            "date:",
            "request_id:",
            "field: api_key",
            "code: api_key_length_is_invalid",
            "message: api_key should be 64 character(s) long",
            "length: 64",
        ]

        error_str = str(error)
        missing = False
        for f in expected_error_fields:
            if f not in error_str:
                missing = True
                break

        assert missing is False

    async def test_error_is_raised_on_incorrect_authentication_details(self) -> None:
        login_id = "non-existent-login-id"
        api_key = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"
        tmp_client = Client(login_id, api_key, Config.ENV_DEMO)

        with my_vcr.use_cassette("errors/is_raised_on_incorrect_authentication_details"):
            error = None
            try:
                await tmp_client.auth.authenticate()
                raise Exception("Should have failed")
            except AuthenticationError as e:
                error = e

            assert error.code == "auth_failed"
            assert error.raw_response is not None
            assert error.status_code == 401
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.field == "username"
            assert error_message.code == "invalid_supplied_credentials"
            assert error_message.message == "Authentication failed with the supplied credentials"
            assert not error_message.params

    async def test_error_is_raised_when_a_resource_is_not_found(self) -> None:
        with my_vcr.use_cassette("errors/is_raised_when_a_resource_is_not_found.json"):
            error = None
            try:
                await self.client.beneficiaries.retrieve("081596c9-02de-483e-9f2a-4cf55dcdf98c")
                raise Exception("Should have failed")
            except NotFoundError as e:
                error = e

            assert error.code == "beneficiary_not_found"
            assert error.raw_response is not None
            assert error.status_code == 404
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.field == "id"
            assert error_message.code == "beneficiary_not_found"
            assert error_message.message == "Beneficiary was not found for this id"
            assert not error_message.params

    async def test_error_is_raised_when_too_many_requests_have_been_issued(self) -> None:
        with my_vcr.use_cassette("errors/is_raised_when_too_many_requests_have_been_issued"):
            error = None
            try:
                await self.client.auth.authenticate()
                raise Exception("Should have failed")
            except TooManyRequestsError as e:
                error = e

            assert error.code == "too_many_requests"
            assert error.raw_response is not None
            assert error.status_code == 429
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.field == "base"
            assert error_message.code == "too_many_requests"
            assert (
                error_message.message
                == "Too many requests have been made to the api. Please refer to the Developer Center for more information"
            )
            assert not error_message.params

    async def test_error_is_raised_on_forbidden_request(self) -> None:
        with my_vcr.use_cassette("errors/is_raised_on_forbidden_request.json"):
            error = None
            try:
                await self.client.transfers.find()
                raise Exception("Should have failed")
            except ForbiddenError as e:
                error = e

            assert error.code == "permission_denied"
            assert error.raw_response is not None
            assert error.status_code == 403
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.code == "permission_denied"
            assert error_message.message == "You do not have permission 'transfer_read' to perform this operation"
            assert not error_message.params

    async def test_error_is_raised_on_missing_iban(self) -> None:
        with my_vcr.use_cassette("errors/is_raised_on_missing_iban.json"):
            error = None
            try:
                await self.client.reference.bank_details(identifier_type="iban", identifier_value="123abc456xyz")
                raise Exception("Should have failed")
            except BadRequestError as e:
                error = e

            assert error.code == "invalid_iban"
            assert error.raw_response is not None
            assert error.status_code == 400
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.code == "invalid_iban"
            assert error_message.message == "IBAN is invalid."
            assert not error_message.params

    async def test_error_is_handled_non_json_format(self) -> None:
        with my_vcr.use_cassette("errors/is_handled_invalid_error_format.json"):
            try:
                await self.client.beneficiaries.find()
                raise Exception("Should have failed")
            except JSONDecodeError:
                pass

    async def test_error_is_handled_different_json_format(self) -> None:
        with my_vcr.use_cassette("errors/is_handled_json_error_message_different_format"):
            error = None
            try:
                await self.client.beneficiaries.find()
                raise Exception("Should have failed")
            except ApiError as e:
                error = e

            assert error.code == "unknown"
            assert error.raw_response is not None
            assert error.status_code == 500
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.code == "unknown_error"
            assert error_message.message == "Unhandled Error occurred. Check params for details"
            assert error_message.params

    async def test_error_is_handled_different_json_format_2(self) -> None:
        with my_vcr.use_cassette("errors/is_handled_json_error_message_different_format_2"):
            error = None
            try:
                await self.client.beneficiaries.find()
                raise Exception("Should have failed")
            except ApiError as e:
                error = e

            assert error.code == "test_code"
            assert error.raw_response is not None
            assert error.status_code == 500
            assert len(error.messages) == 1

            error_message = error.messages[0]
            assert error_message.code == "unknown_error"
            assert error_message.message == "Unhandled Error occurred. Check params for details"
            assert error_message.params

    async def test_error_is_handled_missing_params_in_error_message(self) -> None:
        with my_vcr.use_cassette("errors/is_handled_missing_params_in_error_message.json"):
            error = None
            try:
                await self.client.auth.authenticate()
                raise Exception("Should have failed")
            except TooManyRequestsError as e:
                error = e

            assert len(error.messages) == 1
            error_message = error.messages[0]
            assert error_message.field == "base"
            assert error_message.code == "No Code"
            assert error_message.message == "No Message"
            assert not error_message.params

    def test_error_parameter_redaction(self) -> None:
        api_key = "IDoNotWantToSeeThis"
        login_id = "test@currencycloud.com"
        params = {"api_key": api_key, "login_id": login_id}
        url = "https://devapi.currencycloud.com/v2/authenticate/api"
        verb = "post"
        response = Response(status_code=401)
        response._content = b'{"error_code": "auth_failed","error_messages": {"username": [{"code": "invalid_supplied_credentials","message": "Authentication failed with the supplied credentials","params": {}}]}}'
        response.headers["Date"] = datetime.datetime(2023, 3, 20, 0, 0, tzinfo=datetime.UTC)
        response.headers["x-request-id"] = "06ac2168-8d8f-4a0c-8033-e81a22a2feb5"

        error = AuthenticationError(verb, url, params, response)
        s = str(error)
        assert api_key not in s
        assert REDACTED_STRING in s
