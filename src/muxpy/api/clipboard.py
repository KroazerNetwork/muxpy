"""Clipboard API for Termux."""

from __future__ import annotations

from ..core.executor import AsyncExecutor


class ClipboardApi:
    """Interface to termux-clipboard-get and termux-clipboard-set."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def get(self) -> str:
        """Get current system clipboard text."""
        result = await self._executor.run("termux-clipboard-get")
        return str(result)

    async def set(self, text: str) -> None:
        """Set system clipboard text."""
        await self._executor.run("termux-clipboard-set", input_data=text)
