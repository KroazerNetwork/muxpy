# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2026-10-11

### Added
- **`WakelockApi`**: CPU wakelock manager with `async with keep_awake():` context manager to prevent Android from killing background processes.
- **`LocationApi`**: GPS & network location provider returning `LocationInfo` dataclass (latitude, longitude, altitude, accuracy, speed, bearing).
- **`CameraApi`**: Camera snapshot (`take_photo()`) and camera sensor enumeration (`get_cameras()`).
- **`VolumeApi`**: System audio stream volume inspector and setter for music, ring, alarm, call, notification, and system streams.
- **`SmsApi`**: SMS sending (`send()`) and inbox/outbox listing (`list_messages()`), returning typed `SmsMessage` dataclass.
- **Built-in CLI diagnostic tool**: Run `muxpy info` or `python -m muxpy info` to print a full device hardware summary from the terminal.
- **PEP 561 compliance marker**: Added `py.typed` for full IDE type-checking and autocompletion support.
- **Expanded Mock Engine**: Default synthetic mock data added for all new APIs (Location, Camera, Volume, SMS).
- **12 unit tests**: Full test coverage for all core and extended APIs.
- `__main__.py` entrypoint for `python -m muxpy` invocation.

### Changed
- Version bumped to `0.2.0`.
- `TermuxClient.__aexit__` now also auto-releases wakelock if held on exit.
- `pyproject.toml`: Added `keywords`, `classifiers`, and `[project.urls]` metadata.

---

## [0.1.0] - 2026-10-11

### Added
- Initial release of `muxpy` (renamed from internal codename `aiotermux`).
- `AsyncExecutor`: Non-blocking `asyncio.subprocess` wrapper with mock fallback engine.
- `BatteryApi`: `get_status()` returning `BatteryStatus`, `monitor()` async generator.
- `NotificationApi` with fluent `NotificationBuilder` (action buttons, sound, vibration, ongoing flags).
- `ToastApi`: Android toast popup.
- `VibratorApi`: Haptic feedback with duration and force options.
- `TorchApi`: Flashlight toggle with cached state.
- `ClipboardApi`: Async get/set for system clipboard.
- `TtsApi`: Text-to-speech with language, pitch, rate, and stream support.
- `DialogApi`: Native Android GUI dialogs — text, confirm, radio, checkbox, date, time.
- `WifiApi`: Connection info, scan, and enable/disable.
- `SensorApi`: Sensor enumeration and single-shot reading.
- `TermuxClient` async context manager facade.
- 7 unit tests with Python `unittest.IsolatedAsyncioTestCase`.
- GitHub Actions CI matrix for Python 3.9–3.12.
