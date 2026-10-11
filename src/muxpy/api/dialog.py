"""Native Android Dialogs API for Termux."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..core.executor import AsyncExecutor


@dataclass(frozen=True)
class DialogResult:
    """Result returned by a Termux dialog interaction."""
    code: int
    text: str

    @property
    def is_confirmed(self) -> bool:
        """True if user confirmed / pressed positive button."""
        return self.code in (0, -1) and self.text.lower() in ("yes", "ok", "true")

    @property
    def is_cancelled(self) -> bool:
        """True if user cancelled or dismissed dialog."""
        return self.code in (-2, 1) or self.text.lower() in ("no", "cancel")


@dataclass(frozen=True)
class RadioResult:
    """Result of a single-choice radio dialog."""
    code: int
    index: int
    text: str


@dataclass(frozen=True)
class CheckboxResult:
    """Result of a multi-choice checkbox dialog."""
    code: int
    selected_texts: List[str]


class DialogApi:
    """Interface to termux-dialog for interactive native Android GUI prompts."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def confirm(
        self,
        title: str = "Konfirmasi",
        hint: Optional[str] = None,
    ) -> bool:
        """Show a Yes/No confirmation dialog."""
        args = ["confirm", "-t", title]
        if hint:
            args.extend(["-i", hint])

        data = await self._executor.run("termux-dialog", args=args, parse_json=True)
        text = str(data.get("text", "")).lower()
        return text == "yes"

    async def text(
        self,
        title: str = "Input",
        hint: Optional[str] = None,
        multiline: bool = False,
        password: bool = False,
    ) -> Optional[str]:
        """Show a text input dialog."""
        args = ["text", "-t", title]
        if hint:
            args.extend(["-i", hint])
        if multiline:
            args.append("-m")
        if password:
            args.append("-p")

        data = await self._executor.run("termux-dialog", args=args, parse_json=True)
        # code -1 indicates submission, code -2 is cancelled
        if data.get("code") == -2:
            return None
        return str(data.get("text", ""))

    async def radio(
        self,
        options: List[str],
        title: str = "Pilih Opsi",
    ) -> Optional[RadioResult]:
        """Show a single-choice radio dialog."""
        options_csv = ",".join(options)
        args = ["radio", "-t", title, "-v", options_csv]

        data = await self._executor.run("termux-dialog", args=args, parse_json=True)
        if data.get("code") == -2:
            return None

        return RadioResult(
            code=int(data.get("code", 0)),
            index=int(data.get("index", -1)),
            text=str(data.get("text", "")),
        )

    async def checkbox(
        self,
        options: List[str],
        title: str = "Pilih Opsi (Multi)",
    ) -> Optional[CheckboxResult]:
        """Show a multi-choice checkbox dialog."""
        options_csv = ",".join(options)
        args = ["checkbox", "-t", title, "-v", options_csv]

        data = await self._executor.run("termux-dialog", args=args, parse_json=True)
        if data.get("code") == -2:
            return None

        raw_values = data.get("values", [])
        selected = [str(item.get("text", "")) for item in raw_values if isinstance(item, dict)]

        return CheckboxResult(
            code=int(data.get("code", 0)),
            selected_texts=selected,
        )

    async def date(self, title: str = "Pilih Tanggal") -> Optional[str]:
        """Show Android date picker dialog and return 'YYYY-MM-DD'."""
        args = ["date", "-t", title]
        data = await self._executor.run("termux-dialog", args=args, parse_json=True)
        if data.get("code") == -2:
            return None
        return str(data.get("text", ""))

    async def time(self, title: str = "Pilih Waktu") -> Optional[str]:
        """Show Android time picker dialog and return 'HH:MM'."""
        args = ["time", "-t", title]
        data = await self._executor.run("termux-dialog", args=args, parse_json=True)
        if data.get("code") == -2:
            return None
        return str(data.get("text", ""))
