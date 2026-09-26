"""Memory data collector."""

from typing import Any

import psutil

from collectors.base import BaseCollector


def _bytes_to_gb(value: int) -> float:
    return round(value / (1024 ** 3), 2)


class MemoryCollector(BaseCollector):
    """Collects RAM and Swap usage."""

    @property
    def name(self) -> str:
        return "memory"

    def collect(self) -> dict[str, Any]:
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()

        data: dict[str, Any] = {
            "ram": {
                "total": ram.total,
                "used": ram.used,
                "available": ram.available,
                "percent": ram.percent,
                "total_gb": _bytes_to_gb(ram.total),
                "used_gb": _bytes_to_gb(ram.used),
                "available_gb": _bytes_to_gb(ram.available),
            },
            "swap": {
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent,
                "total_gb": _bytes_to_gb(swap.total),
                "used_gb": _bytes_to_gb(swap.used),
            },
        }

        # Add cached/buffers on Linux
        try:
            data["ram"]["cached_gb"] = _bytes_to_gb(getattr(ram, "cached", 0))
            data["ram"]["buffers_gb"] = _bytes_to_gb(getattr(ram, "buffers", 0))
        except Exception:
            pass

        return data
