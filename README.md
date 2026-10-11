# muxpy ⚡

[![CI](https://github.com/KroazerNetwork/muxpy/actions/workflows/ci.yml/badge.svg)](https://github.com/KroazerNetwork/muxpy/actions)
![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Typing](https://img.shields.io/badge/typing-PEP%20561-informational)

> Ultra-light, modern, and asynchronous Python framework for **Termux:API** on Android.

Bebas *blocking*, terintegrasi mulus dengan `asyncio`, bot frameworks (Telegram/Discord/WhatsApp), dan dilengkapi **Mock Simulation Engine** sehingga Anda dapat menguji dan mengembangkan seluruh fungsionalitas Android langsung dari PC/laptop sebelum dideploy ke ponsel.

> 📖 **Dokumentasi Visi & Arsitektur:**  
> Untuk membaca latar belakang teknis, arsitektur internal, dan sasaran proyek, silakan buka: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md).

---

## 📑 Daftar Isi
- [Fitur Utama](#-fitur-utama)
- [Prasyarat di Android (Termux)](#-prasyarat-di-android-termux)
- [Instalasi](#-instalasi)
- [CLI Diagnostics](#-cli-diagnostics)
- [Quickstart & Contoh Kode](#-quickstart--contoh-kode)
  - [1. Status Baterai & Notifikasi](#1-status-baterai--notifikasi)
  - [2. CPU Wakelock (Penting untuk Bot Background)](#2-cpu-wakelock-penting-untuk-bot-background)
  - [3. Dialog Interaktif Native Android](#3-dialog-interaktif-native-android)
  - [4. GPS & Lokasi](#4-gps--lokasi)
  - [5. SMS & Pesan](#5-sms--pesan)
  - [6. Kamera & Foto](#6-kamera--foto)
  - [7. Kontrol Audio & Volume](#7-kontrol-audio--volume)
  - [8. Fitur Perangkat Lainnya (Senter, Getar, TTS, Clipboard)](#8-fitur-perangkat-lainnya)
- [Tabel API Reference](#-tabel-api-reference)
- [Mock Engine (Pengujian di PC/Mac)](#-mock-engine-pengujian-di-pcmac)
- [Lisensi](#-lisensi)

---

## ✨ Fitur Utama
* **Non-Blocking Async First:** Seluruh eksekusi berjalan di atas `asyncio.subprocess`, tidak pernah mengunci event loop bot Telegram, Discord, atau server FastAPI Anda.
* **CPU Wakelock Manager:** Mencegah Android mematikan proses background/bot saat layar ponsel mati (`async with client.wakelock.keep_awake():`).
* **Strongly-Typed (PEP 561):** Dilengkapi model dataclass lengkap (`BatteryStatus`, `LocationInfo`, `SmsMessage`, dll.) untuk autocompletion instan di VS Code, PyCharm, dan Neovim.
* **Mock Simulation:** Berjalan otomatis dengan data sintetis jika dieksekusi di Windows/Linux/macOS tanpa binary Termux.
* **CLI Tool Bawaan:** Periksa status sensor & perangkat langsung dengan perintah `muxpy info`.

---

## 📦 Prasyarat di Android (Termux)

Pastikan paket `termux-api` dan aplikasi Android companion sudah terpasang:
```bash
pkg update && pkg install python termux-api
```
*(Catatan: Pasang aplikasi Android **Termux:API** dari F-Droid atau GitHub Releases dan izinkan permission yang diminta).*

---

## ⚡ Instalasi

```bash
pip install git+https://github.com/KroazerNetwork/muxpy.git
```
*Atau clone repository ini dan install dalam editable mode:*
```bash
git clone https://github.com/KroazerNetwork/muxpy.git
cd muxpy
pip install -e .
```

---

## 🖥️ CLI Diagnostics

`muxpy` dilengkapi tool diagnostik baris perintah:

```bash
# Periksa status seluruh perangkat & konektivitas
muxpy info

# Atau menggunakan modul Python langsung
python -m muxpy info
```

---

## 🛠️ Quickstart & Contoh Kode

### 1. Status Baterai & Notifikasi
```python
import asyncio
from muxpy import TermuxClient

async def main():
    async with TermuxClient() as client:
        # Baca status baterai
        battery = await client.battery.get_status()
        print(f"Level: {battery.percentage}% | Charging: {battery.is_charging}")

        # Kirim notifikasi Android dengan builder pattern
        await (
            client.notification.builder()
            .id(101)
            .title("Bot Alert")
            .content(f"Perangkat aktif pada daya {battery.percentage}%")
            .priority("high")
            .sound(True)
            .send()
        )

asyncio.run(main())
```

### 2. CPU Wakelock (Penting untuk Bot Background)
Android secara agresif mematikan script background saat layar mati. Gunakan context manager wakelock untuk menjaga CPU tetap aktif:
```python
import asyncio
from muxpy import TermuxClient

async def background_worker():
    async with TermuxClient() as client:
        # Menjaga CPU tetap hidup selama blok kode berjalan
        async with client.wakelock.keep_awake():
            print("CPU Wakelock aktif: Script aman dari pembunuhan proses Android")
            await asyncio.sleep(60) # Menjalankan tugas panjang / loop bot

asyncio.run(background_worker())
```

### 3. Dialog Interaktif Native Android
```python
async with TermuxClient() as client:
    # Dialog teks
    nama = await client.dialog.text(title="Setup", hint="Masukkan username...")
    
    # Dialog pilihan radio
    pilihan = await client.dialog.radio(
        options=["Server 1", "Server 2", "Batal"],
        title="Pilih Target Server"
    )
    if pilihan:
        print(f"Pilihan: {pilihan.text}")
```

### 4. GPS & Lokasi
```python
async with TermuxClient() as client:
    loc = await client.location.get_location(provider="gps")
    print(f"Koordinat: {loc.latitude}, {loc.longitude} (Akurasi: {loc.accuracy}m)")
```

### 5. SMS & Pesan
```python
async with TermuxClient() as client:
    # Kirim SMS
    await client.sms.send(phone_number="+628123456789", text="Server restarted.")

    # Baca pesan masuk terakhir
    inbox = await client.sms.list_messages(limit=5)
    for msg in inbox:
        print(f"Dari: {msg.number} | Pesan: {msg.body}")
```

### 6. Kamera & Foto
```python
async with TermuxClient() as client:
    # Ambil foto dari kamera belakang (ID 0)
    await client.camera.take_photo(output_path="/sdcard/DCIM/capture.jpg", camera_id=0)
```

### 7. Kontrol Audio & Volume
```python
async with TermuxClient() as client:
    volumes = await client.volume.get_volumes()
    print(f"Volume Musik: {volumes['music'].percentage}%")

    # Atur volume media
    await client.volume.set_volume("music", 12)
```

### 8. Fitur Perangkat Lainnya
```python
async with TermuxClient() as client:
    # Senter / Flashlight
    await client.torch.on()
    await client.torch.toggle()

    # Getar (Haptic Feedback)
    await client.vibrator.vibrate(duration_ms=500)

    # Text-to-Speech (Suara)
    await client.tts.speak("Sistem berhasil diaktifkan", language="id")

    # Clipboard
    await client.clipboard.set("Teks tersimpan")
    clip = await client.clipboard.get()
```

---

## 📊 Tabel API Reference

| Modul | Method Utama | Deskripsi |
| :--- | :--- | :--- |
| `client.battery` | `get_status()`, `monitor()` | Status persentase, suhu, dan event loop monitor daya |
| `client.wakelock` | `acquire()`, `release()`, `keep_awake()` | Pengunci CPU agar proses background tidak mati |
| `client.notification`| `builder()`, `show()`, `remove()` | Notifikasi rich dengan action button & vibration pattern |
| `client.dialog` | `text()`, `confirm()`, `radio()`, `checkbox()` | GUI pop-up dialog interaktif bawaan Android |
| `client.location` | `get_location()` | Koordinat GPS, elevasi, kecepatan, akurasi |
| `client.sms` | `send()`, `list_messages()` | Pengiriman dan pembacaan SMS |
| `client.camera` | `get_cameras()`, `take_photo()` | Pengambilan foto dari kamera belakang/depan |
| `client.volume` | `get_volumes()`, `set_volume()` | Manajemen volume audio stream |
| `client.wifi` | `get_connection_info()`, `scan()`, `enable()` | Informasi status Wi-Fi, SSID, IP, dan signal level |
| `client.sensor` | `list_sensors()`, `read_once()` | Pembacaan sensor (cahaya, akselerometer, dll.) |
| `client.torch` | `on()`, `off()`, `toggle()` | Kontrol lampu senter LED |
| `client.tts` | `speak()`, `get_engines()` | Text-to-Speech multi-bahasa |
| `client.toast` | `show()` | Pop-up toast singkat di layar Android |
| `client.clipboard` | `get()`, `set()` | Membaca dan menulis clipboard sistem |

---

## 🧪 Mock Engine (Pengujian di PC/Mac)

Anda tidak perlu selalu menguji kode di layar ponsel:

```python
from muxpy import TermuxClient

# Otomatis aktif di luar Android atau aktifkan secara eksplisit:
client = TermuxClient(mock_mode=True)
```

Menjalankan test suite:
```bash
python -m unittest discover tests
```

---

## 📜 Lisensi
Dilisensikan di bawah lisensi [MIT](LICENSE). Dibuat untuk ekosistem komunitas Termux & Android Developers.
