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
        with patch("cia_sync.auto_sync.requests.get") as mock_get:
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
            patch("cia_sync.auto_sync.requests.get") as mock_get,
            patch("cia_sync.auto_sync.ARIA_AlertsSystem") as mock_alerts,
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
        with patch("cia_sync.auto_sync.requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 503
            mock_get.return_value = mock_response

            # Devrait s'exécuter sans erreur
            auto_sync._check_medical_appointments()
