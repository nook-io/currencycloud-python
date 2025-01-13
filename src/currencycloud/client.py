"""This module provides a Client interface to the CC APIs"""

from collections.abc import Awaitable, Callable, Generator
from contextlib import contextmanager
from typing import Literal

import httpx

from currencycloud.clients import (
    Accounts,
    Auth,
    Balances,
    Beneficiaries,
    Contacts,
    Conversions,
    Funding,
    Ibans,
    Payers,
    Payments,
    Rates,
    Reference,
    Reports,
    Senders,
    Transactions,
    Transfers,
    Vans,
    WithdrawalAccounts,
)
from currencycloud.config import Config
from currencycloud.http import Http


class Client(Http):
    """The Client interfacing to the CC APIs"""

    _auth_client = None
    _accounts_client = None
    _balances_client = None
    _beneficiaries_client = None
    _contacts_client = None
    _conversions_client = None
    _funding_client = None
    _ibans_client = None
    _payers_client = None
    _payments_client = None
    _rates_client = None
    _reference_client = None
    _settlements_client = None
    _transactions_client = None
    _transfers_client = None
    _vans_client = None
    _report_client = None
    _sender_client = None
    _withdrawal_accounts_client = None

    def __init__(
        self,
        login_id: str,
        api_key: str,
        environment: Literal["demo", "prod"] = Config.ENV_DEMO,
        token_getter: Callable[[], Awaitable[str]] | None = None,
        client: httpx.AsyncClient | None = None,
    ):
        config = Config(login_id, api_key, environment, token_getter=token_getter, client=client)
        super().__init__(config)

    @classmethod
    def with_config(cls, config):
        """Instantiate a new Client using a config instance"""
        return cls(config.login_id, config.api_key, config.environment)

    async def authenticate(self) -> None:
        """Generate an auth token and store it in the config."""
        await self.config.get_auth_token()

    async def close_session(self):
        """Terminate the Auth Token validity"""
        await self.auth.close_session()
        self.config.auth_token = None
        return True

    @contextmanager
    def on_behalf_of(self, uuid) -> Generator["Client", None, None]:
        """Yields a new client object with an on_behalf_of setting."""

        # Use a new client, without changing the `self` configuration to stay thread-safe.

        clone = Client.with_config(self.config)
        clone.config.auth_token = self.config.auth_token
        clone.config.on_behalf_of = uuid

        yield clone

    @contextmanager
    def as_house_account(self) -> Generator["Client", None, None]:
        """Yields a new client object without an on_behalf_of setting."""

        # Use a new client, without changing the `self` configuration to stay thread-safe.

        clone = self.with_config(self.config)
        clone.config.auth_token = self.config.auth_token
        clone.config.on_behalf_of = None
        yield clone

    @property
    def auth(self):
        """Get the Authentication client."""
        if self._auth_client is None:
            self._auth_client = Auth(self.config)
        return self._auth_client

    @property
    def accounts(self) -> Accounts:
        """Get the Accounts client."""
        if self._accounts_client is None:
            self._accounts_client = Accounts(self.config)
        return self._accounts_client

    @property
    def balances(self) -> Balances:
        """Get the Balances client."""
        if self._balances_client is None:
            self._balances_client = Balances(self.config)
        return self._balances_client

    @property
    def beneficiaries(self) -> Beneficiaries:
        """Get the Beneficiaries client."""
        if self._beneficiaries_client is None:
            self._beneficiaries_client = Beneficiaries(self.config)
        return self._beneficiaries_client

    @property
    def contacts(self) -> Contacts:
        """Get the Contacts client."""
        if self._contacts_client is None:
            self._contacts_client = Contacts(self.config)
        return self._contacts_client

    @property
    def conversions(self) -> Conversions:
        """Get the Conversions client."""
        if self._conversions_client is None:
            self._conversions_client = Conversions(self.config)
        return self._conversions_client

    @property
    def funding(self) -> Funding:
        """Get the Funding client."""
        if self._funding_client is None:
            self._funding_client = Funding(self.config)
        return self._funding_client

    @property
    def ibans(self) -> Ibans:
        """Get the IBANs client."""
        if self._ibans_client is None:
            self._ibans_client = Ibans(self.config)
        return self._ibans_client

    @property
    def payers(self):
        """Get the Payers client."""
        if self._payers_client is None:
            self._payers_client = Payers(self.config)
        return self._payers_client

    @property
    def payments(self) -> Payments:
        """Get the Payments client."""
        if self._payments_client is None:
            self._payments_client = Payments(self.config)
        return self._payments_client

    @property
    def rates(self):
        """Get the Rates client."""
        if self._rates_client is None:
            self._rates_client = Rates(self.config)
        return self._rates_client

    @property
    def reference(self):
        """Get the Reference client."""
        if self._reference_client is None:
            self._reference_client = Reference(self.config)
        return self._reference_client

    @property
    def transactions(self) -> Transactions:
        """Get the Transactions client."""
        if self._transactions_client is None:
            self._transactions_client = Transactions(self.config)
        return self._transactions_client

    @property
    def transfers(self) -> Transfers:
        """Get the Transfers client."""
        if self._transfers_client is None:
            self._transfers_client = Transfers(self.config)
        return self._transfers_client

    @property
    def vans(self) -> Vans:
        """Get the VANs client."""
        if self._vans_client is None:
            self._vans_client = Vans(self.config)
        return self._vans_client

    @property
    def report(self) -> Reports:
        """Get the Reports client."""
        if self._report_client is None:
            self._report_client = Reports(self.config)
        return self._report_client

    @property
    def senders(self) -> Senders:
        """Get the Senders client."""
        if self._sender_client is None:
            self._sender_client = Senders(self.config)
        return self._sender_client

    @property
    def withdrawal_accounts(self) -> WithdrawalAccounts:
        """Get the WithdrawalAccounts client."""
        if self._withdrawal_accounts_client is None:
            self._withdrawal_accounts_client = WithdrawalAccounts(self.config)
        return self._withdrawal_accounts_client
