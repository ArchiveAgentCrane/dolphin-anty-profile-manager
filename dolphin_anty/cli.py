"""Typer CLI surface for dolphin-anty-profile-manager."""

from __future__ import annotations

import asyncio

import typer
from rich.console import Console

from dolphin_anty.bootstrap import launch_batch
from dolphin_anty.config.settings import load_settings

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


@app.command("launch")
def launch(
    count: int = typer.Option(10, "--count", "-n", help="Profiles to launch."),
    concurrency: int = typer.Option(4, "--concurrency", "-c"),
) -> None:
    """Launch a batch of Dolphin Anty profiles from the pool."""
    cfg = load_settings().model_copy(update={"target_profile_count": count, "max_concurrency": concurrency})
    launched = asyncio.run(launch_batch(cfg))
    console.print(f"[bold green]launched[/] {launched}/{count} profiles")


@app.command("doctor")
def doctor() -> None:
    """Check local Dolphin Anty API reachability."""
    cfg = load_settings()
    console.print(f"api_base_url = {cfg.api_base_url}")
    console.print(f"dolphin_exe  = {cfg.dolphin_exe}")


if __name__ == "__main__":
    app()