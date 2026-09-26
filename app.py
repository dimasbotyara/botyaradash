"""Main application class for botyaradash."""

import sys
import time
from typing import Any, Callable, Optional

from rich.console import Console
from rich.live import Live

from alerts import AlertManager
from config import Config
from export import Exporter
from history import HistoryManager
from hotkeys import HotkeyManager
from i18n import set_language, next_language, get_language, t
from ui.dashboard import DashboardRenderer
from ui.themes import next_theme, prev_theme
from ui.layouts import next_layout

from collectors import (
    CPUCollector,
    MemoryCollector,
    DiskCollector,
    NetworkCollector,
    GPUCollector,
    BatteryCollector,
    ProcessCollector,
    SystemCollector,
)


class App:
    """Main application orchestrator."""

    def __init__(
        self,
        overrides: Optional[dict[str, Any]] = None,
        save_on_exit: bool = False,
    ) -> None:
        self._console = Console()
        self._running = False
        self._save_on_exit = save_on_exit

        # Config
        self._config = Config()
        self._config.load()
        if overrides:
            self._config.update(overrides)

        # Language
        set_language(self._config.get("language"))

        # History
        self._history = HistoryManager(
            max_length=self._config.get("history_length")
        )

        # Collectors
        self._cpu = CPUCollector()
        self._memory = MemoryCollector()
        self._disk = DiskCollector()
        self._network = NetworkCollector()
        self._process = ProcessCollector(
            count=self._config.get("process_count")
        )
        self._system = SystemCollector()

        self._gpu: Optional[GPUCollector] = None
        if self._config.get("show_gpu"):
            self._gpu = GPUCollector()
            if not self._gpu.available:
                self._gpu = None

        self._battery: Optional[BatteryCollector] = None
        if self._config.get("show_battery"):
            self._battery = BatteryCollector()
            if not self._battery.available:
                self._battery = None

        # Alerts
        self._alerts = AlertManager(self._config)

        # Export
        self._exporter = Exporter(fmt=self._config.get("export_format"))
        self._last_export_time: float = 0

        # Dashboard
        self._dashboard = DashboardRenderer(self._config, self._history)

        # Hotkeys
        self._hotkeys = HotkeyManager()
        self._setup_hotkeys()

        # Cached state
        self._last_snapshot: dict[str, Any] = {}
        self._last_alerts: list = []

    def _setup_hotkeys(self) -> None:
        """Register all hotkey bindings."""
        self._hotkeys.bind("q", self._quit)
        self._hotkeys.bind("Q", self._quit)

        self._hotkeys.bind("t", self._next_theme)
        self._hotkeys.bind("T", self._prev_theme)

        self._hotkeys.bind("l", self._next_layout)

        self._hotkeys.bind("L", self._next_lang)

        self._hotkeys.bind("e", self._export_snapshot)
        self._hotkeys.bind("E", self._export_snapshot)

        self._hotkeys.bind("a", self._toggle_alerts)
        self._hotkeys.bind("A", self._toggle_alerts)

        self._hotkeys.bind("h", self._toggle_help)
        self._hotkeys.bind("H", self._toggle_help)
        self._hotkeys.bind("?", self._toggle_help)

        self._hotkeys.bind("c", self._toggle_per_core)
        self._hotkeys.bind("C", self._toggle_per_core)

        for i in range(1, 6):
            self._hotkeys.bind(str(i), self._make_tab_switcher(i))

        self._hotkeys.bind("LEFT", self._prev_tab)
        self._hotkeys.bind("RIGHT", self._next_tab)
        self._hotkeys.bind("\t", self._next_tab)

    def _make_tab_switcher(self, tab: int) -> Callable:
        """Create a closure for tab switching."""
        def switcher() -> None:
            self._dashboard.current_tab = tab
            self._dashboard.set_status(f"Tab {tab}")
        return switcher

    def _quit(self) -> None:
        self._running = False

    def _next_theme(self) -> None:
        current = self._config.get("theme")
        new = next_theme(current)
        self._config.set("theme", new)
        self._dashboard.set_status(f"Theme: {new}")

    def _prev_theme(self) -> None:
        current = self._config.get("theme")
        new = prev_theme(current)
        self._config.set("theme", new)
        self._dashboard.set_status(f"Theme: {new}")

    def _next_layout(self) -> None:
        current = self._config.get("layout")
        new = next_layout(current)
        self._config.set("layout", new)
        self._dashboard.set_status(f"Layout: {new}")

    def _next_lang(self) -> None:
        new = next_language()
        self._config.set("language", new)
        self._dashboard.set_status(f"Language: {new.upper()}")

    def _export_snapshot(self) -> None:
        try:
            data = self._last_snapshot or self._collect_all()
            path = self._exporter.export_snapshot(data)
            self._dashboard.set_status(t("export_success", path=str(path)))
        except Exception as e:
            self._dashboard.set_status(f"Export error: {e}")

    def _toggle_alerts(self) -> None:
        state = self._alerts.toggle()
        self._dashboard.set_status(f"Alerts: {'ON' if state else 'OFF'}")

    def _toggle_help(self) -> None:
        self._dashboard.show_help = not self._dashboard.show_help

    def _toggle_per_core(self) -> None:
        self._dashboard.show_per_core = not self._dashboard.show_per_core
        state = "ON" if self._dashboard.show_per_core else "OFF"
        self._dashboard.set_status(f"Per-core CPU: {state}")

    def _prev_tab(self) -> None:
        tab = self._dashboard.current_tab - 1
        if tab < 1:
            tab = 5
        self._dashboard.current_tab = tab
        self._dashboard.set_status(f"Tab {tab}")

    def _next_tab(self) -> None:
        tab = self._dashboard.current_tab + 1
        if tab > 5:
            tab = 1
        self._dashboard.current_tab = tab
        self._dashboard.set_status(f"Tab {tab}")

    def _collect_all(self) -> dict[str, Any]:
        """Collect data from every collector."""
        cpu_data = self._cpu.collect()
        mem_data = self._memory.collect()
        disk_data = self._disk.collect()
        net_data = self._network.collect()
        sys_data = self._system.collect()

        snapshot: dict[str, Any] = {
            "cpu_percent": cpu_data["percent"],
            "cpu_per_core": cpu_data["per_core"],
            "cpu_freq_current": cpu_data["freq_current"],
            "cpu_freq_max": cpu_data["freq_max"],
            "cpu_per_core_freq": cpu_data["per_core_freq"],
            "cpu_temp": cpu_data["temperature"],
            "cpu_logical_cores": cpu_data["logical_cores"],
            "cpu_physical_cores": cpu_data["physical_cores"],
            "ram_percent": mem_data["ram"]["percent"],
            "ram_used_gb": mem_data["ram"]["used_gb"],
            "ram_total_gb": mem_data["ram"]["total_gb"],
            "ram_available_gb": mem_data["ram"]["available_gb"],
            "ram_cached_gb": mem_data["ram"].get("cached_gb"),
            "ram_buffers_gb": mem_data["ram"].get("buffers_gb"),
            "swap_percent": mem_data["swap"]["percent"],
            "swap_used_gb": mem_data["swap"]["used_gb"],
            "swap_total_gb": mem_data["swap"]["total_gb"],
            "disks": disk_data["disks"],
            "disk_io": disk_data["io"],
            "network_interfaces": net_data["interfaces"],
            "network_total": net_data["total"],
            "system": sys_data,
            "uptime": sys_data["uptime"],
        }

        if self._gpu:
            gpu_data = self._gpu.collect()
            snapshot["gpus"] = gpu_data.get("gpus", [])
        else:
            snapshot["gpus"] = []

        if self._battery:
            snapshot["battery"] = self._battery.collect()
        else:
            snapshot["battery"] = {"available": False}

        proc_data = self._process.collect()
        snapshot["top_cpu"] = proc_data["top_cpu"]
        snapshot["top_mem"] = proc_data["top_mem"]
        snapshot["process_total"] = proc_data["total_count"]

        return snapshot

    def _update_history(self, snapshot: dict[str, Any]) -> None:
        """Push values into history for sparklines."""
        self._history.push("cpu", snapshot.get("cpu_percent", 0))
        self._history.push("ram", snapshot.get("ram_percent", 0))

        for i, v in enumerate(snapshot.get("cpu_per_core", [])):
            self._history.push(f"cpu_core_{i}", v)

        temp = snapshot.get("cpu_temp")
        if temp is not None:
            self._history.push("cpu_temp", temp)

        net = snapshot.get("network_total", {})
        self._history.push("net_sent", net.get("sent_speed_mbs", 0))
        self._history.push("net_recv", net.get("recv_speed_mbs", 0))

        for gpu in snapshot.get("gpus", []):
            self._history.push(
                f"gpu_{gpu.get('id', 0)}", gpu.get("load_percent", 0)
            )

    def _auto_export(self, snapshot: dict[str, Any]) -> None:
        """Export on interval if configured."""
        interval = self._config.get("export_interval")
        if interval <= 0:
            return
        now = time.time()
        if now - self._last_export_time >= interval:
            try:
                self._exporter.export_snapshot(snapshot)
                self._last_export_time = now
            except Exception:
                pass

    def run(self) -> None:
        """Main loop."""
        self._running = True
        refresh_rate = self._config.get("refresh_rate")
        collect_interval = 1.0 / refresh_rate

        self._console.print(
            f"[bold yellow]{t('starting')}[/bold yellow]"
        )
        time.sleep(0.5)

        self._hotkeys.start()

        try:
            self._last_snapshot = self._collect_all()
            self._update_history(self._last_snapshot)
            self._last_alerts = self._alerts.check_all(self._last_snapshot)

            rendered = self._dashboard.render(
                self._last_snapshot, self._last_alerts
            )

            with Live(
                rendered,
                refresh_per_second=int(refresh_rate) + 1,
                console=self._console,
                screen=False,
            ) as live:
                last_collect = time.monotonic()

                while self._running:
                    self._hotkeys.process_pending()

                    if not self._running:
                        break

                    now = time.monotonic()
                    if now - last_collect >= collect_interval:
                        self._last_snapshot = self._collect_all()
                        self._update_history(self._last_snapshot)
                        self._last_alerts = self._alerts.check_all(
                            self._last_snapshot
                        )
                        self._auto_export(self._last_snapshot)
                        last_collect = now

                    live.update(
                        self._dashboard.render(
                            self._last_snapshot, self._last_alerts
                        )
                    )

                    time.sleep(0.05)

        except KeyboardInterrupt:
            pass
        finally:
            self._hotkeys.stop()
            if self._save_on_exit:
                self._config.save()
                self._console.print(
                    f"[dim]Config saved to {self._config.config_path}[/dim]"
                )
            self._console.print(
                f"\n[bold red]{t('quit_message')}[/bold red]"
            )
