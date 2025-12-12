"""
Tests pour l'API Research Tools
"""

from fastapi.testclient import TestClient

from main import app
from research_tools.api import router

# Intégrer le router dans l'app principale pour les tests
app.include_router(router, prefix="/research", tags=["research"])

client = TestClient(app)


class TestResearchToolsAPI:
    """Tests pour l'API Research Tools"""

    def test_research_tools_status(self):
        """Test GET /research/status"""
        response = client.get("/research/status")
        assert response.status_code == 200
        data = response.json()
        assert data["module"] == "research_tools"
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "features" in data
        assert isinstance(data["features"], list)
        assert "data_laboratory" in data["features"]
        assert "controlled_experiments" in data["features"]

    def test_list_experiments(self):
        """Test GET /research/experiments"""
        response = client.get("/research/experiments")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "experiments" in data
        assert "active_count" in data
        assert isinstance(data["experiments"], list)
        assert data["active_count"] == 0

    def test_create_experiment(self):
        """Test POST /research/experiment/create"""
        experiment_data = {
            "name": "Test Experiment",
            "description": "Test description",
            "parameters": {"param1": "value1"},
        }
        response = client.post("/research/experiment/create", json=experiment_data)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "experiment_id" in data
        assert "status" in data
        assert data["status"] == "pending"

    def test_create_experiment_empty_data(self):
        """Test POST /research/experiment/create avec données vides"""
        response = client.post("/research/experiment/create", json={})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"

    def test_create_experiment_complex_data(self):
        """Test POST /research/experiment/create avec données complexes"""
        complex_data = {
            "name": "Complex Experiment",
            "description": "A complex experiment",
            "parameters": {
                "param1": "value1",
                "param2": 123,
                "param3": [1, 2, 3],
                "param4": {"nested": "data"},
            },
            "metadata": {"author": "test", "version": "1.0"},
        }
        response = client.post("/research/experiment/create", json=complex_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"
