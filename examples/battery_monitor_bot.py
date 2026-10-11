"""Example: Autonomous Battery Monitor using muxpy.

Monitors battery state and triggers Android notifications & TTS alerts
when battery level drops or charger is unplugged.
"""

import asyncio
import sys
from pathlib import Path

# Add src directory if running locally
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from muxpy import TermuxClient


async def main():
    async with TermuxClient() as termux:
        print("Mengecek status baterai...")
        status = await termux.battery.get_status()
        print(f"Persentase: {status.percentage}%")
        print(f"Kesehatan: {status.health}")
        print(f"Status Pengisian: {status.status} (Plugged: {status.plugged})")

        # Tampilkan toast
        await termux.toast.show(f"Baterai: {status.percentage}% ({status.status})")

        # Jika baterai di bawah 20% dan tidak sedang dicas, kirim notifikasi & peringatan suara
        if status.percentage <= 20 and not status.is_charging:
            print("Peringatan: Baterai lemah!")
            await (
                termux.notification.builder()
                .id(99)
                .title("Baterai Lemah!")
                .content(f"Sisa baterai tinggal {status.percentage}%. Segera hubungkan charger.")
                .priority("high")
                .sound(True)
                .vibrate("500,200,500")
                .send()
            )
            await termux.tts.speak(f"Perhatian, sisa baterai tinggal {status.percentage} persen")


if __name__ == "__main__":
    asyncio.run(main())
