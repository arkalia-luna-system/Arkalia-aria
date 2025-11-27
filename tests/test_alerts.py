"""
Tests pour le système d'alertes ARIA
"""

from fastapi.testclient import TestClient

from core.alerts import AlertSeverity, AlertType, ARIA_AlertsSystem, get_alerts_system
from main import app

client = TestClient(app)


class TestAlertsSystem:
    """Tests pour le système d'alertes."""

    def test_create_alert(self):
        """Test la création d'une alerte."""
        alerts_system = ARIA_AlertsSystem()
        alert_id = alerts_system.create_alert(
            alert_type=AlertType.PATTERN_DETECTED,
            severity=AlertSeverity.WARNING,
            title="Test Alerte",
            message="Message de test",
            data={"test": True},
        )
        assert alert_id > 0

    def test_get_alerts(self):
        """Test la récupération des alertes."""
        alerts_system = ARIA_AlertsSystem()
        result = alerts_system.get_alerts(limit=10, offset=0)
        assert "alerts" in result
        assert "total" in result
        assert "limit" in result
        assert "offset" in result
        assert "has_more" in result

    def test_mark_as_read(self):
        """Test le marquage d'une alerte comme lue."""
        alerts_system = ARIA_AlertsSystem()
        # Créer une alerte
        alert_id = alerts_system.create_alert(
            alert_type=AlertType.PATTERN_DETECTED,
            severity=AlertSeverity.INFO,
            title="Test",
            message="Test",
        )
        # Marquer comme lue
        success = alerts_system.mark_as_read(alert_id)
        assert success is True

    def test_mark_all_as_read(self):
        """Test le marquage de toutes les alertes comme lues."""
        alerts_system = ARIA_AlertsSystem()
        count = alerts_system.mark_all_as_read()
        assert count >= 0

    def test_check_patterns(self):
        """Test la vérification des patterns."""
        alerts_system = ARIA_AlertsSystem()
        # Ne devrait pas lever d'exception même sans données
        result = alerts_system.check_patterns(days_back=30)
        assert isinstance(result, list)

    def test_check_predictions(self):
        """Test la vérification des prédictions."""
        alerts_system = ARIA_AlertsSystem()
        # Ne devrait pas lever d'exception même sans données
        result = alerts_system.check_predictions()
        assert isinstance(result, list)

    def test_check_correlations(self):
        """Test la vérification des corrélations."""
        alerts_system = ARIA_AlertsSystem()
        # Ne devrait pas lever d'exception même sans données
        result = alerts_system.check_correlations(days_back=30)
        assert isinstance(result, list)

    def test_check_all(self):
        """Test la vérification complète."""
        alerts_system = ARIA_AlertsSystem()
        result = alerts_system.check_all(days_back=30)
        assert "patterns" in result
        assert "predictions" in result
        assert "correlations" in result
        assert "total" in result
        assert "timestamp" in result


class TestAlertsAPI:
    """Tests pour l'API des alertes."""

    def test_alerts_status(self):
        """Test le statut de l'API alertes."""
        response = client.get("/api/alerts/status")
        assert response.status_code == 200
        data = response.json()
        # BaseAPI modifie la réponse, vérifier les champs disponibles
        assert "status" in data or "api_name" in data
        assert response.status_code == 200

    def test_get_alerts(self):
        """Test la récupération des alertes via API."""
        response = client.get("/api/alerts?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert "alerts" in data
        assert "total" in data

    def test_get_unread_count(self):
        """Test le comptage des alertes non lues."""
        response = client.get("/api/alerts/unread/count")
        assert response.status_code == 200
        data = response.json()
        assert "unread_count" in data

    def test_check_alerts(self):
        """Test la vérification des alertes via API."""
        response = client.post("/api/alerts/check?days_back=30")
        assert response.status_code == 200
        data = response.json()
        assert "patterns" in data
        assert "predictions" in data
        assert "correlations" in data
        assert "total" in data

    def test_mark_alert_as_read(self):
        """Test le marquage d'une alerte comme lue via API."""
        # Créer une alerte d'abord
        alerts_system = get_alerts_system()
        alert_id = alerts_system.create_alert(
            alert_type=AlertType.PATTERN_DETECTED,
            severity=AlertSeverity.INFO,
            title="Test API",
            message="Test",
        )

        response = client.post(f"/api/alerts/{alert_id}/read")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["alert_id"] == alert_id

    def test_mark_all_alerts_as_read(self):
        """Test le marquage de toutes les alertes comme lues via API."""
        response = client.post("/api/alerts/read-all")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "count" in data
