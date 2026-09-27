"""Windows process adapter — spawn / kill DolphinAnty.exe for legacy paths."""

from __future__ import annotations

import asyncio
import shlex
import sys
from pathlib import Path


class WindowsProcessAdapter:
    def __init__(self, exe_path: Path) -> None:
        self._exe = Path(exe_path)

    async def spawn_profile(self, profile_id: str) -> int:
        if sys.platform != "win32":
            raise RuntimeError("windows_process adapter is win32-only")
        args = [str(self._exe), "--profile", shlex.quote(profile_id)]
        proc = await asyncio.create_subprocess_exec(*args)
        return proc.pid

    async def is_alive(self, pid: int) -> bool:
        if sys.platform != "win32":
            return False
        try:
            proc = await asyncio.create_subprocess_exec(
                "tasklist", "/FI", f"PID eq {pid}", "/NH",
                stdout=asyncio.subprocess.PIPE,
            )
            out, _ = await proc.communicate()
            return b"No tasks" not in out
        except OSError:
            return False