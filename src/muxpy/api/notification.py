"""Notification API for Termux."""

from __future__ import annotations

from typing import List, Optional

from ..core.executor import AsyncExecutor


class NotificationBuilder:
    """Fluent builder for constructing complex Termux notifications."""

    def __init__(self, api: "NotificationApi"):
        self._api = api
        self._id: Optional[str] = None
        self._title: Optional[str] = None
        self._content: Optional[str] = None
        self._priority: str = "default"
        self._sound: bool = False
        self._vibrate_pattern: Optional[str] = None
        self._ongoing: bool = False
        self._alert_once: bool = False
        self._action: Optional[str] = None
        self._on_delete: Optional[str] = None
        self._led_color: Optional[str] = None
        self._button1: Optional[tuple[str, str]] = None
        self._button2: Optional[tuple[str, str]] = None
        self._button3: Optional[tuple[str, str]] = None

    def id(self, notif_id: str | int) -> "NotificationBuilder":
        self._id = str(notif_id)
        return self

    def title(self, title: str) -> "NotificationBuilder":
        self._title = title
        return self

    def content(self, content: str) -> "NotificationBuilder":
        self._content = content
        return self

    def priority(self, priority: str) -> "NotificationBuilder":
        # high, low, max, min, default
        self._priority = priority
        return self

    def sound(self, enable: bool = True) -> "NotificationBuilder":
        self._sound = enable
        return self

    def vibrate(self, pattern: str) -> "NotificationBuilder":
        """Vibration pattern e.g. '500,1000,500' (ms)."""
        self._vibrate_pattern = pattern
        return self

    def ongoing(self, enable: bool = True) -> "NotificationBuilder":
        """Pin notification so user cannot swipe it away."""
        self._ongoing = enable
        return self

    def alert_once(self, enable: bool = True) -> "NotificationBuilder":
        self._alert_once = enable
        return self

    def on_click(self, action_cmd: str) -> "NotificationBuilder":
        self._action = action_cmd
        return self

    def on_delete(self, action_cmd: str) -> "NotificationBuilder":
        self._on_delete = action_cmd
        return self

    def button1(self, text: str, action_cmd: str) -> "NotificationBuilder":
        self._button1 = (text, action_cmd)
        return self

    def button2(self, text: str, action_cmd: str) -> "NotificationBuilder":
        self._button2 = (text, action_cmd)
        return self

    def button3(self, text: str, action_cmd: str) -> "NotificationBuilder":
        self._button3 = (text, action_cmd)
        return self

    def _build_args(self) -> List[str]:
        args: List[str] = []
        if self._id:
            args.extend(["--id", self._id])
        if self._title:
            args.extend(["--title", self._title])
        if self._content:
            args.extend(["--content", self._content])
        if self._priority:
            args.extend(["--priority", self._priority])
        if self._sound:
            args.append("--sound")
        if self._vibrate_pattern:
            args.extend(["--vibrate", self._vibrate_pattern])
        if self._ongoing:
            args.append("--ongoing")
        if self._alert_once:
            args.append("--alert-once")
        if self._action:
            args.extend(["--action", self._action])
        if self._on_delete:
            args.extend(["--on-delete", self._on_delete])
        if self._led_color:
            args.extend(["--led-color", self._led_color])
        if self._button1:
            args.extend(["--button1", self._button1[0], "--button1-action", self._button1[1]])
        if self._button2:
            args.extend(["--button2", self._button2[0], "--button2-action", self._button2[1]])
        if self._button3:
            args.extend(["--button3", self._button3[0], "--button3-action", self._button3[1]])
        return args

    async def send(self) -> None:
        """Send the notification to Android."""
        await self._api._send_raw(self._build_args())


class NotificationApi:
    """Interface to termux-notification and termux-notification-remove."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    def builder(self) -> NotificationBuilder:
        """Create a NotificationBuilder for granular control."""
        return NotificationBuilder(self)

    async def _send_raw(self, args: List[str]) -> None:
        await self._executor.run("termux-notification", args=args)

    async def show(
        self,
        title: str,
        content: str,
        id: Optional[str | int] = None,
        priority: str = "default",
        sound: bool = False,
        ongoing: bool = False,
    ) -> None:
        """Quickly display a notification with standard parameters."""
        builder = self.builder().title(title).content(content).priority(priority).sound(sound).ongoing(ongoing)
        if id is not None:
            builder.id(id)
        await builder.send()

    async def remove(self, notif_id: str | int) -> None:
        """Remove a notification by its ID."""
        await self._executor.run("termux-notification-remove", args=[str(notif_id)])
