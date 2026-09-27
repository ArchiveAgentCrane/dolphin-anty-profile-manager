"""Adapter for the Dolphin Anty local desktop HTTP API (127.0.0.1:3001)."""

from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from dolphin_anty.models.profile import Profile, ProfileStatus


class DolphinLocalApi:
    def __init__(self, base_url: str, timeout: float = 15.0) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    @retry(stop=stop_after_attempt(4), wait=wait_exponential_jitter(0.2, 2.0))
    async def start_profile(self, profile_id: str) -> Profile:
        r = await self._client.get(f"/v1.0/browser_profiles/{profile_id}/start")
        r.raise_for_status()
        payload = r.json().get("data", {})
        return Profile(
            id=profile_id,
            name=payload.get("name", profile_id),
            status=ProfileStatus.RUNNING,
            fingerprint_seed=int(payload.get("fingerprint_seed", 0)),
            created_at=__import__("datetime").datetime.now(),
        )

    @retry(stop=stop_after_attempt(4), wait=wait_exponential_jitter(0.2, 2.0))
    async def stop_profile(self, profile_id: str) -> None:
        r = await self._client.get(f"/v1.0/browser_profiles/{profile_id}/stop")
        r.raise_for_status()

    async def list_profiles(self) -> list[dict]:
        r = await self._client.get("/v1.0/browser_profiles")
        r.raise_for_status()
        return r.json().get("data", [])

    async def aclose(self) -> None:
        await self._client.aclose()