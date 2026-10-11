"""Toast notification API for Termux."""

from __future__ import annotations

from typing import List, Optional

from ..core.executor import AsyncExecutor


class ToastApi:
    """Interface to termux-toast."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def show(
        self,
        text: str,
        short: bool = True,
        background: Optional[str] = None,
        color: Optional[str] = None,
        gravity: Optional[str] = None,
    ) -> None:
        """Display an Android toast popup message.

        :param text: Message to display.
        :param short: True for short duration, False for long.
        :param background: Hex or color name (e.g. '#222222' or 'gray').
        :param color: Text color (e.g. '#FFFFFF' or 'white').
        :param gravity: 'top', 'middle', or 'bottom'.
        """
        args: List[str] = []
        if short:
            args.append("-s")
        if background:
            args.extend(["-b", background])
        if color:
            args.extend(["-c", color])
        if gravity:
            args.extend(["-g", gravity])

        args.append(text)
        await self._executor.run("termux-toast", args=args)
