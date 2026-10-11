"""Torch (Flashlight) API for Termux."""

from __future__ import annotations

from ..core.executor import AsyncExecutor


class TorchApi:
    """Interface to termux-torch."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor
        self._is_on: bool = False

    @property
    def is_on(self) -> bool:
        """Cached state of the torch (based on client calls)."""
        return self._is_on

    async def on(self) -> None:
        """Turn on the camera flashlight."""
        await self._executor.run("termux-torch", args=["on"])
        self._is_on = True

    async def off(self) -> None:
        """Turn off the camera flashlight."""
        await self._executor.run("termux-torch", args=["off"])
        self._is_on = False

    async def toggle(self) -> bool:
        """Toggle torch state."""
        if self._is_on:
            await self.off()
        else:
            await self.on()
        return self._is_on
