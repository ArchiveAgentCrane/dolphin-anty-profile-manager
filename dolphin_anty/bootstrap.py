"""Entry/bootstrap layer: wire services, adapters, and the profile pool."""

from __future__ import annotations

import asyncio
import structlog

from dolphin_anty.adapters.dolphin_local_api import DolphinLocalApi
from dolphin_anty.adapters.windows_process import WindowsProcessAdapter
from dolphin_anty.config.settings import Settings, load_settings
from dolphin_anty.services.event_bus import EventBus
from dolphin_anty.services.profile_pool import ProfilePool
from dolphin_anty.services.profile_service import ProfileService
from dolphin_anty.utils.logging import configure_logging

log = structlog.get_logger(__name__)


async def launch_batch(settings: Settings | None = None) -> int:
    """Spin up N profiles from the pool. Returns count actually launched."""
    cfg = settings or load_settings()
    configure_logging(cfg.log_level)

    api = DolphinLocalApi(base_url=cfg.api_base_url, timeout=cfg.api_timeout_s)
    proc = WindowsProcessAdapter(exe_path=cfg.dolphin_exe)
    bus = EventBus()

    service = ProfileService(api=api, process=proc, bus=bus, settings=cfg)
    pool = ProfilePool(service=service, concurrency=cfg.max_concurrency)

    log.info("bootstrap.launch_batch.start", target=cfg.target_profile_count)
    launched = await pool.run(cfg.target_profile_count)
    log.info("bootstrap.launch_batch.done", launched=launched)
    return launched


def main() -> None:
    asyncio.run(launch_batch())


if __name__ == "__main__":
    main()