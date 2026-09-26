"""System information collector."""

import datetime
import time
from typing import Any

import psutil

from collectors.base import BaseCollector
from platform_utils import get_system_info


class SystemCollector(BaseCollector):
    """Collects static and dynamic system information."""

    def __init__(self) -> None:
        self._static_info = get_system_info()

    @property
    def name(self) -> str:
        return "system"

    def collect(self) -> dict[str, Any]:
        uptime_seconds = int(time.time() - psutil.boot_time())
        uptime = str(datetime.timedelta(seconds=uptime_seconds))

        return {
            **self._static_info,
            "uptime": uptime,
            "uptime_seconds": uptime_seconds,
            "boot_time": datetime.datetime.fromtimestamp(
                psutil.boot_time()
            ).isoformat(),
            "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
