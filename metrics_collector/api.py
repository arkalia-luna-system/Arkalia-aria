#!/usr/bin/env python3
"""
ARKALIA ARIA - API des Métriques
===============================

API FastAPI pour exposer les métriques ARIA via des endpoints REST.
Intégration complète avec le système de collecte, validation et dashboard.
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .collectors.aria_metrics_collector import ARIA_MetricsCollector
from .dashboard.aria_metrics_dashboard import ARIA_MetricsDashboard
from .exporters.aria_metrics_exporter import ARIA_MetricsExporter
from .validators.aria_metrics_validator import ARIA_MetricsValidator


class ARIA_MetricsAPI:
    """
    API REST pour les métriques ARIA.

    Endpoints disponibles :
    - GET /metrics : Métriques complètes
    - GET /metrics/health : Statut de santé
    - GET /metrics/dashboard : Dashboard HTML
    - GET /metrics/export/{format} : Export des métriques
    - POST /metrics/collect : Collecte forcée
    """

    def __init__(self, project_root: str = ".") -> None:
        """
        Initialise l'API des métriques ARIA.

        Args:
            project_root: Racine du projet ARIA
        """
        self.project_root = project_root
        self.collector = ARIA_MetricsCollector(project_root)
        self.exporter = ARIA_MetricsExporter("metrics_reports")
        self.validator = ARIA_MetricsValidator()
        self.dashboard = ARIA_MetricsDashboard()

        self.router = APIRouter(prefix="/metrics", tags=["metrics"])
        self._setup_routes()

        # Cache des métriques
        self._metrics_cache: dict[str, Any] | None = None
        self._cache_timestamp: datetime | None = None
        self._cache_duration_seconds = 300  # 5 minutes

    def _setup_routes(self) -> None:
        """Configure les routes de l'API."""

        @self.router.get("/", response_model=dict[str, Any])
        async def get_metrics():
            """Récupère toutes les métriques ARIA."""
            try:
                metrics = await self._get_cached_metrics()
                return {
                    "status": "success",
                    "data": metrics,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur collecte métriques: {str(e)}"
                ) from e

        @self.router.get("/health", response_model=dict[str, Any])
        async def get_health_status():
            """Récupère le statut de santé du projet."""
            try:
                metrics = await self._get_cached_metrics()
                health_status = self.validator.get_health_status(metrics)
                return {
                    "status": "success",
                    "health": health_status,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur statut santé: {str(e)}"
                ) from e

        @self.router.get("/dashboard", response_class=HTMLResponse)
        async def get_dashboard(request: Request):
            """Retourne le dashboard HTML interactif."""
            try:
                metrics = await self._get_cached_metrics()
                dashboard_html = self.dashboard.generate_dashboard_html(metrics)
                return HTMLResponse(content=dashboard_html)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur génération dashboard: {str(e)}"
                ) from e

        @self.router.get("/export/{format}")
        async def export_metrics(format: str):
            """Exporte les métriques dans le format spécifié."""
            try:
                metrics = await self._get_cached_metrics()

                if format.lower() == "json":
                    file_path = self.exporter.export_json(metrics)
                elif format.lower() == "markdown":
                    file_path = self.exporter.export_markdown(metrics)
                elif format.lower() == "html":
                    file_path = self.exporter.export_html(metrics)
                elif format.lower() == "csv":
                    file_path = self.exporter.export_csv(metrics)
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="Format non supporté. Utilisez: json, markdown, html, csv",
                    )

                return {
                    "status": "success",
                    "message": f"Métriques exportées en {format.upper()}",
                    "file_path": str(file_path),
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur export: {str(e)}"
                ) from e

        @self.router.post("/collect")
        async def force_collect_metrics():
            """Force la collecte des métriques (ignore le cache)."""
            try:
                metrics = self.collector.collect_all_metrics()
                self._metrics_cache = metrics
                self._cache_timestamp = datetime.now()

                return {
                    "status": "success",
                    "message": "Métriques collectées avec succès",
                    "data": metrics,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur collecte forcée: {str(e)}"
                ) from e

        @self.router.get("/validate", response_model=dict[str, Any])
        async def validate_metrics():
            """Valide les métriques et retourne les résultats de validation."""
            try:
                metrics = await self._get_cached_metrics()
                validation_results = self.validator.validate_metrics(metrics)

                return {
                    "status": "success",
                    "validation": validation_results,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur validation: {str(e)}"
                ) from e

        @self.router.get("/summary", response_model=dict[str, Any])
        async def get_metrics_summary():
            """Retourne un résumé des métriques principales."""
            try:
                metrics = await self._get_cached_metrics()

                summary = {
                    "project_name": (
                        metrics.get("project_info", {}).get("name", "ARKALIA ARIA")
                    ),
                    "python_files": metrics.get("python_files", {}).get("count", 0),
                    "total_lines": (
                        metrics.get("python_files", {}).get("total_lines", 0)
                    ),
                    "test_files": metrics.get("tests", {}).get("test_files_count", 0),
                    "coverage": metrics.get("tests", {}).get("coverage_percentage", 0),
                    "pain_entries": (
                        metrics.get("aria_specific", {}).get("pain_tracking", 0)
                    ),
                    "patterns": (
                        metrics.get("aria_specific", {}).get("pattern_analysis", 0)
                    ),
                    "predictions": (
                        metrics.get("aria_specific", {}).get("predictions", 0)
                    ),
                    "security_issues": (
                        metrics.get("security", {})
                        .get("bandit_scan", {})
                        .get("issues_found", 0)
                    ),
                    "memory_usage": (
                        metrics.get("performance", {}).get("memory_usage_mb", 0)
                    ),
                    "cpu_usage": metrics.get("performance", {}).get("cpu_percent", 0),
                }

                return {
                    "status": "success",
                    "summary": summary,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur résumé: {str(e)}"
                ) from e

        @self.router.get("/alerts", response_model=dict[str, Any])
        async def get_alerts():
            """Retourne les alertes et recommandations."""
            try:
                metrics = await self._get_cached_metrics()
                validation_results = self.validator.validate_metrics(metrics)

                return {
                    "status": "success",
                    "alerts": validation_results.get("alerts", []),
                    "recommendations": validation_results.get("recommendations", []),
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur alertes: {str(e)}"
                ) from e

    async def _get_cached_metrics(self) -> dict[str, Any]:
        """Récupère les métriques depuis le cache ou les collecte."""
        now = datetime.now()

        # Vérifier si le cache est valide
        if (
            self._metrics_cache is not None
            and self._cache_timestamp is not None
            and (now - self._cache_timestamp).total_seconds()
            < self._cache_duration_seconds
        ):
            return self._metrics_cache

        # Collecter de nouvelles métriques
        metrics = self.collector.collect_all_metrics()
        self._metrics_cache = metrics
        self._cache_timestamp = now

        return metrics

    def get_router(self) -> APIRouter:
        """Retourne le router FastAPI configuré."""
        return self.router

    def integrate_with_app(self, app) -> None:
        """Intègre l'API des métriques avec une application FastAPI."""
        app.include_router(self.router)

        # Configurer le dashboard
        self.dashboard = ARIA_MetricsDashboard(app)

        # Créer les fichiers statiques
        self.dashboard.create_static_files()

        # Monter les fichiers statiques
        static_dir = self.dashboard.static_dir
        if static_dir.exists():
            app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        else:
            print(f"⚠️ Répertoire static non trouvé: {static_dir}")
