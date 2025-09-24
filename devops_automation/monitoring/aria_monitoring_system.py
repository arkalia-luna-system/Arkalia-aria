#!/usr/bin/env python3

"""
ARKALIA ARIA - Monitoring System
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

# Import psutil de façon sûre et typée
psutil: Any  # sera défini ci-dessous
try:  # pragma: no cover - l'environnement peut ne pas avoir psutil
    import psutil as _psutil
    psutil = _psutil
except Exception:  # pragma: no cover
    psutil = None


class ARIA_MonitoringSystem:
    def __init__(self, project_root: str = ".") -> None:
        self.project_root = project_root
        self.is_monitoring: bool = True
        self.monitoring_data: list[dict[str, Any]] = []
        self.alerts: list[dict[str, Any]] = []

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
            metrics["note"] = "psutil non installé - métriques système désactivées"
            return metrics
        try:
            metrics["process_count"] = len(psutil.pids())
            metrics["cpu_percent"] = psutil.cpu_percent(interval=0.1)
            metrics["memory_usage_mb"] = psutil.virtual_memory().used / (1024 * 1024)
            metrics["disk_usage_percent"] = psutil.disk_usage("/").percent
        except Exception as e:  # pragma: no cover
            metrics["error"] = str(e)
        return metrics

    # ==== Compat helpers pour API DevOps ====
    def get_health_status(self) -> dict[str, Any]:
        """Retourne un statut de santé minimal basé sur les métriques collectées."""
        metrics = self.collect_metrics()
        status = "excellent"
        if metrics.get("cpu_percent") and metrics["cpu_percent"] > 80:
            status = "degraded"
        return {"status": status, "metrics": metrics}

    def get_performance_summary(self, hours: int = 24) -> dict[str, Any]:
        """Retourne un résumé de performance simple pour les dernières heures."""
        metrics = self.collect_metrics()
        return {"hours": hours, "current": metrics}

    def get_alerts_summary(self, hours: int = 24) -> dict[str, Any]:
        """Retourne un résumé d'alertes minimal."""
        return {
            "hours": hours,
            "alerts_count": len(self.alerts),
            "alerts": self.alerts[-50:],
        }

    def generate_monitoring_dashboard_html(self) -> str:
        """Génère un petit HTML statique pour le dashboard de monitoring."""
        m = self.collect_metrics()
        return f"""
<!doctype html>
<html lang=fr>
  <meta charset=utf-8>
  <title>Monitoring ARIA</title>
  <body>
    <h1>Monitoring ARIA</h1>
    <p>Timestamp: {m.get('timestamp')}</p>
    <ul>
      <li>CPU: {m.get('cpu_percent')}</li>
      <li>Mémoire (MB): {m.get('memory_usage_mb')}</li>
      <li>Disque (%): {m.get('disk_usage_percent')}</li>
      <li>Processus: {m.get('process_count')}</li>
    </ul>
  </body>
</html>
"""

    def export_monitoring_data(self, format_type: str = "json", hours: int = 24) -> str:
        """Exporte des données de monitoring simulées et retourne un chemin de fichier."""
        filename = f"monitoring_export_{hours}h.{ 'json' if format_type not in {'html','csv'} else format_type }"
        return str(filename)
