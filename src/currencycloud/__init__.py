"""
This is the official Python SDK for v2 of Currency Cloud's API. Additional documentation for each
API endpoint can be found at https://www.currencycloud.com/developers/overview. If you have any queries or you require
support, please contact our Support team at support@currencycloud.com.
"""

from currencycloud.client import Client as Client
from currencycloud.config import Config as Config
from currencycloud.version import VERSION

__title__ = "currencycloud"
__version__ = VERSION
__license__ = "MIT"
__copyright__ = "Copyright 2015-2019 Currencycloud"

import yaml
from decimal import Decimal
from currencycloud.errors.api import ApiError

yaml.representer.SafeRepresenter.add_representer(
    ApiError,
    lambda dumper, data: dumper.represent_scalar(
        f"!{data.__class__.__name__}", "\n".join([m.message for m in data.messages])
    ),
)
yaml.representer.SafeRepresenter.add_representer(
    Decimal, lambda dumper, data: dumper.represent_scalar("!decimal", str(data))
)