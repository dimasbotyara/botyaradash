"""Value history tracking for sparklines and graphs."""

from collections import deque
from typing import Optional


class ValueHistory:
    """Stores a rolling window of float values."""

    def __init__(self, max_length: int = 60) -> None:
        self._data: deque[float] = deque(maxlen=max_length)
        self._max_length = max_length

    def push(self, value: float) -> None:
        """Add a new value."""
        self._data.append(value)

    def values(self) -> list[float]:
        """Get all stored values."""
        return list(self._data)

    def last(self) -> Optional[float]:
        """Get the most recent value."""
        return self._data[-1] if self._data else None

    def average(self) -> float:
        """Get the average of stored values."""
        if not self._data:
            return 0.0
        return sum(self._data) / len(self._data)

    def peak(self) -> float:
        """Get the maximum value."""
        return max(self._data) if self._data else 0.0

    def minimum(self) -> float:
        """Get the minimum value."""
        return min(self._data) if self._data else 0.0

    def __len__(self) -> int:
        return len(self._data)

    def clear(self) -> None:
        """Clear all history."""
        self._data.clear()


class HistoryManager:
    """Manages multiple named value histories."""

    def __init__(self, max_length: int = 60) -> None:
        self._histories: dict[str, ValueHistory] = {}
        self._max_length = max_length

    def push(self, name: str, value: float) -> None:
        """Push a value to a named history, creating it if needed."""
        if name not in self._histories:
            self._histories[name] = ValueHistory(self._max_length)
        self._histories[name].push(value)

    def get(self, name: str) -> ValueHistory:
        """Get a named history."""
        if name not in self._histories:
            self._histories[name] = ValueHistory(self._max_length)
        return self._histories[name]

    def values(self, name: str) -> list[float]:
        """Get values for a named history."""
        return self.get(name).values()

    def last(self, name: str) -> Optional[float]:
        """Get last value for a named history."""
        return self.get(name).last()

    def keys(self) -> list[str]:
        """Get all history names."""
        return list(self._histories.keys())

    def clear_all(self) -> None:
        """Clear all histories."""
        self._histories.clear()

    def to_dict(self) -> dict[str, list[float]]:
        """Export all histories as a dictionary."""
        return {name: hist.values() for name, hist in self._histories.items()}
