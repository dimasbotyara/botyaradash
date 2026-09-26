import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional


def get_os_name() -> str:
    """Return normalized OS name."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    return system


def get_config_dir() -> Path:
    """Return platform-appropriate config directory."""
    system = get_os_name()

    if system == "windows":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "botyaradash"
        return Path.home() / "AppData" / "Roaming" / "botyaradash"

    if system == "macos":
        return Path.home() / "Library" / "Application Support" / "botyaradash"

    # Linux and others — follow XDG
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "botyaradash"
    return Path.home() / ".config" / "botyaradash"


def get_export_dir() -> Path:
    """Return default export directory."""
    system = get_os_name()

    if system == "windows":
        docs = Path.home() / "Documents"
    elif system == "macos":
        docs = Path.home() / "Documents"
    else:
        docs = Path.home()

    export_dir = docs / "botyaradash_exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    return export_dir


def get_disk_type(device: str) -> str:
    """Detect disk type: NVMe, SSD, HDD, or Unknown."""
    system = get_os_name()

    try:
        if system == "linux":
            return _get_disk_type_linux(device)
        if system == "macos":
            return _get_disk_type_macos(device)
        if system == "windows":
            return _get_disk_type_windows(device)
    except Exception:
        pass

    return "Unknown"


def _get_disk_type_linux(device: str) -> str:
    """Detect disk type on Linux."""
    dev_name = device.split("/")[-1]

    # Strip partition number: sda1 -> sda, nvme0n1p1 -> nvme0n1
    if "nvme" in dev_name:
        # nvme0n1p1 -> nvme0n1
        parts = dev_name.split("p")
        if len(parts) > 1 and parts[-1].isdigit():
            dev_name = "p".join(parts[:-1])
        return "NVMe"

    # Strip trailing digits for regular drives
    base_name = dev_name.rstrip("0123456789")

    rotational_path = Path(f"/sys/block/{base_name}/queue/rotational")
    if rotational_path.exists():
        val = rotational_path.read_text().strip()
        return "HDD" if val == "1" else "SSD"

    return "Unknown"


def _get_disk_type_macos(device: str) -> str:
    """Detect disk type on macOS."""
    try:
        result = subprocess.run(
            ["diskutil", "info", device],
            capture_output=True,
            text=True,
            timeout=5,
        )
        output = result.stdout.lower()
        if "solid state" in output:
            return "SSD"
        if "nvmexpress" in output or "nvme" in output:
            return "NVMe"
        if "rotational" in output or "mechanical" in output:
            return "HDD"
    except Exception:
        pass

    return "SSD"  # Most modern Macs use SSD


def _get_disk_type_windows(device: str) -> str:
    """Detect disk type on Windows."""
    try:
        # Use PowerShell to get media type
        drive_letter = device.rstrip("\\").rstrip(":")
        ps_cmd = (
            f"Get-PhysicalDisk | Get-Disk | Get-Partition | "
            f"Where-Object DriveLetter -eq '{drive_letter}' | "
            f"Get-Disk | Get-PhysicalDisk | "
            f"Select-Object -ExpandProperty MediaType"
        )

        # Simpler approach
        ps_cmd = "Get-PhysicalDisk | Select-Object DeviceId, MediaType | ConvertTo-Json"
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            output = result.stdout.lower()
            if "ssd" in output:
                return "SSD"
            if "hdd" in output:
                return "HDD"
            if "nvme" in output:
                return "NVMe"
    except Exception:
        pass

    return "Unknown"


def get_cpu_temp() -> Optional[float]:
    """Get CPU temperature in Celsius."""
    try:
        temps = __import__("psutil").sensors_temperatures()
        if not temps:
            return None

        # Try common sensor names
        for name in ("coretemp", "cpu_thermal", "k10temp", "zenpower", "acpitz"):
            if name in temps:
                readings = temps[name]
                if readings:
                    return readings[0].current

        # Fallback: first available sensor
        for entries in temps.values():
            if entries:
                return entries[0].current
    except (AttributeError, Exception):
        # sensors_temperatures() not available on all platforms
        pass

    return None


def get_cpu_freq_per_core() -> list[Optional[float]]:
    """Get per-core CPU frequency in MHz."""
    try:
        freqs = __import__("psutil").cpu_freq(percpu=True)
        if freqs:
            return [f.current for f in freqs]
    except Exception:
        pass

    return []


def get_system_info() -> dict:
    """Gather comprehensive system information."""
    uname = platform.uname()

    info = {
        "hostname": uname.node,
        "os": f"{uname.system} {uname.release}",
        "os_version": uname.version,
        "arch": uname.machine,
        "processor": uname.processor or platform.processor() or "Unknown",
        "python": platform.python_version(),
        "platform": get_os_name(),
    }

    # Try to get pretty OS name
    system = get_os_name()
    if system == "linux":
        try:
            import distro  # type: ignore
            info["os"] = f"{distro.name()} {distro.version()}"
        except ImportError:
            try:
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            info["os"] = line.split("=", 1)[1].strip().strip('"')
                            break
            except FileNotFoundError:
                pass
    elif system == "macos":
        try:
            ver = platform.mac_ver()[0]
            info["os"] = f"macOS {ver}"
        except Exception:
            pass

    return info


def supports_gpu() -> bool:
    """Check if GPU monitoring is available."""
    try:
        import GPUtil  # type: ignore
        gpus = GPUtil.getGPUs()
        return len(gpus) > 0
    except Exception:
        return False


def is_laptop() -> bool:
    """Heuristic to detect if running on a laptop."""
    try:
        battery = __import__("psutil").sensors_battery()
        return battery is not None
    except Exception:
        return False
