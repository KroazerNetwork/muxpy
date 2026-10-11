"""Text-To-Speech (TTS) API for Termux."""

from __future__ import annotations

from typing import Any, List, Optional

from ..core.executor import AsyncExecutor


class TtsApi:
    """Interface to termux-tts-speak and termux-tts-engines."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def get_engines(self) -> List[dict[str, Any]]:
        """List available TTS engines on the device."""
        result = await self._executor.run("termux-tts-engines", parse_json=True)
        return result if isinstance(result, list) else []

    async def speak(
        self,
        text: str,
        engine: Optional[str] = None,
        language: Optional[str] = None,
        pitch: Optional[float] = None,
        rate: Optional[float] = None,
        stream: Optional[str] = None,
    ) -> None:
        """Speak given text using Android Text-To-Speech engine.

        :param text: Text to be read aloud.
        :param engine: Specific TTS engine package name.
        :param language: Language code, e.g. 'id', 'en-US'.
        :param pitch: Speech pitch (0.0 to 2.0, default 1.0).
        :param rate: Speech rate (0.0 to 2.0, default 1.0).
        :param stream: Audio stream (ALARM, MUSIC, NOTIFICATION, RING, SYSTEM, VOICE_CALL).
        """
        args: List[str] = []
        if engine:
            args.extend(["-e", engine])
        if language:
            args.extend(["-l", language])
        if pitch is not None:
            args.extend(["-p", str(pitch)])
        if rate is not None:
            args.extend(["-r", str(rate)])
        if stream:
            args.extend(["-s", stream])

        await self._executor.run("termux-tts-speak", args=args, input_data=text)
