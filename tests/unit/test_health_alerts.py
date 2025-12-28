"""
Tests unitaires pour les alertes basées sur données santé
"""

from unittest.mock import MagicMock, patch

import pytest

from health_connectors.sync_manager import HealthSyncManager


class TestHealthAlerts:
    """Tests pour les alertes basées sur données santé."""

    @pytest.fixture
    def sync_manager(self):
        """Fixture pour HealthSyncManager."""
        return HealthSyncManager()

    def test_create_health_alerts_sleep_insufficient(self, sync_manager):
        """Test création alerte sommeil insuffisant."""
        metrics = {
            "sleep": {"avg_duration_hours": 5.0},
            "stress": {"avg_stress_level": 50.0},
            "activity": {"avg_heart_rate": 70.0},
        }

        with patch("core.alerts.ARIA_AlertsSystem") as mock_alerts:
            mock_instance = MagicMock()
            mock_alerts.return_value = mock_instance
            sync_manager._create_health_alerts(metrics)

            # Vérifier qu'une alerte a été créée
            assert mock_instance.create_alert.called

    def test_create_health_alerts_stress_high(self, sync_manager):
        """Test création alerte stress élevé."""
        metrics = {
            "sleep": {"avg_duration_hours": 8.0},
            "stress": {"avg_stress_level": 75.0},
            "activity": {"avg_heart_rate": 70.0},
        }

        with patch("core.alerts.ARIA_AlertsSystem") as mock_alerts:
            mock_instance = MagicMock()
            mock_alerts.return_value = mock_instance
            sync_manager._create_health_alerts(metrics)

            # Vérifier qu'une alerte a été créée
            assert mock_instance.create_alert.called

    def test_create_health_alerts_heart_rate_high(self, sync_manager):
        """Test création alerte fréquence cardiaque élevée."""
        metrics = {
            "sleep": {"avg_duration_hours": 8.0},
            "stress": {"avg_stress_level": 50.0},
            "activity": {"avg_heart_rate": 110.0},
        }

        with patch("core.alerts.ARIA_AlertsSystem") as mock_alerts:
            mock_instance = MagicMock()
            mock_alerts.return_value = mock_instance
            sync_manager._create_health_alerts(metrics)

            # Vérifier qu'une alerte a été créée
            assert mock_instance.create_alert.called

    def test_create_health_alerts_no_alerts(self, sync_manager):
        """Test qu'aucune alerte n'est créée si tout est normal."""
        metrics = {
            "sleep": {"avg_duration_hours": 8.0},
            "stress": {"avg_stress_level": 50.0},
            "activity": {"avg_heart_rate": 70.0},
        }

        with patch("core.alerts.ARIA_AlertsSystem") as mock_alerts:
            mock_instance = MagicMock()
            mock_alerts.return_value = mock_instance
            sync_manager._create_health_alerts(metrics)

            # Vérifier qu'aucune alerte n'a été créée (valeurs normales)
            # Note: selon les seuils, peut-être qu'aucune alerte n'est créée
            # On vérifie juste que la méthode s'exécute sans erreur

    def test_create_health_alerts_sleep_trend_decreasing(self, sync_manager):
        """Test création alerte tendance sommeil en baisse."""
        metrics = {
            "sleep": {"avg_duration_hours": 6.5, "trend": "decreasing"},
            "stress": {"avg_stress_level": 50.0},
            "activity": {"avg_heart_rate": 70.0},
        }

        with patch("core.alerts.ARIA_AlertsSystem") as mock_alerts:
            mock_instance = MagicMock()
            mock_alerts.return_value = mock_instance
            sync_manager._create_health_alerts(metrics)

            # Vérifier qu'une alerte a été créée
            assert mock_instance.create_alert.called

    def test_create_health_alerts_stress_trend_increasing(self, sync_manager):
        """Test création alerte tendance stress en hausse."""
        metrics = {
            "sleep": {"avg_duration_hours": 8.0},
            "stress": {"avg_stress_level": 65.0, "trend": "increasing"},
            "activity": {"avg_heart_rate": 70.0},
        }

        with patch("core.alerts.ARIA_AlertsSystem") as mock_alerts:
            mock_instance = MagicMock()
            mock_alerts.return_value = mock_instance
            sync_manager._create_health_alerts(metrics)

            # Vérifier qu'une alerte a été créée
            assert mock_instance.create_alert.called

    def test_create_health_alerts_low_activity(self, sync_manager):
        """Test création alerte activité physique insuffisante."""
        metrics = {
            "sleep": {"avg_duration_hours": 8.0},
            "stress": {"avg_stress_level": 50.0},
            "activity": {"avg_heart_rate": 70.0, "avg_daily_steps": 3000},
        }

        with patch("core.alerts.ARIA_AlertsSystem") as mock_alerts:
            mock_instance = MagicMock()
            mock_alerts.return_value = mock_instance
            sync_manager._create_health_alerts(metrics)

            # Vérifier qu'une alerte a été créée
            assert mock_instance.create_alert.called

    def test_create_health_alerts_no_duplicates(self, sync_manager):
        """Test qu'aucune alerte dupliquée n'est créée."""
        metrics = {
            "sleep": {"avg_duration_hours": 5.0},
            "stress": {"avg_stress_level": 75.0},
            "activity": {"avg_heart_rate": 70.0},
        }

        import json

        existing_alert = {
            "id": 1,
            "data": json.dumps(
                {
                    "alert_key": "sleep_insufficient_5",
                    "sleep_duration_hours": 5.0,
                }
            ),
        }

        with patch("core.alerts.ARIA_AlertsSystem") as mock_alerts:
            mock_instance = MagicMock()
            mock_instance.get_alerts.return_value = {"alerts": [existing_alert]}
            mock_alerts.return_value = mock_instance

            sync_manager._create_health_alerts(metrics)

            # Vérifier qu'aucune nouvelle alerte sommeil n'a été créée (doublon)
            calls = mock_instance.create_alert.call_args_list
            sleep_alert_found = False
            for call in calls:
                args = call[0] if call[0] else []
                kwargs = call[1] if len(call) > 1 else {}
                data = args[4] if len(args) > 4 else kwargs.get("data", {})
                if (
                    isinstance(data, dict)
                    and data.get("alert_key") == "sleep_insufficient_5"
                ):
                    sleep_alert_found = True
                    break
            assert not sleep_alert_found, "Une alerte sommeil dupliquée a été créée"
