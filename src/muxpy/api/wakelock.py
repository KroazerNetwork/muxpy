"""Wakelock API for Termux to keep CPU alive in background."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from ..core.executor import AsyncExecutor


class WakelockApi:
    """Interface to termux-wake-lock and termux-wake-unlock.

    Ensures the device CPU stays active even when the screen is turned off,
    preventing Android OS from killing long-running bots and daemons.
    """

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor
        self._is_locked: bool = False

    @property
    def is_locked(self) -> bool:
        """True if wakelock is currently held by this client."""
        return self._is_locked

    async def acquire(self) -> None:
        """Acquire CPU wakelock to prevent system sleep."""
        await self._executor.run("termux-wake-lock")
        self._is_locked = True

    async def release(self) -> None:
        """Release CPU wakelock and restore normal power management."""
        await self._executor.run("termux-wake-unlock")
        self._is_locked = False

    @asynccontextmanager
    async def keep_awake(self) -> AsyncIterator[None]:
        """Asynchronous context manager to hold wakelock during an operation.

        Example:
            async with client.wakelock.keep_awake():
                await run_long_bot_process()
        """
        await self.acquire()
        try:
            yield
        finally:
            await self.release()
