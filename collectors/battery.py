"""Battery data collector."""

from typing import Any

import psutil

from collectors.base import BaseCollector


class BatteryCollector(BaseCollector):
    """Collects battery information."""

    @property
    def name(self) -> str:
        return "battery"

    @property
    def available(self) -> bool:
        try:
            b = psutil.sensors_battery()
            return b is not None
        except Exception:
            return False

    def collect(self) -> dict[str, Any]:
        try:
            battery = psutil.sensors_battery()
        except Exception:
            battery = None

        if battery is None:
            return {"available": False}

        # Calculate time left
        time_left = None
        if battery.secsleft > 0:
            hours = battery.secsleft // 3600
            minutes = (battery.secsleft % 3600) // 60
            time_left = f"{hours}h {minutes}m"
        elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            time_left = "∞"
        elif battery.secsleft == psutil.POWER_TIME_UNKNOWN:
            time_left = "?"

        if battery.power_plugged:
            status = "charging" if battery.percent < 100 else "full"
        else:
            status = "discharging"

        return {
            "available": True,
            "percent": battery.percent,
            "plugged": battery.power_plugged,
            "status": status,
            "time_left": time_left,
            "seconds_left": battery.secsleft if battery.secsleft > 0 else None,
        }
