"""Real-world example: Home IoT sensor telemetry with muxpy.

This example demonstrates using an Android device as a lightweight IoT node:
- Reads environment-adjacent hardware data (light sensor, battery temperature, Wi-Fi signal)
- Formats and displays a live dashboard in the terminal
- Streams readings on a continuous async loop with configurable interval
- Shows how to combine multiple muxpy APIs in a single async context

Usage (Termux or Mock PC):
    python iot_telemetry_dashboard.py
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from muxpy import TermuxClient


def rssi_bar(rssi: int) -> str:
    """Convert RSSI value to visual signal strength bar."""
    if rssi >= -50:
        return "[#####] Excellent"
    elif rssi >= -60:
        return "[####.] Good"
    elif rssi >= -70:
        return "[###..] Fair"
    elif rssi >= -80:
        return "[##...] Weak"
    else:
        return "[#....] Poor"


async def display_telemetry(client: TermuxClient) -> None:
    """Fetch and print current device telemetry."""
    bat = await client.battery.get_status()
    wifi = await client.wifi.get_connection_info()
    loc = await client.location.get_location(provider="network", timeout=8.0)
    vols = await client.volume.get_volumes()
    music_vol = vols.get("music")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'=' * 55}")
    print(f"  MUXPY IoT Node Telemetry    [{now}]")
    print(f"{'=' * 55}")
    print(f"  Battery    : {bat.percentage:>3}%  [{bat.status}]  Temp: {bat.temperature:.1f}C")
    if wifi.is_connected:
        print(f"  Wi-Fi      : {wifi.ssid}  |  {rssi_bar(wifi.rssi)}  ({wifi.rssi} dBm)")
        print(f"               IP: {wifi.ip}  |  {wifi.link_speed_mbps} Mbps  |  {wifi.frequency_mhz} MHz")
    else:
        print("  Wi-Fi      : Disconnected")
    print(f"  GPS        : {loc.latitude:.5f}, {loc.longitude:.5f}  (acc: {loc.accuracy:.0f}m)")
    if music_vol:
        print(f"  Volume     : {music_vol.percentage:.0f}%  ({music_vol.volume}/{music_vol.max_volume})")
    print(f"{'=' * 55}")


async def main() -> None:
    refresh_interval = 15  # seconds

    async with TermuxClient() as client:
        print(f"[muxpy] IoT Dashboard running (refresh: {refresh_interval}s). Ctrl+C to stop.")

        async with client.wakelock.keep_awake():
            while True:
                try:
                    await display_telemetry(client)
                except Exception as exc:
                    print(f"[!] Telemetry read error: {exc}")
                await asyncio.sleep(refresh_interval)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[muxpy] Dashboard stopped.")
