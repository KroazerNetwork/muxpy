"""Real-world example: Telegram Bot alerting with muxpy.

This example shows how to build a simple Telegram bot that:
- Sends device battery alerts to a Telegram chat
- Monitors battery in the background using async generator
- Acquires CPU wakelock to prevent Android killing the process
- Uses a Telegram Bot token via environment variable

Requirements (Termux):
    pkg install python termux-api
    pip install httpx muxpy

Usage:
    TELEGRAM_TOKEN=<your_bot_token> CHAT_ID=<your_chat_id> python telegram_battery_alert.py
"""

import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False

from muxpy import TermuxClient

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")
ALERT_THRESHOLD = 20  # Notify when battery drops at or below this percent


async def send_telegram_message(text: str) -> None:
    """Send a Telegram message via Bot API."""
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print(f"[MOCK TG] Would send: {text}")
        return
    if not HAS_HTTPX:
        print(f"[MOCK TG] httpx not installed. Would send: {text}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    async with httpx.AsyncClient() as http:
        await http.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})


async def run_battery_monitor() -> None:
    """Monitor battery every 30 seconds and alert on low charge."""
    async with TermuxClient() as client:
        print("[muxpy] Starting battery monitor bot...")

        # Acquire CPU wakelock so Android won't kill this process when screen is off
        async with client.wakelock.keep_awake():
            print("[muxpy] CPU wakelock acquired. Monitoring battery...")

            # Notify startup
            bat = await client.battery.get_status()
            await send_telegram_message(
                f"<b>muxpy Bot started</b>\n"
                f"Battery: <b>{bat.percentage}%</b> | Status: {bat.status}"
            )

            alerted_once = False  # Prevent repeat spam alerts
            async for status in client.battery.monitor(interval_seconds=30, only_on_change=True):
                info = (
                    f"<b>Battery Alert</b>\n"
                    f"Level: <b>{status.percentage}%</b>\n"
                    f"Status: {status.status} | Charging: {status.is_charging}"
                )

                if status.percentage <= ALERT_THRESHOLD and not status.is_charging:
                    if not alerted_once:
                        await send_telegram_message(
                            f"⚠️ {info}\n\n<i>Please connect charger!</i>"
                        )
                        await client.notification.show(
                            title="Low Battery",
                            content=f"Battery at {status.percentage}%. Connect charger!",
                            id=200,
                            priority="high",
                            sound=True,
                        )
                        await client.vibrator.vibrate(500)
                        alerted_once = True
                elif status.is_charging and alerted_once:
                    await send_telegram_message(f"✅ Charging resumed.\n{info}")
                    alerted_once = False

                print(f"[monitor] {status.percentage}% | {status.status}")


if __name__ == "__main__":
    asyncio.run(run_battery_monitor())
