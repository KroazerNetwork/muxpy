"""Camera API for Termux."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from ..core.executor import AsyncExecutor


@dataclass(frozen=True)
class CameraInfo:
    """Hardware camera sensor description."""
    id: str
    facing: str
    auto_exposure_modes: List[str]


class CameraApi:
    """Interface to termux-camera-photo and termux-camera-info."""

    def __init__(self, executor: AsyncExecutor):
        self._executor = executor

    async def get_cameras(self) -> List[CameraInfo]:
        """List available cameras on the device."""
        data = await self._executor.run("termux-camera-info", parse_json=True)
        results: List[CameraInfo] = []
        if isinstance(data, list):
            for cam in data:
                if isinstance(cam, dict):
                    results.append(
                        CameraInfo(
                            id=str(cam.get("id", "0")),
                            facing=str(cam.get("facing", "back")),
                            auto_exposure_modes=cam.get("auto_exposure_modes", []),
                        )
                    )
        return results

    async def take_photo(
        self,
        output_path: str,
        camera_id: str | int = 0,
    ) -> str:
        """Take a photo and save it to the specified file path.

        :param output_path: Destination file path (e.g. '/sdcard/DCIM/photo.jpg').
        :param camera_id: ID of the camera to use (0 usually back, 1 usually front).
        :return: output_path
        """
        args = ["-c", str(camera_id), output_path]
        await self._executor.run("termux-camera-photo", args=args)
        return output_path
