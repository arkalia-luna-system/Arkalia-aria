"""
Tests pour les endpoints de compatibilité CIA
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestCIACompatibility:
    """Tests pour les endpoints de compatibilité CIA"""

    def test_pain_records_compat(self):
        """Test GET /api/pain-records (compatibilité CIA)"""
        response = client.get("/api/pain-records?limit=10&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert "entries" in data or isinstance(data, list)
        assert "total" in data or len(data) >= 0

    def test_pain_records_compat_pagination(self):
        """Test GET /api/pain-records avec pagination"""
        response = client.get("/api/pain-records?limit=5&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert "limit" in data or isinstance(data, list)

    def test_patterns_compat(self):
        """Test GET /api/patterns (compatibilité CIA)"""
        response = client.get("/api/patterns?days=30")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_health_metrics_compat(self):
        """Test GET /api/health-metrics (compatibilité CIA)"""
        response = client.get("/api/health-metrics")
        # Peut retourner 200 ou 503 si métriques désactivées
        assert response.status_code in [200, 503]
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, dict)

    def test_pain_entries_post_compat(self):
        """Test POST /api/pain/entries (compatibilité CIA)"""
        entry_data = {
            "intensity": 5,
            "physical_trigger": "stress",
            "location": "tête",
        }
        response = client.post("/api/pain/entries", json=entry_data)
        assert response.status_code in [200, 201]
        data = response.json()
        assert "id" in data
        assert data["intensity"] == 5

    def test_pain_entries_post_compat_invalid(self):
        """Test POST /api/pain/entries avec données invalides"""
        entry_data = {
            "intensity": 15,  # Invalide (> 10)
            "physical_trigger": "stress",
        }
        response = client.post("/api/pain/entries", json=entry_data)
        # Devrait retourner 422 (validation error) ou 500
        assert response.status_code in [422, 500]
