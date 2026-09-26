"""Process data collector."""

from typing import Any

import psutil

from collectors.base import BaseCollector


class ProcessCollector(BaseCollector):
    """Collects top processes by CPU and memory usage."""

    def __init__(self, count: int = 8) -> None:
        self._count = count

    @property
    def name(self) -> str:
        return "process"

    def collect(self) -> dict[str, Any]:
        processes: list[dict[str, Any]] = []

        try:
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent", "status"]
            ):
                try:
                    info = proc.info
                    if info and info.get("pid") and info.get("pid") != 0:
                        processes.append({
                            "pid": info["pid"],
                            "name": info.get("name", "?")[:30],
                            "cpu_percent": round(info.get("cpu_percent", 0) or 0, 1),
                            "memory_percent": round(
                                info.get("memory_percent", 0) or 0, 1
                            ),
                            "status": info.get("status", "?"),
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception:
            pass

        # Sort by CPU usage descending
        processes.sort(key=lambda p: p["cpu_percent"], reverse=True)
        top_cpu = processes[: self._count]

        # Sort by memory usage descending for a separate list
        processes.sort(key=lambda p: p["memory_percent"], reverse=True)
        top_mem = processes[: self._count]

        return {
            "top_cpu": top_cpu,
            "top_mem": top_mem,
            "total_count": len(processes),
        }
