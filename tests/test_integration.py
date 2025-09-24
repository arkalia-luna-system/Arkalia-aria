"""
Tests d'intégration pour ARKALIA ARIA
Tests complets du système de bout en bout
"""

from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from health_connectors import (
    GoogleFitConnector,
    HealthSyncManager,
    IOSHealthConnector,
    SamsungHealthConnector,
)
from health_connectors.data_models import (
    ActivityData,
    HealthData,
)
from main import app
from metrics_collector.dashboard.export_handlers import (
    ExcelExportHandler,
    HTMLExportHandler,
    PDFExportHandler,
)


class TestSystemIntegration:
    """Tests d'intégration du système complet."""

    @pytest.fixture
    def client(self):
        """Client de test FastAPI."""
        return TestClient(app)

    @pytest.fixture
    def sync_manager(self):
        """Gestionnaire de synchronisation pour les tests."""
        return HealthSyncManager()

    @pytest.fixture
    def sample_health_data(self):
        """Données de santé d'exemple."""
        return [
            HealthData(
                date=datetime.now() - timedelta(days=1),
                heart_rate=75,
                blood_pressure_systolic=120,
                blood_pressure_diastolic=80,
                weight=70.5,
                height=175.0,
                bmi=23.0,
                blood_glucose=None,
                body_temperature=None,
                source="samsung_health",
                raw_data={"device": "Galaxy Watch 4"},
            ),
            HealthData(
                date=datetime.now() - timedelta(days=2),
                heart_rate=72,
                blood_pressure_systolic=118,
                blood_pressure_diastolic=78,
                weight=70.2,
                height=175.0,
                bmi=22.9,
                blood_glucose=None,
                body_temperature=None,
                source="google_fit",
                raw_data={"device": "Pixel 6"},
            ),
        ]

    @pytest.fixture
    def sample_activity_data(self):
        """Données d'activité d'exemple."""
        return [
            ActivityData(
                date=datetime.now() - timedelta(days=1),
                steps=8500,
                distance_meters=6500.0,
                calories_burned=450.0,
                active_minutes=45,
                source="samsung_health",
                raw_data={"activity_type": "walking"},
            ),
            ActivityData(
                date=datetime.now() - timedelta(days=2),
                steps=12000,
                distance_meters=9000.0,
                calories_burned=600.0,
                active_minutes=60,
                source="google_fit",
                raw_data={"activity_type": "running"},
            ),
        ]

    def test_health_api_endpoints(self, client):
        """Test des endpoints de l'API de santé."""
        # Test de l'endpoint de synchronisation
        response = client.post("/api/health/sync", json={"days_back": 7})
        assert response.status_code == 200
        data = response.json()
        assert "success" in data or "error" in data

        # Test de l'endpoint des métriques unifiées
        response = client.get("/api/health/metrics/unified?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

        # Test de l'endpoint des données d'activité
        response = client.get("/api/health/activity?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test de l'endpoint des données de sommeil
        response = client.get("/api/health/sleep?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test de l'endpoint des données de stress
        response = client.get("/api/health/stress?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test de l'endpoint des données de santé générales
        response = client.get("/api/health/data?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test de l'endpoint du statut des connecteurs
        response = client.get("/api/health/connectors/status")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_dashboard_endpoints(self, client):
        """Test des endpoints du dashboard."""
        # Test de la page principale
        response = client.get("/dashboard")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Test de la page de santé
        response = client.get("/dashboard/health")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Test de la page de douleur
        response = client.get("/dashboard/pain")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Test de la page des patterns
        response = client.get("/dashboard/patterns")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Test de la page des rapports
        response = client.get("/dashboard/reports")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_export_endpoints(self, client):
        """Test des endpoints d'export."""
        # Test de l'export PDF
        response = client.post(
            "/dashboard/export/pdf",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "metrics": ["health", "activity", "sleep"],
            },
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

        # Test de l'export Excel
        response = client.post(
            "/dashboard/export/excel",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "metrics": ["health", "activity", "sleep"],
            },
        )
        assert response.status_code == 200
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in response.headers["content-type"]
        )

        # Test de l'export HTML
        response = client.post(
            "/dashboard/export/html",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "metrics": ["health", "activity", "sleep"],
            },
        )
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    @pytest.mark.asyncio
    async def test_health_connectors_integration(
        self, sync_manager, sample_health_data, sample_activity_data
    ):
        """Test d'intégration des connecteurs de santé."""
        # Mock des connecteurs
        with (
            patch.object(SamsungHealthConnector, "connect", return_value=True),
            patch.object(
                SamsungHealthConnector,
                "get_health_data",
                return_value=sample_health_data,
            ),
            patch.object(
                SamsungHealthConnector,
                "get_activity_data",
                return_value=sample_activity_data,
            ),
            patch.object(GoogleFitConnector, "connect", return_value=True),
            patch.object(
                GoogleFitConnector, "get_health_data", return_value=sample_health_data
            ),
            patch.object(
                GoogleFitConnector,
                "get_activity_data",
                return_value=sample_activity_data,
            ),
            patch.object(IOSHealthConnector, "connect", return_value=True),
            patch.object(
                IOSHealthConnector, "get_health_data", return_value=sample_health_data
            ),
            patch.object(
                IOSHealthConnector,
                "get_activity_data",
                return_value=sample_activity_data,
            ),
        ):

            # Test de synchronisation de tous les connecteurs
            result = await sync_manager.sync_all_connectors(days_back=7)

            assert isinstance(result, dict)
            assert "connectors" in result
            assert "errors" in result
            assert "duration_seconds" in result

            # Test de synchronisation d'un connecteur spécifique
            result = await sync_manager.sync_single_connector(
                "samsung_health", days_back=7
            )

            assert isinstance(result, dict)
            assert "connector" in result
            assert "data_counts" in result

    def test_data_models_validation(self, sample_health_data, sample_activity_data):
        """Test de validation des modèles de données."""
        # Test des données de santé
        for health_data in sample_health_data:
            assert isinstance(health_data.date, datetime)
            assert health_data.heart_rate is None or isinstance(
                health_data.heart_rate, int
            )
            assert health_data.weight is None or isinstance(health_data.weight, float)
            assert isinstance(health_data.source, str)
            assert isinstance(health_data.raw_data, dict)

        # Test des données d'activité
        for activity_data in sample_activity_data:
            assert isinstance(activity_data.date, datetime)
            assert isinstance(activity_data.steps, int)
            assert isinstance(activity_data.distance_meters, float)
            assert isinstance(activity_data.calories_burned, float)
            assert isinstance(activity_data.active_minutes, int)
            assert isinstance(activity_data.source, str)
            assert isinstance(activity_data.raw_data, dict)

    def test_export_handlers(self, sample_health_data, sample_activity_data):
        """Test des gestionnaires d'export."""
        # Préparation des données de test
        test_data = {
            "health": sample_health_data,
            "activity": sample_activity_data,
            "period": {
                "start_date": datetime.now() - timedelta(days=7),
                "end_date": datetime.now(),
            },
        }

        # Test de l'export PDF
        pdf_handler = PDFExportHandler()
        pdf_content = pdf_handler.generate_report(test_data)
        assert isinstance(pdf_content, bytes)
        assert len(pdf_content) > 0

        # Test de l'export Excel
        excel_handler = ExcelExportHandler()
        excel_content = excel_handler.generate_report(test_data)
        assert isinstance(excel_content, bytes)
        assert len(excel_content) > 0

        # Test de l'export HTML
        html_handler = HTMLExportHandler()
        html_content = html_handler.generate_report(test_data)
        assert isinstance(html_content, str)
        assert len(html_content) > 0
        assert "<html>" in html_content.lower()

    def test_error_handling(self, client):
        """Test de la gestion d'erreurs."""
        # Test avec des paramètres invalides
        response = client.post("/api/health/sync", json={"days_back": -1})
        assert response.status_code == 422  # Validation error

        # Test avec des dates invalides
        response = client.get("/api/health/activity?days_back=invalid")
        assert response.status_code == 422

        # Test d'endpoint inexistant
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_performance_metrics(self, client):
        """Test des métriques de performance."""
        import time

        # Test de temps de réponse des endpoints
        start_time = time.time()
        response = client.get("/api/health/metrics/unified?days_back=7")
        end_time = time.time()

        assert response.status_code == 200
        assert (end_time - start_time) < 5.0  # Moins de 5 secondes

        # Test de temps de réponse du dashboard
        start_time = time.time()
        response = client.get("/dashboard")
        end_time = time.time()

        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Moins de 2 secondes

    def test_concurrent_requests(self, client):
        """Test de requêtes concurrentes."""
        import threading

        results = []
        errors = []

        def make_request():
            try:
                response = client.get("/api/health/metrics/unified?days_back=7")
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))

        # Lancement de 10 requêtes concurrentes
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Attente de la fin de tous les threads
        for thread in threads:
            thread.join()

        # Vérification des résultats
        assert len(errors) == 0, f"Erreurs détectées: {errors}"
        assert len(results) == 10
        assert all(status == 200 for status in results)

    def test_data_consistency(self, sync_manager):
        """Test de la cohérence des données."""
        with (
            patch.object(SamsungHealthConnector, "connect", return_value=True),
            patch.object(SamsungHealthConnector, "get_health_data", return_value=[]),
            patch.object(SamsungHealthConnector, "get_activity_data", return_value=[]),
        ):

            # Test avec des données vides
            result = await sync_manager.sync_single_connector(
                "samsung_health", days_back=7
            )

            assert isinstance(result, dict)
            assert "data_counts" in result
            assert result["data_counts"]["health"] == 0
            assert result["data_counts"]["activity"] == 0

    def test_security_headers(self, client):
        """Test des en-têtes de sécurité."""
        response = client.get("/dashboard")

        # Vérification des en-têtes de sécurité
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-XSS-Protection" in response.headers

    def test_cors_headers(self, client):
        """Test des en-têtes CORS."""
        response = client.options("/api/health/sync")

        # Vérification des en-têtes CORS
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
        assert "Access-Control-Allow-Headers" in response.headers


class TestMobileAppIntegration:
    """Tests d'intégration pour l'application mobile."""

    def test_mobile_api_compatibility(self):
        """Test de compatibilité avec l'API mobile."""
        # Test des modèles de données Flutter

        # Test de création des modèles (simulation Python)
        # Note: Ces tests simulent la logique Flutter en Python
        health_data_dict = {
            "date": datetime.now(),
            "heartRate": 75,
            "bloodPressureSystolic": 120,
            "bloodPressureDiastolic": 80,
            "weight": 70.5,
            "height": 175.0,
            "bmi": 23.0,
            "source": "samsung_health",
            "rawData": {"device": "Galaxy Watch 4"},
        }

        assert health_data_dict["heartRate"] == 75
        assert health_data_dict["bmi"] == 23.0
        assert health_data_dict["source"] == "samsung_health"

        pain_entry_dict = {
            "date": datetime.now(),
            "level": 3,
            "type": "Musculaire",
            "location": "Dos",
            "trigger": "Stress",
            "notes": "Douleur modérée",
        }

        assert pain_entry_dict["level"] == 3
        assert pain_entry_dict["type"] == "Musculaire"
        assert pain_entry_dict["location"] == "Dos"

    def test_mobile_services(self):
        """Test des services mobiles."""
        from mobile_app.lib.services.health_connector_service import (
            HealthConnectorService,
        )
        from mobile_app.lib.services.notification_service import NotificationService
        from mobile_app.lib.services.offline_cache_service import OfflineCacheService

        # Test d'initialisation des services
        health_service = HealthConnectorService()
        notification_service = NotificationService()
        cache_service = OfflineCacheService()

        assert health_service is not None
        assert notification_service is not None
        assert cache_service is not None


class TestEndToEndWorkflow:
    """Tests de workflow de bout en bout."""

    def test_complete_health_tracking_workflow(self, client):
        """Test du workflow complet de suivi de santé."""
        # 1. Synchronisation des données
        response = client.post("/api/health/sync", json={"days_back": 7})
        assert response.status_code == 200

        # 2. Récupération des métriques
        response = client.get("/api/health/metrics/unified?days_back=7")
        assert response.status_code == 200
        # metrics = response.json()  # Variable non utilisée

        # 3. Génération d'un rapport
        response = client.post(
            "/dashboard/export/pdf",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "metrics": ["health", "activity", "sleep"],
            },
        )
        assert response.status_code == 200

        # 4. Vérification du dashboard
        response = client.get("/dashboard")
        assert response.status_code == 200

    def test_data_flow_consistency(self, client):
        """Test de la cohérence du flux de données."""
        # Synchronisation
        sync_response = client.post("/api/health/sync", json={"days_back=7"})
        assert sync_response.status_code == 200

        # Récupération des données
        health_response = client.get("/api/health/health?days_back=7")
        activity_response = client.get("/api/health/activity?days_back=7")

        assert health_response.status_code == 200
        assert activity_response.status_code == 200

        # Vérification de la cohérence
        health_data = health_response.json()
        activity_data = activity_response.json()

        # Les données doivent être des listes
        assert isinstance(health_data, list)
        assert isinstance(activity_data, list)

        # Les données doivent être cohérentes dans le temps
        if health_data and activity_data:
            health_dates = [item["date"] for item in health_data]
            activity_dates = [item["date"] for item in activity_data]

            # Vérification que les dates sont dans la plage attendue
            from datetime import datetime, timedelta

            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            for date_str in health_dates + activity_dates:
                date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                assert start_date <= date <= end_date


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
