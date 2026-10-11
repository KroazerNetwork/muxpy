"""Command Line Interface (CLI) diagnostic tool for muxpy."""

import asyncio
import sys
from .client import TermuxClient

# Ensure UTF-8 output when possible on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


async def run_diagnostics():
    """Print Android device hardware summary."""
    async with TermuxClient() as client:
        env = "Android (Termux)" if client.is_termux else "PC / Host (Mock Mode)"
        print("=" * 50)
        print(f"[*] MUXPY SYSTEM DIAGNOSTICS ({env})")
        print("=" * 50)

        # Battery
        try:
            bat = await client.battery.get_status()
            print(f"[+] Battery     : {bat.percentage}% [{bat.status}] (Health: {bat.health})")
        except Exception as e:
            print(f"[!] Battery     : Error ({e})")

        # Wi-Fi
        try:
            wifi = await client.wifi.get_connection_info()
            if wifi.is_connected:
                print(f"[+] Wi-Fi       : {wifi.ssid} ({wifi.ip}) @ {wifi.link_speed_mbps} Mbps")
            else:
                print(f"[-] Wi-Fi       : Disconnected")
        except Exception as e:
            print(f"[!] Wi-Fi       : Error ({e})")

        # Location
        try:
            loc = await client.location.get_location(timeout=5.0)
            print(f"[+] GPS Location: {loc.latitude:.4f}, {loc.longitude:.4f} (Acc: {loc.accuracy}m)")
        except Exception as e:
            print(f"[-] GPS Location: Unavailable ({e})")

        # Wakelock
        status = "Active" if client.wakelock.is_locked else "Inactive"
        print(f"[*] Wakelock    : {status}")

        # Audio Volume
        try:
            vols = await client.volume.get_volumes()
            v_summary = ", ".join(f"{k}:{v.volume}/{v.max_volume}" for k, v in list(vols.items())[:3])
            print(f"[+] Audio Volume: {v_summary}")
        except Exception as e:
            print(f"[!] Audio Volume: Error ({e})")

        print("=" * 50)


def main():
    """CLI Entrypoint."""
    args = sys.argv[1:]
    command = args[0] if args else "info"

    if command in ("info", "status", "diag"):
        asyncio.run(run_diagnostics())
    elif command in ("--help", "-h", "help"):
        print("muxpy - Ultra-light Termux:API wrapper\n")
        print("Usage:")
        print("  muxpy info       Tampilkan status perangkat & diagnostik")
        print("  muxpy --help     Bantuan perintah")
    else:
        print(f"Perintah tidak dikenal: '{command}'. Ketik 'muxpy --help' untuk bantuan.")


if __name__ == "__main__":
    main()
