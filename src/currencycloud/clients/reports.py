"""This module provides a class for Report Creating for Conversions to the CC API"""

from typing import Any

from currencycloud.http import Http
from currencycloud.resources import PaginatedCollection, Report


class Reports(Http):
    async def create_report_for_conversions(self, **kwargs: Any) -> Report:
        """
        Creates a new conversion report and returns a hash containing the details of the new conversion report.
        """
        return Report(**await self.post("/v2/reports/conversions/create", kwargs))

    async def find(self, **kwargs: Any) -> PaginatedCollection[Report]:
        """
        Return an array containing json structures of details of the reports matching the search
        criteria for the logged in user.
        """
        response = await self.get("/v2/reports/report_requests/find", query=kwargs)
        data = [Report(**fields) for fields in response["report_requests"]]
        return PaginatedCollection(data, response["pagination"])

    async def create_report_for_payments(self, **kwargs: Any) -> Report:
        """
        Creates a new payment report and returns a hash containing the details of the new payment report.
        """
        return Report(**await self.post("/v2/reports/payments/create", kwargs))

    async def find_via_id(self, resource_id: str, **kwargs: Any) -> Report:
        """
        Returns a json structure containing the details of the requested report.
        """
        return Report(
            **await self.get("/v2/reports/report_requests/" + resource_id, query=kwargs)
        )
