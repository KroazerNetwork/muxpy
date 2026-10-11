"""Location (GPS & Network) API for Termux."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..core.executor import AsyncExecutor


@dataclass(frozen=True)
class LocationInfo:
    """Geographic location coordinates and metadata."""
    latitude: float
    longitude: float
    altitude: float
    accuracy: float
    bearing: float
    speed: float
    provider: str
    vertical_accuracy: Optional[float] = None
    elapsed_ms: Optional[int] = None


class LocationApi:
    """Interface to termux-location for GPS and network location queries."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def get_location(
        self,
        provider: str = "gps",
        request_type: str = "once",
        timeout: float = 30.0,
    ) -> LocationInfo:
        """Get current geographical location of the device.

        :param provider: Location provider ('gps', 'network', 'passive').
        :param request_type: 'once' (fresh fix) or 'last' (cached fix).
        :param timeout: Command timeout in seconds (GPS fix can take some seconds).
        """
        args: List[str] = ["-p", provider, "-r", request_type]
        data = await self._executor.run(
            "termux-location",
            args=args,
            timeout=timeout,
            parse_json=True,
        )

        return LocationInfo(
            latitude=float(data.get("latitude", 0.0)),
            longitude=float(data.get("longitude", 0.0)),
            altitude=float(data.get("altitude", 0.0)),
            accuracy=float(data.get("accuracy", 0.0)),
            bearing=float(data.get("bearing", 0.0)),
            speed=float(data.get("speed", 0.0)),
            provider=str(data.get("provider", provider)),
            vertical_accuracy=data.get("vertical_accuracy"),
            elapsed_ms=data.get("elapsedMs"),
        )
