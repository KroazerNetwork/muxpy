# PROJECT OVERVIEW & OBJECTIVES: muxpy

## 1. Latar Belakang & Masalah
Termux adalah lingkungan Linux terminal yang sangat populer di Android. Melalui package tambahan `termux-api` dan aplikasi companion Android Termux:API, pengguna dapat mengakses sensor dan fitur hardware Android (baterai, SMS, kamera, senter, getar, notifikasi, dialog interaktif, dll.) langsung dari baris perintah.

Namun, dalam ekosistem pemrograman Python di Termux:
1. **CLI Calling yang Kaku:** Kebanyakan script memanggil `termux-api` menggunakan `os.system()` atau `subprocess.run()` secara synchronous. Hal ini memblokir event loop utama, yang sangat merugikan ketika script terhubung ke library modern berbasis async (seperti `aiogram`, `python-telegram-bot` versi async, Discord bots, FastAPI, atau automated IoT scripts).
2. **Tidak Ada Tipe Data / Data Parsing:** Perintah bawaan Termux API mengembalikan string JSON mentah. Developer harus menulis parsing manual `json.loads()` berulang kali tanpa perlindungan type hint / autocompletion IDE.
3. **Ketergantungan Eksekusi di HP Saja (Susah Debugging):** Menulis script Termux di laptop/PC sering kali error karena binary `termux-battery-status` dsb. tidak ada di PC. Pengembang membutuhkan mode simulasi / mock agar bisa mengembangkan dan menguji kode di laptop sebelum dideploy ke Android.

---

## 2. Visi & Tujuan Project

### Visi
Menjadi library Python asynchronous paling ringkas (*ultra-light*), elegan, dan standar untuk berinteraksi dengan API hardware Android di Termux, dengan performa tinggi, kemudahan integrasi bot, dan dukungan *developer experience* (DX) kelas satu.

### Tujuan Utama (Core Objectives)
1. **Asynchronous First:** Dibangun di atas `asyncio` Python untuk eksekusi non-blocking subprocess, siap disandingkan langsung dengan framework bot (Telegram/WhatsApp/Discord) dan web servers.
2. **Pydantic / Dataclass Typed Models:** Mengonversi respon JSON mentah menjadi objek Python berstruktur lengkap dengan type-hints (autocompletion di IDE/editor).
3. **Modular Sub-APIs:** Membagi akses perangkat ke dalam modul-modul logis:
   - `Battery` (status, monitor perubahan daya/persentase)
   - `Notification` (builder notifikasi, update, cancel)
   - `Toast` & `Vibrator` & `Torch` (feedback fisik dan visual)
   - `TTS` (Text-to-Speech)
   - `Clipboard` (baca & tulis clipboard)
   - `Dialog` (dialog input, konfirmasi, radio, checkbox Android)
   - `Wifi` & `Sensors` (status jaringan dan telemetri perangkat)
4. **Mock / Simulation Engine:** Memiliki runtime yang mampu mendeteksi ketersediaan binary Termux, dengan opsi fallback mock data jika dijalankan di Windows/macOS/Linux biasa untuk mempermudah unit testing.
5. **Robust Error Handling:** Penanganan timeout eksekusi, penanganan jika aplikasi companion Termux:API belum diinstal atau izin Android belum diberikan.

---

## 3. Target Pengguna
- **Bot Developers:** Pengembang yang menjalankan bot Telegram/WA di HP bekas untuk smart home, alert server, atau otomasi pribadi.
- **HomeLab & IoT Enthusiasts:** Pengguna yang memanfaatkan HP Android sebagai sensor node (sensor cahaya, status daya/UPS monitor).
- **Automation Hackers:** Pengguna yang membuat skrip otomasi sehari-hari (clipboard auto-processor, auto-SMS responder, speech reminder).

---

## 4. Arsitektur Teknis
```
muxpy/
├── core/
│   ├── executor.py       # Asynchronous process runner (asyncio.subprocess)
│   ├── exceptions.py     # Custom exceptions (TermuxApiNotFoundError, CommandTimeoutError, dll.)
│   └── models.py         # Base data structures
├── api/
│   ├── battery.py        # Battery status & async event polling
│   ├── notification.py   # Rich notification builder
│   ├── toast.py          # Android toast popup
│   ├── vibrator.py       # Haptic feedback control
│   ├── torch.py          # Flashlight toggle
│   ├── tts.py            # Text-to-speech engine
│   ├── clipboard.py      # System clipboard getter/setter
│   ├── dialog.py         # Native Android GUI prompt dialogs
│   ├── wifi.py           # Network status & info
│   └── sensor.py         # Sensor reading & streams
├── mock/
│   └── provider.py       # Synthetic data provider untuk pengujian non-Android
└── client.py             # Facade utama: TermuxClient
```
