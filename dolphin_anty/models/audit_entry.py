"""Append-only audit record for every profile mutation."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field


class AuditEntry(BaseModel):
    ts: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    profile_id: str
    action: str
    ok: bool
    detail: str | None = None

    def to_line(self) -> str:
        return self.model_dump_json()