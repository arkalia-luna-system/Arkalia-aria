#!/usr/bin/env python3

"""
ARKALIA ARIA - Monitoring System
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

try:
    import psutil  # type: ignore
except Exception:  # pragma: no cover
    psutil = None  # fallback minimal si non installé


class ARIA_MonitoringSystem:
    def __init__(self, project_root: str = ".") -> None:
        self.project_root = project_root

    def _now(self) -> str:
        return datetime.now().isoformat()

    def collect_metrics(self) -> dict[str, Any]:
        metrics: dict[str, Any] = {
            "timestamp": self._now(),
            "process_count": None,
            "cpu_percent": None,
            "memory_usage_mb": None,
            "disk_usage_percent": None,
        }
        if psutil is None:
            metrics.update(
                {
                    "note": "psutil non installé - métriques système désactivées",
                }
            )
            return metrics
        try:
            metrics["process_count"] = len(psutil.pids())
            metrics["cpu_percent"] = psutil.cpu_percent(interval=0.1)
            metrics["memory_usage_mb"] = psutil.virtual_memory().used / (1024 * 1024)
            metrics["disk_usage_percent"] = psutil.disk_usage("/").percent
        except Exception as e:  # pragma: no cover
            metrics["error"] = str(e)
        return metrics
