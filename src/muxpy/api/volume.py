"""Volume & Audio stream API for Termux."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Literal

from ..core.executor import AsyncExecutor

StreamType = Literal["call", "system", "ring", "music", "alarm", "notification"]


@dataclass(frozen=True)
class VolumeStream:
    """Volume level for a specific Android audio stream."""
    stream: str
    volume: int
    max_volume: int

    @property
    def percentage(self) -> float:
        """Volume as a percentage (0.0 to 100.0)."""
        if self.max_volume == 0:
            return 0.0
        return round((self.volume / self.max_volume) * 100.0, 1)


class VolumeApi:
    """Interface to termux-volume for inspecting and controlling system audio."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def get_volumes(self) -> Dict[str, VolumeStream]:
        """Get current volume levels for all audio streams."""
        data = await self._executor.run("termux-volume", parse_json=True)
        results: Dict[str, VolumeStream] = {}
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    name = str(item.get("stream", ""))
                    results[name] = VolumeStream(
                        stream=name,
                        volume=int(item.get("volume", 0)),
                        max_volume=int(item.get("max_volume", 1)),
                    )
        return results

    async def set_volume(self, stream: StreamType | str, volume: int) -> None:
        """Set volume level for a specific audio stream.

        :param stream: Audio stream ('call', 'system', 'ring', 'music', 'alarm', 'notification').
        :param volume: Desired volume level integer.
        """
        await self._executor.run("termux-volume", args=[stream, str(volume)])
