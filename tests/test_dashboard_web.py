"""
Tests unitaires pour le dashboard web ARKALIA ARIA
==================================================

Tests complets pour toutes les fonctionnalités du dashboard web.
"""

from unittest.mock import AsyncMock, Mock

import pytest
from fastapi.testclient import TestClient

from metrics_collector.dashboard.aria_metrics_dashboard import ARIA_MetricsDashboard
from metrics_collector.dashboard.export_handlers import (
    ExcelExportHandler,
    HTMLExportHandler,
    PDFExportHandler,
    ReportPreviewHandler,
)


class TestARIA_MetricsDashboard:
    """Tests du dashboard ARIA."""

    @pytest.fixture
    def dashboard(self):
        """Fixture pour le dashboard."""
        from fastapi import FastAPI

        app = FastAPI()
        dashboard = ARIA_MetricsDashboard(app)
        return dashboard

    @pytest.fixture
    def client(self, dashboard):
        """Fixture pour le client de test."""
        return TestClient(dashboard.app)

    def test_dashboard_initialization(self, dashboard):
        """Test initialisation du dashboard."""
        assert dashboard.app is not None
        assert dashboard.templates is not None

    def test_dashboard_routes(self, dashboard):
        """Test que les routes du dashboard sont ajoutées."""
        routes = [route.path for route in dashboard.app.routes]

        # Routes principales
        assert "/dashboard" in routes
        assert "/dashboard/health" in routes
        assert "/dashboard/pain" in routes
        assert "/dashboard/patterns" in routes
        assert "/dashboard/reports" in routes

        # Routes d'export
        assert "/dashboard/export/pdf" in routes
        assert "/dashboard/export/excel" in routes
        assert "/dashboard/export/html" in routes
        assert "/dashboard/preview" in routes


class TestDashboardPages:
    """Tests des pages du dashboard."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        app = FastAPI()
        _dashboard = ARIA_MetricsDashboard(app)
        return TestClient(app)

    def test_dashboard_main_page(self, client):
        """Test page principale du dashboard."""
        response = client.get("/dashboard")

        assert response.status_code == 200
        assert "ARKALIA ARIA" in response.text
        assert "Accueil" in response.text
        assert "Santé" in response.text

    def test_dashboard_health_page(self, client):
        """Test page des métriques santé."""
        response = client.get("/dashboard/health")

        assert response.status_code == 200
        assert "ARKALIA ARIA" in response.text
        assert "Santé" in response.text
        assert "Synchroniser Santé" in response.text

    def test_dashboard_pain_page(self, client):
        """Test page d'analyse de douleur."""
        response = client.get("/dashboard/pain")

        assert response.status_code == 200
        assert "Analyse Douleur ARIA" in response.text
        assert "Intensité" in response.text
        assert "Déclencheurs" in response.text

    def test_dashboard_patterns_page(self, client):
        """Test page de visualisation des patterns."""
        response = client.get("/dashboard/patterns")

        assert response.status_code == 200
        assert "ARKALIA ARIA" in response.text
        assert "Patterns" in response.text

    def test_dashboard_reports_page(self, client):
        """Test page de génération de rapports."""
        response = client.get("/dashboard/reports")

        assert response.status_code == 200
        assert "Rapports ARIA" in response.text
        assert "Génération" in response.text
        assert "Export" in response.text


class TestExportHandlers:
    """Tests des gestionnaires d'export."""

    @pytest.fixture
    def pdf_handler(self):
        """Fixture pour le gestionnaire PDF."""
        return PDFExportHandler()

    @pytest.fixture
    def excel_handler(self):
        """Fixture pour le gestionnaire Excel."""
        return ExcelExportHandler()

    @pytest.fixture
    def html_handler(self):
        """Fixture pour le gestionnaire HTML."""
        return HTMLExportHandler()

    @pytest.fixture
    def preview_handler(self):
        """Fixture pour le gestionnaire d'aperçu."""
        return ReportPreviewHandler()

    @pytest.fixture
    def mock_request(self):
        """Fixture pour une requête mock."""
        request = Mock()
        request.json = AsyncMock(
            return_value={
                "start_date": "2024-01-01",
                "end_date": "2024-01-07",
                "data_types": ["pain", "activity", "sleep"],
                "include_charts": True,
                "include_summary": True,
                "include_recommendations": True,
                "data": {
                    "pain": [],
                    "activity": [],
                    "sleep": [],
                    "stress": [],
                    "health": [],
                },
            }
        )
        return request

    @pytest.mark.asyncio
    async def test_pdf_export_handler(self, pdf_handler, mock_request):
        """Test gestionnaire d'export PDF."""
        response = await pdf_handler.export(mock_request)

        assert response is not None
        assert hasattr(response, "body")
        assert hasattr(response, "headers")

        # Vérifier le type de contenu
        assert "application/pdf" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_excel_export_handler(self, excel_handler, mock_request):
        """Test gestionnaire d'export Excel."""
        response = await excel_handler.export(mock_request)

        assert response is not None
        assert hasattr(response, "body")
        assert hasattr(response, "headers")

        # Vérifier le type de contenu
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in response.headers.get("content-type", "")
        )

    @pytest.mark.asyncio
    async def test_html_export_handler(self, html_handler, mock_request):
        """Test gestionnaire d'export HTML."""
        response = await html_handler.export(mock_request)

        assert response is not None
        assert hasattr(response, "body")
        assert hasattr(response, "headers")

        # Vérifier le type de contenu
        assert "text/html" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_report_preview_handler(self, preview_handler, mock_request):
        """Test gestionnaire d'aperçu de rapport."""
        response = await preview_handler.preview(mock_request)

        assert response is not None
        assert hasattr(response, "body")
        assert hasattr(response, "headers")

        # Vérifier le type de contenu
        assert "text/html" in response.headers.get("content-type", "")


class TestExportEndpoints:
    """Tests des endpoints d'export."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        app = FastAPI()
        dashboard = ARIA_MetricsDashboard(app)
        return TestClient(dashboard.app)

    def test_export_pdf_endpoint(self, client):
        """Test endpoint d'export PDF."""
        response = client.post(
            "/dashboard/export/pdf",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-07",
                "data_types": ["pain", "activity"],
                "include_charts": True,
                "include_summary": True,
                "include_recommendations": True,
                "data": {
                    "pain": [],
                    "activity": [],
                    "sleep": [],
                    "stress": [],
                    "health": [],
                },
            },
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert len(response.content) > 0

    def test_export_excel_endpoint(self, client):
        """Test endpoint d'export Excel."""
        response = client.post(
            "/dashboard/export/excel",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-07",
                "data_types": ["pain", "activity"],
                "include_charts": True,
                "include_summary": True,
                "include_recommendations": True,
                "data": {
                    "pain": [],
                    "activity": [],
                    "sleep": [],
                    "stress": [],
                    "health": [],
                },
            },
        )

        assert response.status_code == 200
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in response.headers["content-type"]
        )
        assert len(response.content) > 0

    def test_export_html_endpoint(self, client):
        """Test endpoint d'export HTML."""
        response = client.post(
            "/dashboard/export/html",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-07",
                "data_types": ["pain", "activity"],
                "include_charts": True,
                "include_summary": True,
                "include_recommendations": True,
                "data": {
                    "pain": [],
                    "activity": [],
                    "sleep": [],
                    "stress": [],
                    "health": [],
                },
            },
        )

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert len(response.content) > 0

    def test_preview_endpoint(self, client):
        """Test endpoint d'aperçu."""
        response = client.post(
            "/dashboard/preview",
            json={
                "type": "health_report",
                "period": 7,
                "format": "html",
                "language": "fr",
                "options": {
                    "includeCharts": True,
                    "includeInsights": True,
                    "includeRecommendations": True,
                    "includeRawData": False,
                },
            },
        )

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "ARKALIA ARIA" in response.text
        assert "Aperçu du Rapport" in response.text


class TestExportErrorHandling:
    """Tests de gestion des erreurs d'export."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        app = FastAPI()
        dashboard = ARIA_MetricsDashboard(app)
        return TestClient(dashboard.app)

    def test_export_pdf_invalid_data(self, client):
        """Test export PDF avec données invalides."""
        response = client.post("/dashboard/export/pdf", json={"invalid": "data"})

        assert response.status_code == 200
        assert "application/pdf" in response.headers["content-type"]

    def test_export_excel_missing_data(self, client):
        """Test export Excel avec données manquantes."""
        response = client.post("/dashboard/export/excel", json={})

        assert response.status_code == 200
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in response.headers["content-type"]
        )

    def test_export_html_invalid_json(self, client):
        """Test export HTML avec JSON invalide."""
        response = client.post(
            "/dashboard/export/html",
            data="invalid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 500


class TestDashboardTemplates:
    """Tests des templates du dashboard."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        app = FastAPI()
        dashboard = ARIA_MetricsDashboard(app)
        return TestClient(dashboard.app)

    def test_dashboard_template_content(self, client):
        """Test contenu du template principal."""
        response = client.get("/dashboard")

        assert response.status_code == 200
        content = response.text

        # Vérifier les éléments HTML essentiels
        assert "<!DOCTYPE html>" in content
        assert "<html" in content
        assert "<head>" in content
        assert "<body>" in content
        assert "ARKALIA ARIA" in content

        # Vérifier les scripts JavaScript
        assert "charts.js" in content
        assert "realtime.js" in content
        assert "dashboard.js" in content

    def test_health_metrics_template_content(self, client):
        """Test contenu du template métriques santé."""
        response = client.get("/dashboard/health")

        assert response.status_code == 200
        content = response.text

        # Vérifier les éléments spécifiques aux métriques santé
        assert "ARKALIA ARIA" in content
        assert "Fréquence Cardiaque" in content
        assert "Pression Artérielle" in content
        assert "Poids" in content
        assert "IMC" in content

    def test_pain_analytics_template_content(self, client):
        """Test contenu du template analyse douleur."""
        response = client.get("/dashboard/pain")

        assert response.status_code == 200
        content = response.text

        # Vérifier les éléments spécifiques à l'analyse de douleur
        assert "Analyse Douleur" in content
        assert "Intensité" in content
        assert "Déclencheurs" in content
        assert "Localisation" in content
        assert "Actions" in content

    def test_patterns_template_content(self, client):
        """Test contenu du template patterns."""
        response = client.get("/dashboard/patterns")

        assert response.status_code == 200
        content = response.text

        # Vérifier les éléments spécifiques aux patterns
        assert "ARKALIA ARIA" in content
        assert "Corrélations" in content
        assert "Patterns" in content
        assert "Analyse" in content

    def test_reports_template_content(self, client):
        """Test contenu du template rapports."""
        response = client.get("/dashboard/reports")

        assert response.status_code == 200
        content = response.text

        # Vérifier les éléments spécifiques aux rapports
        assert "Rapports" in content
        assert "Génération" in content
        assert "Export" in content
        assert "PDF" in content
        assert "Excel" in content
        assert "HTML" in content


class TestDashboardStaticAssets:
    """Tests des assets statiques du dashboard."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        app = FastAPI()
        dashboard = ARIA_MetricsDashboard(app)
        return TestClient(dashboard.app)

    def test_charts_js_exists(self, client):
        """Test existence du fichier charts.js."""
        # Note: En réalité, ces fichiers seraient servis par un serveur statique
        # Ici on teste juste que les références existent dans les templates
        response = client.get("/dashboard")

        assert response.status_code == 200
        assert "charts.js" in response.text

    def test_realtime_js_exists(self, client):
        """Test existence du fichier realtime.js."""
        response = client.get("/dashboard")

        assert response.status_code == 200
        assert "realtime.js" in response.text

    def test_exports_js_exists(self, client):
        """Test existence du fichier exports.js."""
        response = client.get("/dashboard")

        assert response.status_code == 200
        assert "dashboard.js" in response.text


class TestDashboardPerformance:
    """Tests de performance du dashboard."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        app = FastAPI()
        dashboard = ARIA_MetricsDashboard(app)
        return TestClient(dashboard.app)

    def test_dashboard_page_load_time(self, client):
        """Test temps de chargement de la page dashboard."""
        import time

        start_time = time.time()
        response = client.get("/dashboard")
        end_time = time.time()

        assert response.status_code == 200
        duration = end_time - start_time
        assert duration < 2  # Page doit se charger en moins de 2 secondes

    def test_export_performance(self, client):
        """Test performance des exports."""
        import time

        export_data = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-07",
            "data_types": ["pain", "activity"],
            "include_charts": True,
            "include_summary": True,
            "include_recommendations": True,
            "data": {
                "pain": [],
                "activity": [],
                "sleep": [],
                "stress": [],
                "health": [],
            },
        }

        # Test export PDF
        start_time = time.time()
        response = client.post("/dashboard/export/pdf", json=export_data)
        end_time = time.time()

        assert response.status_code == 200
        duration = end_time - start_time
        assert duration < 5  # Export PDF doit prendre moins de 5 secondes

        # Test export Excel
        start_time = time.time()
        response = client.post("/dashboard/export/excel", json=export_data)
        end_time = time.time()

        assert response.status_code == 200
        duration = end_time - start_time
        assert duration < 5  # Export Excel doit prendre moins de 5 secondes

        # Test export HTML
        start_time = time.time()
        response = client.post("/dashboard/export/html", json=export_data)
        end_time = time.time()

        assert response.status_code == 200
        duration = end_time - start_time
        assert duration < 3  # Export HTML doit prendre moins de 3 secondes


class TestDashboardIntegration:
    """Tests d'intégration du dashboard."""

    @pytest.fixture
    def client(self):
        """Fixture pour le client de test."""
        from fastapi import FastAPI

        app = FastAPI()
        dashboard = ARIA_MetricsDashboard(app)
        return TestClient(dashboard.app)

    def test_dashboard_navigation(self, client):
        """Test navigation entre les pages du dashboard."""
        # Page principale
        response = client.get("/dashboard")
        assert response.status_code == 200

        # Navigation vers métriques santé
        response = client.get("/dashboard/health")
        assert response.status_code == 200

        # Navigation vers analyse douleur
        response = client.get("/dashboard/pain")
        assert response.status_code == 200

        # Navigation vers patterns
        response = client.get("/dashboard/patterns")
        assert response.status_code == 200

        # Navigation vers rapports
        response = client.get("/dashboard/reports")
        assert response.status_code == 200

    def test_dashboard_export_workflow(self, client):
        """Test workflow complet d'export."""
        # 1. Accéder à la page des rapports
        response = client.get("/dashboard/reports")
        assert response.status_code == 200

        # 2. Générer un aperçu
        preview_data = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-07",
            "data_types": ["pain", "activity"],
            "include_charts": True,
            "include_summary": True,
            "include_recommendations": True,
            "data": {
                "pain": [],
                "activity": [],
                "sleep": [],
                "stress": [],
                "health": [],
            },
        }

        response = client.post("/dashboard/preview", json=preview_data)
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "ARKALIA ARIA" in response.text

        # 3. Exporter en PDF
        response = client.post("/dashboard/export/pdf", json=preview_data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"

        # 4. Exporter en Excel
        response = client.post("/dashboard/export/excel", json=preview_data)
        assert response.status_code == 200
        assert (
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            in response.headers["content-type"]
        )

        # 5. Exporter en HTML
        response = client.post("/dashboard/export/html", json=preview_data)
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
