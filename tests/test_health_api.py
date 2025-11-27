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
        assert "/health/sync/all" in routes
        assert "/health/metrics/unified" in routes
        assert "/health/data/activity" in routes
        assert "/health/data/sleep" in routes
        assert "/health/data/stress" in routes
        assert "/health/data/health" in routes
        assert "/health/connectors/status" in routes


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
        response = client.post("/health/sync/all", json={"days_back": 7})

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "sync_summary" in data
        assert "samsung_health" in data["sync_summary"]["connectors"]
        assert "google_fit" in data["sync_summary"]["connectors"]
        assert "ios_health" in data["sync_summary"]["connectors"]

    @pytest.mark.asyncio
    async def test_sync_specific_connector(self, client):
        """Test synchronisation d'un connecteur spécifique."""
        response = client.post(
            "/health/sync/all", json={"connector": "samsung_health", "days_back": 7}
        )

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "sync_summary" in data
        assert "samsung_health" in data["sync_summary"]["connectors"]

    @pytest.mark.asyncio
    async def test_sync_invalid_connector(self, client):
        """Test synchronisation avec un connecteur invalide."""
        response = client.post(
            "/health/sync/all", json={"connector": "invalid_connector", "days_back": 7}
        )

        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    @pytest.mark.asyncio
    async def test_sync_invalid_days_back(self, client):
        """Test synchronisation avec un nombre de jours invalide."""
        response = client.post("/health/sync/all", json={"days_back": -1})

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


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
        response = client.get("/health/metrics/unified?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert "period" in data
        assert "activity" in data
        assert "sleep" in data
        assert "stress" in data

        assert isinstance(data["activity"]["total_steps"], int)
        assert isinstance(data["activity"]["total_calories"], float)
        assert isinstance(data["activity"]["total_distance"], float)
        assert isinstance(data["sleep"]["avg_duration_minutes"], float)
        assert isinstance(data["sleep"]["avg_quality_score"], float)
        assert isinstance(data["stress"]["avg_stress_level"], float)
        assert isinstance(data["activity"]["avg_heart_rate"], float)

    @pytest.mark.asyncio
    async def test_get_unified_metrics_default_days(self, client):
        """Test récupération des métriques avec jours par défaut."""
        response = client.get("/health/metrics/unified")

        assert response.status_code == 200
        data = response.json()

        assert "period" in data
        assert "activity" in data

    @pytest.mark.asyncio
    async def test_get_unified_metrics_invalid_days(self, client):
        """Test récupération des métriques avec jours invalides."""
        response = client.get("/health/metrics/unified?days_back=-1")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


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
        response = client.get("/health/data/activity?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "timestamp" in item
            assert "steps" in item
            assert "calories_burned" in item
            assert "distance_meters" in item
            assert "active_minutes" in item
            assert "source" in item
            assert "heart_rate_bpm" in item

            assert isinstance(item["steps"], int)
            assert isinstance(item["calories_burned"], float)
            assert isinstance(item["distance_meters"], float)
            assert isinstance(item["active_minutes"], int)
            assert isinstance(item["source"], str)
            assert isinstance(item["heart_rate_bpm"], int)

    @pytest.mark.asyncio
    async def test_get_activity_data_default_days(self, client):
        """Test récupération des données d'activité avec jours par défaut."""
        response = client.get("/health/data/activity")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)

    @pytest.mark.asyncio
    async def test_get_activity_data_invalid_days(self, client):
        """Test récupération des données d'activité avec jours invalides."""
        response = client.get("/health/data/activity?days_back=-1")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


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
        response = client.get("/health/data/sleep?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "sleep_start" in item
            assert "duration_minutes" in item
            assert "quality_score" in item
            assert "deep_sleep_minutes" in item
            assert "light_sleep_minutes" in item
            assert "rem_sleep_minutes" in item
            assert "awakenings_count" in item

            assert isinstance(item["duration_minutes"], int)
            assert isinstance(item["quality_score"], float)
            assert isinstance(item["deep_sleep_minutes"], int)
            assert isinstance(item["light_sleep_minutes"], int)
            assert isinstance(item["rem_sleep_minutes"], int)
            assert isinstance(item["awakenings_count"], int)

            assert 0 <= item["quality_score"] <= 1
            assert item["duration_minutes"] > 0


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
        response = client.get("/health/data/stress?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "timestamp" in item
            assert "stress_level" in item
            assert "heart_rate_variability" in item
            assert "resting_heart_rate" in item

            assert isinstance(item["stress_level"], float)
            assert isinstance(item["heart_rate_variability"], float)
            assert isinstance(item["resting_heart_rate"], int)

            assert 0 <= item["stress_level"] <= 100
            assert item["heart_rate_variability"] > 0


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
        response = client.get("/health/data/health?days_back=7")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) > 0

        for item in data:
            assert "timestamp" in item
            assert "weight_kg" in item

            assert isinstance(item["weight_kg"], float)
            assert item["weight_kg"] > 0

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
        response = client.get("/health/connectors/status")

        assert response.status_code == 200
        data = response.json()

        assert "samsung_health" in data
        assert "google_fit" in data
        assert "ios_health" in data

        assert isinstance(data["samsung_health"]["is_connected"], bool)
        assert isinstance(data["google_fit"]["is_connected"], bool)
        assert isinstance(data["ios_health"]["is_connected"], bool)

        assert data["samsung_health"]["status"] in ["connected", "disconnected"]
        assert data["google_fit"]["status"] in ["connected", "disconnected"]
        assert data["ios_health"]["status"] in ["connected", "disconnected"]

        # Vérifier que les connecteurs ont les champs requis
        for connector_name in ["samsung_health", "google_fit", "ios_health"]:
            connector = data[connector_name]
            assert "connector_name" in connector
            assert "is_connected" in connector
            assert "status" in connector


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
            "/health/sync/all",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_missing_required_fields(self, client):
        """Test requête avec champs requis manquants."""
        response = client.post("/health/sync/all", json={})

        assert response.status_code == 200  # days_back a une valeur par défaut

    @pytest.mark.asyncio
    async def test_invalid_query_parameters(self, client):
        """Test paramètres de requête invalides."""
        response = client.get("/health/metrics/unified?days_back=abc")

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
        response = client.post("/health/sync/all", json={"days_back": 7})
        end_time = time.time()

        assert response.status_code == 200
        duration = end_time - start_time
        assert duration < 10  # Synchronisation doit prendre moins de 10 secondes

    @pytest.mark.asyncio
    async def test_metrics_performance(self, client):
        """Test performance de récupération des métriques."""
        import time

        start_time = time.time()
        response = client.get("/health/metrics/unified?days_back=30")
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
            try:
                response = client.get("/health/metrics/unified?days_back=7")
                return response.status_code == 200
            except Exception as e:
                # Logger l'erreur mais ne pas faire échouer le test immédiatement
                print(f"Erreur dans make_request: {e}")
                return False

        try:
            start_time = time.time()
            # Limiter le nombre de requêtes concurrentes pour éviter la surcharge
            results = await asyncio.gather(
                *[make_request() for _ in range(10)], return_exceptions=True
            )
            end_time = time.time()

            # Filtrer les exceptions et vérifier les résultats
            valid_results = [r for r in results if isinstance(r, bool)]
            exceptions = [r for r in results if isinstance(r, Exception)]

            if exceptions:
                print(f"Exceptions détectées: {exceptions}")

            assert len(valid_results) == 10
            assert all(valid_results)
            duration = end_time - start_time
            assert (
                duration < 15
            )  # 10 requêtes concurrentes doivent prendre moins de 15 secondes
        finally:
            # Nettoyage : s'assurer que toutes les tâches sont terminées
            await asyncio.sleep(0.1)  # Petite pause pour le nettoyage


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
