"""muxpy: Ultra-light, modern, and asynchronous Python wrapper for Termux:API on Android."""

from .api.battery import BatteryStatus
from .api.dialog import CheckboxResult, DialogResult, RadioResult
from .api.notification import NotificationBuilder
from .api.wifi import WifiConnectionInfo
from .client import TermuxClient
from .core.exceptions import (
    TermuxApiNotFoundError,
    TermuxError,
    TermuxExecutionError,
    TermuxPermissionError,
    TermuxTimeoutError,
)

__version__ = "0.1.0"
__all__ = [
    "TermuxClient",
    "NotificationBuilder",
    "BatteryStatus",
    "WifiConnectionInfo",
    "DialogResult",
    "RadioResult",
    "CheckboxResult",
    "TermuxError",
    "TermuxApiNotFoundError",
    "TermuxExecutionError",
    "TermuxTimeoutError",
    "TermuxPermissionError",
]
