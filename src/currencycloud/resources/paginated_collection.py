"""This module the PaginatedCollection class"""

from typing import Any, Generic, TypeVar

from currencycloud.resources.pagination import Pagination

T = TypeVar("T")


class PaginatedCollection(Generic[T], list[T]):
    """Provides a wrapper around an array of Resources with additional pagination details"""

    def __init__(self, collection: list[T], pagination: dict[str, Any]):
        super(PaginatedCollection, self).__init__(collection)
        self.__pagination = Pagination(**pagination)

    @property
    def pagination(self) -> Pagination:
        """
        Provides the pagination informations for this response, like page number and results per
        page
        """
        return self.__pagination
