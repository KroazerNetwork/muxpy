"""Battery API for Termux."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import AsyncIterator, Optional

from ..core.executor import AsyncExecutor


@dataclass(frozen=True)
class BatteryStatus:
    """Represents current device battery information."""
    health: str
    percentage: int
    plugged: str
    status: str
    temperature: float
    current: Optional[int] = None

    @property
    def is_charging(self) -> bool:
        """Return True if the device is currently charging."""
        return self.status.upper() in ("CHARGING", "FULL")

    @property
    def is_plugged(self) -> bool:
        """Return True if connected to AC, USB, or wireless power."""
        return self.plugged.upper() not in ("UNPLUGGED", "NONE", "")


class BatteryApi:
    """Interface to termux-battery-status."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def get_status(self) -> BatteryStatus:
        """Retrieve current battery status from Android."""
        data = await self._executor.run("termux-battery-status", parse_json=True)
        return BatteryStatus(
            health=str(data.get("health", "UNKNOWN")),
            percentage=int(data.get("percentage", 0)),
            plugged=str(data.get("plugged", "UNPLUGGED")),
            status=str(data.get("status", "UNKNOWN")),
            temperature=float(data.get("temperature", 0.0)),
            current=data.get("current"),
        )

    async def monitor(
        self,
        interval_seconds: float = 10.0,
        only_on_change: bool = True,
    ) -> AsyncIterator[BatteryStatus]:
        """Asynchronously stream battery status updates over time."""
        last_percentage: Optional[int] = None
        last_status: Optional[str] = None

        while True:
            current = await self.get_status()
            if not only_on_change or (
                current.percentage != last_percentage or current.status != last_status
            ):
                last_percentage = current.percentage
                last_status = current.status
                yield current
            await asyncio.sleep(interval_seconds)
