import datetime
import os
import time

import psutil
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

console = Console()

# Настройки отображения
BAR_WIDTH = 20
REFRESH_DELAY = 0.5
WARN_PERCENT = 60
CRIT_PERCENT = 85

# Состояние сети для расчета скорости
_net_state = {
    "time": None,
    "sent": None,
    "recv": None,
}


def bytes_to_gb(value: float) -> float:
    """Конвертация байтов в гигабайты."""
    return round(value / (1024 ** 3), 2)


def get_color(percent: float) -> str:
    """Возвращает цвет в зависимости от процента загрузки."""
    if percent < WARN_PERCENT:
        return "green"
    if percent < CRIT_PERCENT:
        return "yellow"
    return "red"


def make_bar(percent: float, color: str) -> str:
    """Рисует прогресс-бар."""
    percent = max(0.0, min(100.0, float(percent)))
    filled = int(BAR_WIDTH * percent / 100)
    return f"[{color}]{'█' * filled}{'░' * (BAR_WIDTH - filled)}[/{color}]"


def get_disk_path() -> str:
    """Возвращает путь для проверки диска с учетом ОС."""
    if os.name == "nt":
        return os.environ.get("SystemDrive", "C:") + "\\"
    return "/"


def add_resource_row(table: Table, name: str, percent: float, extra: str = "") -> None:
    """Добавляет строку ресурса в таблицу."""
    color = get_color(percent)
    bar = make_bar(percent, color)
    value = f"{bar} {extra}".strip()
    table.add_row(name, value, f"[{color}]{percent:.0f}%[/{color}]")


def get_network_stats() -> tuple[float, float, float, float]:
    """Возвращает всего отправлено/получено и текущую скорость."""
    net = psutil.net_io_counters()
    now = time.monotonic()

    sent_total_mb = net.bytes_sent / (1024 ** 2)
    recv_total_mb = net.bytes_recv / (1024 ** 2)

    sent_speed_mbps = 0.0
    recv_speed_mbps = 0.0

    if _net_state["time"] is not None:
        delta_time = now - _net_state["time"]
        if delta_time > 0:
            sent_delta = net.bytes_sent - _net_state["sent"]
            recv_delta = net.bytes_recv - _net_state["recv"]

            sent_speed_mbps = max(0.0, sent_delta / delta_time / (1024 ** 2))
            recv_speed_mbps = max(0.0, recv_delta / delta_time / (1024 ** 2))

    _net_state["time"] = now
    _net_state["sent"] = net.bytes_sent
    _net_state["recv"] = net.bytes_recv

    return sent_total_mb, recv_total_mb, sent_speed_mbps, recv_speed_mbps


def generate_dashboard() -> Panel:
    """Генерация панели мониторинга."""
    cpu_percent = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()

    table = Table(
        title="📊 Статистика ресурсов",
        expand=True,
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("Ресурс", style="bold white", width=18)
    table.add_column("Значение / Загрузка", justify="left")
    table.add_column("Процент", justify="right", width=10)

    # CPU
    add_resource_row(table, "ЦП (CPU)", cpu_percent)

    # RAM
    add_resource_row(
        table,
        "ОЗУ (RAM)",
        ram.percent,
        f"({bytes_to_gb(ram.used)} / {bytes_to_gb(ram.total)} ГБ)",
    )

    # Диск
    try:
        disk = psutil.disk_usage(get_disk_path())
        add_resource_row(
            table,
            "Диск (SSD/HDD)",
            disk.percent,
            f"({bytes_to_gb(disk.used)} / {bytes_to_gb(disk.total)} ГБ)",
        )
    except OSError:
        table.add_row("Диск (SSD/HDD)", "[dim]недоступен[/dim]", "-")

    # Сеть
    sent_total_mb, recv_total_mb, sent_speed_mbps, recv_speed_mbps = get_network_stats()

    uptime = datetime.timedelta(seconds=int(time.time() - psutil.boot_time()))

    info_text = (
        f"🌐 [bold]Сеть:[/bold] "
        f"Отправлено: [cyan]{sent_total_mb:.1f} МБ[/cyan] "
        f"([cyan]{sent_speed_mbps:.2f} МБ/с[/cyan]) | "
        f"Получено: [cyan]{recv_total_mb:.1f} МБ[/cyan] "
        f"([cyan]{recv_speed_mbps:.2f} МБ/с[/cyan])\n"
    )
    info_text += f"⏱ [bold]Время работы:[/bold] {uptime}"

    main_layout = Layout()
    main_layout.split_column(
        Layout(table, ratio=2),
        Layout(Panel(info_text, title="ℹ️ Дополнительно", border_style="blue"), ratio=1),
    )

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return Panel(
        main_layout,
        title=f"[bold green]💻 System Monitor Dashboard[/bold green] | [dim]{now}[/dim]",
        border_style="cyan",
    )


def main() -> None:
    """Запуск основного цикла программы."""
    # Разогрев psutil для точного первого измерения CPU
    psutil.cpu_percent(interval=None)

    console.print("[bold yellow]Запуск монитора... Нажмите Ctrl+C для выхода.[/bold yellow]")
    time.sleep(1)

    try:
        with Live(generate_dashboard(), refresh_per_second=2, console=console) as live:
            while True:
                time.sleep(REFRESH_DELAY)
                live.update(generate_dashboard())
    except KeyboardInterrupt:
        console.print("\n[bold red]Мониторинг остановлен.[/bold red]")


if __name__ == "__main__":
    main()