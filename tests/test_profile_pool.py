"""Pool concurrency + launch accounting tests."""

from __future__ import annotations

import pytest

from dolphin_anty.services.profile_pool import ProfilePool


class FakeService:
    def __init__(self) -> None:
        self.launched: list[str] = []
        self.fail_at: set[int] = set()

    async def launch_one(self, profile_id: str) -> bool:
        idx = int(profile_id.split("-")[-1])
        if idx in self.fail_at:
            return False
        self.launched.append(profile_id)
        return True


@pytest.mark.asyncio
async def test_pool_launches_all_when_healthy() -> None:
    svc = FakeService()
    pool = ProfilePool(service=svc, concurrency=4)  # type: ignore[arg-type]
    launched = await pool.run(25)
    assert launched == 25
    assert len(svc.launched) == 25


@pytest.mark.asyncio
async def test_pool_counts_only_successes() -> None:
    svc = FakeService()
    svc.fail_at = {3, 7, 11}
    pool = ProfilePool(service=svc, concurrency=2)  # type: ignore[arg-type]
    launched = await pool.run(20)
    assert launched == 17