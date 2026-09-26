"""Layout definitions for botyaradash."""

LAYOUT_NAMES = ["full", "compact", "minimal"]


def next_layout(current: str) -> str:
    """Return the next layout name."""
    idx = LAYOUT_NAMES.index(current) if current in LAYOUT_NAMES else 0
    return LAYOUT_NAMES[(idx + 1) % len(LAYOUT_NAMES)]
