
from typing import Any

from currencycloud.http import Http
from currencycloud.resources.demo import SimulateFunding


class Demo(Http):
    """This class provides an interface to the Demo endpoints of the CC API"""

    async def create_funding_for_demo(self, **kwargs: Any) -> SimulateFunding:
        """
        Triggers a production-like flow for processing funds, topping up CM balance or rejecting the
        transaction without topping up CM balance. This resource is only available in the
        Currencycloud Demo environment; it is not implemented in the Production environment.
        """
        return SimulateFunding(**await self.post("/v2/demo/funding/create", kwargs))