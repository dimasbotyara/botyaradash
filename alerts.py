"""Alert system for botyaradash."""

import time
from dataclasses import dataclass, field
from typing import Optional

from config import Config
from i18n import t


@dataclass
class Alert:
    """Single alert entry."""

    message: str
    level: str  # "warn", "crit"
    timestamp: float = field(default_factory=time.time)
    source: str = ""


class AlertManager:
    """Manages system alerts based on thresholds."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._active_alerts: list[Alert] = []
        self._history: list[Alert] = []
        self._max_history = 100
        self._enabled = config.get("alerts_enabled")
        self._cooldowns: dict[str, float] = {}
        self._cooldown_seconds = 10.0

    @property
    def enabled(self) -> bool:
        return self._enabled

    def toggle(self) -> bool:
        """Toggle alerts on/off. Returns new state."""
        self._enabled = not self._enabled
        return self._enabled

    def check_all(self, snapshot: dict) -> list[Alert]:
        """Check all thresholds and return active alerts."""
        self._active_alerts.clear()

        if not self._enabled:
            return []

        self._check_cpu(snapshot.get("cpu_percent", 0))
        self._check_ram(snapshot.get("ram_percent", 0))
        self._check_disks(snapshot.get("disks", []))
        self._check_temp(snapshot.get("cpu_temp"))

        return list(self._active_alerts)

    def _should_alert(self, source: str) -> bool:
        """Check cooldown for an alert source."""
        now = time.time()
        last = self._cooldowns.get(source, 0)
        if now - last < self._cooldown_seconds:
            return False
        self._cooldowns[source] = now
        return True

    def _add_alert(self, message: str, level: str, source: str) -> None:
        """Add an alert."""
        if not self._should_alert(source):
            # Still show as active, just don't re-add to history
            self._active_alerts.append(Alert(message=message, level=level, source=source))
            return

        alert = Alert(message=message, level=level, source=source)
        self._active_alerts.append(alert)
        self._history.append(alert)

        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

    def _check_cpu(self, percent: float) -> None:
        threshold = self._config.get("alert_cpu_threshold")
        if percent >= threshold:
            level = "crit" if percent >= 95 else "warn"
            self._add_alert(
                t("alert_cpu_high", v=int(percent)),
                level,
                "cpu",
            )

    def _check_ram(self, percent: float) -> None:
        threshold = self._config.get("alert_ram_threshold")
        if percent >= threshold:
            level = "crit" if percent >= 95 else "warn"
            self._add_alert(
                t("alert_ram_high", v=int(percent)),
                level,
                "ram",
            )

    def _check_disks(self, disks: list[dict]) -> None:
        threshold = self._config.get("alert_disk_threshold")
        for disk in disks:
            percent = disk.get("percent", 0)
            name = disk.get("mountpoint", "?")
            if percent >= threshold:
                level = "crit" if percent >= 98 else "warn"
                self._add_alert(
                    t("alert_disk_high", name=name, v=int(percent)),
                    level,
                    f"disk_{name}",
                )

    def _check_temp(self, temp: Optional[float]) -> None:
        if temp is None:
            return
        threshold = self._config.get("alert_temp_threshold")
        if temp >= threshold:
            level = "crit" if temp >= 95 else "warn"
            self._add_alert(
                t("alert_temp_high", v=int(temp)),
                level,
                "temp",
            )

    def get_active(self) -> list[Alert]:
        """Get currently active alerts."""
        return list(self._active_alerts)

    def get_history(self) -> list[Alert]:
        """Get alert history."""
        return list(self._history)

    def clear_history(self) -> None:
        """Clear alert history."""
        self._history.clear()
