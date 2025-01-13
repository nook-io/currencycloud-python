"""This module provides the abstract Resource class"""

from collections.abc import Iterator
from typing import Any


class Resource:
    """
    An abstract CurrencyCloud resource. Maintains all the attributes and provides a common set of
    operations to all domain objects
    """

    def __init__(self, **data: Any) -> None:
        self._attributes = data
        self.__changed_attributes: set[str] = set()

    def __dir__(self) -> list[str]:
        return list(self._attributes.keys())

    def __len__(self) -> int:
        return len(self._attributes)

    def __iter__(self) -> Iterator[str]:
        return iter(self._attributes)

    def __contains__(self, name: str) -> bool:
        return name in self._attributes

    def __getitem__(self, name: str) -> Any:
        return self._attributes[name]

    def __setitem__(self, name: str, value: Any) -> None:
        self._attributes[name] = value
        self.__changed_attributes.add(name)

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_") or name not in self._attributes:
            return object.__getattribute__(self, name)
        return self.__getitem__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self.__setitem__(name, value)

    @property
    def changed_attributes(self) -> set[str]:
        """Provides the set of all attributes that have been changed since the retrieve"""
        return self.__changed_attributes

    @property
    def changed_items(self) -> dict[str, Any]:
        """Provides an hashmap of all attributes that have been changed since the retrieve"""
        items = {}
        for name in self.__changed_attributes:
            items[name] = self[name]

        return items
