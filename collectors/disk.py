"""Disk data collector."""

import time
from typing import Any, Optional

import psutil

from collectors.base import BaseCollector
from platform_utils import get_disk_type, get_os_name


class DiskCollector(BaseCollector):
    """Collects disk usage, type detection, and I/O stats."""

    def __init__(self) -> None:
        self._prev_io: Optional[Any] = None
        self._prev_time: Optional[float] = None

    @property
    def name(self) -> str:
        return "disk"

    def _bytes_to_gb(self, value: int) -> float:
        return round(value / (1024 ** 3), 2)

    def _bytes_to_mb(self, value: float) -> float:
        return round(value / (1024 ** 2), 2)

    def _get_io_speeds(self) -> tuple[float, float]:
        """Calculate disk I/O speeds in MB/s."""
        try:
            io = psutil.disk_io_counters()
        except Exception:
            return 0.0, 0.0

        if io is None:
            return 0.0, 0.0

        now = time.monotonic()
        read_speed = 0.0
        write_speed = 0.0

        if self._prev_io is not None and self._prev_time is not None:
            dt = now - self._prev_time
            if dt > 0:
                read_delta = io.read_bytes - self._prev_io.read_bytes
                write_delta = io.write_bytes - self._prev_io.write_bytes
                read_speed = max(0.0, self._bytes_to_mb(read_delta / dt))
                write_speed = max(0.0, self._bytes_to_mb(write_delta / dt))

        self._prev_io = io
        self._prev_time = now

        return read_speed, write_speed

    def collect(self) -> dict[str, Any]:
        partitions = psutil.disk_partitions(all=False)
        disks: list[dict[str, Any]] = []

        for part in partitions:
            # Skip special filesystems
            if get_os_name() == "linux" and part.fstype in (
                "squashfs", "tmpfs", "devtmpfs", "overlay"
            ):
                continue

            try:
                usage = psutil.disk_usage(part.mountpoint)
            except (PermissionError, OSError):
                continue

            disk_type = get_disk_type(part.device)

            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "disk_type": disk_type,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
                "total_gb": self._bytes_to_gb(usage.total),
                "used_gb": self._bytes_to_gb(usage.used),
                "free_gb": self._bytes_to_gb(usage.free),
            })

        read_speed, write_speed = self._get_io_speeds()

        return {
            "disks": disks,
            "io": {
                "read_mb_s": read_speed,
                "write_mb_s": write_speed,
            },
        }
