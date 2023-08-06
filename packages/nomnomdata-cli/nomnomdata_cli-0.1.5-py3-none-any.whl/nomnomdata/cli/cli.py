import logging
import platform
import sys
from pathlib import Path

import click
import coloredlogs
from click_plugins import with_plugins
from pkg_resources import iter_entry_points
from rich import box, print
from rich.panel import Panel
from rich.table import Table

from . import __version__


@with_plugins(iter_entry_points("nomnomdata.cli_plugins"))
@click.group()
@click.version_option(version=__version__, prog_name="nomnomdata-cli")
@click.option(
    "-l",
    "--loglevel",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
)
@click.pass_context
def cli(ctx, loglevel=None):
    """Nom Nom Data Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj["LOG_LEVEL"] = loglevel
    coloredlogs.install(
        level=logging.getLevelName(loglevel),
        stream=sys.stdout,
        fmt="%(msecs)d:%(levelname)s:%(name)s:%(message)s",
    )
    dists = [
        f"{x.dist.project_name}-{x.dist.version}"
        for x in iter_entry_points("nomnomdata.cli_plugins")
    ]

    table = Table(
        "",
        box=box.MINIMAL,
        show_header=False,
        pad_edge=True,
        show_edge=False,
    )
    msg = [
        ("Version", __version__),
        ("Directory", str(Path.cwd())),
        ("Platform", sys.platform),
        ("Python", platform.python_version()),
        ("Plugins", " ".join(dists)),
    ]
    table.add_column()
    for row in msg:
        table.add_row(*row)
    print(
        Panel(
            table,
            box=box.HEAVY,
            title_align="left",
            title="[orange1]Nom Nom Data CLI[/orange1]",
        )
    )
