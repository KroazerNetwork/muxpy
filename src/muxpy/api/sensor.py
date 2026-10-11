"""Sensors API for Termux."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..core.executor import AsyncExecutor


class SensorApi:
    """Interface to termux-sensor."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def list_sensors(self) -> List[str]:
        """List all available sensor names on this device."""
        data = await self._executor.run("termux-sensor", args=["-l"], parse_json=True)
        if isinstance(data, dict):
            return data.get("sensors", [])
        elif isinstance(data, list):
            return [str(s) for s in data]
        return []

    async def read_once(self, sensor_name: str, delay_ms: Optional[int] = None) -> Dict[str, Any]:
        """Take a single reading from a specified sensor.

        :param sensor_name: Sensor name from list_sensors() (e.g. 'light', 'gravity').
        :param delay_ms: Delay in milliseconds between sensor events.
        """
        args = ["-s", sensor_name, "-n", "1"]
        if delay_ms is not None:
            args.extend(["-d", str(delay_ms)])

        data = await self._executor.run("termux-sensor", args=args, parse_json=True)
        if isinstance(data, dict):
            return data
        return {}

    async def cleanup(self) -> None:
        """Release all active sensor listeners."""
        await self._executor.run("termux-sensor", args=["-c"])
