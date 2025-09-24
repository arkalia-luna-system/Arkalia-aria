"""
Tests unitaires pour l'API des connecteurs santé ARKALIA ARIA
===========================================================

Tests complets pour tous les endpoints de l'API santé.
"""

import pytest
from fastapi.testclient import TestClient

from health_connectors.api import HealthConnectorsAPI


class TestHealthConnectorsAPI:
    """Tests de l'API des connecteurs santé."""

    @pytest.fixture
    def api(self):
        """Fixture pour l'API."""
        return HealthConnectorsAPI()

    @pytest.fixture
    def client(self, api):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        app = FastAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    def test_api_initialization(self, api):
        """Test initialisation de l'API."""
        assert api.sync_manager is not None
        assert api.router is not None

    def test_integrate_with_app(self, api):
        """Test intégration avec l'application FastAPI."""
        from fastapi import FastAPI

        app = FastAPI()

        api.integrate_with_app(app)

        # Vérifier que les routes sont ajoutées
        routes = [route.path for route in app.routes]
        assert "/api/health/sync" in routes
        assert "/api/health/metrics/unified" in routes
        assert "/api/health/activity" in routes
        assert "/api/health/sleep" in routes
        assert "/api/health/stress" in routes
        assert "/api/health/data" in routes
        assert "/api/health/connectors/status" in routes


class TestHealthSyncEndpoint:
    """Tests de l'endpoint de synchronisation."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_sync_all_connectors(self, client):
        """Test synchronisation de tous les connecteurs."""
        response = client.post("/api/health/sync", json={"days_back": 7})

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "sync_results" in data
        assert "total_data_synced" in data
        assert "errors" in data

        sync_results = data["sync_results"]
        assert "samsung_health" in sync_results
        assert "google_fit" in sync_results
        assert "ios_health" in sync_results

    @pytest.mark.asyncio
    async def test_sync_specific_connector(self, client):
        """Test synchronisation d'un connecteur spécifique."""
        response = client.post(
            "/api/health/sync", json={"connector": "samsung_health", "days_back": 7}
        )

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "sync_results" in data
        assert "samsung_health" in data["sync_results"]

    @pytest.mark.asyncio
    async def test_sync_invalid_connector(self, client):
        """Test synchronisation avec un connecteur invalide."""
        response = client.post(
            "/api/health/sync", json={"connector": "invalid_connector", "days_back": 7}
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    @pytest.mark.asyncio
    async def test_sync_invalid_days_back(self, client):
        """Test synchronisation avec un nombre de jours invalide."""
        response = client.post("/api/health/sync", json={"days_back": -1})

        assert response.status_code == 400
        data = response.json()
        assert "error" in data


class TestHealthMetricsEndpoints:
    """Tests des endpoints de métriques santé."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_get_unified_metrics(self, client):
        """Test récupération des métriques unifiées."""
        response = client.get("/api/health/metrics/unified?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert "timestamp" in data
        assert "total_steps" in data
        assert "total_calories" in data
        assert "distance" in data
        assert "sleep_duration" in data
        assert "sleep_quality" in data
        assert "stress_level" in data
        assert "heart_rate" in data

        assert isinstance(data["total_steps"], int)
        assert isinstance(data["total_calories"], float)
        assert isinstance(data["distance"], float)
        assert isinstance(data["sleep_duration"], float)
        assert isinstance(data["sleep_quality"], float)
        assert isinstance(data["stress_level"], float)
        assert isinstance(data["heart_rate"], float)

    @pytest.mark.asyncio
    async def test_get_unified_metrics_default_days(self, client):
        """Test récupération des métriques avec jours par défaut."""
        response = client.get("/api/health/metrics/unified")

        assert response.status_code == 200
        data = response.json()

        assert "timestamp" in data
        assert "total_steps" in data

    @pytest.mark.asyncio
    async def test_get_unified_metrics_invalid_days(self, client):
        """Test récupération des métriques avec jours invalides."""
        response = client.get("/api/health/metrics/unified?days_back=-1")

        assert response.status_code == 400
        data = response.json()
        assert "error" in data


class TestActivityDataEndpoint:
    """Tests de l'endpoint des données d'activité."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_get_activity_data(self, client):
        """Test récupération des données d'activité."""
        response = client.get("/api/health/activity?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "timestamp" in item
            assert "steps" in item
            assert "calories" in item
            assert "distance" in item
            assert "active_minutes" in item
            assert "activity_type" in item
            assert "intensity" in item

            assert isinstance(item["steps"], int)
            assert isinstance(item["calories"], float)
            assert isinstance(item["distance"], float)
            assert isinstance(item["active_minutes"], int)
            assert isinstance(item["activity_type"], str)
            assert isinstance(item["intensity"], str)

    @pytest.mark.asyncio
    async def test_get_activity_data_default_days(self, client):
        """Test récupération des données d'activité avec jours par défaut."""
        response = client.get("/api/health/activity")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_activity_data_invalid_days(self, client):
        """Test récupération des données d'activité avec jours invalides."""
        response = client.get("/api/health/activity?days_back=-1")

        assert response.status_code == 400
        data = response.json()
        assert "error" in data


class TestSleepDataEndpoint:
    """Tests de l'endpoint des données de sommeil."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_get_sleep_data(self, client):
        """Test récupération des données de sommeil."""
        response = client.get("/api/health/sleep?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "timestamp" in item
            assert "duration" in item
            assert "quality" in item
            assert "deep_sleep" in item
            assert "light_sleep" in item
            assert "rem_sleep" in item
            assert "awakenings" in item

            assert isinstance(item["duration"], float)
            assert isinstance(item["quality"], float)
            assert isinstance(item["deep_sleep"], float)
            assert isinstance(item["light_sleep"], float)
            assert isinstance(item["rem_sleep"], float)
            assert isinstance(item["awakenings"], int)

            assert 0 <= item["quality"] <= 10
            assert item["duration"] > 0


class TestStressDataEndpoint:
    """Tests de l'endpoint des données de stress."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_get_stress_data(self, client):
        """Test récupération des données de stress."""
        response = client.get("/api/health/stress?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "timestamp" in item
            assert "level" in item
            assert "heart_rate" in item
            assert "stress_events" in item

            assert isinstance(item["level"], float)
            assert isinstance(item["heart_rate"], float)
            assert isinstance(item["stress_events"], list)

            assert 0 <= item["level"] <= 10
            assert item["heart_rate"] > 0


class TestHealthDataEndpoint:
    """Tests de l'endpoint des données de santé."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_get_health_data(self, client):
        """Test récupération des données de santé."""
        response = client.get("/api/health/data?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "timestamp" in item
            assert "heart_rate" in item

            assert isinstance(item["heart_rate"], float)
            assert item["heart_rate"] > 0

            # Vérifier les champs optionnels
            if "blood_pressure_systolic" in item:
                assert isinstance(item["blood_pressure_systolic"], int)
            if "blood_pressure_diastolic" in item:
                assert isinstance(item["blood_pressure_diastolic"], int)
            if "weight" in item:
                assert isinstance(item["weight"], float)
            if "bmi" in item:
                assert isinstance(item["bmi"], float)


class TestConnectorsStatusEndpoint:
    """Tests de l'endpoint de statut des connecteurs."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_get_connectors_status(self, client):
        """Test récupération du statut des connecteurs."""
        response = client.get("/api/health/connectors/status")

        assert response.status_code == 200
        data = response.json()

        assert "timestamp" in data
        assert "connectors" in data
        assert "total_connectors" in data
        assert "connected_connectors" in data
        assert "total_data_synced" in data
        assert "global_errors" in data
        assert "overall_status" in data

        assert isinstance(data["total_connectors"], int)
        assert isinstance(data["connected_connectors"], int)
        assert isinstance(data["total_data_synced"], int)
        assert isinstance(data["global_errors"], list)
        assert isinstance(data["overall_status"], str)

        assert data["total_connectors"] == 3
        assert data["connected_connectors"] == 3
        assert data["total_data_synced"] > 0

        connectors = data["connectors"]
        assert "samsung_health" in connectors
        assert "google_fit" in connectors
        assert "ios_health" in connectors

        for _connector_name, connector_data in connectors.items():
            assert "status" in connector_data
            assert "last_sync" in connector_data
            assert "data_count" in connector_data

            assert isinstance(connector_data["status"], str)
            assert isinstance(connector_data["data_count"], int)


class TestErrorHandling:
    """Tests de gestion des erreurs."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_invalid_json_request(self, client):
        """Test requête avec JSON invalide."""
        response = client.post(
            "/api/health/sync",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_missing_required_fields(self, client):
        """Test requête avec champs requis manquants."""
        response = client.post("/api/health/sync", json={})

        assert response.status_code == 200  # days_back a une valeur par défaut

    @pytest.mark.asyncio
    async def test_invalid_query_parameters(self, client):
        """Test paramètres de requête invalides."""
        response = client.get("/api/health/metrics/unified?days_back=abc")

        assert response.status_code == 422


class TestPerformance:
    """Tests de performance."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        from health_connectors.api import HealthConnectorsAPI

        app = FastAPI()
        api = HealthConnectorsAPI()
        api.integrate_with_app(app)
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_sync_performance(self, client):
        """Test performance de synchronisation."""
        import time

        start_time = time.time()
        response = client.post("/api/health/sync", json={"days_back": 7})
        end_time = time.time()

        assert response.status_code == 200
        duration = end_time - start_time
        assert duration < 10  # Synchronisation doit prendre moins de 10 secondes

    @pytest.mark.asyncio
    async def test_metrics_performance(self, client):
        """Test performance de récupération des métriques."""
        import time

        start_time = time.time()
        response = client.get("/api/health/metrics/unified?days_back=30")
        end_time = time.time()

        assert response.status_code == 200
        duration = end_time - start_time
        assert (
            duration < 5
        )  # Récupération des métriques doit prendre moins de 5 secondes

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client):
        """Test requêtes concurrentes."""
        import asyncio
        import time

        async def make_request():
            response = client.get("/api/health/metrics/unified?days_back=7")
            return response.status_code == 200

        start_time = time.time()
        results = await asyncio.gather(*[make_request() for _ in range(10)])
        end_time = time.time()

        assert all(results)
        duration = end_time - start_time
        assert (
            duration < 15
        )  # 10 requêtes concurrentes doivent prendre moins de 15 secondes


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
