#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_MonitoringSystem
==========================================

Tests complets pour le système de monitoring ARIA.
"""

from unittest.mock import Mock, patch

from devops_automation.monitoring.aria_monitoring_system import ARIA_MonitoringSystem


class TestARIA_MonitoringSystem:
    """Tests unitaires pour ARIA_MonitoringSystem"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.monitoring = ARIA_MonitoringSystem(".")

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        monitoring = ARIA_MonitoringSystem(".")

        # Assert
        assert monitoring.project_root == "."
        assert monitoring.is_monitoring is True
        assert isinstance(monitoring.monitoring_data, list)
        assert isinstance(monitoring.alerts, list)

    def test_init_with_custom_root(self):
        """Test initialisation avec racine personnalisée"""
        # Arrange
        custom_root = "/custom/path"

        # Act
        monitoring = ARIA_MonitoringSystem(custom_root)

        # Assert
        assert monitoring.project_root == custom_root

    def test_collect_metrics_success(self):
        """Test cas nominal de collect_metrics"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        metrics = monitoring.collect_metrics()

        # Assert
        assert isinstance(metrics, dict)
        assert "timestamp" in metrics
        assert "process_count" in metrics
        assert "cpu_percent" in metrics
        assert "memory_usage_mb" in metrics
        assert "disk_usage_percent" in metrics
        assert isinstance(metrics["timestamp"], str)

    @patch("devops_automation.monitoring.aria_monitoring_system.psutil")
    def test_collect_metrics_with_psutil(self, mock_psutil):
        """Test collect_metrics avec psutil disponible"""
        # Arrange
        mock_psutil.pids.return_value = [1, 2, 3, 4, 5]
        mock_psutil.cpu_percent.return_value = 25.5
        mock_memory = Mock()
        mock_memory.used = 1024 * 1024 * 512  # 512 MB
        mock_psutil.virtual_memory.return_value = mock_memory
        mock_disk = Mock()
        mock_disk.percent = 45.0
        mock_psutil.disk_usage.return_value = mock_disk

        monitoring = ARIA_MonitoringSystem(".")

        # Act
        metrics = monitoring.collect_metrics()

        # Assert
        assert metrics["process_count"] == 5
        assert metrics["cpu_percent"] == 25.5
        assert metrics["memory_usage_mb"] == 512.0
        assert metrics["disk_usage_percent"] == 45.0
        assert "note" not in metrics
        assert "error" not in metrics

    def test_collect_metrics_without_psutil(self):
        """Test collect_metrics sans psutil"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Mock psutil comme None
        with patch("devops_automation.monitoring.aria_monitoring_system.psutil", None):
            # Act
            metrics = monitoring.collect_metrics()

            # Assert
            assert metrics["process_count"] is None
            assert metrics["cpu_percent"] is None
            assert metrics["memory_usage_mb"] is None
            assert metrics["disk_usage_percent"] is None
            assert "note" in metrics
            assert "psutil non installé" in metrics["note"]

    @patch("devops_automation.monitoring.aria_monitoring_system.psutil")
    def test_collect_metrics_error_handling(self, mock_psutil):
        """Test gestion d'erreur de collect_metrics"""
        # Arrange
        mock_psutil.pids.side_effect = Exception("Test error")
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        metrics = monitoring.collect_metrics()

        # Assert
        assert "error" in metrics
        assert "Test error" in metrics["error"]

    def test_get_health_status_success(self):
        """Test cas nominal de get_health_status"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        health_status = monitoring.get_health_status()

        # Assert
        assert isinstance(health_status, dict)
        assert "status" in health_status
        assert "metrics" in health_status
        assert health_status["status"] in ["excellent", "degraded", "critical"]
        assert isinstance(health_status["metrics"], dict)
        assert "timestamp" in health_status["metrics"]

    def test_get_health_status_with_data(self):
        """Test get_health_status avec données de monitoring"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.monitoring_data = [
            {"timestamp": "2024-01-01T00:00:00", "cpu_percent": 20},
            {"timestamp": "2024-01-01T00:01:00", "cpu_percent": 25},
            {"timestamp": "2024-01-01T00:02:00", "cpu_percent": 30},
        ]

        # Act
        health_status = monitoring.get_health_status()

        # Assert
        assert isinstance(health_status, dict)
        assert "status" in health_status
        assert "metrics" in health_status
        assert health_status["status"] in ["excellent", "degraded", "critical"]

    def test_get_performance_summary_success(self):
        """Test cas nominal de get_performance_summary"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        performance_summary = monitoring.get_performance_summary()

        # Assert
        assert isinstance(performance_summary, dict)
        assert "hours" in performance_summary
        assert "current" in performance_summary
        assert isinstance(performance_summary["hours"], int)
        assert isinstance(performance_summary["current"], dict)
        assert "timestamp" in performance_summary["current"]

    def test_get_performance_summary_with_data(self):
        """Test get_performance_summary avec données"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.monitoring_data = [
            {"cpu_percent": 20, "memory_usage_mb": 100, "disk_usage_percent": 30},
            {"cpu_percent": 30, "memory_usage_mb": 150, "disk_usage_percent": 35},
            {"cpu_percent": 25, "memory_usage_mb": 125, "disk_usage_percent": 32},
        ]

        # Act
        performance_summary = monitoring.get_performance_summary()

        # Assert
        assert isinstance(performance_summary, dict)
        assert "hours" in performance_summary
        assert "current" in performance_summary
        assert isinstance(performance_summary["hours"], int)
        assert isinstance(performance_summary["current"], dict)

    def test_get_performance_summary_empty_data(self):
        """Test get_performance_summary avec données vides"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.monitoring_data = []

        # Act
        performance_summary = monitoring.get_performance_summary()

        # Assert
        assert isinstance(performance_summary, dict)
        assert "hours" in performance_summary
        assert "current" in performance_summary
        assert isinstance(performance_summary["hours"], int)
        assert isinstance(performance_summary["current"], dict)

    def test_get_alerts_summary_success(self):
        """Test cas nominal de get_alerts_summary"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        alerts_summary = monitoring.get_alerts_summary()

        # Assert
        assert isinstance(alerts_summary, dict)
        assert "hours" in alerts_summary
        assert "alerts_count" in alerts_summary
        assert "alerts" in alerts_summary
        assert isinstance(alerts_summary["hours"], int)
        assert isinstance(alerts_summary["alerts_count"], int)
        assert isinstance(alerts_summary["alerts"], list)

    def test_get_alerts_summary_with_alerts(self):
        """Test get_alerts_summary avec alertes"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.alerts = [
            {
                "level": "critical",
                "message": "High CPU usage",
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "level": "warning",
                "message": "Memory usage high",
                "timestamp": "2024-01-01T00:01:00",
            },
            {
                "level": "info",
                "message": "System check",
                "timestamp": "2024-01-01T00:02:00",
            },
            {
                "level": "critical",
                "message": "Disk full",
                "timestamp": "2024-01-01T00:03:00",
            },
        ]

        # Act
        alerts_summary = monitoring.get_alerts_summary()

        # Assert
        assert isinstance(alerts_summary, dict)
        assert "hours" in alerts_summary
        assert "alerts_count" in alerts_summary
        assert "alerts" in alerts_summary
        assert alerts_summary["alerts_count"] == 4
        assert len(alerts_summary["alerts"]) == 4

    def test_generate_monitoring_dashboard_html_success(self):
        """Test cas nominal de generate_monitoring_dashboard_html"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        html_content = monitoring.generate_monitoring_dashboard_html()

        # Assert
        assert isinstance(html_content, str)
        assert "<!doctype html>" in html_content
        assert "<title>Monitoring ARIA</title>" in html_content
        assert "<h1>Monitoring ARIA</h1>" in html_content
        assert "Timestamp:" in html_content
        assert "CPU:" in html_content
        assert "Mémoire (MB):" in html_content
        assert "Disque (%):" in html_content
        assert "Processus:" in html_content

    def test_export_monitoring_data_success(self):
        """Test cas nominal de export_monitoring_data"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        filename = monitoring.export_monitoring_data("json", 24)

        # Assert
        assert isinstance(filename, str)
        assert "monitoring_export_24h.json" == filename

    def test_export_monitoring_data_html(self):
        """Test export_monitoring_data avec format HTML"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        filename = monitoring.export_monitoring_data("html", 12)

        # Assert
        assert isinstance(filename, str)
        assert "monitoring_export_12h.html" == filename

    def test_export_monitoring_data_csv(self):
        """Test export_monitoring_data avec format CSV"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        filename = monitoring.export_monitoring_data("csv", 48)

        # Assert
        assert isinstance(filename, str)
        assert "monitoring_export_48h.csv" == filename

    def test_now_success(self):
        """Test cas nominal de _now"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        timestamp = monitoring._now()

        # Assert
        assert isinstance(timestamp, str)
        assert "T" in timestamp
        assert len(timestamp) >= 19  # Format ISO minimum
