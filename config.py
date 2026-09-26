"""Configuration management for botyaradash."""

import sys
from pathlib import Path
from typing import Any

try:
    import toml
except ImportError:
    toml = None  # type: ignore

from platform_utils import get_config_dir


# Default configuration
DEFAULTS: dict[str, Any] = {
    "theme": "default",
    "language": "en",
    "layout": "full",
    "refresh_rate": 2.0,
    "bar_width": 20,
    "warn_percent": 60,
    "crit_percent": 85,
    "alerts_enabled": True,
    "alert_cpu_threshold": 90,
    "alert_ram_threshold": 90,
    "alert_disk_threshold": 95,
    "alert_temp_threshold": 85,
    "export_format": "json",
    "export_interval": 60,
    "history_length": 60,
    "show_per_core_cpu": False,
    "show_gpu": True,
    "show_battery": True,
    "show_processes": True,
    "process_count": 8,
    "sparkline_width": 20,
}


class Config:
    """Application configuration with persistence."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = dict(DEFAULTS)
        self._config_path: Path = get_config_dir() / "config.toml"
        self._loaded = False

    @property
    def config_path(self) -> Path:
        return self._config_path

    def load(self) -> None:
        """Load config from file."""
        if not self._config_path.exists():
            self._loaded = True
            return

        if toml is None:
            self._loaded = True
            return

        try:
            with open(self._config_path, "r", encoding="utf-8") as f:
                data = toml.load(f)
            for key, value in data.items():
                if key in DEFAULTS:
                    self._data[key] = value
        except Exception as e:
            print(f"Warning: Could not load config: {e}", file=sys.stderr)

        self._loaded = True

    def save(self) -> None:
        """Save config to file."""
        if toml is None:
            return

        try:
            self._config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self._config_path, "w", encoding="utf-8") as f:
                toml.dump(self._data, f)
        except Exception as e:
            print(f"Warning: Could not save config: {e}", file=sys.stderr)

    def get(self, key: str) -> Any:
        """Get config value."""
        return self._data.get(key, DEFAULTS.get(key))

    def set(self, key: str, value: Any) -> None:
        """Set config value."""
        self._data[key] = value

    def update(self, data: dict[str, Any]) -> None:
        """Update multiple config values."""
        for key, value in data.items():
            if key in DEFAULTS and value is not None:
                self._data[key] = value

    def to_dict(self) -> dict[str, Any]:
        """Return config as dictionary."""
        return dict(self._data)

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"Config has no attribute '{name}'")

    def __repr__(self) -> str:
        return f"Config({self._data})"
