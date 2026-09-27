"""Thin handler: single-profile stop request → service call."""

from __future__ import annotations

from dolphin_anty.services.profile_service import ProfileService


class StopHandler:
    def __init__(self, service: ProfileService) -> None:
        self._svc = service

    async def handle(self, profile_id: str) -> bool:
        return await self._svc.stop_one(profile_id)