"""This module provides a class for Withdrawal Accounts calls to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, WithdrawalAccount, WithdrawalAccountFunds


class WithdrawalAccounts(Http):
    """This class provides an interface to the Reference endpoints of the CC API"""

    async def find(self, **kwargs: Any) -> PaginatedCollection[WithdrawalAccount]:
        """Search for WithdrawalAccounts that meet a number of criteria and receive a paged response."""
        response = await self.get("/v2/withdrawal_accounts/find", query=kwargs)
        data = [WithdrawalAccount(**fields) for fields in response["withdrawal_accounts"]]
        return PaginatedCollection(data, response["pagination"])

    async def pull_funds(self, resource_id: str, **kwargs: Any) -> WithdrawalAccountFunds:
        """Submits an ACH pull request from a specific withdrawal account.
        The funds will be pulled into the account the specified withdrawal account is related to"""
        response = await self.post("/v2/withdrawal_accounts/" + resource_id + "/pull_funds", kwargs)
        return WithdrawalAccountFunds(**response)
