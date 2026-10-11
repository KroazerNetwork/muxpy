"""Wi-Fi API for Termux."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from ..core.executor import AsyncExecutor


@dataclass(frozen=True)
class WifiConnectionInfo:
    """Current connected Wi-Fi network information."""
    ssid: str
    bssid: str
    ip: str
    rssi: int
    link_speed_mbps: int
    frequency_mhz: int
    supplicant_state: str
    ssid_hidden: bool = False
    mac_address: Optional[str] = None
    network_id: Optional[int] = None

    @property
    def is_connected(self) -> bool:
        """True if Wi-Fi state is COMPLETED and valid IP assigned."""
        return self.supplicant_state.upper() == "COMPLETED" and bool(self.ip)


class WifiApi:
    """Interface to termux-wifi-* commands."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def get_connection_info(self) -> WifiConnectionInfo:
        """Get information about the currently connected Wi-Fi network."""
        data = await self._executor.run("termux-wifi-connectioninfo", parse_json=True)
        return WifiConnectionInfo(
            ssid=str(data.get("ssid", "")).strip('"'),
            bssid=str(data.get("bssid", "")),
            ip=str(data.get("ip", "")),
            rssi=int(data.get("rssi", -100)),
            link_speed_mbps=int(data.get("link_speed_mbps", 0)),
            frequency_mhz=int(data.get("frequency_mhz", 0)),
            supplicant_state=str(data.get("supplicant_state", "DISCONNECTED")),
            ssid_hidden=bool(data.get("ssid_hidden", False)),
            mac_address=data.get("mac_address"),
            network_id=data.get("network_id"),
        )

    async def scan(self) -> List[dict[str, Any]]:
        """Scan for nearby Wi-Fi networks (requires Location permission on Android)."""
        result = await self._executor.run("termux-wifi-scaninfo", parse_json=True)
        return result if isinstance(result, list) else []

    async def enable(self, state: bool = True) -> None:
        """Turn Wi-Fi on or off."""
        arg = "true" if state else "false"
        await self._executor.run("termux-wifi-enable", args=[arg])
