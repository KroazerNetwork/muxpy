"""Telephony & SMS API for Termux."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from ..core.executor import AsyncExecutor


@dataclass(frozen=True)
class SmsMessage:
    """Represents an SMS message from device inbox/outbox."""
    thread_id: int
    type: str
    read: bool
    number: str
    received: str
    body: str


class SmsApi:
    """Interface to termux-sms-send and termux-sms-list."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def send(self, phone_number: str | List[str], text: str) -> None:
        """Send an SMS message.

        :param phone_number: Single phone number string or list of recipient numbers.
        :param text: Message body content.
        """
        recipients = [phone_number] if isinstance(phone_number, str) else phone_number
        recipients_arg = ",".join(recipients)
        await self._executor.run(
            "termux-sms-send",
            args=["-n", recipients_arg],
            input_data=text,
        )

    async def list_messages(
        self,
        limit: int = 10,
        offset: int = 0,
        box_type: str = "inbox",
    ) -> List[SmsMessage]:
        """Fetch list of SMS messages from the device.

        :param limit: Maximum messages to retrieve.
        :param offset: Pagination offset.
        :param box_type: 'inbox', 'sent', 'draft', or 'outbox'.
        """
        args = ["-l", str(limit), "-o", str(offset), "-t", box_type]
        data = await self._executor.run("termux-sms-list", args=args, parse_json=True)
        results: List[SmsMessage] = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    results.append(
                        SmsMessage(
                            thread_id=int(item.get("threadid", 0)),
                            type=str(item.get("type", box_type)),
                            read=bool(item.get("read", False)),
                            number=str(item.get("number", "")),
                            received=str(item.get("received", "")),
                            body=str(item.get("body", "")),
                        )
                    )
        return results
