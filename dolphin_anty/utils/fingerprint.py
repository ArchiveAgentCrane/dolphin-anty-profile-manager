"""Deterministic per-profile fingerprint seed derivation."""

from __future__ import annotations

import hashlib


def stable_seed(profile_id: str, salt: str = "dapm-v1") -> int:
    """Return a stable 31-bit seed for a profile id."""
    h = hashlib.blake2s(f"{salt}:{profile_id}".encode(), digest_size=4).digest()
    return int.from_bytes(h, "big") & 0x7FFF_FFFF