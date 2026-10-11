"""Unified client facade for muxpy."""

from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

from .api.battery import BatteryApi
from .api.camera import CameraApi
from .api.clipboard import ClipboardApi
from .api.dialog import DialogApi
from .api.location import LocationApi
from .api.notification import NotificationApi
from .api.sensor import SensorApi
from .api.sms import SmsApi
from .api.toast import ToastApi
from .api.torch import TorchApi
from .api.tts import TtsApi
from .api.vibrator import VibratorApi
from .api.volume import VolumeApi
from .api.wakelock import WakelockApi
from .api.wifi import WifiApi
from .core.executor import AsyncExecutor


class TermuxClient:
    """Main entrypoint for interacting with Termux Android APIs asynchronously."""

    def __init__(
        self,
        mock_mode: bool = False,
        default_timeout: float = 15.0,
    ):
        """Initialize the Termux client.

        :param mock_mode: If True, uses mock simulation instead of calling real Termux binaries.
                          Automatically active when run on non-Termux systems if commands aren't found.
        :param default_timeout: Default command execution timeout in seconds.
        """
        self.executor = AsyncExecutor(mock_mode=mock_mode, default_timeout=default_timeout)

        # Core hardware & interaction APIs
        self.battery = BatteryApi(self.executor)
        self.notification = NotificationApi(self.executor)
        self.toast = ToastApi(self.executor)
        self.vibrator = VibratorApi(self.executor)
        self.torch = TorchApi(self.executor)
        self.clipboard = ClipboardApi(self.executor)
        self.tts = TtsApi(self.executor)
        self.dialog = DialogApi(self.executor)
        self.wifi = WifiApi(self.executor)
        self.sensor = SensorApi(self.executor)

        # Extended professional APIs
        self.camera = CameraApi(self.executor)
        self.location = LocationApi(self.executor)
        self.volume = VolumeApi(self.executor)
        self.sms = SmsApi(self.executor)
        self.wakelock = WakelockApi(self.executor)

    @property
    def is_termux(self) -> bool:
        """Return True if executing inside genuine Termux on Android."""
        return self.executor.is_termux

    async def __aenter__(self) -> "TermuxClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        # Cleanup sensors or wakelocks if held
        try:
            await self.sensor.cleanup()
        except Exception:
            pass

        if self.wakelock.is_locked:
            try:
                await self.wakelock.release()
            except Exception:
                pass
