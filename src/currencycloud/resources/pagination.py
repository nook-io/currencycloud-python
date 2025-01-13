from typing import Literal

from currencycloud.resources.resource import Resource


class Pagination(Resource):
    total_entries: int
    total_pages: int
    current_page: int
    per_page: int
    previous_page: int
    next_page: int
    order: str
    order_asc_desc: Literal["asc", "desc"]
