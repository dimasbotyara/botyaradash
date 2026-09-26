"""CLI argument parsing for botyaradash."""

import click

from ui.themes import THEME_NAMES
from ui.layouts import LAYOUT_NAMES
from i18n import SUPPORTED_LANGUAGES


@click.command()
@click.option(
    "--theme",
    type=click.Choice(THEME_NAMES, case_sensitive=False),
    default=None,
    help="Color theme.",
)
@click.option(
    "--lang",
    type=click.Choice(SUPPORTED_LANGUAGES, case_sensitive=False),
    default=None,
    help="Interface language.",
)
@click.option(
    "--layout",
    type=click.Choice(LAYOUT_NAMES, case_sensitive=False),
    default=None,
    help="Dashboard layout mode.",
)
@click.option(
    "--refresh",
    type=float,
    default=None,
    help="Refresh rate in seconds.",
)
@click.option(
    "--export",
    "export_fmt",
    type=click.Choice(["json", "csv"], case_sensitive=False),
    default=None,
    help="Auto-export format.",
)
@click.option(
    "--export-interval",
    type=int,
    default=None,
    help="Auto-export interval in seconds.",
)
@click.option(
    "--no-gpu",
    is_flag=True,
    default=False,
    help="Disable GPU monitoring.",
)
@click.option(
    "--processes",
    type=int,
    default=None,
    help="Number of top processes to show.",
)
@click.option(
    "--bar-width",
    type=int,
    default=None,
    help="Progress bar width.",
)
@click.option(
    "--save-config",
    is_flag=True,
    default=False,
    help="Save current options as default config.",
)
def main(
    theme,
    lang,
    layout,
    refresh,
    export_fmt,
    export_interval,
    no_gpu,
    processes,
    bar_width,
    save_config,
):
    """botyaradash — A powerful system monitoring dashboard."""
    from app import App

    overrides = {}
    if theme:
        overrides["theme"] = theme
    if lang:
        overrides["language"] = lang
    if layout:
        overrides["layout"] = layout
    if refresh:
        overrides["refresh_rate"] = refresh
    if export_fmt:
        overrides["export_format"] = export_fmt
    if export_interval:
        overrides["export_interval"] = export_interval
    if no_gpu:
        overrides["show_gpu"] = False
    if processes:
        overrides["process_count"] = processes
    if bar_width:
        overrides["bar_width"] = bar_width

    app = App(overrides=overrides, save_on_exit=save_config)
    app.run()
