"""Bounded-concurrency pool driving N parallel profile launches."""

from __future__ import annotations

import asyncio

import structlog

from dolphin_anty.services.profile_service import ProfileService

log = structlog.get_logger(__name__)


class ProfilePool:
    def __init__(self, service: ProfileService, concurrency: int) -> None:
        self._svc = service
        self._sem = asyncio.Semaphore(concurrency)
        self._concurrency = concurrency

    async def _guarded(self, idx: int) -> bool:
        async with self._sem:
            pid = f"auto-{idx:05d}"
            return await self._svc.launch_one(pid)

    async def run(self, count: int) -> int:
        log.info("pool.run.start", count=count, concurrency=self._concurrency)
        results = await asyncio.gather(*(self._guarded(i) for i in range(count)))
        return sum(1 for r in results if r)