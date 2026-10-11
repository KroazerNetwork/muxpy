"""Exceptions for aiotermux."""

class TermuxError(Exception):
    """Base exception for all aiotermux errors."""
    pass


class TermuxApiNotFoundError(TermuxError):
    """Raised when termux-api CLI tools or the Termux:API app are not installed."""
    def __init__(self, command: str):
        super().__init__(
            f"Perintah '{command}' tidak ditemukan. "
            "Pastikan paket 'termux-api' sudah terpasang (pkg install termux-api) "
            "dan aplikasi Termux:API Android sudah diinstal dan diizinkan."
        )
        self.command = command


class TermuxExecutionError(TermuxError):
    """Raised when a Termux API command returns a non-zero exit code or error output."""
    def __init__(self, command: str, returncode: int, stderr: str):
        super().__init__(f"Perintah '{command}' gagal (code {returncode}): {stderr.strip()}")
        self.command = command
        self.returncode = returncode
        self.stderr = stderr


class TermuxTimeoutError(TermuxError):
    """Raised when a Termux API command times out."""
    def __init__(self, command: str, timeout: float):
        super().__init__(f"Perintah '{command}' melebihi batas waktu {timeout} detik.")
        self.command = command
        self.timeout = timeout


class TermuxPermissionError(TermuxError):
    """Raised when an Android runtime permission is denied or missing."""
    pass
