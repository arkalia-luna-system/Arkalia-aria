"""
Tests unitaires pour les alertes RDV médicaux
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

from cia_sync.auto_sync import AutoSyncManager


class TestMedicalAppointmentsAlerts:
    """Tests pour les alertes RDV médicaux depuis CIA."""

    @pytest.fixture
    def auto_sync(self):
        """Fixture pour AutoSyncManager."""
        return AutoSyncManager(cia_base_url="http://127.0.0.1:8000")

    def test_check_medical_appointments_no_appointments(self, auto_sync):
        """Test vérification appointments sans RDV."""
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"appointments": []}
            mock_get.return_value = mock_response

            # Devrait s'exécuter sans erreur
            auto_sync._check_medical_appointments()

    def test_check_medical_appointments_with_appointment_today(self, auto_sync):
        """Test création alerte pour RDV aujourd'hui."""
        tomorrow = datetime.now() + timedelta(days=1)
        appointments = [
            {
                "date": tomorrow.isoformat(),
                "title": "Consultation",
                "doctor": "Dr. Test",
            }
        ]

        with (
            patch("requests.get") as mock_get,
            patch("core.alerts.ARIA_AlertsSystem") as mock_alerts,
        ):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"appointments": appointments}
            mock_get.return_value = mock_response

            mock_instance = MagicMock()
            mock_alerts.return_value = mock_instance

            auto_sync._check_medical_appointments()

            # Vérifier qu'une alerte a été créée
            assert mock_instance.create_alert.called

    def test_check_medical_appointments_cia_unavailable(self, auto_sync):
        """Test gestion CIA indisponible."""
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 503
            mock_get.return_value = mock_response

            # Devrait s'exécuter sans erreur
            auto_sync._check_medical_appointments()

    def test_check_medical_appointments_reminder_24h(self, auto_sync):
        """Test création alerte de rappel 24h avant RDV."""
        # RDV dans 24 heures
        tomorrow = datetime.now() + timedelta(hours=24)
        appointments = [
            {
                "id": "appt_123",
                "date": tomorrow.isoformat(),
                "title": "Consultation",
                "doctor": "Dr. Test",
                "location": "Cabinet médical",
            }
        ]

        with (
            patch("requests.get") as mock_get,
            patch("core.alerts.ARIA_AlertsSystem") as mock_alerts,
        ):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "pulled_data": {"appointments": appointments}
            }
            mock_get.return_value = mock_response

            mock_instance = MagicMock()
            mock_instance.get_alerts.return_value = {"alerts": []}
            mock_alerts.return_value = mock_instance

            auto_sync._check_medical_appointments()

            # Vérifier qu'au moins une alerte a été créée (générale + rappel)
            assert mock_instance.create_alert.call_count >= 1

            # Vérifier qu'une alerte de rappel a été créée
            calls = mock_instance.create_alert.call_args_list
            reminder_found = False
            for call in calls:
                # call[0] = args (positional), call[1] = kwargs
                args = call[0] if call[0] else []
                kwargs = call[1] if len(call) > 1 else {}
                # data peut être dans args (position 4) ou kwargs
                if len(args) > 4:
                    data = args[4]
                else:
                    data = kwargs.get("data", {})
                if isinstance(data, dict) and data.get("alert_type") == "reminder_24h":
                    reminder_found = True
                    break
            assert reminder_found, "Aucune alerte de rappel 24h créée"

    def test_check_medical_appointments_no_duplicates(self, auto_sync):
        """Test qu'aucune alerte dupliquée n'est créée."""
        tomorrow = datetime.now() + timedelta(days=1)
        appointments = [
            {
                "id": "appt_456",
                "date": tomorrow.isoformat(),
                "title": "Consultation",
                "doctor": "Dr. Test",
            }
        ]

        # Simuler une alerte existante
        existing_alert = {
            "id": 1,
            "data": (
                '{"appointment_id": "appt_456", "appointment_date": "'
                + tomorrow.isoformat()
                + '", "alert_type": "general"}'
            ),
        }

        with (
            patch("requests.get") as mock_get,
            patch("core.alerts.ARIA_AlertsSystem") as mock_alerts,
        ):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "pulled_data": {"appointments": appointments}
            }
            mock_get.return_value = mock_response

            mock_instance = MagicMock()
            mock_instance.get_alerts.return_value = {"alerts": [existing_alert]}
            mock_alerts.return_value = mock_instance

            auto_sync._check_medical_appointments()

            # Vérifier qu'aucune nouvelle alerte générale n'a été créée
            calls = mock_instance.create_alert.call_args_list
            general_calls = [
                call
                for call in calls
                if call[1].get("data", {}).get("alert_type") == "general"
            ]
            assert len(general_calls) == 0

    def test_check_medical_appointments_different_date_formats(self, auto_sync):
        """Test gestion de différents formats de dates."""
        now = datetime.now()
        appointments = [
            {
                "id": "appt_1",
                "date": (now + timedelta(days=2)).isoformat(),
                "title": "RDV ISO",
            },
            {
                "id": "appt_2",
                "date": (now + timedelta(days=3)).strftime("%Y-%m-%d"),
                "title": "RDV Date simple",
            },
            {
                "id": "appt_3",
                "appointment_date": (now + timedelta(days=4)).isoformat(),
                "title": "RDV avec appointment_date",
            },
        ]

        with (
            patch("requests.get") as mock_get,
            patch("core.alerts.ARIA_AlertsSystem") as mock_alerts,
        ):
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "pulled_data": {"appointments": appointments}
            }
            mock_get.return_value = mock_response

            mock_instance = MagicMock()
            mock_instance.get_alerts.return_value = {"alerts": []}
            mock_alerts.return_value = mock_instance

            # Ne devrait pas lever d'exception
            auto_sync._check_medical_appointments()

            # Devrait créer des alertes pour les RDV valides (au moins 2 sur 3)
            assert mock_instance.create_alert.call_count >= 2
