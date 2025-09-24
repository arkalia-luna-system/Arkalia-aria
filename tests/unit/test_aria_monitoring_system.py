#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_MonitoringSystem
==========================================

Tests complets pour le système de monitoring ARIA.
"""

from unittest.mock import Mock, patch

import pytest

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
        assert "timestamp" in health_status
        assert "monitoring_active" in health_status
        assert "data_points" in health_status
        assert health_status["status"] in ["healthy", "warning", "critical"]
        assert isinstance(health_status["monitoring_active"], bool)
        assert isinstance(health_status["data_points"], int)

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
        assert health_status["data_points"] == 3
        assert health_status["monitoring_active"] is True

    def test_get_performance_summary_success(self):
        """Test cas nominal de get_performance_summary"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        performance_summary = monitoring.get_performance_summary()

        # Assert
        assert isinstance(performance_summary, dict)
        assert "timestamp" in performance_summary
        assert "avg_cpu_percent" in performance_summary
        assert "avg_memory_usage_mb" in performance_summary
        assert "avg_disk_usage_percent" in performance_summary
        assert "peak_cpu_percent" in performance_summary
        assert "peak_memory_usage_mb" in performance_summary
        assert "data_points" in performance_summary

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
        assert performance_summary["data_points"] == 3
        assert performance_summary["avg_cpu_percent"] == 25.0
        assert performance_summary["avg_memory_usage_mb"] == 125.0
        assert performance_summary["avg_disk_usage_percent"] == 32.33
        assert performance_summary["peak_cpu_percent"] == 30
        assert performance_summary["peak_memory_usage_mb"] == 150

    def test_get_performance_summary_empty_data(self):
        """Test get_performance_summary avec données vides"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.monitoring_data = []

        # Act
        performance_summary = monitoring.get_performance_summary()

        # Assert
        assert performance_summary["data_points"] == 0
        assert performance_summary["avg_cpu_percent"] is None
        assert performance_summary["avg_memory_usage_mb"] is None
        assert performance_summary["avg_disk_usage_percent"] is None
        assert performance_summary["peak_cpu_percent"] is None
        assert performance_summary["peak_memory_usage_mb"] is None

    def test_get_alerts_summary_success(self):
        """Test cas nominal de get_alerts_summary"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")

        # Act
        alerts_summary = monitoring.get_alerts_summary()

        # Assert
        assert isinstance(alerts_summary, dict)
        assert "timestamp" in alerts_summary
        assert "total_alerts" in alerts_summary
        assert "critical_alerts" in alerts_summary
        assert "warning_alerts" in alerts_summary
        assert "info_alerts" in alerts_summary
        assert "recent_alerts" in alerts_summary
        assert isinstance(alerts_summary["total_alerts"], int)
        assert isinstance(alerts_summary["critical_alerts"], int)
        assert isinstance(alerts_summary["warning_alerts"], int)
        assert isinstance(alerts_summary["info_alerts"], int)
        assert isinstance(alerts_summary["recent_alerts"], list)

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
        assert alerts_summary["total_alerts"] == 4
        assert alerts_summary["critical_alerts"] == 2
        assert alerts_summary["warning_alerts"] == 1
        assert alerts_summary["info_alerts"] == 1
        assert len(alerts_summary["recent_alerts"]) <= 4

    def test_start_monitoring_success(self):
        """Test cas nominal de start_monitoring"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.is_monitoring = False

        # Act
        result = monitoring.start_monitoring()

        # Assert
        assert result is True
        assert monitoring.is_monitoring is True

    def test_stop_monitoring_success(self):
        """Test cas nominal de stop_monitoring"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.is_monitoring = True

        # Act
        result = monitoring.stop_monitoring()

        # Assert
        assert result is True
        assert monitoring.is_monitoring is False

    def test_add_alert_success(self):
        """Test cas nominal de add_alert"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        alert_data = {
            "level": "warning",
            "message": "Test alert",
            "source": "test",
            "details": {"cpu_percent": 85},
        }

        # Act
        monitoring.add_alert(alert_data)

        # Assert
        assert len(monitoring.alerts) == 1
        assert monitoring.alerts[0]["level"] == "warning"
        assert monitoring.alerts[0]["message"] == "Test alert"
        assert "timestamp" in monitoring.alerts[0]

    def test_add_alert_error_handling(self):
        """Test gestion d'erreur de add_alert"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        invalid_alert = None

        # Act & Assert
        with pytest.raises(Exception):
            monitoring.add_alert(invalid_alert)

    def test_clear_alerts_success(self):
        """Test cas nominal de clear_alerts"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.alerts = [
            {"level": "warning", "message": "Test alert 1"},
            {"level": "critical", "message": "Test alert 2"},
        ]

        # Act
        monitoring.clear_alerts()

        # Assert
        assert len(monitoring.alerts) == 0

    def test_get_monitoring_data_success(self):
        """Test cas nominal de get_monitoring_data"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.monitoring_data = [
            {"timestamp": "2024-01-01T00:00:00", "cpu_percent": 20},
            {"timestamp": "2024-01-01T00:01:00", "cpu_percent": 25},
        ]

        # Act
        data = monitoring.get_monitoring_data()

        # Assert
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["cpu_percent"] == 20
        assert data[1]["cpu_percent"] == 25

    def test_get_monitoring_data_with_limit(self):
        """Test get_monitoring_data avec limite"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        monitoring.monitoring_data = [
            {"timestamp": "2024-01-01T00:00:00", "cpu_percent": 20},
            {"timestamp": "2024-01-01T00:01:00", "cpu_percent": 25},
            {"timestamp": "2024-01-01T00:02:00", "cpu_percent": 30},
        ]

        # Act
        data = monitoring.get_monitoring_data(limit=2)

        # Assert
        assert len(data) == 2
        assert data[0]["cpu_percent"] == 20
        assert data[1]["cpu_percent"] == 25

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

    def test_calculate_average_success(self):
        """Test cas nominal de _calculate_average"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        values = [10, 20, 30, 40, 50]

        # Act
        average = monitoring._calculate_average(values)

        # Assert
        assert average == 30.0

    def test_calculate_average_empty_list(self):
        """Test _calculate_average avec liste vide"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        values = []

        # Act
        average = monitoring._calculate_average(values)

        # Assert
        assert average is None

    def test_calculate_average_with_none_values(self):
        """Test _calculate_average avec valeurs None"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        values = [10, None, 30, None, 50]

        # Act
        average = monitoring._calculate_average(values)

        # Assert
        assert average == 30.0  # Devrait ignorer les None

    def test_calculate_peak_success(self):
        """Test cas nominal de _calculate_peak"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        values = [10, 20, 30, 40, 50]

        # Act
        peak = monitoring._calculate_peak(values)

        # Assert
        assert peak == 50

    def test_calculate_peak_empty_list(self):
        """Test _calculate_peak avec liste vide"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        values = []

        # Act
        peak = monitoring._calculate_peak(values)

        # Assert
        assert peak is None

    def test_calculate_peak_with_none_values(self):
        """Test _calculate_peak avec valeurs None"""
        # Arrange
        monitoring = ARIA_MonitoringSystem(".")
        values = [10, None, 30, None, 50]

        # Act
        peak = monitoring._calculate_peak(values)

        # Assert
        assert peak == 50  # Devrait ignorer les None
