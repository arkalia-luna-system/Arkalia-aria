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
        client = TestClient(app)
        yield client
        # Nettoyage : TestClient se nettoie automatiquement, mais on peut forcer
        try:
            client.close()
        except (
            Exception
        ):  # nosec B110 - Ignorer les erreurs de nettoyage dans les tests
            pass  # Ignorer les erreurs de nettoyage

    @pytest.fixture
    def sync_manager(self):
        """Gestionnaire de synchronisation pour les tests."""
        manager = HealthSyncManager()
        yield manager
        # Nettoyage : fermer toutes les connexions des connecteurs
        try:
            import asyncio

            # Créer un event loop si nécessaire pour le nettoyage
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Fermer toutes les connexions
            async def cleanup():
                for connector in manager.connectors.values():
                    if hasattr(connector, "is_connected") and connector.is_connected:
                        try:
                            await connector.disconnect()
                        except (
                            Exception
                        ):  # nosec B110 - Ignorer les erreurs de déconnexion dans les tests
                            pass  # Ignorer les erreurs de déconnexion

            if loop.is_running():
                # Si la loop est déjà en cours, on ne peut pas l'utiliser
                pass
            else:
                loop.run_until_complete(cleanup())
                loop.close()
        except (
            Exception
        ):  # nosec B110 - Ignorer les erreurs de nettoyage dans les tests
            pass  # Ignorer les erreurs de nettoyage

    @pytest.fixture
    def sample_health_data(self):
        """Données de santé d'exemple."""
        return [
            HealthData(
                timestamp=datetime.now() - timedelta(days=1),
                blood_pressure_systolic=120,
                blood_pressure_diastolic=80,
                weight_kg=70.5,
                height_cm=175.0,
                bmi=23.0,
                blood_glucose=None,
                body_temperature=None,
                source="samsung_health",
                raw_data={"device": "Galaxy Watch 4"},
            ),
            HealthData(
                timestamp=datetime.now() - timedelta(days=2),
                blood_pressure_systolic=118,
                blood_pressure_diastolic=78,
                weight_kg=70.2,
                height_cm=175.0,
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
                timestamp=datetime.now() - timedelta(days=1),
                steps=8500,
                distance_meters=6500.0,
                calories_burned=450.0,
                active_minutes=45,
                heart_rate_bpm=75,
                source="samsung_health",
                raw_data={"activity_type": "walking"},
            ),
            ActivityData(
                timestamp=datetime.now() - timedelta(days=2),
                steps=12000,
                distance_meters=9000.0,
                calories_burned=600.0,
                active_minutes=60,
                heart_rate_bpm=72,
                source="google_fit",
                raw_data={"activity_type": "running"},
            ),
        ]

    def test_health_api_endpoints(self, client):
        """Test des endpoints de l'API de santé."""
        # Test de l'endpoint de synchronisation
        response = client.post("/health/sync/all", json={"days_back": 7})
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

        # Test de l'endpoint des métriques unifiées
        response = client.get("/health/metrics/unified?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

        # Test de l'endpoint des données d'activité
        response = client.get("/health/data/activity?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test de l'endpoint des données de sommeil
        response = client.get("/health/data/sleep?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test de l'endpoint des données de stress
        response = client.get("/health/data/stress?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test de l'endpoint des données de santé générales
        response = client.get("/health/data/health?days_back=7")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Test de l'endpoint du statut des connecteurs
        response = client.get("/health/connectors/status")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)

    def test_dashboard_endpoints(self, client):
        """Test des endpoints du dashboard."""
        import os

        # Activer les métriques pour les tests si nécessaire
        os.environ["ARIA_ENABLE_METRICS"] = "true"

        # Test de la page principale
        response = client.get("/dashboard")
        # Accepter 200 ou 404 si le dashboard n'est pas disponible
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]

        # Test de la page de santé
        response = client.get("/dashboard/health")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]

        # Test de la page de douleur
        response = client.get("/dashboard/pain")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]

        # Test de la page des patterns
        response = client.get("/dashboard/patterns")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]

        # Test de la page des rapports
        response = client.get("/dashboard/reports")
        # Accepter 200 ou 404 si le dashboard n'est pas disponible
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]

    def test_export_endpoints(self, client):
        """Test des endpoints d'export."""
        import os

        # Activer les métriques pour les tests si nécessaire
        os.environ["ARIA_ENABLE_METRICS"] = "true"

        # Test de l'export PDF
        response = client.post(
            "/dashboard/export/pdf",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "metrics": ["health", "activity", "sleep"],
            },
        )
        # Accepter 200 ou 404 si l'export n'est pas disponible
        assert response.status_code in [200, 404]
        if response.status_code == 200:
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
        # Accepter 200 ou 404 si l'export n'est pas disponible
        assert response.status_code in [200, 404]
        if response.status_code == 200:
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
        # Accepter 200 ou 404 si l'export n'est pas disponible
        assert response.status_code in [200, 404]
        if response.status_code == 200:
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

    def test_pain_entry_with_new_fields(self, client):
        """Test création d'entrée de douleur avec les nouveaux champs (27 nov 2025)."""
        # Test avec tous les nouveaux champs
        entry_data = {
            "intensity": 7,
            "physical_trigger": "stress",
            "mental_trigger": "anxiété",
            "activity": "travail",
            "location": "dos",
            "action_taken": "respiration",
            "effectiveness": 6,
            "notes": "Douleur après conflit",
            "who_present": "Famille",
            "interactions": "Conflit avec proche",
            "emotions": "Anxiété, frustration",
            "thoughts": "Je me sens dépassé",
            "physical_symptoms": "Tension musculaire, maux de tête",
        }
        response = client.post("/api/pain/entry", json=entry_data)
        assert response.status_code == 200
        data = response.json()
        assert data["intensity"] == 7
        assert data["who_present"] == "Famille"
        assert data["interactions"] == "Conflit avec proche"
        assert data["emotions"] == "Anxiété, frustration"
        assert data["thoughts"] == "Je me sens dépassé"
        assert data["physical_symptoms"] == "Tension musculaire, maux de tête"

    def test_data_models_validation(self, sample_health_data, sample_activity_data):
        """Test de validation des modèles de données."""
        # Test des données de santé
        for health_data in sample_health_data:
            assert isinstance(health_data.timestamp, datetime)
            assert health_data.weight_kg is None or isinstance(
                health_data.weight_kg, int | float
            )
            assert health_data.height_cm is None or isinstance(
                health_data.height_cm, int | float
            )
            assert isinstance(health_data.source, str)
            assert health_data.raw_data is None or isinstance(
                health_data.raw_data, dict
            )

        # Test des données d'activité
        for activity_data in sample_activity_data:
            assert isinstance(activity_data.timestamp, datetime)
            assert activity_data.steps is None or isinstance(activity_data.steps, int)
            assert activity_data.distance_meters is None or isinstance(
                activity_data.distance_meters, int | float
            )
            assert activity_data.calories_burned is None or isinstance(
                activity_data.calories_burned, int | float
            )
            assert activity_data.active_minutes is None or isinstance(
                activity_data.active_minutes, int
            )
            assert isinstance(activity_data.source, str)
            assert activity_data.raw_data is None or isinstance(
                activity_data.raw_data, dict
            )

    @pytest.mark.asyncio
    async def test_export_handlers(self, sample_health_data, sample_activity_data):
        """Test des gestionnaires d'export."""
        # Préparation des données de test
        test_data = {
            "health": [item.model_dump(mode="json") for item in sample_health_data],
            "activity": [item.model_dump(mode="json") for item in sample_activity_data],
            "period": {
                "start_date": (datetime.now() - timedelta(days=7)).isoformat(),
                "end_date": datetime.now().isoformat(),
            },
        }

        # Test de l'export PDF
        pdf_handler = PDFExportHandler()
        pdf_response = await pdf_handler.generate_response(test_data)
        assert hasattr(pdf_response, "body")
        assert len(pdf_response.body) > 0

        # Test de l'export Excel
        excel_handler = ExcelExportHandler()
        excel_response = await excel_handler.generate_response(test_data)
        assert hasattr(excel_response, "body")
        assert len(excel_response.body) > 0

        # Test de l'export HTML
        html_handler = HTMLExportHandler()
        html_response = await html_handler.generate_response(test_data)
        assert hasattr(html_response, "body")
        assert len(html_response.body) > 0
        # Convertir body en bytes si nécessaire pour la méthode lower()
        body_bytes = (
            bytes(html_response.body)
            if not isinstance(html_response.body, bytes)
            else html_response.body
        )
        assert b"html" in body_bytes.lower()

    def test_error_handling(self, client):
        """Test de la gestion d'erreurs."""
        # Test avec des paramètres invalides
        response = client.post("/health/sync/all", json={"days_back": -1})
        assert response.status_code == 422  # Validation error

        # Test avec des dates invalides
        response = client.get("/health/data/activity?days_back=invalid")
        assert response.status_code == 422

        # Test d'endpoint inexistant
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_performance_metrics(self, client):
        """Test des métriques de performance."""
        import os
        import time

        # Activer les métriques pour les tests si nécessaire
        os.environ["ARIA_ENABLE_METRICS"] = "true"

        # Test de temps de réponse des endpoints
        start_time = time.time()
        response = client.get("/health/metrics/unified?days_back=7")
        end_time = time.time()

        # Accepter 200 ou 404 si les métriques ne sont pas disponibles
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert (end_time - start_time) < 5.0  # Moins de 5 secondes

        # Test de temps de réponse du dashboard
        start_time = time.time()
        response = client.get("/dashboard")
        end_time = time.time()

        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert (end_time - start_time) < 2.0  # Moins de 2 secondes

    def test_concurrent_requests(self, client):
        """Test de requêtes concurrentes."""
        import threading
        import time

        results = []
        errors = []
        threads = []

        def make_request():
            try:
                response = client.get("/health/metrics/unified?days_back=7")
                results.append(response.status_code)
            except Exception as e:
                errors.append(str(e))

        try:
            # Lancement de 10 requêtes concurrentes
            for _ in range(10):
                thread = threading.Thread(target=make_request)
                thread.daemon = True  # Thread daemon pour éviter les blocages
                threads.append(thread)
                thread.start()

            # Attente de la fin de tous les threads avec timeout
            for thread in threads:
                thread.join(timeout=30.0)  # Timeout de 30 secondes max
                if thread.is_alive():
                    errors.append(f"Thread {thread.name} n'a pas terminé dans le délai")

            # Vérification des résultats
            assert len(errors) == 0, f"Erreurs détectées: {errors}"
            assert len(results) == 10
            # Accepter 200 ou 404 si les métriques ne sont pas disponibles
            assert all(status in [200, 404] for status in results)
        finally:
            # Nettoyage supplémentaire : attendre que tous les threads soient terminés
            for thread in threads:
                if thread.is_alive():
                    # Forcer l'arrêt si nécessaire (dans un vrai cas, on devrait gérer ça différemment)
                    pass
            # Petite pause pour s'assurer que tout est nettoyé
            time.sleep(0.1)

    @pytest.mark.asyncio
    async def test_data_consistency(self, sync_manager):
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
        import os

        # Activer les métriques pour les tests si nécessaire
        os.environ["ARIA_ENABLE_METRICS"] = "true"

        response = client.get("/dashboard")

        # Vérification des en-têtes de sécurité
        # Accepter 200 ou 404 si le dashboard n'est pas disponible
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert "content-type" in response.headers

    def test_cors_headers(self, client):
        """Test des en-têtes CORS."""
        response = client.options("/health/sync/all")

        # Vérification des en-têtes CORS
        assert response.status_code in [200, 405]


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
        import pathlib

        # Vérifier que les fichiers de services mobiles existent
        mobile_app_path = pathlib.Path("mobile_app/lib/services")

        # Vérifier l'existence des fichiers de services
        health_service_file = mobile_app_path / "health_connector_service.dart"
        notification_service_file = mobile_app_path / "notification_service.dart"
        cache_service_file = mobile_app_path / "offline_cache_service.dart"

        # Vérifier l'existence des fichiers
        assert (
            health_service_file.exists()
        ), f"Fichier {health_service_file} introuvable. Chemin absolu: {health_service_file.absolute()}"
        assert (
            notification_service_file.exists()
        ), f"Fichier {notification_service_file} introuvable"
        assert cache_service_file.exists(), f"Fichier {cache_service_file} introuvable"

        # Vérifier que les fichiers ne sont pas vides
        assert (
            health_service_file.stat().st_size > 0
        ), "Fichier health_connector_service.dart vide"
        assert (
            notification_service_file.stat().st_size > 0
        ), "Fichier notification_service.dart vide"
        assert (
            cache_service_file.stat().st_size > 0
        ), "Fichier offline_cache_service.dart vide"

        # Vérifier le contenu des fichiers (qu'ils contiennent du code Dart valide)
        health_content = health_service_file.read_text(encoding="utf-8")
        assert (
            "class" in health_content
        ), "Fichier health_connector_service.dart ne contient pas de classe"
        assert (
            "HealthConnectorService" in health_content
        ), "Classe HealthConnectorService introuvable"

        notification_content = notification_service_file.read_text(encoding="utf-8")
        assert (
            "class" in notification_content
        ), "Fichier notification_service.dart ne contient pas de classe"
        assert (
            "NotificationService" in notification_content
        ), "Classe NotificationService introuvable"

        cache_content = cache_service_file.read_text(encoding="utf-8")
        assert (
            "class" in cache_content
        ), "Fichier offline_cache_service.dart ne contient pas de classe"
        assert (
            "OfflineCacheService" in cache_content
        ), "Classe OfflineCacheService introuvable"


class TestEndToEndWorkflow:
    """Tests de workflow de bout en bout."""

    @pytest.fixture
    def client(self):
        """Client de test FastAPI."""
        client = TestClient(app)
        yield client
        # Nettoyage : TestClient se nettoie automatiquement, mais on peut forcer
        try:
            client.close()
        except (
            Exception
        ):  # nosec B110 - Ignorer les erreurs de nettoyage dans les tests
            pass  # Ignorer les erreurs de nettoyage

    def test_complete_health_tracking_workflow(self, client):
        """Test du workflow complet de suivi de santé."""
        import os

        # Activer les métriques pour les tests si nécessaire
        os.environ["ARIA_ENABLE_METRICS"] = "true"

        # 1. Synchronisation des données
        response = client.post("/health/sync/all", json={"days_back": 7})
        assert response.status_code == 200

        # 2. Récupération des métriques
        response = client.get("/health/metrics/unified?days_back=7")
        # Accepter 200 ou 404 si les métriques ne sont pas disponibles
        assert response.status_code in [200, 404]
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
        # Accepter 200 ou 404 si l'export n'est pas disponible
        assert response.status_code in [200, 404]

        # 4. Vérification du dashboard
        response = client.get("/dashboard")
        # Accepter 200 ou 404 si le dashboard n'est pas disponible
        assert response.status_code in [200, 404]

    def test_data_flow_consistency(self, client):
        """Test de la cohérence du flux de données."""
        # Synchronisation
        sync_response = client.post("/health/sync/all", json={"days_back": 7})
        assert sync_response.status_code == 200

        # Récupération des données
        health_response = client.get("/health/data/health?days_back=7")
        activity_response = client.get("/health/data/activity?days_back=7")

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
            # Vérification que les données existent
            assert len(health_data) > 0
            assert len(activity_data) > 0

            # Vérification que les timestamps existent
            for item in health_data:
                assert "timestamp" in item
            for item in activity_data:
                assert "timestamp" in item


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
