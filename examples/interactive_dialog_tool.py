"""Example: Interactive Native Android Dialogs using muxpy.

Prompts user for input using native Android UI dialogs and responds.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from muxpy import TermuxClient


async def main():
    async with TermuxClient() as termux:
        print("Menampilkan dialog teks...")
        name = await termux.dialog.text(title="Identitas Pengguna", hint="Ketik nama Anda...")
        if not name:
            print("Dialog dibatalkan atau kosong.")
            return

        print(f"Nama yang dimasukkan: {name}")

        pilihan = await termux.dialog.radio(
            options=["Mulai Service", "Cek Status Wi-Fi", "Keluar"],
            title="Pilih Aksi",
        )

        if pilihan:
            print(f"Pilihan user: {pilihan.text} (index: {pilihan.index})")
            await termux.toast.show(f"Halo {name}, Anda memilih: {pilihan.text}")


if __name__ == "__main__":
    asyncio.run(main())
