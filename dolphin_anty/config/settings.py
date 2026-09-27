"""Pydantic settings for the profile manager."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field


class Settings(BaseModel):
    api_base_url: str = Field(default="http://127.0.0.1:3001")
    api_timeout_s: float = Field(default=15.0, gt=0)
    dolphin_exe: Path = Field(default=Path("C:/Program Files/Dolphin Anty/DolphinAnty.exe"))
    target_profile_count: int = Field(default=10, ge=1, le=2000)
    max_concurrency: int = Field(default=4, ge=1, le=64)
    profile_store_dir: Path = Field(default=Path("./profile_store"))
    log_level: str = Field(default="INFO")
    log_proxy_creds: bool = Field(default=False)
    launch_timeout_s: float = Field(default=45.0, gt=0)


def load_settings() -> Settings:
    """Env-var override loader. Prefix: DAPM_ (e.g. DAPM_MAX_CONCURRENCY=8)."""
    raw: dict[str, object] = {}
    for name in Settings.model_fields:
        env_key = f"DAPM_{name.upper()}"
        if env_key in os.environ:
            raw[name] = os.environ[env_key]
    return Settings(**raw)