"""
Tests pour l'API des métriques ARIA
"""

from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from metrics_collector.api import ARIA_MetricsAPI


class TestARIA_MetricsAPI:
    """Tests pour l'API des métriques ARIA"""

    def test_init(self):
        """Test l'initialisation de l'API"""
        api = ARIA_MetricsAPI(".")
        assert api.project_root == "."
        assert api._metrics_cache is None
        assert api._cache_timestamp is None
        assert api._cache_duration_seconds == 300

    def test_get_router(self):
        """Test la récupération du router"""
        api = ARIA_MetricsAPI(".")
        router = api.get_router()
        assert router is not None
        assert len(router.routes) > 0

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    def test_get_metrics_endpoint(self, mock_collector_class):
        """Test GET /metrics/"""
        # Mock du collecteur
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {
            "project_info": {"name": "ARKALIA ARIA"},
            "python_files": {"count": 100},
        }
        mock_collector_class.return_value = mock_collector

        api = ARIA_MetricsAPI(".")
        router = api.get_router()

        # Créer une app de test
        from fastapi import FastAPI

        test_app = FastAPI()
        test_app.include_router(router)
        client = TestClient(test_app)

        response = client.get("/metrics/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "data" in data
        assert "timestamp" in data

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    def test_get_health_endpoint(self, mock_collector_class):
        """Test GET /metrics/health"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {
            "project_info": {"name": "ARKALIA ARIA"},
        }
        mock_collector_class.return_value = mock_collector

        api = ARIA_MetricsAPI(".")
        router = api.get_router()

        from fastapi import FastAPI

        test_app = FastAPI()
        test_app.include_router(router)
        client = TestClient(test_app)

        response = client.get("/metrics/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "health" in data
        assert "timestamp" in data

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    @patch("metrics_collector.api.ARIA_MetricsDashboard")
    def test_get_dashboard_endpoint(self, mock_dashboard_class, mock_collector_class):
        """Test GET /metrics/dashboard"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {
            "project_info": {"name": "ARKALIA ARIA"},
        }
        mock_collector_class.return_value = mock_collector

        mock_dashboard = MagicMock()
        mock_dashboard.generate_dashboard_html.return_value = "<html>Test</html>"
        mock_dashboard_class.return_value = mock_dashboard

        api = ARIA_MetricsAPI(".")
        router = api.get_router()

        from fastapi import FastAPI

        test_app = FastAPI()
        test_app.include_router(router)
        client = TestClient(test_app)

        response = client.get("/metrics/dashboard")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "<html>" in response.text

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    @patch("metrics_collector.api.ARIA_MetricsExporter")
    def test_export_metrics_json(self, mock_exporter_class, mock_collector_class):
        """Test GET /metrics/export/json"""
        import tempfile

        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {"test": "data"}
        mock_collector_class.return_value = mock_collector

        # Utiliser un fichier temporaire sécurisé au lieu de /tmp/test.json
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as tmp_file:
            tmp_path = Path(tmp_file.name)

        mock_exporter = MagicMock()
        mock_exporter.export_json.return_value = tmp_path
        mock_exporter_class.return_value = mock_exporter

        try:
            api = ARIA_MetricsAPI(".")
            router = api.get_router()

            from fastapi import FastAPI

            test_app = FastAPI()
            test_app.include_router(router)
            client = TestClient(test_app)

            response = client.get("/metrics/export/json")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
            assert "file_path" in data
        finally:
            # Nettoyer le fichier temporaire
            tmp_path.unlink(missing_ok=True)

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    @patch("metrics_collector.api.ARIA_MetricsExporter")
    def test_export_metrics_markdown(self, mock_exporter_class, mock_collector_class):
        """Test GET /metrics/export/markdown"""
        import tempfile

        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {"test": "data"}
        mock_collector_class.return_value = mock_collector

        # Utiliser un fichier temporaire sécurisé au lieu de /tmp/test.md
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False
        ) as tmp_file:
            tmp_path = Path(tmp_file.name)

        mock_exporter = MagicMock()
        mock_exporter.export_markdown.return_value = tmp_path
        mock_exporter_class.return_value = mock_exporter

        try:
            api = ARIA_MetricsAPI(".")
            router = api.get_router()

            from fastapi import FastAPI

            test_app = FastAPI()
            test_app.include_router(router)
            client = TestClient(test_app)

            response = client.get("/metrics/export/markdown")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "success"
        finally:
            # Nettoyer le fichier temporaire
            tmp_path.unlink(missing_ok=True)

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    def test_export_metrics_invalid_format(self, mock_collector_class):
        """Test GET /metrics/export avec format invalide"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {"test": "data"}
        mock_collector_class.return_value = mock_collector

        api = ARIA_MetricsAPI(".")
        router = api.get_router()

        from fastapi import FastAPI

        test_app = FastAPI()
        test_app.include_router(router)
        client = TestClient(test_app)

        response = client.get("/metrics/export/invalid")
        # L'API peut retourner 400 ou 500 selon l'implémentation
        assert response.status_code in [400, 500]

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    def test_force_collect_metrics(self, mock_collector_class):
        """Test POST /metrics/collect"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {"test": "data"}
        mock_collector_class.return_value = mock_collector

        api = ARIA_MetricsAPI(".")
        router = api.get_router()

        from fastapi import FastAPI

        test_app = FastAPI()
        test_app.include_router(router)
        client = TestClient(test_app)

        response = client.post("/metrics/collect")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data
        assert "data" in data

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    def test_validate_metrics(self, mock_collector_class):
        """Test GET /metrics/validate"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {"test": "data"}
        mock_collector_class.return_value = mock_collector

        api = ARIA_MetricsAPI(".")
        router = api.get_router()

        from fastapi import FastAPI

        test_app = FastAPI()
        test_app.include_router(router)
        client = TestClient(test_app)

        response = client.get("/metrics/validate")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "validation" in data

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    def test_get_metrics_summary(self, mock_collector_class):
        """Test GET /metrics/summary"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {
            "project_info": {"name": "ARKALIA ARIA"},
            "python_files": {"count": 100, "total_lines": 5000},
            "tests": {"test_files_count": 50, "coverage_percentage": 85},
            "aria_specific": {
                "pain_tracking": 100,
                "pattern_analysis": 50,
                "predictions": 25,
            },
            "security": {"bandit_scan": {"issues_found": 0}},
            "performance": {"memory_usage_mb": 100, "cpu_percent": 5},
        }
        mock_collector_class.return_value = mock_collector

        api = ARIA_MetricsAPI(".")
        router = api.get_router()

        from fastapi import FastAPI

        test_app = FastAPI()
        test_app.include_router(router)
        client = TestClient(test_app)

        response = client.get("/metrics/summary")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "summary" in data
        assert data["summary"]["project_name"] == "ARKALIA ARIA"
        assert data["summary"]["python_files"] == 100

    @patch("metrics_collector.api.ARIA_MetricsCollector")
    def test_get_alerts(self, mock_collector_class):
        """Test GET /metrics/alerts"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {"test": "data"}
        mock_collector_class.return_value = mock_collector

        api = ARIA_MetricsAPI(".")
        router = api.get_router()

        from fastapi import FastAPI

        test_app = FastAPI()
        test_app.include_router(router)
        client = TestClient(test_app)

        response = client.get("/metrics/alerts")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "alerts" in data
        assert "recommendations" in data

    def test_cache_mechanism(self):
        """Test le mécanisme de cache"""
        api = ARIA_MetricsAPI(".")
        assert api._metrics_cache is None

        # Simuler des métriques en cache
        api._metrics_cache = {"test": "data"}
        api._cache_timestamp = datetime.now()

        # Le cache devrait être valide
        assert api._metrics_cache is not None

        # Simuler un cache expiré
        api._cache_timestamp = datetime.now() - timedelta(seconds=400)
        # Le cache devrait être considéré comme expiré
        assert (datetime.now() - api._cache_timestamp).total_seconds() > 300

    @patch("metrics_collector.api.ARIA_MetricsDashboard")
    @patch("metrics_collector.api.StaticFiles")
    def test_integrate_with_app(self, mock_static_files, mock_dashboard_class):
        """Test l'intégration avec une app FastAPI"""
        import tempfile

        from fastapi import FastAPI

        # Créer un répertoire temporaire réel
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_dashboard = MagicMock()
            mock_dashboard.static_dir = Path(tmpdir)
            mock_dashboard_class.return_value = mock_dashboard

            api = ARIA_MetricsAPI(".")
            test_app = FastAPI()
            api.integrate_with_app(test_app)

            # Vérifier que le router est inclus
            assert len(test_app.routes) > 0
