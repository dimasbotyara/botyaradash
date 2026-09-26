"""Main dashboard rendering for botyaradash."""

import datetime
import time as _time
from typing import Any, Optional

from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from alerts import Alert
from config import Config
from history import HistoryManager
from i18n import t
from ui.themes import Theme, get_theme
from ui.widgets import (
    progress_bar,
    sparkline,
    gauge_icon,
    temp_icon,
    battery_icon,
    colored_percent,
    format_speed,
    status_dot,
)


class DashboardRenderer:
    """Renders the complete dashboard using Tables and Panels only."""

    def __init__(self, config: Config, history: HistoryManager) -> None:
        self._config = config
        self._history = history
        self._current_tab = 1
        self._show_help = False
        self._show_per_core = False
        self._status_message: Optional[str] = None
        self._status_time: Optional[float] = None

    @property
    def current_tab(self) -> int:
        return self._current_tab

    @current_tab.setter
    def current_tab(self, value: int) -> None:
        self._current_tab = max(1, min(5, value))

    @property
    def show_help(self) -> bool:
        return self._show_help

    @show_help.setter
    def show_help(self, value: bool) -> None:
        self._show_help = value

    @property
    def show_per_core(self) -> bool:
        return self._show_per_core

    @show_per_core.setter
    def show_per_core(self, value: bool) -> None:
        self._show_per_core = value

    def set_status(self, message: str) -> None:
        self._status_message = message
        self._status_time = _time.time()

    def render(
        self,
        snapshot: dict[str, Any],
        alerts: list[Alert],
    ) -> Panel:
        """Render the full dashboard as a single Panel."""
        theme = get_theme(self._config.get("theme"))
        layout_name = self._config.get("layout")

        # Build parts list — will be wrapped in Group
        parts: list[Any] = []

        # Tab bar
        parts.append(self._render_tab_bar(theme))
        parts.append(Text(""))

        # Main content based on layout + tab
        if layout_name == "minimal":
            parts.append(self._render_minimal(snapshot, theme))
        elif layout_name == "compact":
            parts.append(self._render_overview_table(snapshot, theme))
            parts.append(self._render_alerts_panel(alerts, theme))
        else:
            # Full layout — tab-based
            if self._current_tab == 1:
                parts.append(self._render_overview_table(snapshot, theme))
                parts.append(Text(""))
                parts.append(
                    Columns(
                        [
                            self._render_system_info(snapshot, theme),
                            self._render_alerts_panel(alerts, theme),
                        ],
                        equal=True,
                        expand=True,
                    )
                )
            elif self._current_tab == 2:
                parts.append(self._render_cpu_detail(snapshot, theme))
                parts.append(Text(""))
                parts.append(self._render_memory_detail(snapshot, theme))
            elif self._current_tab == 3:
                parts.append(self._render_disk_detail(snapshot, theme))
            elif self._current_tab == 4:
                parts.append(self._render_network_detail(snapshot, theme))
            elif self._current_tab == 5:
                parts.append(self._render_process_detail(snapshot, theme))

        # Help overlay
        if self._show_help:
            parts.append(Text(""))
            parts.append(self._render_help(theme))

        # Build title
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = ""
        if self._status_message and self._status_time:
            if _time.time() - self._status_time < 3:
                status = f" | [{theme.accent}]{self._status_message}[/{theme.accent}]"
            else:
                self._status_message = None

        title = (
            f"[{theme.title}]💻 botyaradash[/{theme.title}] "
            f"[{theme.dim}]|[/{theme.dim}] "
            f"[{theme.dim}]{now}[/{theme.dim}] "
            f"[{theme.dim}]|[/{theme.dim}] "
            f"[{theme.secondary}]🎨 {theme.display_name}[/{theme.secondary}] "
            f"[{theme.dim}]|[/{theme.dim}] "
            f"[{theme.secondary}]🌐 {self._config.get('language').upper()}[/{theme.secondary}]"
            f"{status}"
        )

        subtitle = (
            f"[{theme.dim}]q:quit  t/T:theme  l:layout  L:lang  "
            f"e:export  a:alerts  h:help  c:cores  1-5:tabs  ←→:nav[/{theme.dim}]"
        )

        return Panel(
            Group(*parts),
            title=title,
            subtitle=subtitle,
            border_style=theme.border,
            expand=True,
        )

    # ── Tab bar ────────────────────────────────────────────────

    def _render_tab_bar(self, theme: Theme) -> Text:
        tabs = [
            (1, t("tab_overview")),
            (2, t("tab_cpu_mem")),
            (3, t("tab_disks")),
            (4, t("tab_network")),
            (5, t("tab_processes")),
        ]
        text = Text()
        for num, label in tabs:
            if num == self._current_tab:
                text.append(f" 【{num}:{label}】 ", style=f"bold {theme.accent}")
            else:
                text.append(f"  {num}:{label}  ", style=theme.dim)
        return text

    # ── Minimal ────────────────────────────────────────────────

    def _render_minimal(self, snapshot: dict[str, Any], theme: Theme) -> Panel:
        cpu_pct = snapshot.get("cpu_percent", 0)
        ram_pct = snapshot.get("ram_percent", 0)

        lines = []
        lines.append(
            f"{gauge_icon(cpu_pct)} {t('cpu')}: "
            f"{colored_percent(cpu_pct, theme)}  "
            f"{sparkline(self._history.values('cpu'), 15, theme.sparkline_color)}"
        )
        lines.append(
            f"{gauge_icon(ram_pct)} {t('ram')}: "
            f"{colored_percent(ram_pct, theme)}  "
            f"{sparkline(self._history.values('ram'), 15, theme.sparkline_color)}"
        )

        temp = snapshot.get("cpu_temp")
        if temp is not None:
            lines.append(f"{temp_icon(temp)} {t('cpu_temp')}: {temp:.0f}°C")

        net = snapshot.get("network_total", {})
        lines.append(
            f"🌐 {t('network')}: ↑{format_speed(net.get('sent_speed_mbs', 0))} "
            f"↓{format_speed(net.get('recv_speed_mbs', 0))}"
        )
        lines.append(f"⏱  {t('uptime')}: {snapshot.get('uptime', '?')}")

        return Panel("\n".join(lines), border_style=theme.border)

    # ── Overview table ─────────────────────────────────────────

    def _render_overview_table(self, snapshot: dict[str, Any], theme: Theme) -> Table:
        bar_w = self._config.get("bar_width")
        sp_w = self._config.get("sparkline_width")

        table = Table(
            title=f"📊 {t('tab_overview')}",
            title_style=theme.title,
            expand=True,
            show_header=True,
            header_style=theme.header,
            border_style=theme.border,
        )
        table.add_column("", width=2)
        table.add_column(t("resource"), style=f"bold {theme.text}", width=20)
        table.add_column(t("usage"), justify="left", min_width=30)
        table.add_column(t("percent"), justify="right", width=8)
        table.add_column(t("history"), justify="right", width=sp_w + 2)

        # CPU
        cpu_pct = snapshot.get("cpu_percent", 0)
        freq = snapshot.get("cpu_freq_current")
        freq_s = f" @ {freq:.0f}MHz" if freq else ""
        table.add_row(
            status_dot(cpu_pct, theme),
            t("cpu"),
            progress_bar(cpu_pct, theme, bar_w) + freq_s,
            colored_percent(cpu_pct, theme),
            sparkline(self._history.values("cpu"), sp_w, theme.sparkline_color),
        )

        # Per-core
        if self._show_per_core:
            for i, core_pct in enumerate(snapshot.get("cpu_per_core", [])):
                table.add_row(
                    "",
                    f"  {t('cpu_core', n=i)}",
                    progress_bar(core_pct, theme, bar_w),
                    colored_percent(core_pct, theme),
                    sparkline(
                        self._history.values(f"cpu_core_{i}"),
                        sp_w,
                        theme.sparkline_color,
                    ),
                )

        # CPU temp
        temp = snapshot.get("cpu_temp")
        if temp is not None:
            table.add_row(
                temp_icon(temp),
                t("cpu_temp"),
                f"[{theme.text}]{temp:.0f}°C[/{theme.text}]",
                "",
                sparkline(
                    self._history.values("cpu_temp"), sp_w, theme.sparkline_color
                ),
            )

        # RAM
        ram_pct = snapshot.get("ram_percent", 0)
        ram_info = (
            f"({snapshot.get('ram_used_gb', 0)}"
            f"/{snapshot.get('ram_total_gb', 0)} GB)"
        )
        table.add_row(
            status_dot(ram_pct, theme),
            t("ram"),
            progress_bar(ram_pct, theme, bar_w) + f" {ram_info}",
            colored_percent(ram_pct, theme),
            sparkline(self._history.values("ram"), sp_w, theme.sparkline_color),
        )

        # Swap
        swap_total = snapshot.get("swap_total_gb", 0)
        if swap_total > 0:
            swap_pct = snapshot.get("swap_percent", 0)
            swap_info = (
                f"({snapshot.get('swap_used_gb', 0)}/{swap_total} GB)"
            )
            table.add_row(
                status_dot(swap_pct, theme),
                t("swap"),
                progress_bar(swap_pct, theme, bar_w) + f" {swap_info}",
                colored_percent(swap_pct, theme),
                "",
            )

        # Disks
        for disk in snapshot.get("disks", []):
            pct = disk.get("percent", 0)
            dtype = disk.get("disk_type", "?")
            mount = disk.get("mountpoint", "?")
            d_info = (
                f"({disk.get('used_gb', 0)}/{disk.get('total_gb', 0)} GB)"
                f" [{theme.dim}]{dtype}[/{theme.dim}]"
            )
            table.add_row(
                status_dot(pct, theme),
                f"{t('disk')} [{theme.dim}]{mount}[/{theme.dim}]",
                progress_bar(pct, theme, bar_w) + f" {d_info}",
                colored_percent(pct, theme),
                "",
            )

        # Network
        net = snapshot.get("network_total", {})
        net_info = (
            f"[{theme.ok}]↑ {format_speed(net.get('sent_speed_mbs', 0))}[/{theme.ok}]"
            f"  [{theme.primary}]↓ {format_speed(net.get('recv_speed_mbs', 0))}"
            f"[/{theme.primary}]"
        )
        table.add_row(
            "🌐",
            t("network"),
            net_info,
            "",
            sparkline(self._history.values("net_recv"), sp_w, theme.sparkline_color),
        )

        # GPU
        for gpu in snapshot.get("gpus", []):
            load = gpu.get("load_percent", 0)
            gpu_info = (
                f"{gpu.get('temperature', 0)}°C  "
                f"Mem:{gpu.get('memory_percent', 0):.0f}%"
            )
            table.add_row(
                status_dot(load, theme),
                f"{t('gpu')} [{theme.dim}]{gpu.get('name', '?')[:18]}[/{theme.dim}]",
                progress_bar(load, theme, bar_w) + f" {gpu_info}",
                colored_percent(load, theme),
                sparkline(
                    self._history.values(f"gpu_{gpu.get('id', 0)}"),
                    sp_w,
                    theme.sparkline_color,
                ),
            )

        # Battery
        battery = snapshot.get("battery", {})
        if battery.get("available"):
            batt_pct = battery.get("percent", 0)
            plugged = battery.get("plugged", False)
            batt_info = (
                f"{t(battery.get('status', 'discharging'))}"
                f" ({battery.get('time_left', '?')})"
            )
            table.add_row(
                battery_icon(batt_pct, plugged),
                t("battery"),
                progress_bar(batt_pct, theme, bar_w) + f" {batt_info}",
                colored_percent(batt_pct, theme),
                "",
            )

        return table

    # ── CPU detail (tab 2) ─────────────────────────────────────

    def _render_cpu_detail(self, snapshot: dict[str, Any], theme: Theme) -> Panel:
        bar_w = self._config.get("bar_width")
        sp_w = self._config.get("sparkline_width")

        table = Table(
            expand=True,
            show_header=True,
            header_style=theme.header,
            border_style=theme.border,
        )
        table.add_column(t("cpu_core", n=""), style=f"bold {theme.text}", width=14)
        table.add_column(t("usage"), justify="left", min_width=25)
        table.add_column(t("percent"), justify="right", width=8)
        table.add_column(t("history"), justify="right", width=sp_w + 2)

        # Overall
        cpu_pct = snapshot.get("cpu_percent", 0)
        table.add_row(
            f"[bold]{t('cpu')} (Total)[/bold]",
            progress_bar(cpu_pct, theme, bar_w),
            colored_percent(cpu_pct, theme),
            sparkline(self._history.values("cpu"), sp_w, theme.sparkline_color),
        )
        table.add_section()

        # Per core
        per_core = snapshot.get("cpu_per_core", [])
        per_core_freq = snapshot.get("cpu_per_core_freq", [])
        for i, core_pct in enumerate(per_core):
            freq_s = ""
            if i < len(per_core_freq) and per_core_freq[i]:
                freq_s = f" {per_core_freq[i]:.0f}MHz"
            table.add_row(
                t("cpu_core", n=i),
                progress_bar(core_pct, theme, bar_w) + freq_s,
                colored_percent(core_pct, theme),
                sparkline(
                    self._history.values(f"cpu_core_{i}"),
                    sp_w,
                    theme.sparkline_color,
                ),
            )

        # Info line
        info_parts = []
        info_parts.append(
            f"{t('cores_logical')}: [{theme.primary}]"
            f"{snapshot.get('cpu_logical_cores', '?')}[/{theme.primary}]"
        )
        info_parts.append(
            f"{t('cores_physical')}: [{theme.primary}]"
            f"{snapshot.get('cpu_physical_cores', '?')}[/{theme.primary}]"
        )
        freq = snapshot.get("cpu_freq_current")
        freq_max = snapshot.get("cpu_freq_max")
        if freq:
            fs = f"{freq:.0f}"
            if freq_max:
                fs += f" / {freq_max:.0f}"
            info_parts.append(
                f"{t('cpu_freq')}: [{theme.primary}]{fs} MHz[/{theme.primary}]"
            )
        temp = snapshot.get("cpu_temp")
        if temp is not None:
            info_parts.append(
                f"{t('cpu_temp')}: [{theme.primary}]{temp:.1f}°C[/{theme.primary}]"
            )

        info_text = "  |  ".join(info_parts)

        return Panel(
            Group(table, Text(""), Text.from_markup(info_text)),
            title=f"[{theme.title}]🧠 CPU Detail[/{theme.title}]",
            border_style=theme.border,
        )

    # ── Memory detail (tab 2) ──────────────────────────────────

    def _render_memory_detail(self, snapshot: dict[str, Any], theme: Theme) -> Panel:
        bar_w = self._config.get("bar_width")

        table = Table(
            expand=True,
            show_header=True,
            header_style=theme.header,
            border_style=theme.border,
        )
        table.add_column(t("resource"), style=f"bold {theme.text}", width=14)
        table.add_column(t("usage"), min_width=25)
        table.add_column(t("used"), justify="right", width=10)
        table.add_column(t("total"), justify="right", width=10)
        table.add_column(t("percent"), justify="right", width=8)

        ram_pct = snapshot.get("ram_percent", 0)
        table.add_row(
            t("ram"),
            progress_bar(ram_pct, theme, bar_w),
            f"{snapshot.get('ram_used_gb', 0)} GB",
            f"{snapshot.get('ram_total_gb', 0)} GB",
            colored_percent(ram_pct, theme),
        )

        swap_total = snapshot.get("swap_total_gb", 0)
        if swap_total > 0:
            swap_pct = snapshot.get("swap_percent", 0)
            table.add_row(
                t("swap"),
                progress_bar(swap_pct, theme, bar_w),
                f"{snapshot.get('swap_used_gb', 0)} GB",
                f"{swap_total} GB",
                colored_percent(swap_pct, theme),
            )

        extras = []
        cached = snapshot.get("ram_cached_gb")
        buffers = snapshot.get("ram_buffers_gb")
        if cached and cached > 0:
            extras.append(f"Cached: [{theme.primary}]{cached} GB[/{theme.primary}]")
        if buffers and buffers > 0:
            extras.append(f"Buffers: [{theme.primary}]{buffers} GB[/{theme.primary}]")

        parts: list[Any] = [table]
        if extras:
            parts.append(Text(""))
            parts.append(Text.from_markup("  |  ".join(extras)))

        return Panel(
            Group(*parts),
            title=f"[{theme.title}]🧠 {t('ram')} & {t('swap')}[/{theme.title}]",
            border_style=theme.border,
        )

    # ── Disk detail (tab 3) ────────────────────────────────────

    def _render_disk_detail(self, snapshot: dict[str, Any], theme: Theme) -> Panel:
        bar_w = self._config.get("bar_width")

        table = Table(
            expand=True,
            show_header=True,
            header_style=theme.header,
            border_style=theme.border,
        )
        table.add_column(t("mount"), style=f"bold {theme.text}", width=16)
        table.add_column("Device", width=20)
        table.add_column(t("type"), width=8)
        table.add_column("FS", width=10)
        table.add_column(t("usage"), min_width=20)
        table.add_column(t("used"), justify="right", width=10)
        table.add_column(t("total"), justify="right", width=10)
        table.add_column(t("percent"), justify="right", width=8)

        for disk in snapshot.get("disks", []):
            pct = disk.get("percent", 0)
            table.add_row(
                disk.get("mountpoint", "?"),
                f"[{theme.dim}]{disk.get('device', '?')}[/{theme.dim}]",
                disk.get("disk_type", "?"),
                disk.get("fstype", "?"),
                progress_bar(pct, theme, bar_w),
                f"{disk.get('used_gb', 0)} GB",
                f"{disk.get('total_gb', 0)} GB",
                colored_percent(pct, theme),
            )

        io = snapshot.get("disk_io", {})
        io_text = (
            f"📖 {t('read_speed')}: [{theme.primary}]"
            f"{io.get('read_mb_s', 0):.2f} MB/s[/{theme.primary}]"
            f"  |  📝 {t('write_speed')}: [{theme.primary}]"
            f"{io.get('write_mb_s', 0):.2f} MB/s[/{theme.primary}]"
        )

        return Panel(
            Group(table, Text(""), Text.from_markup(io_text)),
            title=f"[{theme.title}]💾 {t('tab_disks')}[/{theme.title}]",
            border_style=theme.border,
        )

    # ── Network detail (tab 4) ─────────────────────────────────

    def _render_network_detail(self, snapshot: dict[str, Any], theme: Theme) -> Panel:
        sp_w = self._config.get("sparkline_width")

        table = Table(
            expand=True,
            show_header=True,
            header_style=theme.header,
            border_style=theme.border,
        )
        table.add_column(t("interface"), style=f"bold {theme.text}", width=16)
        table.add_column(t("ip_address"), width=16)
        table.add_column(f"↑ {t('speed')}", justify="right", width=14)
        table.add_column(f"↓ {t('speed')}", justify="right", width=14)
        table.add_column(f"↑ {t('total')}", justify="right", width=12)
        table.add_column(f"↓ {t('total')}", justify="right", width=12)

        for iface in snapshot.get("network_interfaces", []):
            ips = ", ".join(iface.get("ip_addresses", []))
            table.add_row(
                iface.get("name", "?"),
                f"[{theme.primary}]{ips or '-'}[/{theme.primary}]",
                f"[{theme.ok}]{format_speed(iface.get('sent_speed_mbs', 0))}[/{theme.ok}]",
                f"[{theme.primary}]{format_speed(iface.get('recv_speed_mbs', 0))}[/{theme.primary}]",
                f"{iface.get('sent_total_mb', 0):.1f} MB",
                f"{iface.get('recv_total_mb', 0):.1f} MB",
            )

        net = snapshot.get("network_total", {})
        total_line = (
            f"📊 Total: "
            f"↑ [{theme.ok}]{format_speed(net.get('sent_speed_mbs', 0))}[/{theme.ok}]"
            f"  ↓ [{theme.primary}]{format_speed(net.get('recv_speed_mbs', 0))}[/{theme.primary}]"
            f"  |  ↑ {net.get('sent_total_mb', 0):.1f} MB"
            f"  ↓ {net.get('recv_total_mb', 0):.1f} MB"
            f"  |  {sparkline(self._history.values('net_recv'), sp_w, theme.sparkline_color)}"
        )

        return Panel(
            Group(table, Text(""), Text.from_markup(total_line)),
            title=f"[{theme.title}]🌐 {t('tab_network')}[/{theme.title}]",
            border_style=theme.border,
        )

    # ── Process detail (tab 5) ─────────────────────────────────

    def _render_process_detail(self, snapshot: dict[str, Any], theme: Theme) -> Panel:
        # Top by CPU
        cpu_table = Table(
            title="🔥 Top by CPU",
            title_style=theme.title,
            expand=True,
            show_header=True,
            header_style=theme.header,
            border_style=theme.border,
        )
        cpu_table.add_column(t("pid"), width=8)
        cpu_table.add_column(t("proc_name"), width=25)
        cpu_table.add_column(t("proc_cpu"), justify="right", width=8)
        cpu_table.add_column(t("proc_mem"), justify="right", width=8)
        cpu_table.add_column(t("proc_status"), width=12)

        for proc in snapshot.get("top_cpu", []):
            cpu_pct = proc.get("cpu_percent", 0)
            color = (
                theme.bar_high if cpu_pct > 50
                else theme.bar_mid if cpu_pct > 20
                else theme.text
            )
            cpu_table.add_row(
                str(proc.get("pid", "?")),
                proc.get("name", "?"),
                f"[{color}]{cpu_pct:.1f}%[/{color}]",
                f"{proc.get('memory_percent', 0):.1f}%",
                proc.get("status", "?"),
            )

        # Top by Memory
        mem_table = Table(
            title="🧠 Top by Memory",
            title_style=theme.title,
            expand=True,
            show_header=True,
            header_style=theme.header,
            border_style=theme.border,
        )
        mem_table.add_column(t("pid"), width=8)
        mem_table.add_column(t("proc_name"), width=25)
        mem_table.add_column(t("proc_cpu"), justify="right", width=8)
        mem_table.add_column(t("proc_mem"), justify="right", width=8)
        mem_table.add_column(t("proc_status"), width=12)

        for proc in snapshot.get("top_mem", []):
            mem_pct = proc.get("memory_percent", 0)
            color = (
                theme.bar_high if mem_pct > 50
                else theme.bar_mid if mem_pct > 20
                else theme.text
            )
            mem_table.add_row(
                str(proc.get("pid", "?")),
                proc.get("name", "?"),
                f"{proc.get('cpu_percent', 0):.1f}%",
                f"[{color}]{mem_pct:.1f}%[/{color}]",
                proc.get("status", "?"),
            )

        total = snapshot.get("process_total", 0)
        info = (
            f"📊 {t('total')} {t('processes').lower()}: "
            f"[{theme.primary}]{total}[/{theme.primary}]"
        )

        return Panel(
            Group(
                Columns([cpu_table, mem_table], equal=True, expand=True),
                Text(""),
                Text.from_markup(info),
            ),
            title=f"[{theme.title}]⚡ {t('tab_processes')}[/{theme.title}]",
            border_style=theme.border,
        )

    # ── System info panel ──────────────────────────────────────

    def _render_system_info(self, snapshot: dict[str, Any], theme: Theme) -> Panel:
        sys_info = snapshot.get("system", {})
        lines = [
            f"🖥  {t('hostname')}: [{theme.primary}]{sys_info.get('hostname', '?')}[/{theme.primary}]",
            f"💿 {t('os')}: [{theme.primary}]{sys_info.get('os', '?')}[/{theme.primary}]",
            f"🏗  {t('arch')}: [{theme.primary}]{sys_info.get('arch', '?')}[/{theme.primary}]",
            f"⚙️  {t('processor_label')}: [{theme.primary}]{sys_info.get('processor', '?')}[/{theme.primary}]",
            f"🐍 {t('python_version')}: [{theme.primary}]{sys_info.get('python', '?')}[/{theme.primary}]",
            f"⏱  {t('uptime')}: [{theme.primary}]{sys_info.get('uptime', '?')}[/{theme.primary}]",
            f"📁 {t('config_path_label')}: [{theme.dim}]{self._config.config_path}[/{theme.dim}]",
        ]
        return Panel(
            "\n".join(lines),
            title=f"[{theme.title}]ℹ️  {t('system_info')}[/{theme.title}]",
            border_style=theme.border,
        )

    # ── Alerts panel ───────────────────────────────────────────

    def _render_alerts_panel(self, alerts: list[Alert], theme: Theme) -> Panel:
        if not alerts:
            content = f"[{theme.ok}]{t('no_alerts')}[/{theme.ok}]"
        else:
            lines = []
            for alert in alerts:
                color = theme.crit if alert.level == "crit" else theme.warn
                lines.append(f"[{color}]{alert.message}[/{color}]")
            content = "\n".join(lines)
        return Panel(
            content,
            title=f"[{theme.title}]🔔 {t('alerts')}[/{theme.title}]",
            border_style=theme.border,
        )

    # ── Help panel ─────────────────────────────────────────────

    def _render_help(self, theme: Theme) -> Panel:
        table = Table(
            show_header=False,
            expand=True,
            border_style=theme.border,
            padding=(0, 2),
        )
        table.add_column("Key", style=f"bold {theme.accent}", width=12)
        table.add_column("Action", style=theme.text)

        hotkeys = [
            ("q", t("help_quit")),
            ("t / T", t("help_theme")),
            ("l", t("help_layout")),
            ("L", t("help_lang")),
            ("e", t("help_export")),
            ("a", t("help_alerts")),
            ("h / ?", t("help_help")),
            ("c", t("help_per_core")),
            ("1-5", t("help_tab")),
            ("← →", "Navigate tabs"),
            ("Tab", "Next tab"),
        ]

        for key, action in hotkeys:
            table.add_row(key, action)

        return Panel(
            table,
            title=f"[{theme.title}]⌨️  {t('help_title')}[/{theme.title}]",
            border_style=theme.accent,
        )
