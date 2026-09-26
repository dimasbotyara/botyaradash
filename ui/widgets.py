"""UI widgets: bars, sparklines, gauges for botyaradash."""

from ui.themes import Theme


SPARKLINE_CHARS = "▁▂▃▄▅▆▇█"
BLOCK_FULL = "█"
BLOCK_EMPTY = "░"


def progress_bar(
    percent: float,
    theme: Theme,
    width: int = 20,
    show_percent: bool = False,
) -> str:
    """Create a colored progress bar string."""
    percent = max(0.0, min(100.0, float(percent)))
    filled = int(width * percent / 100)

    color = _get_bar_color(percent, theme)

    bar = f"[{color}]{BLOCK_FULL * filled}{BLOCK_EMPTY * (width - filled)}[/{color}]"

    if show_percent:
        bar += f" [{color}]{percent:.0f}%[/{color}]"

    return bar


def _get_bar_color(percent: float, theme: Theme) -> str:
    """Get bar color based on percentage."""
    if percent < 60:
        return theme.bar_low
    if percent < 85:
        return theme.bar_mid
    return theme.bar_high


def sparkline(values: list[float], width: int = 20, color: str = "cyan") -> str:
    """Create a sparkline from values."""
    if not values:
        return f"[{color}]{' ' * width}[/{color}]"

    # Trim or pad to width
    if len(values) > width:
        values = values[-width:]

    min_val = min(values) if values else 0
    max_val = max(values) if values else 0
    val_range = max_val - min_val

    chars = []
    for v in values:
        if val_range == 0:
            idx = 0
        else:
            idx = int((v - min_val) / val_range * (len(SPARKLINE_CHARS) - 1))
            idx = max(0, min(len(SPARKLINE_CHARS) - 1, idx))
        chars.append(SPARKLINE_CHARS[idx])

    # Pad with spaces if shorter than width
    line = "".join(chars)
    if len(line) < width:
        line = " " * (width - len(line)) + line

    return f"[{color}]{line}[/{color}]"


def gauge_icon(percent: float) -> str:
    """Return an emoji gauge based on percentage."""
    if percent < 20:
        return "🟢"
    if percent < 40:
        return "🟢"
    if percent < 60:
        return "🟡"
    if percent < 80:
        return "🟠"
    return "🔴"


def temp_icon(temp: float) -> str:
    """Return temperature emoji."""
    if temp < 50:
        return "🌡️"
    if temp < 70:
        return "🔥"
    if temp < 85:
        return "🔥🔥"
    return "🔥🔥🔥"


def battery_icon(percent: float, plugged: bool) -> str:
    """Return battery emoji."""
    if plugged:
        return "🔌"
    if percent > 75:
        return "🔋"
    if percent > 25:
        return "🪫"
    return "⚠️🪫"


def format_bytes(value: float, suffix: str = "B") -> str:
    """Format bytes to human readable string."""
    for unit in ("", "K", "M", "G", "T"):
        if abs(value) < 1024:
            return f"{value:.1f} {unit}{suffix}"
        value /= 1024
    return f"{value:.1f} P{suffix}"


def format_speed(mb_per_sec: float) -> str:
    """Format network speed."""
    if mb_per_sec < 1:
        return f"{mb_per_sec * 1024:.0f} KB/s"
    return f"{mb_per_sec:.2f} MB/s"


def status_dot(percent: float, theme: Theme) -> str:
    """Colored status dot."""
    color = _get_bar_color(percent, theme)
    return f"[{color}]●[/{color}]"


def colored_percent(percent: float, theme: Theme) -> str:
    """Return percentage with appropriate color."""
    color = _get_bar_color(percent, theme)
    return f"[{color}]{percent:.1f}%[/{color}]"


def mini_bar(percent: float, theme: Theme, width: int = 10) -> str:
    """Smaller progress bar for inline use."""
    return progress_bar(percent, theme, width=width)
