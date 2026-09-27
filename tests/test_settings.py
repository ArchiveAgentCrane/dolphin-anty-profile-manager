"""Env override smoke tests for Settings."""

from __future__ import annotations

import os
from pathlib import Path

from dolphin_anty.config.settings import load_settings


def test_defaults_are_loopback_only() -> None:
    for k in list(os.environ):
        if k.startswith("DAPM_"):
            del os.environ[k]
    cfg = load_settings()
    assert cfg.api_base_url.startswith("http://127.0.0.1")
    assert cfg.max_concurrency >= 1


def test_env_override(monkeypatch) -> None:
    monkeypatch.setenv("DAPM_MAX_CONCURRENCY", "12")
    monkeypatch.setenv("DAPM_PROFILE_STORE_DIR", "D:/profiles")
    cfg = load_settings()
    assert cfg.max_concurrency == 12
    assert cfg.profile_store_dir == Path("D:/profiles")
</parameter>
</invoke>