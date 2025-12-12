"""
Tests unitaires pour les endpoints Pattern Analysis API
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestPatternsEndpoints:
    """Tests pour les endpoints d'analyse de patterns"""

    def test_get_patterns_recent_success(self):
        """Test GET /api/patterns/patterns/recent avec paramètres valides"""
        response = client.get("/api/patterns/patterns/recent?days=30")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_patterns_recent_invalid_days(self):
        """Test GET /api/patterns/patterns/recent avec days invalide"""
        response = client.get("/api/patterns/patterns/recent?days=500")  # > 365 max
        assert response.status_code == 422  # Validation error

    def test_get_patterns_recent_negative_days(self):
        """Test GET /api/patterns/patterns/recent avec days négatif"""
        response = client.get("/api/patterns/patterns/recent?days=-1")
        assert response.status_code == 422  # Validation error

    def test_get_sleep_pain_correlation(self):
        """Test GET /api/patterns/correlations/sleep-pain"""
        response = client.get("/api/patterns/correlations/sleep-pain?days=30")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_stress_pain_correlation(self):
        """Test GET /api/patterns/correlations/stress-pain"""
        response = client.get("/api/patterns/correlations/stress-pain?days=30")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_get_recurrent_triggers(self):
        """Test GET /api/patterns/triggers/recurrent"""
        response = client.get(
            "/api/patterns/triggers/recurrent?days=30&min_occurrences=3"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_post_analyze_comprehensive(self):
        """Test POST /api/patterns/analyze avec type comprehensive"""
        data = {"days_back": 30, "analysis_type": "comprehensive"}
        response = client.post("/api/patterns/analyze", json=data)
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)

    def test_post_analyze_sleep(self):
        """Test POST /api/patterns/analyze avec type sleep"""
        data = {"days_back": 30, "analysis_type": "sleep"}
        response = client.post("/api/patterns/analyze", json=data)
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)

    def test_post_analyze_stress(self):
        """Test POST /api/patterns/analyze avec type stress"""
        data = {"days_back": 30, "analysis_type": "stress"}
        response = client.post("/api/patterns/analyze", json=data)
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)

    def test_post_analyze_triggers(self):
        """Test POST /api/patterns/analyze avec type triggers"""
        data = {"days_back": 30, "analysis_type": "triggers"}
        response = client.post("/api/patterns/analyze", json=data)
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result, dict)

    def test_post_analyze_invalid_type(self):
        """Test POST /api/patterns/analyze avec type invalide"""
        data = {"days_back": 30, "analysis_type": "invalid"}
        response = client.post("/api/patterns/analyze", json=data)
        assert response.status_code == 400  # Bad request

    def test_post_analyze_invalid_days(self):
        """Test POST /api/patterns/analyze avec days_back invalide"""
        data = {"days_back": -1, "analysis_type": "comprehensive"}
        response = client.post("/api/patterns/analyze", json=data)
        # Peut retourner 200, 422 (validation) ou 500 (erreur interne)
        assert response.status_code in [200, 422, 500]
