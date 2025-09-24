#!/usr/bin/env python3
"""
ARKALIA ARIA - Système de Monitoring
====================================

Système de monitoring automatisé pour ARIA avec :
- Surveillance en temps réel
- Alertes automatiques
- Métriques de performance
- Health checks
- Dashboard de monitoring
"""

import json
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import psutil

from ..security.aria_security_validator import ARIA_SecurityValidator

logger = logging.getLogger(__name__)


class ARIA_MonitoringSystem:
    """
    Système de monitoring automatisé pour ARIA.

    Fonctionnalités :
    - Surveillance en temps réel
    - Alertes automatiques
    - Métriques de performance
    - Health checks
    - Dashboard de monitoring
    """

    def __init__(self, project_root: str = ".") -> None:
        """
        Initialise le système de monitoring ARIA.

        Args:
            project_root: Racine du projet ARIA
        """
        self.project_root = Path(project_root).resolve()
        self.security_validator = ARIA_SecurityValidator()
        self.monitoring_data: list[dict[str, Any]] = []
        self.alerts: list[dict[str, Any]] = []
        self.is_monitoring = False

        # Configuration des seuils
        self.thresholds = {
            "cpu_percent": 80.0,
            "memory_percent": 85.0,
            "disk_percent": 90.0,
            "response_time_ms": 5000,
            "error_rate_percent": 5.0,
        }

    def start_monitoring(self, interval_seconds: int = 60) -> None:
        """
        Démarre le monitoring en continu.

        Args:
            interval_seconds: Intervalle de collecte des métriques
        """
        logger.info(f"Démarrage du monitoring ARIA (intervalle: {interval_seconds}s)")
        self.is_monitoring = True

        while self.is_monitoring:
            try:
                # Collecter les métriques
                metrics = self.collect_metrics()
                self.monitoring_data.append(metrics)

                # Vérifier les alertes
                self._check_alerts(metrics)

                # Garder seulement les dernières 1000 entrées
                if len(self.monitoring_data) > 1000:
                    self.monitoring_data = self.monitoring_data[-1000:]

                # Attendre l'intervalle suivant
                time.sleep(interval_seconds)

            except Exception as e:
                logger.error(f"Erreur lors du monitoring: {e}")
                time.sleep(interval_seconds)

    def stop_monitoring(self) -> None:
        """Arrête le monitoring."""
        logger.info("Arrêt du monitoring ARIA")
        self.is_monitoring = False

    def collect_metrics(self) -> dict[str, Any]:
        """
        Collecte les métriques système et applicatives.

        Returns:
            Métriques collectées
        """
        timestamp = datetime.now().isoformat()

        # Métriques système
        system_metrics = {
            "timestamp": timestamp,
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
            "load_average": (
                psutil.getloadavg() if hasattr(psutil, "getloadavg") else [0, 0, 0]
            ),
            "process_count": len(psutil.pids()),
        }

        # Métriques réseau
        network_metrics = self._collect_network_metrics()

        # Métriques applicatives ARIA
        aria_metrics = self._collect_aria_metrics()

        # Métriques de sécurité
        security_metrics = self._collect_security_metrics()

        return {
            **system_metrics,
            "network": network_metrics,
            "aria": aria_metrics,
            "security": security_metrics,
        }

    def _collect_network_metrics(self) -> dict[str, Any]:
        """Collecte les métriques réseau."""
        try:
            net_io = psutil.net_io_counters()
            return {
                "bytes_sent": net_io.bytes_sent,
                "bytes_recv": net_io.bytes_recv,
                "packets_sent": net_io.packets_sent,
                "packets_recv": net_io.packets_recv,
                "errin": net_io.errin,
                "errout": net_io.errout,
                "dropin": net_io.dropin,
                "dropout": net_io.dropout,
            }
        except Exception as e:
            logger.error(f"Erreur collecte métriques réseau: {e}")
            return {}

    def _collect_aria_metrics(self) -> dict[str, Any]:
        """Collecte les métriques spécifiques à ARIA."""
        try:
            # Simuler la collecte des métriques ARIA
            return {
                "active_connections": 0,
                "requests_per_minute": 0,
                "response_time_avg": 0,
                "error_count": 0,
                "pain_entries_today": 0,
                "patterns_analyzed": 0,
                "predictions_generated": 0,
            }
        except Exception as e:
            logger.error(f"Erreur collecte métriques ARIA: {e}")
            return {}

    def _collect_security_metrics(self) -> dict[str, Any]:
        """Collecte les métriques de sécurité."""
        try:
            security_report = self.security_validator.get_security_report()
            return {
                "total_validations": security_report.get("total_validations", 0),
                "blocked_attempts": security_report.get("blocked_attempts", 0),
                "risk_summary": security_report.get("risk_summary", {}),
            }
        except Exception as e:
            logger.error(f"Erreur collecte métriques sécurité: {e}")
            return {}

    def _check_alerts(self, metrics: dict[str, Any]) -> None:
        """Vérifie les seuils et génère des alertes."""
        alerts_generated = []

        # Vérifier CPU
        cpu_percent = metrics.get("cpu_percent", 0)
        if cpu_percent > self.thresholds["cpu_percent"]:
            alerts_generated.append(
                {
                    "type": "cpu_high",
                    "severity": "warning",
                    "message": f"Utilisation CPU élevée: {cpu_percent:.1f}%",
                    "value": cpu_percent,
                    "threshold": self.thresholds["cpu_percent"],
                }
            )

        # Vérifier mémoire
        memory_percent = metrics.get("memory_percent", 0)
        if memory_percent > self.thresholds["memory_percent"]:
            alerts_generated.append(
                {
                    "type": "memory_high",
                    "severity": "warning",
                    "message": f"Utilisation mémoire élevée: {memory_percent:.1f}%",
                    "value": memory_percent,
                    "threshold": self.thresholds["memory_percent"],
                }
            )

        # Vérifier disque
        disk_percent = metrics.get("disk_percent", 0)
        if disk_percent > self.thresholds["disk_percent"]:
            alerts_generated.append(
                {
                    "type": "disk_high",
                    "severity": "critical",
                    "message": f"Utilisation disque élevée: {disk_percent:.1f}%",
                    "value": disk_percent,
                    "threshold": self.thresholds["disk_percent"],
                }
            )

        # Vérifier les métriques de sécurité
        security_metrics = metrics.get("security", {})
        blocked_attempts = security_metrics.get("blocked_attempts", 0)
        if blocked_attempts > 10:  # Seuil arbitraire
            alerts_generated.append(
                {
                    "type": "security_high",
                    "severity": "warning",
                    "message": (
                        f"Nombre élevé de tentatives bloquées: {blocked_attempts}"
                    ),
                    "value": blocked_attempts,
                    "threshold": 10,
                }
            )

        # Ajouter les alertes générées
        for alert in alerts_generated:
            alert["timestamp"] = metrics["timestamp"]
            self.alerts.append(alert)
            logger.warning(f"ALERTE: {alert['message']}")

    def get_health_status(self) -> dict[str, Any]:
        """
        Retourne le statut de santé global du système.

        Returns:
            Statut de santé
        """
        if not self.monitoring_data:
            return {
                "status": "unknown",
                "message": "Aucune donnée de monitoring disponible",
                "timestamp": datetime.now().isoformat(),
            }

        latest_metrics = self.monitoring_data[-1]

        # Déterminer le statut basé sur les métriques
        status = "healthy"
        issues = []

        cpu_percent = latest_metrics.get("cpu_percent", 0)
        memory_percent = latest_metrics.get("memory_percent", 0)
        disk_percent = latest_metrics.get("disk_percent", 0)

        if cpu_percent > self.thresholds["cpu_percent"]:
            status = "warning"
            issues.append(f"CPU élevé: {cpu_percent:.1f}%")

        if memory_percent > self.thresholds["memory_percent"]:
            status = "warning"
            issues.append(f"Mémoire élevée: {memory_percent:.1f}%")

        if disk_percent > self.thresholds["disk_percent"]:
            status = "critical"
            issues.append(f"Disque élevé: {disk_percent:.1f}%")

        return {
            "status": status,
            "timestamp": latest_metrics["timestamp"],
            "issues": issues,
            "metrics": latest_metrics,
            "active_alerts": len(
                [
                    a
                    for a in self.alerts
                    if a.get("timestamp", "")
                    > (datetime.now() - timedelta(hours=1)).isoformat()
                ]
            ),
        }

    def get_performance_summary(self, hours: int = 24) -> dict[str, Any]:
        """
        Retourne un résumé des performances sur une période.

        Args:
            hours: Nombre d'heures à analyser

        Returns:
            Résumé des performances
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cutoff_iso = cutoff_time.isoformat()

        recent_data = [m for m in self.monitoring_data if m["timestamp"] > cutoff_iso]

        if not recent_data:
            return {
                "period_hours": hours,
                "data_points": 0,
                "message": "Aucune donnée disponible pour cette période",
            }

        # Calculer les statistiques
        cpu_values = [m["cpu_percent"] for m in recent_data]
        memory_values = [m["memory_percent"] for m in recent_data]
        disk_values = [m["disk_percent"] for m in recent_data]

        return {
            "period_hours": hours,
            "data_points": len(recent_data),
            "cpu": {
                "avg": sum(cpu_values) / len(cpu_values),
                "max": max(cpu_values),
                "min": min(cpu_values),
            },
            "memory": {
                "avg": sum(memory_values) / len(memory_values),
                "max": max(memory_values),
                "min": min(memory_values),
            },
            "disk": {
                "avg": sum(disk_values) / len(disk_values),
                "max": max(disk_values),
                "min": min(disk_values),
            },
            "alerts_count": len(
                [a for a in self.alerts if a.get("timestamp", "") > cutoff_iso]
            ),
        }

    def get_alerts_summary(self, hours: int = 24) -> dict[str, Any]:
        """
        Retourne un résumé des alertes sur une période.

        Args:
            hours: Nombre d'heures à analyser

        Returns:
            Résumé des alertes
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cutoff_iso = cutoff_time.isoformat()

        recent_alerts = [a for a in self.alerts if a.get("timestamp", "") > cutoff_iso]

        # Grouper par type et sévérité
        alert_types = {}
        severity_counts = {"critical": 0, "warning": 0, "info": 0}

        for alert in recent_alerts:
            alert_type = alert.get("type", "unknown")
            severity = alert.get("severity", "info")

            if alert_type not in alert_types:
                alert_types[alert_type] = 0
            alert_types[alert_type] += 1

            if severity in severity_counts:
                severity_counts[severity] += 1

        return {
            "period_hours": hours,
            "total_alerts": len(recent_alerts),
            "alert_types": alert_types,
            "severity_counts": severity_counts,
            "recent_alerts": recent_alerts[-10:],  # Dernières 10 alertes
        }

    def export_monitoring_data(self, format: str = "json", hours: int = 24) -> Path:
        """
        Exporte les données de monitoring.

        Args:
            format: Format d'export (json, csv)
            hours: Nombre d'heures à exporter

        Returns:
            Chemin du fichier exporté
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        cutoff_iso = cutoff_time.isoformat()

        recent_data = [m for m in self.monitoring_data if m["timestamp"] > cutoff_iso]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if format.lower() == "json":
            file_path = self.project_root / f"monitoring_data_{timestamp}.json"
            file_path.write_text(json.dumps(recent_data, indent=2))
        elif format.lower() == "csv":
            file_path = self.project_root / f"monitoring_data_{timestamp}.csv"
            # Conversion simple en CSV
            if recent_data:
                headers = list(recent_data[0].keys())
                csv_content = ",".join(headers) + "\n"
                for data in recent_data:
                    csv_content += (
                        ",".join(str(data.get(h, "")) for h in headers) + "\n"
                    )
                file_path.write_text(csv_content)
        else:
            raise ValueError(f"Format non supporté: {format}")

        return file_path

    def generate_monitoring_dashboard_html(self) -> str:
        """Génère un dashboard HTML de monitoring."""
        health_status = self.get_health_status()
        performance_summary = self.get_performance_summary(24)
        alerts_summary = self.get_alerts_summary(24)

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARKALIA ARIA - Monitoring Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .status-section {{
            padding: 30px;
            text-align: center;
            background: #f8f9fa;
        }}
        .status-healthy {{ color: #28a745; }}
        .status-warning {{ color: #ffc107; }}
        .status-critical {{ color: #dc3545; }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .metric-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #667eea;
        }}
        .chart-container {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 ARKALIA ARIA</h1>
            <p>Monitoring Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="status-section">
            <h2>Statut de Santé</h2>
            <div class="status-{health_status['status']}">
                <h3>{health_status['status'].upper()}</h3>
                <p>Alertes actives: {health_status['active_alerts']}</p>
            </div>
        </div>

        <div class="metrics-grid">
            <div class="metric-card">
                <h3>CPU</h3>
                <p>Moyenne: {performance_summary.get('cpu', {}).get('avg', 0):.1f}%</p>
                <p>Maximum: {performance_summary.get('cpu', {}).get('max', 0):.1f}%</p>
            </div>

            <div class="metric-card">
                <h3>Mémoire</h3>
                <p>Moyenne: {performance_summary.get('memory', {}).get('avg', 0):.1f}%</p>
                <p>Maximum: {performance_summary.get('memory', {}).get('max', 0):.1f}%</p>
            </div>

            <div class="metric-card">
                <h3>Disque</h3>
                <p>Moyenne: {performance_summary.get('disk', {}).get('avg', 0):.1f}%</p>
                <p>Maximum: {performance_summary.get('disk', {}).get('max', 0):.1f}%</p>
            </div>

            <div class="metric-card">
                <h3>Alertes</h3>
                <p>Total: {alerts_summary.get('total_alerts', 0)}</p>
                <p>Critiques: {alerts_summary.get('severity_counts', {}).get('critical', 0)}</p>
                <p>Avertissements: {alerts_summary.get('severity_counts', {}).get('warning', 0)}</p>
            </div>
        </div>

        <div class="chart-container">
            <h3>Métriques en Temps Réel</h3>
            <canvas id="metricsChart" width="400" height="200"></canvas>
        </div>
    </div>

    <script>
        // Graphique des métriques
        const ctx = document.getElementById('metricsChart').getContext('2d');
        const chart = new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: ['CPU', 'Mémoire', 'Disque'],
                datasets: [{{
                    label: 'Utilisation (%)',
                    data: [
                        {performance_summary.get('cpu', {}).get('avg', 0)},
                        {performance_summary.get('memory', {}).get('avg', 0)},
                        {performance_summary.get('disk', {}).get('avg', 0)}
                    ],
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)',
                        'rgba(255, 193, 7, 0.8)'
                    ],
                    borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(118, 75, 162, 1)',
                        'rgba(255, 193, 7, 1)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100
                    }}
                }}
            }}
        }});

        // Actualisation automatique toutes les 30 secondes
        setInterval(() => {{
            location.reload();
        }}, 30000);
    </script>
</body>
</html>"""

        return html
