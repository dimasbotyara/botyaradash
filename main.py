import time
import datetime
import psutil
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
from rich.console import Console

console = Console()

def bytes_to_gb(bytes_value):
    """Конвертация байтов в гигабайты."""
    return round(bytes_value / (1024 ** 3), 2)

def make_layout() -> Layout:
    """Создание разметки терминала."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    return layout

def generate_dashboard() -> Panel:
    """Генерация таблицы с метриками системы."""
    
    # 1. Загрузка CPU
    cpu_percent = psutil.cpu_percent(interval=None)
    cpu_color = "green" if cpu_percent < 60 else "yellow" if cpu_percent < 85 else "red"
    
    # 2. Использование RAM
    ram = psutil.virtual_memory()
    ram_used_gb = bytes_to_gb(ram.used)
    ram_total_gb = bytes_to_gb(ram.total)
    ram_color = "green" if ram.percent < 60 else "yellow" if ram.percent < 85 else "red"
    
    # 3. Использование Диска
    disk = psutil.disk_usage('/')
    disk_used_gb = bytes_to_gb(disk.used)
    disk_total_gb = bytes_to_gb(disk.total)
    disk_color = "green" if disk.percent < 60 else "yellow" if disk.percent < 85 else "red"

    # Создание таблицы
    table = Table(title="📊 Статистика ресурсов", expand=True, show_header=True, header_style="bold cyan")
    table.add_column("Ресурс", style="bold white", width=15)
    table.add_column("Значение / Загрузка", justify="left")
    table.add_column("Процент", justify="right", width=10)

    # Строка CPU
    cpu_bar = f"[{cpu_color}]{'█' * int(cpu_percent / 5)}{'░' * (20 - int(cpu_percent / 5))}[/{cpu_color}]"
    table.add_row("ЦП (CPU)", f"{cpu_bar}", f"[{cpu_color}]{cpu_percent}%[/{cpu_color}]")

    # Строка ОЗУ
    ram_bar = f"[{ram_color}]{'█' * int(ram.percent / 5)}{'░' * (20 - int(ram.percent / 5))}[/{ram_color}]"
    table.add_row("ОЗУ (RAM)", f"{ram_bar} ({ram_used_gb} / {ram_total_gb} ГБ)", f"[{ram_color}]{ram.percent}%[/{ram_color}]")

    # Строка Диска
    disk_bar = f"[{disk_color}]{'█' * int(disk.percent / 5)}{'░' * (20 - int(disk.percent / 5))}[/{disk_color}]"
    table.add_row("Диск (SSD/HDD)", f"{disk_bar} ({disk_used_gb} / {disk_total_gb} ГБ)", f"[{disk_color}]{disk.percent}%[/{disk_color}]")

    # Сеть
    net = psutil.net_io_counters()
    sent_mb = round(net.bytes_sent / (1024 ** 2), 1)
    recv_mb = round(net.bytes_recv / (1024 ** 2), 1)
    
    # Дополнительная инфо-панель
    info_text = f"🌐 [bold]Сеть:[/bold] Отправлено: [cyan]{sent_mb} МБ[/cyan] | Получено: [cyan]{recv_mb} МБ[/cyan]\n"
    info_text += f"⏱ [bold]Время работы:[/bold] {datetime.timedelta(seconds=int(time.time() - psutil.boot_time()))}"

    main_layout = Layout()
    main_layout.split_column(
        Layout(table, ratio=2),
        Layout(Panel(info_text, title="ℹ️ Дополнительно", border_style="blue"), ratio=1)
    )

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return Panel(
        main_layout,
        title=f"[bold green]💻 System Monitor Dashboard[/bold green] | [dim]{now}[/dim]",
        border_style="cyan"
    )

def main():
    """Запуск основного цикла программы."""
    # Разогрев psutil для точного первого измерения CPU
    psutil.cpu_percent(interval=None)
    
    console.print("[bold yellow]Запуск монитора... Нажмите Ctrl+C для выхода.[/bold yellow]")
    time.sleep(1)

    try:
        with Live(generate_dashboard(), refresh_per_second=2, console=console) as live:
            while True:
                time.sleep(0.5)
                live.update(generate_dashboard())
    except KeyboardInterrupt:
        console.print("\n[bold red]Мониторинг остановлен.[/bold red]")

if __name__ == "__main__":
    main()