"""
Tests unitaires pour les graphiques de corrélations dans le dashboard
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestDashboardCorrelations:
    """Tests pour les graphiques de corrélations interactifs."""

    def test_sleep_pain_correlation_endpoint(self):
        """Test que l'endpoint corrélation sommeil-douleur fonctionne."""
        response = client.get("/api/patterns/correlations/sleep-pain?days=30")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "correlation" in data

    def test_stress_pain_correlation_endpoint(self):
        """Test que l'endpoint corrélation stress-douleur fonctionne."""
        response = client.get("/api/patterns/correlations/stress-pain?days=30")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "correlation" in data

    def test_correlation_with_different_periods(self):
        """Test corrélations avec différentes périodes."""
        for days in [7, 30, 90]:
            response = client.get(f"/api/patterns/correlations/sleep-pain?days={days}")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, dict)
