"""Network data collector."""

import socket
import time
from typing import Any, Optional

import psutil

from collectors.base import BaseCollector


class NetworkCollector(BaseCollector):
    """Collects network stats: per-interface traffic, IPs, speeds."""

    def __init__(self) -> None:
        self._prev_counters: Optional[dict] = None
        self._prev_time: Optional[float] = None

    @property
    def name(self) -> str:
        return "network"

    def _bytes_to_mb(self, value: float) -> float:
        return round(value / (1024 ** 2), 2)

    def _get_ip_addresses(self) -> dict[str, list[str]]:
        """Get IP addresses per interface."""
        result: dict[str, list[str]] = {}
        try:
            addrs = psutil.net_if_addrs()
            for iface, addr_list in addrs.items():
                ips = []
                for addr in addr_list:
                    if addr.family == socket.AF_INET:
                        ips.append(addr.address)
                if ips:
                    result[iface] = ips
        except Exception:
            pass
        return result

    def collect(self) -> dict[str, Any]:
        now = time.monotonic()
        per_nic = psutil.net_io_counters(pernic=True)
        total = psutil.net_io_counters()
        ip_addrs = self._get_ip_addresses()

        interfaces: list[dict[str, Any]] = []
        total_sent_speed = 0.0
        total_recv_speed = 0.0

        for iface, counters in per_nic.items():
            # Skip loopback
            if iface.startswith("lo") or iface == "lo0":
                continue

            sent_speed = 0.0
            recv_speed = 0.0

            if self._prev_counters and self._prev_time:
                dt = now - self._prev_time
                if dt > 0 and iface in self._prev_counters:
                    prev = self._prev_counters[iface]
                    sent_delta = counters.bytes_sent - prev.bytes_sent
                    recv_delta = counters.bytes_recv - prev.bytes_recv
                    sent_speed = max(0.0, sent_delta / dt / (1024 ** 2))
                    recv_speed = max(0.0, recv_delta / dt / (1024 ** 2))

            total_sent_speed += sent_speed
            total_recv_speed += recv_speed

            ips = ip_addrs.get(iface, [])

            interfaces.append({
                "name": iface,
                "sent_total_mb": self._bytes_to_mb(counters.bytes_sent),
                "recv_total_mb": self._bytes_to_mb(counters.bytes_recv),
                "sent_speed_mbs": round(sent_speed, 2),
                "recv_speed_mbs": round(recv_speed, 2),
                "packets_sent": counters.packets_sent,
                "packets_recv": counters.packets_recv,
                "errors_in": counters.errin,
                "errors_out": counters.errout,
                "ip_addresses": ips,
            })

        self._prev_counters = per_nic
        self._prev_time = now

        return {
            "interfaces": interfaces,
            "total": {
                "sent_total_mb": self._bytes_to_mb(total.bytes_sent) if total else 0,
                "recv_total_mb": self._bytes_to_mb(total.bytes_recv) if total else 0,
                "sent_speed_mbs": round(total_sent_speed, 2),
                "recv_speed_mbs": round(total_recv_speed, 2),
            },
        }
