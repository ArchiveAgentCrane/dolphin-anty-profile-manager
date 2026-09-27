"""Business logic: launch / stop a single Dolphin Anty profile with audit."""

from __future__ import annotations

import structlog

from dolphin_anty.adapters.dolphin_local_api import DolphinLocalApi
from dolphin_anty.adapters.windows_process import WindowsProcessAdapter
from dolphin_anty.config.settings import Settings
from dolphin_anty.models.audit_entry import AuditEntry
from dolphin_anty.services.event_bus import EventBus

log = structlog.get_logger(__name__)


class ProfileService:
    def __init__(
        self,
        api: DolphinLocalApi,
        process: WindowsProcessAdapter,
        bus: EventBus,
        settings: Settings,
    ) -> None:
        self._api = api
        self._proc = process
        self._bus = bus
        self._cfg = settings

    async def launch_one(self, profile_id: str) -> bool:
        try:
            profile = await self._api.start_profile(profile_id)
            await self._bus.publish(AuditEntry(profile_id=profile_id, action="launch", ok=True))
            log.info("profile.launch.ok", profile_id=profile_id, status=profile.status)
            return True
        except Exception as exc:  # noqa: BLE001
            await self._bus.publish(
                AuditEntry(profile_id=profile_id, action="launch", ok=False, detail=str(exc))
            )
            log.warning("profile.launch.fail", profile_id=profile_id, err=str(exc))
            return False

    async def stop_one(self, profile_id: str) -> bool:
        try:
            await self._api.stop_profile(profile_id)
            await self._bus.publish(AuditEntry(profile_id=profile_id, action="stop", ok=True))
            return True
        except Exception as exc:  # noqa: BLE001
            await self._bus.publish(
                AuditEntry(profile_id=profile_id, action="stop", ok=False, detail=str(exc))
            )
            return False