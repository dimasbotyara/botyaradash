"""CPU data collector."""

from typing import Any, Optional

import psutil

from collectors.base import BaseCollector
from platform_utils import get_cpu_temp, get_cpu_freq_per_core


class CPUCollector(BaseCollector):
    """Collects CPU usage, frequency, temperature, and per-core data."""

    def __init__(self) -> None:
        # Warm up psutil CPU measurement
        psutil.cpu_percent(interval=None)
        psutil.cpu_percent(interval=None, percpu=True)

    @property
    def name(self) -> str:
        return "cpu"

    def collect(self) -> dict[str, Any]:
        overall = psutil.cpu_percent(interval=None)
        per_core = psutil.cpu_percent(interval=None, percpu=True)

        freq = psutil.cpu_freq()
        freq_current: Optional[float] = None
        freq_max: Optional[float] = None

        if freq:
            freq_current = round(freq.current, 0)
            freq_max = round(freq.max, 0) if freq.max else None

        per_core_freq = get_cpu_freq_per_core()
        temp = get_cpu_temp()

        logical_cores = psutil.cpu_count(logical=True) or 0
        physical_cores = psutil.cpu_count(logical=False) or 0

        return {
            "percent": overall,
            "per_core": per_core,
            "freq_current": freq_current,
            "freq_max": freq_max,
            "per_core_freq": per_core_freq,
            "temperature": temp,
            "logical_cores": logical_cores,
            "physical_cores": physical_cores,
        }
