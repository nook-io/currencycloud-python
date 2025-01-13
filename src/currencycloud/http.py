"""This module provides a Mixin to generate http requests to the CC API endpoints"""

from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from httpx import Response
from httpx._types import HeaderTypes, QueryParamTypes, RequestData
from httpx._urls import URL

from currencycloud.errors import (
    ApiError,
    AuthenticationError,
    BadRequestError,
    ForbiddenError,
    InternalApplicationError,
    NotFoundError,
    TooManyRequestsError,
)

if TYPE_CHECKING:
    from currencycloud.config import Config


class Http:
    """
    Mixin for other Client classes. Provides abstract get/post methods that will add authentication
    headers when necessary and point to the appropriate host for the environment.
    """

    def __init__(self, config: "Config"):
        self.config = config
        self.session = self.config.session

    async def get(
        self, endpoint: str, query: dict[str, Any] | None = None, authenticated: bool = True, retry: bool = True
    ) -> dict[str, Any]:
        """Executes a GET request."""

        url = self.__build_url(endpoint)
        query = self.__encode_arrays(self.__handle_on_behalf_of(query))
        headers = await self.__build_headers(authenticated)

        async def execute_request(url: URL | str, headers: HeaderTypes, data: QueryParamTypes):
            return await self.session.get(url, headers=headers, params=data)

        response = await self.__handle_authentication_errors(execute_request, retry, url, headers, query, authenticated)

        return self.__handle_errors("get", url, query, response)

    async def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None,
        authenticated: bool = True,
        retry: bool = True,
        disable_on_behalf_of: bool = False,
    ) -> dict[str, Any]:
        """Executes a POST request."""

        url = self.__build_url(endpoint)
        if not disable_on_behalf_of:
            data = self.__handle_on_behalf_of(data)
        data = self.__encode_arrays(data)
        headers = await self.__build_headers(authenticated)

        async def execute_request(url: URL | str, headers: HeaderTypes, data: RequestData) -> Response:
            return await self.session.post(url, headers=headers, data=data)

        response = await self.__handle_authentication_errors(execute_request, retry, url, headers, data, authenticated)

        return self.__handle_errors("post", url, data, response)

    def __build_url(self, endpoint: str) -> str:
        return self.__environment_url() + endpoint

    def __environment_url(self) -> str:
        return self.config.environment_url()

    def __handle_on_behalf_of(self, data: dict[str, Any] | None):
        if self.config.on_behalf_of is not None:
            data = {} if data is None else data

            if "on_behalf_of" not in data:
                data["on_behalf_of"] = self.config.on_behalf_of

        return data

    def __encode_arrays(self, data: dict[str, Any] | None) -> dict[str, Any] | None:
        if data is not None:
            new_data = {}

            for k in data:
                if isinstance(data[k], list):
                    new_data[k + "[]"] = data[k]
                else:
                    new_data[k] = data[k]

            return new_data

    async def __build_headers(self, authenticated: bool) -> dict[str, str]:
        headers = {}

        if authenticated:
            headers["X-Auth-Token"] = await self.config.get_auth_token()

        return headers

    HTTP_CODE_TO_ERROR = {
        400: BadRequestError,
        401: AuthenticationError,
        403: ForbiddenError,
        404: NotFoundError,
        429: TooManyRequestsError,
        500: InternalApplicationError,
    }

    def __handle_errors(self, verb: str, url: str, params, response: Response) -> dict[str, Any]:
        if int(response.status_code / 100) == 2:
            return response.json()
        klass = Http.HTTP_CODE_TO_ERROR.get(response.status_code, ApiError)
        raise klass(verb, url, params, response)

    async def __handle_authentication_errors(
        self,
        execute_request: Callable[[URL | str, HeaderTypes, QueryParamTypes], Awaitable[Response]]
        | Callable[[URL | str, HeaderTypes, RequestData], Awaitable[Response]],
        retry: bool,
        url: str,
        headers: dict[str, str],
        data,
        authenticated: bool,
    ) -> Response:
        retry_count = 3 if retry else 1

        while retry_count:
            retry_count -= 1
            response = await execute_request(url, headers, data)

            if response.status_code != 401:
                return response

            if retry:
                await self.config.reauthenticate()
                headers = await self.__build_headers(authenticated)

        return response
