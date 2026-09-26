"""Data collectors package for botyaradash."""

from collectors.cpu import CPUCollector
from collectors.memory import MemoryCollector
from collectors.disk import DiskCollector
from collectors.network import NetworkCollector
from collectors.gpu import GPUCollector
from collectors.battery import BatteryCollector
from collectors.process import ProcessCollector
from collectors.system import SystemCollector

__all__ = [
    "CPUCollector",
    "MemoryCollector",
    "DiskCollector",
    "NetworkCollector",
    "GPUCollector",
    "BatteryCollector",
    "ProcessCollector",
    "SystemCollector",
]
