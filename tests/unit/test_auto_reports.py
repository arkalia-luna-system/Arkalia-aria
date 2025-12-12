"""
Tests unitaires pour les rapports automatiques
"""

from unittest.mock import MagicMock, patch

import pytest

from health_connectors.report_generator import HealthReportGenerator


class TestHealthReportGenerator:
    """Tests pour le générateur de rapports automatiques."""

    @pytest.fixture
    def report_generator(self, tmp_path):
        """Fixture pour HealthReportGenerator."""
        return HealthReportGenerator(reports_dir=tmp_path)

    def test_report_generator_initialization(self, report_generator):
        """Test initialisation du générateur."""
        assert report_generator.reports_dir.exists()
        assert report_generator.is_running is False

    def test_start_weekly_reports(self, report_generator):
        """Test démarrage rapports hebdomadaires."""
        success = report_generator.start_weekly_reports()
        assert success is True
        assert report_generator.is_running is True
        assert report_generator.report_thread is not None

        # Arrêter
        report_generator.stop_weekly_reports()

    def test_stop_weekly_reports(self, report_generator):
        """Test arrêt rapports hebdomadaires."""
        report_generator.start_weekly_reports()
        success = report_generator.stop_weekly_reports()
        assert success is True
        assert report_generator.is_running is False

    def test_generate_weekly_report(self, report_generator):
        """Test génération rapport hebdomadaire."""
        with patch("health_connectors.sync_manager.HealthSyncManager") as mock_sync:
            mock_instance = MagicMock()
            mock_sync.return_value = mock_instance

            # Mock des méthodes async

            async def mock_get_activity(*args, **kwargs):
                return []

            async def mock_get_sleep(*args, **kwargs):
                return []

            async def mock_get_stress(*args, **kwargs):
                return []

            async def mock_generate_metrics(*args, **kwargs):
                return {"sleep": {}, "stress": {}, "activity": {}}

            mock_instance.get_unified_activity_data = mock_get_activity
            mock_instance.get_unified_sleep_data = mock_get_sleep
            mock_instance.get_unified_stress_data = mock_get_stress
            mock_instance._generate_unified_metrics = mock_generate_metrics

            result = report_generator.generate_weekly_report()
            assert isinstance(result, dict)
            assert "period" in result
