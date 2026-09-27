"""Thin handler: single-profile launch request → service call."""

from __future__ import annotations

from dolphin_anty.services.profile_service import ProfileService


class LaunchHandler:
    def __init__(self, service: ProfileService) -> None:
        self._svc = service

    async def handle(self, profile_id: str) -> bool:
        return await self._svc.launch_one(profile_id)