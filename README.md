# muxpy ⚡

> Ultra-light, modern, and asynchronous Python wrapper for **Termux:API** on Android.

Bebas *blocking*, terintegrasi mulus dengan `asyncio`, bot frameworks (Telegram/Discord/WhatsApp), dan dilengkapi mode simulasi (mock) sehingga bisa dikembangkan dan di-test langsung dari PC/laptop sebelum dideploy ke Android.

> 📖 **Catatan Dokumentasi:**
> Untuk membaca latar belakang masalah, visi, arsitektur, dan tujuan lengkap proyek ini, silakan baca dokumen terpisah: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md).

---

## 📦 Prasyarat di Termux (Android)

Pastikan paket `termux-api` dan aplikasi companion sudah terpasang:
```bash
pkg update && pkg install python termux-api
```
*Catatan: Pastikan juga aplikasi Android **Termux:API** telah diinstal dari F-Droid / GitHub Releases dan izin telah diberikan.*

---

## ⚡ Instalasi

```bash
pip install .
```
*(Atau clone repo ini dan import folder `src` langsung ke dalam skrip Anda).*

---

## 🛠️ Quickstart

### 1. Cek Status Baterai & Notifikasi Cepat
```python
import asyncio
from muxpy import TermuxClient

async def main():
    async with TermuxClient() as termux:
        # Dapatkan status baterai berformat strongly-typed
        battery = await termux.battery.get_status()
        print(f"Baterai: {battery.percentage}% | Mengisi: {battery.is_charging}")

        # Tampilkan pop-up Toast di Android
        await termux.toast.show(f"Sisa baterai: {battery.percentage}%")

        # Kirim notifikasi Android dengan Builder Pattern
        await (
            termux.notification.builder()
            .id(100)
            .title("Server Alert")
            .content(f"Perangkat aktif pada daya {battery.percentage}%")
            .priority("high")
            .sound(True)
            .send()
        )

asyncio.run(main())
```

### 2. Dialog Interaktif Native Android
```python
import asyncio
from muxpy import TermuxClient

async def main():
    async with TermuxClient() as termux:
        # Membuka pop-up input teks native Android
        nama = await termux.dialog.text(title="Setup Bot", hint="Masukkan nama bot...")
        print(f"Nama bot: {nama}")

        # Pop-up konfirmasi Yes/No
        setuju = await termux.dialog.confirm(title="Jalankan daemon sekarang?")
        if setuju:
            print("Daemon dijalankan...")

asyncio.run(main())
```

### 3. Kontrol Perangkat Lainnya
```python
# Senter / Flashlight
await termux.torch.on()
await termux.torch.off()
await termux.torch.toggle()

# Getar (Haptic Feedback)
await termux.vibrator.vibrate(duration_ms=500)

# Suara (Text-to-Speech)
await termux.tts.speak("Sistem berhasil dimulai", language="id")

# Clipboard
await termux.clipboard.set("Token rahasia berhasil disalin")
isi_clip = await termux.clipboard.get()

# Status Wi-Fi
wifi = await termux.wifi.get_connection_info()
print(f"SSID: {wifi.ssid}, IP: {wifi.ip}, Speed: {wifi.link_speed_mbps} Mbps")
```

---

## 🧪 Pengujian & Mock Mode (Bisa Dijalankan di Windows/Mac/Linux)

Library ini otomatis mendeteksi jika dijalankan di luar Termux, atau Anda dapat mengaktifkannya secara eksplisit untuk unit testing:

```python
from muxpy import TermuxClient

# Mode mock otomatis aktif di PC non-Android
client = TermuxClient(mock_mode=True)
```

Jalankan test suite menggunakan Python bawaan:
```bash
python -m unittest tests/test_client.py
```

---

## 📂 Struktur Project

```
├── PROJECT_OVERVIEW.md      # Dokumen latar belakang, tujuan, dan visi proyek
├── README.md                # Panduan instalasi dan penggunaan cepat
├── pyproject.toml           # Konfigurasi package & build
├── src/
│   └── muxpy/
│       ├── __init__.py
│       ├── client.py        # Facade utama (TermuxClient)
│       ├── core/            # Async executor & custom exceptions
│       └── api/             # Modul battery, notification, dialog, wifi, dll.
├── examples/                # Contoh skrip otomatisasi siap pakai
└── tests/                   # Unit test suite
```

---

## 📜 Lisensi
MIT License.
