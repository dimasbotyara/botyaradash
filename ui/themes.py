"""Color themes for botyaradash."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Theme:
    """Color theme definition."""

    name: str
    display_name: str

    # Main colors
    primary: str
    secondary: str
    accent: str

    # Status colors
    ok: str
    warn: str
    crit: str

    # UI colors
    border: str
    title: str
    header: str
    text: str
    dim: str

    # Bar colors
    bar_low: str
    bar_mid: str
    bar_high: str

    # Special
    background: Optional[str] = None
    sparkline_color: str = "cyan"


THEMES: dict[str, Theme] = {
    "default": Theme(
        name="default",
        display_name="Default",
        primary="cyan",
        secondary="blue",
        accent="magenta",
        ok="green",
        warn="yellow",
        crit="red",
        border="cyan",
        title="bold green",
        header="bold cyan",
        text="white",
        dim="dim white",
        bar_low="green",
        bar_mid="yellow",
        bar_high="red",
        sparkline_color="cyan",
    ),
    "dracula": Theme(
        name="dracula",
        display_name="Dracula",
        primary="#bd93f9",
        secondary="#6272a4",
        accent="#ff79c6",
        ok="#50fa7b",
        warn="#f1fa8c",
        crit="#ff5555",
        border="#bd93f9",
        title="bold #ff79c6",
        header="bold #bd93f9",
        text="#f8f8f2",
        dim="#6272a4",
        bar_low="#50fa7b",
        bar_mid="#f1fa8c",
        bar_high="#ff5555",
        sparkline_color="#8be9fd",
    ),
    "monokai": Theme(
        name="monokai",
        display_name="Monokai",
        primary="#66d9ef",
        secondary="#75715e",
        accent="#f92672",
        ok="#a6e22e",
        warn="#e6db74",
        crit="#f92672",
        border="#66d9ef",
        title="bold #a6e22e",
        header="bold #66d9ef",
        text="#f8f8f2",
        dim="#75715e",
        bar_low="#a6e22e",
        bar_mid="#e6db74",
        bar_high="#f92672",
        sparkline_color="#66d9ef",
    ),
    "nord": Theme(
        name="nord",
        display_name="Nord",
        primary="#88c0d0",
        secondary="#81a1c1",
        accent="#b48ead",
        ok="#a3be8c",
        warn="#ebcb8b",
        crit="#bf616a",
        border="#88c0d0",
        title="bold #88c0d0",
        header="bold #81a1c1",
        text="#eceff4",
        dim="#4c566a",
        bar_low="#a3be8c",
        bar_mid="#ebcb8b",
        bar_high="#bf616a",
        sparkline_color="#88c0d0",
    ),
    "gruvbox": Theme(
        name="gruvbox",
        display_name="Gruvbox",
        primary="#83a598",
        secondary="#458588",
        accent="#d3869b",
        ok="#b8bb26",
        warn="#fabd2f",
        crit="#fb4934",
        border="#83a598",
        title="bold #b8bb26",
        header="bold #83a598",
        text="#ebdbb2",
        dim="#928374",
        bar_low="#b8bb26",
        bar_mid="#fabd2f",
        bar_high="#fb4934",
        sparkline_color="#83a598",
    ),
    "solarized": Theme(
        name="solarized",
        display_name="Solarized",
        primary="#268bd2",
        secondary="#2aa198",
        accent="#d33682",
        ok="#859900",
        warn="#b58900",
        crit="#dc322f",
        border="#268bd2",
        title="bold #268bd2",
        header="bold #2aa198",
        text="#839496",
        dim="#586e75",
        bar_low="#859900",
        bar_mid="#b58900",
        bar_high="#dc322f",
        sparkline_color="#2aa198",
    ),
    "catppuccin": Theme(
        name="catppuccin",
        display_name="Catppuccin",
        primary="#89b4fa",
        secondary="#74c7ec",
        accent="#f5c2e7",
        ok="#a6e3a1",
        warn="#f9e2af",
        crit="#f38ba8",
        border="#89b4fa",
        title="bold #cba6f7",
        header="bold #89b4fa",
        text="#cdd6f4",
        dim="#6c7086",
        bar_low="#a6e3a1",
        bar_mid="#f9e2af",
        bar_high="#f38ba8",
        sparkline_color="#89dceb",
    ),
    "tokyo_night": Theme(
        name="tokyo_night",
        display_name="Tokyo Night",
        primary="#7aa2f7",
        secondary="#7dcfff",
        accent="#bb9af7",
        ok="#9ece6a",
        warn="#e0af68",
        crit="#f7768e",
        border="#7aa2f7",
        title="bold #bb9af7",
        header="bold #7aa2f7",
        text="#c0caf5",
        dim="#565f89",
        bar_low="#9ece6a",
        bar_mid="#e0af68",
        bar_high="#f7768e",
        sparkline_color="#7dcfff",
    ),
    "one_dark": Theme(
        name="one_dark",
        display_name="One Dark",
        primary="#61afef",
        secondary="#56b6c2",
        accent="#c678dd",
        ok="#98c379",
        warn="#e5c07b",
        crit="#e06c75",
        border="#61afef",
        title="bold #c678dd",
        header="bold #61afef",
        text="#abb2bf",
        dim="#5c6370",
        bar_low="#98c379",
        bar_mid="#e5c07b",
        bar_high="#e06c75",
        sparkline_color="#56b6c2",
    ),
    "cyberpunk": Theme(
        name="cyberpunk",
        display_name="Cyberpunk",
        primary="#00ff9f",
        secondary="#00b8ff",
        accent="#ff00a0",
        ok="#00ff9f",
        warn="#ffb800",
        crit="#ff003c",
        border="#00ff9f",
        title="bold #ff00a0",
        header="bold #00ff9f",
        text="#ffffff",
        dim="#666666",
        bar_low="#00ff9f",
        bar_mid="#ffb800",
        bar_high="#ff003c",
        sparkline_color="#00b8ff",
    ),
}

THEME_NAMES = list(THEMES.keys())


def get_theme(name: str) -> Theme:
    """Get a theme by name, falling back to default."""
    return THEMES.get(name, THEMES["default"])


def next_theme(current: str) -> str:
    """Return the next theme name."""
    idx = THEME_NAMES.index(current) if current in THEME_NAMES else 0
    return THEME_NAMES[(idx + 1) % len(THEME_NAMES)]


def prev_theme(current: str) -> str:
    """Return the previous theme name."""
    idx = THEME_NAMES.index(current) if current in THEME_NAMES else 0
    return THEME_NAMES[(idx - 1) % len(THEME_NAMES)]
