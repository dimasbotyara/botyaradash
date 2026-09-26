"""GPU data collector."""

from typing import Any

from collectors.base import BaseCollector


class GPUCollector(BaseCollector):
    """Collects GPU data using GPUtil (NVIDIA) or fallback."""

    def __init__(self) -> None:
        self._available = False
        self._gputil = None

        try:
            import GPUtil  # type: ignore
            gpus = GPUtil.getGPUs()
            if gpus:
                self._available = True
                self._gputil = GPUtil
        except Exception:
            pass

    @property
    def name(self) -> str:
        return "gpu"

    @property
    def available(self) -> bool:
        return self._available

    def collect(self) -> dict[str, Any]:
        if not self._available or self._gputil is None:
            return {"gpus": [], "available": False}

        gpus_data: list[dict[str, Any]] = []

        try:
            gpus = self._gputil.getGPUs()
            for gpu in gpus:
                gpus_data.append({
                    "id": gpu.id,
                    "name": gpu.name,
                    "load_percent": round(gpu.load * 100, 1),
                    "memory_used_mb": round(gpu.memoryUsed, 0),
                    "memory_total_mb": round(gpu.memoryTotal, 0),
                    "memory_percent": round(
                        gpu.memoryUsed / gpu.memoryTotal * 100, 1
                    ) if gpu.memoryTotal > 0 else 0,
                    "temperature": gpu.temperature,
                    "driver": gpu.driver,
                })
        except Exception:
            return {"gpus": [], "available": False}

        return {"gpus": gpus_data, "available": True}
