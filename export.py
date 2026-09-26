"""Data export functionality for botyaradash."""

import csv
import json
import datetime
from pathlib import Path
from typing import Any, Optional

from platform_utils import get_export_dir


class Exporter:
    """Exports monitoring snapshots to JSON or CSV."""

    def __init__(self, export_dir: Optional[Path] = None, fmt: str = "json") -> None:
        self._export_dir = export_dir or get_export_dir()
        self._format = fmt
        self._export_dir.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, ext: str) -> Path:
        """Generate a timestamped filename."""
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return self._export_dir / f"botyaradash_{ts}.{ext}"

    def export_snapshot(self, data: dict[str, Any]) -> Path:
        """Export a single snapshot."""
        data["export_time"] = datetime.datetime.now().isoformat()

        if self._format == "csv":
            return self._export_csv(data)
        return self._export_json(data)

    def _export_json(self, data: dict[str, Any]) -> Path:
        """Export to JSON."""
        path = self._generate_filename("json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return path

    def _export_csv(self, data: dict[str, Any]) -> Path:
        """Export to CSV (flattened)."""
        flat = self._flatten(data)
        path = self._generate_filename("csv")

        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Key", "Value"])
            for key, value in sorted(flat.items()):
                writer.writerow([key, value])

        return path

    def _flatten(self, data: dict, prefix: str = "") -> dict[str, Any]:
        """Flatten nested dict for CSV export."""
        flat: dict[str, Any] = {}
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flat.update(self._flatten(value, full_key))
            elif isinstance(value, (list, tuple)):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flat.update(self._flatten(item, f"{full_key}[{i}]"))
                    else:
                        flat[f"{full_key}[{i}]"] = item
            else:
                flat[full_key] = value
        return flat

    def export_history(self, history_data: dict[str, list[float]]) -> Path:
        """Export history data."""
        data = {
            "type": "history",
            "data": history_data,
        }
        return self.export_snapshot(data)

    def set_format(self, fmt: str) -> None:
        """Set export format."""
        if fmt in ("json", "csv"):
            self._format = fmt
