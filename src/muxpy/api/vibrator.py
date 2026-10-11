"""Vibration API for Termux."""

from __future__ import annotations

from typing import List

from ..core.executor import AsyncExecutor


class VibratorApi:
    """Interface to termux-vibrate."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def vibrate(self, duration_ms: int = 1000, force: bool = False) -> None:
        """Vibrate device for given duration in milliseconds."""
        args: List[str] = ["-d", str(duration_ms)]
        if force:
            args.append("-f")
        await self._executor.run("termux-vibrate", args=args)
