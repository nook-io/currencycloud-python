from typing import Any

from currencycloud.http import Http
from currencycloud.resources import Sender


class Senders(Http):
    """This class provides an interface to the Senders endpoints of the CC API"""

    async def get_sender(self, resource_id: str, **kwargs: Any) -> Sender:
        """Get the details of a specific sender."""
        return Sender(**await self.get("/v2/transactions/sender/" + resource_id, kwargs))
