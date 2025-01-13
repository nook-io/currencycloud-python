"""All the CurrencyCloud API clients that provide interface for specific parts of the API"""

from currencycloud.clients.accounts import Accounts as Accounts
from currencycloud.clients.auth import Auth as Auth
from currencycloud.clients.balances import Balances as Balances
from currencycloud.clients.beneficiaries import Beneficiaries as Beneficiaries
from currencycloud.clients.contacts import Contacts as Contacts
from currencycloud.clients.conversions import Conversions as Conversions
from currencycloud.clients.funding import Funding as Funding
from currencycloud.clients.ibans import Ibans as Ibans
from currencycloud.clients.payers import Payers as Payers
from currencycloud.clients.payments import Payments as Payments
from currencycloud.clients.rates import Rates as Rates
from currencycloud.clients.reference import Reference as Reference
from currencycloud.clients.reports import Reports as Reports
from currencycloud.clients.senders import Senders as Senders
from currencycloud.clients.transactions import Transactions as Transactions
from currencycloud.clients.transfers import Transfers as Transfers
from currencycloud.clients.vans import Vans as Vans
from currencycloud.clients.withdrawal_accounts import (
    WithdrawalAccounts as WithdrawalAccounts,
)
