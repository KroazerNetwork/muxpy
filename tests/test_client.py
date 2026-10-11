"""Tests for muxpy using Python standard library unittest."""

import sys
import unittest
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from muxpy import (
    BatteryStatus,
    CameraInfo,
    LocationInfo,
    SmsMessage,
    TermuxClient,
    VolumeStream,
    WifiConnectionInfo,
)


class TestMuxpy(unittest.IsolatedAsyncioTestCase):
    async def test_battery_status_mock(self):
        client = TermuxClient(mock_mode=True)
        status = await client.battery.get_status()

        self.assertIsInstance(status, BatteryStatus)
        self.assertEqual(status.health, "GOOD")
        self.assertEqual(status.percentage, 88)
        self.assertTrue(status.is_charging)
        self.assertTrue(status.is_plugged)

    async def test_wifi_connection_info_mock(self):
        client = TermuxClient(mock_mode=True)
        info = await client.wifi.get_connection_info()

        self.assertIsInstance(info, WifiConnectionInfo)
        self.assertEqual(info.ssid, "Home-WiFi-5G")
        self.assertEqual(info.ip, "192.168.1.105")
        self.assertTrue(info.is_connected)

    async def test_notification_builder(self):
        client = TermuxClient(mock_mode=True)
        captured_args = []

        def mock_notif_handler(cmd, args, stdin):
            captured_args.extend(args)
            return ""

        client.executor.register_mock("termux-notification", mock_notif_handler)

        await (
            client.notification.builder()
            .id(101)
            .title("Alert")
            .content("System warning")
            .priority("high")
            .sound(True)
            .ongoing(True)
            .send()
        )

        self.assertIn("--id", captured_args)
        self.assertIn("101", captured_args)
        self.assertIn("--title", captured_args)
        self.assertIn("Alert", captured_args)
        self.assertIn("--sound", captured_args)
        self.assertIn("--ongoing", captured_args)

    async def test_dialog_confirm_mock(self):
        client = TermuxClient(mock_mode=True)
        client.executor.register_mock(
            "termux-dialog",
            lambda cmd, args, stdin: {"code": 0, "text": "yes"},
        )

        confirmed = await client.dialog.confirm(title="Apakah yakin?")
        self.assertTrue(confirmed)

    async def test_dialog_text_mock(self):
        client = TermuxClient(mock_mode=True)
        client.executor.register_mock(
            "termux-dialog",
            lambda cmd, args, stdin: {"code": -1, "text": "Halo Termux"},
        )

        result = await client.dialog.text(title="Masukkan Nama")
        self.assertEqual(result, "Halo Termux")

    async def test_clipboard_mock(self):
        client = TermuxClient(mock_mode=True)
        stored = {"clip": "initial"}

        client.executor.register_mock(
            "termux-clipboard-set",
            lambda cmd, args, stdin: stored.update({"clip": stdin or ""}),
        )
        client.executor.register_mock(
            "termux-clipboard-get",
            lambda cmd, args, stdin: stored["clip"],
        )

        await client.clipboard.set("Teks tersimpan")
        val = await client.clipboard.get()
        self.assertEqual(val, "Teks tersimpan")

    async def test_torch_toggle(self):
        client = TermuxClient(mock_mode=True)
        state = await client.torch.toggle()
        self.assertTrue(state)
        self.assertTrue(client.torch.is_on)

        state2 = await client.torch.toggle()
        self.assertFalse(state2)
        self.assertFalse(client.torch.is_on)

    async def test_wakelock(self):
        client = TermuxClient(mock_mode=True)
        self.assertFalse(client.wakelock.is_locked)

        async with client.wakelock.keep_awake():
            self.assertTrue(client.wakelock.is_locked)

        self.assertFalse(client.wakelock.is_locked)

    async def test_location_mock(self):
        client = TermuxClient(mock_mode=True)
        loc = await client.location.get_location()

        self.assertIsInstance(loc, LocationInfo)
        self.assertEqual(loc.provider, "gps")
        self.assertAlmostEqual(loc.latitude, -6.2088)
        self.assertAlmostEqual(loc.longitude, 106.8456)

    async def test_camera_mock(self):
        client = TermuxClient(mock_mode=True)
        cameras = await client.camera.get_cameras()

        self.assertEqual(len(cameras), 2)
        self.assertIsInstance(cameras[0], CameraInfo)
        self.assertEqual(cameras[0].facing, "back")

    async def test_volume_mock(self):
        client = TermuxClient(mock_mode=True)
        volumes = await client.volume.get_volumes()

        self.assertIn("music", volumes)
        self.assertIsInstance(volumes["music"], VolumeStream)
        self.assertEqual(volumes["music"].volume, 10)
        self.assertGreater(volumes["music"].percentage, 0)

    async def test_sms_mock(self):
        client = TermuxClient(mock_mode=True)
        messages = await client.sms.list_messages(limit=1)

        self.assertEqual(len(messages), 1)
        self.assertIsInstance(messages[0], SmsMessage)
        self.assertIn("OTP", messages[0].body)


if __name__ == "__main__":
    unittest.main()
