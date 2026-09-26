"""Base collector class."""

from abc import ABC, abstractmethod
from typing import Any


class BaseCollector(ABC):
    """Abstract base class for all data collectors."""

    @abstractmethod
    def collect(self) -> dict[str, Any]:
        """Collect and return data as a dictionary."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Collector name for identification."""
        ...
