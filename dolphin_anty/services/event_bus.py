"""Tiny in-process pub/sub for audit + telemetry fan-out."""

from __future__ import annotations

import asyncio
from collections.abc import Callable, Awaitable

from dolphin_anty.models.audit_entry import AuditEntry

Handler = Callable[[AuditEntry], Awaitable[None]]


class EventBus:
    def __init__(self) -> None:
        self._subs: list[Handler] = []
        self._lock = asyncio.Lock()

    def subscribe(self, handler: Handler) -> None:
        self._subs.append(handler)

    async def publish(self, entry: AuditEntry) -> None:
        async with self._lock:
            subs = list(self._subs)
        for h in subs:
            try:
                await h(entry)
            except Exception:  # noqa: BLE001 — never let a subscriber kill the bus
                pass