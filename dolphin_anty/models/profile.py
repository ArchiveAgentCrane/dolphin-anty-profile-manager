"""Data models for a Dolphin Anty profile."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class ProfileStatus(StrEnum):
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


class ProxyConfig(BaseModel):
    type: str = Field(pattern=r"^(http|https|socks5)$")
    host: str
    port: int = Field(ge=1, le=65535)
    username: str | None = None
    password: str | None = None


class Profile(BaseModel):
    id: str
    name: str
    status: ProfileStatus = ProfileStatus.IDLE
    proxy: ProxyConfig | None = None
    fingerprint_seed: int
    created_at: datetime
    last_launched_at: datetime | None = None
    tags: list[str] = Field(default_factory=list)