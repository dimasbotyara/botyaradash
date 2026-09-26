"""Internationalization support for botyaradash."""

from typing import Optional

# All translation strings
TRANSLATIONS: dict[str, dict[str, str]] = {
    # General
    "app_title": {
        "en": "botyaradash — System Monitor",
        "ru": "botyaradash — Системный монитор",
    },
    "quit_message": {
        "en": "Monitoring stopped.",
        "ru": "Мониторинг остановлен.",
    },
    "starting": {
        "en": "Starting monitor... Press 'q' to exit.",
        "ru": "Запуск монитора... Нажмите 'q' для выхода.",
    },

    # Resources
    "cpu": {
        "en": "CPU",
        "ru": "ЦП (CPU)",
    },
    "cpu_core": {
        "en": "Core {n}",
        "ru": "Ядро {n}",
    },
    "cpu_freq": {
        "en": "CPU Frequency",
        "ru": "Частота ЦП",
    },
    "cpu_temp": {
        "en": "CPU Temperature",
        "ru": "Температура ЦП",
    },
    "ram": {
        "en": "RAM",
        "ru": "ОЗУ (RAM)",
    },
    "swap": {
        "en": "Swap",
        "ru": "Подкачка (Swap)",
    },
    "disk": {
        "en": "Disk",
        "ru": "Диск",
    },
    "disk_io": {
        "en": "Disk I/O",
        "ru": "Диск I/O",
    },
    "network": {
        "en": "Network",
        "ru": "Сеть",
    },
    "gpu": {
        "en": "GPU",
        "ru": "Видеокарта (GPU)",
    },
    "battery": {
        "en": "Battery",
        "ru": "Батарея",
    },
    "processes": {
        "en": "Top Processes",
        "ru": "Топ процессов",
    },
    "system_info": {
        "en": "System Info",
        "ru": "Система",
    },

    # Table headers
    "resource": {
        "en": "Resource",
        "ru": "Ресурс",
    },
    "usage": {
        "en": "Usage",
        "ru": "Использование",
    },
    "percent": {
        "en": "Percent",
        "ru": "Процент",
    },
    "history": {
        "en": "History",
        "ru": "История",
    },

    # Details
    "sent": {
        "en": "Sent",
        "ru": "Отправлено",
    },
    "received": {
        "en": "Received",
        "ru": "Получено",
    },
    "speed": {
        "en": "Speed",
        "ru": "Скорость",
    },
    "uptime": {
        "en": "Uptime",
        "ru": "Время работы",
    },
    "hostname": {
        "en": "Hostname",
        "ru": "Имя хоста",
    },
    "os": {
        "en": "OS",
        "ru": "ОС",
    },
    "arch": {
        "en": "Architecture",
        "ru": "Архитектура",
    },
    "processor_label": {
        "en": "Processor",
        "ru": "Процессор",
    },
    "python_version": {
        "en": "Python",
        "ru": "Python",
    },
    "config_path_label": {
        "en": "Config",
        "ru": "Конфиг",
    },
    "total": {
        "en": "Total",
        "ru": "Всего",
    },
    "used": {
        "en": "Used",
        "ru": "Использовано",
    },
    "free": {
        "en": "Free",
        "ru": "Свободно",
    },
    "type": {
        "en": "Type",
        "ru": "Тип",
    },
    "mount": {
        "en": "Mount",
        "ru": "Точка монтирования",
    },
    "read_speed": {
        "en": "Read",
        "ru": "Чтение",
    },
    "write_speed": {
        "en": "Write",
        "ru": "Запись",
    },
    "interface": {
        "en": "Interface",
        "ru": "Интерфейс",
    },
    "ip_address": {
        "en": "IP Address",
        "ru": "IP-адрес",
    },
    "gpu_name": {
        "en": "GPU Name",
        "ru": "Видеокарта",
    },
    "gpu_load": {
        "en": "GPU Load",
        "ru": "Загрузка GPU",
    },
    "gpu_mem": {
        "en": "GPU Memory",
        "ru": "Память GPU",
    },
    "gpu_temp": {
        "en": "GPU Temp",
        "ru": "Темп. GPU",
    },
    "battery_level": {
        "en": "Charge",
        "ru": "Заряд",
    },
    "battery_status": {
        "en": "Status",
        "ru": "Статус",
    },
    "battery_time": {
        "en": "Time Left",
        "ru": "Осталось",
    },
    "charging": {
        "en": "Charging",
        "ru": "Заряжается",
    },
    "discharging": {
        "en": "Discharging",
        "ru": "Разряжается",
    },
    "full": {
        "en": "Full",
        "ru": "Полностью",
    },
    "no_battery": {
        "en": "No battery",
        "ru": "Нет батареи",
    },
    "unavailable": {
        "en": "Unavailable",
        "ru": "Недоступно",
    },

    # Processes
    "pid": {
        "en": "PID",
        "ru": "PID",
    },
    "proc_name": {
        "en": "Name",
        "ru": "Имя",
    },
    "proc_cpu": {
        "en": "CPU%",
        "ru": "ЦП%",
    },
    "proc_mem": {
        "en": "MEM%",
        "ru": "ОЗУ%",
    },
    "proc_status": {
        "en": "Status",
        "ru": "Статус",
    },

    # Alerts
    "alerts": {
        "en": "Alerts",
        "ru": "Оповещения",
    },
    "alert_cpu_high": {
        "en": "⚠ CPU usage is above {v}%!",
        "ru": "⚠ Загрузка ЦП выше {v}%!",
    },
    "alert_ram_high": {
        "en": "⚠ RAM usage is above {v}%!",
        "ru": "⚠ Использование ОЗУ выше {v}%!",
    },
    "alert_disk_high": {
        "en": "⚠ Disk '{name}' usage above {v}%!",
        "ru": "⚠ Диск '{name}' заполнен более чем на {v}%!",
    },
    "alert_temp_high": {
        "en": "🌡 CPU temperature is {v}°C!",
        "ru": "🌡 Температура ЦП: {v}°C!",
    },
    "no_alerts": {
        "en": "✅ All systems nominal.",
        "ru": "✅ Все системы в норме.",
    },

    # Help
    "help_title": {
        "en": "Hotkeys",
        "ru": "Горячие клавиши",
    },
    "help_quit": {
        "en": "Quit",
        "ru": "Выход",
    },
    "help_theme": {
        "en": "Next / Prev theme",
        "ru": "Следующая / Предыдущая тема",
    },
    "help_layout": {
        "en": "Next layout",
        "ru": "Следующий макет",
    },
    "help_lang": {
        "en": "Switch language",
        "ru": "Сменить язык",
    },
    "help_export": {
        "en": "Export snapshot",
        "ru": "Экспорт данных",
    },
    "help_alerts": {
        "en": "Toggle alerts",
        "ru": "Вкл/выкл оповещения",
    },
    "help_help": {
        "en": "Toggle help",
        "ru": "Показать/скрыть помощь",
    },
    "help_tab": {
        "en": "Switch tab",
        "ru": "Переключить вкладку",
    },
    "help_per_core": {
        "en": "Toggle per-core CPU",
        "ru": "Показать загрузку ядер",
    },

    # Export
    "export_success": {
        "en": "Exported to {path}",
        "ru": "Экспортировано в {path}",
    },

    # Tabs
    "tab_overview": {
        "en": "Overview",
        "ru": "Обзор",
    },
    "tab_cpu_mem": {
        "en": "CPU & Memory",
        "ru": "ЦП и Память",
    },
    "tab_disks": {
        "en": "Disks",
        "ru": "Диски",
    },
    "tab_network": {
        "en": "Network",
        "ru": "Сеть",
    },
    "tab_processes": {
        "en": "Processes",
        "ru": "Процессы",
    },

    # Additional
    "additional_info": {
        "en": "Additional Info",
        "ru": "Дополнительно",
    },
    "theme_label": {
        "en": "Theme",
        "ru": "Тема",
    },
    "layout_label": {
        "en": "Layout",
        "ru": "Макет",
    },
    "cores_logical": {
        "en": "Logical Cores",
        "ru": "Логич. ядер",
    },
    "cores_physical": {
        "en": "Physical Cores",
        "ru": "Физич. ядер",
    },
}

SUPPORTED_LANGUAGES = ["en", "ru"]

_current_lang = "en"


def set_language(lang: str) -> None:
    """Set the current language."""
    global _current_lang
    if lang in SUPPORTED_LANGUAGES:
        _current_lang = lang


def get_language() -> str:
    """Get current language."""
    return _current_lang


def t(key: str, **kwargs: object) -> str:
    """Translate a key to the current language."""
    entry = TRANSLATIONS.get(key, {})
    text = entry.get(_current_lang, entry.get("en", key))
    if kwargs:
        text = text.format(**kwargs)
    return text


def next_language() -> str:
    """Switch to the next language and return its name."""
    global _current_lang
    idx = SUPPORTED_LANGUAGES.index(_current_lang)
    _current_lang = SUPPORTED_LANGUAGES[(idx + 1) % len(SUPPORTED_LANGUAGES)]
    return _current_lang
