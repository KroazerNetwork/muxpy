"""Asynchronous command executor for Termux API commands."""

from __future__ import annotations

import asyncio
import json
import shutil
from typing import Any, Callable, Dict, List, Optional

from .exceptions import (
    TermuxApiNotFoundError,
    TermuxExecutionError,
    TermuxPermissionError,
    TermuxTimeoutError,
)

MockHandler = Callable[[str, List[str], Optional[str]], Any]


class AsyncExecutor:
    """Executes termux-* commands asynchronously with timeout and mock support."""

    def __init__(self, mock_mode: bool = False, default_timeout: float = 15.0):
        self.mock_mode = mock_mode
        self.default_timeout = default_timeout
        self._mock_registry: Dict[str, MockHandler] = {}
        self._is_termux_environment = self._detect_termux()

    @staticmethod
    def _detect_termux() -> bool:
        """Check if current environment is Termux on Android."""
        import os
        return "TERMUX_VERSION" in os.environ or os.path.exists("/data/data/com.termux/files")

    @property
    def is_termux(self) -> bool:
        """Return True if running in a real Termux environment."""
        return self._is_termux_environment

    def register_mock(self, command: str, handler: MockHandler) -> None:
        """Register a mock handler for testing without Termux."""
        self._mock_registry[command] = handler

    async def run(
        self,
        command: str,
        args: Optional[List[str]] = None,
        input_data: Optional[str] = None,
        timeout: Optional[float] = None,
        parse_json: bool = False,
    ) -> Any:
        """Run a termux command asynchronously and return stdout or parsed JSON."""
        cmd_args = args or []
        effective_timeout = timeout if timeout is not None else self.default_timeout

        # Fallback to mock mode if explicitly enabled or binary is unavailable on non-Termux
        use_mock = self.mock_mode or (not self.is_termux and shutil.which(command) is None)

        if use_mock:
            return await self._run_mock(command, cmd_args, input_data, parse_json)

        # Check binary availability in real execution
        if shutil.which(command) is None:
            raise TermuxApiNotFoundError(command)

        stdin_pipe = asyncio.subprocess.PIPE if input_data is not None else None

        try:
            process = await asyncio.create_subprocess_exec(
                command,
                *cmd_args,
                stdin=stdin_pipe,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdin_bytes = input_data.encode("utf-8") if input_data is not None else None

            stdout_bytes, stderr_bytes = await asyncio.wait_for(
                process.communicate(input=stdin_bytes),
                timeout=effective_timeout,
            )
        except asyncio.TimeoutError:
            try:
                process.kill()
            except ProcessLookupError:
                pass
            raise TermuxTimeoutError(command, effective_timeout)
        except FileNotFoundError:
            raise TermuxApiNotFoundError(command)

        stdout = stdout_bytes.decode("utf-8", errors="replace")
        stderr = stderr_bytes.decode("utf-8", errors="replace")

        if process.returncode != 0:
            if "permission" in stderr.lower() or "denied" in stderr.lower():
                raise TermuxPermissionError(f"Izin ditolak untuk {command}: {stderr.strip()}")
            raise TermuxExecutionError(command, process.returncode, stderr)

        if parse_json:
            clean_stdout = stdout.strip()
            if not clean_stdout:
                return {}
            try:
                return json.loads(clean_stdout)
            except json.JSONDecodeError as exc:
                raise TermuxExecutionError(
                    command,
                    process.returncode,
                    f"Gagal mem-parsing JSON: {exc}. Output mentah: {clean_stdout}",
                )

        return stdout

    async def _run_mock(
        self,
        command: str,
        args: List[str],
        input_data: Optional[str],
        parse_json: bool,
    ) -> Any:
        """Simulate execution in mock mode."""
        if command in self._mock_registry:
            result = self._mock_registry[command](command, args, input_data)
            if asyncio.iscoroutine(result):
                result = await result
            return result

        # Default fallback mock data
        if parse_json:
            return self._default_mock_json(command)
        return "mock_ok"

    @staticmethod
    def _default_mock_json(command: str) -> Any:
        """Default synthetic data for common termux commands."""
        if command == "termux-battery-status":
            return {
                "health": "GOOD",
                "percentage": 88,
                "plugged": "PLUGGED_AC",
                "status": "CHARGING",
                "temperature": 29.5,
                "current": 1200000,
            }
        elif command == "termux-wifi-connectioninfo":
            return {
                "bssid": "00:11:22:33:44:55",
                "frequency_mhz": 5180,
                "ip": "192.168.1.105",
                "link_speed_mbps": 433,
                "mac_address": "02:00:00:00:00:00",
                "network_id": 1,
                "rssi": -55,
                "ssid": "Home-WiFi-5G",
                "ssid_hidden": False,
                "supplicant_state": "COMPLETED",
            }
        elif command == "termux-clipboard-get":
            return ""
        return {}
