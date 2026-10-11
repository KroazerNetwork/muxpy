"""muxpy: Ultra-light, modern, and asynchronous Python wrapper for Termux:API on Android."""

from .api.battery import BatteryStatus
from .api.camera import CameraInfo
from .api.dialog import CheckboxResult, DialogResult, RadioResult
from .api.location import LocationInfo
from .api.notification import NotificationBuilder
from .api.sms import SmsMessage
from .api.volume import VolumeStream
from .api.wifi import WifiConnectionInfo
from .client import TermuxClient
from .core.exceptions import (
    TermuxApiNotFoundError,
    TermuxError,
    TermuxExecutionError,
    TermuxPermissionError,
    TermuxTimeoutError,
)

__version__ = "0.2.0"
__all__ = [
    "TermuxClient",
    "NotificationBuilder",
    "BatteryStatus",
    "WifiConnectionInfo",
    "LocationInfo",
    "CameraInfo",
    "VolumeStream",
    "SmsMessage",
    "DialogResult",
    "RadioResult",
    "CheckboxResult",
    "TermuxError",
    "TermuxApiNotFoundError",
    "TermuxExecutionError",
    "TermuxTimeoutError",
    "TermuxPermissionError",
]
