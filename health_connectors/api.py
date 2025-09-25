"""
ARKALIA ARIA - API Connecteurs Santé
====================================

API FastAPI pour les connecteurs santé permettant :
- Synchronisation avec Samsung Health, Google Fit, iOS Health
- Récupération des données unifiées
- Gestion des connecteurs et statuts
"""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from core import BaseAPI, get_logger

from .config import HealthConnectorConfig
from .data_models import (
    ActivityData,
    HealthData,
    HealthSyncStatus,
    SleepData,
    StressData,
)
from .sync_manager import HealthSyncManager

logger = get_logger("health_connectors")


class SyncRequest(BaseModel):
    """Requête de synchronisation."""

    days_back: int | None = Field(
        30, ge=1, le=365, description="Nombre de jours à synchroniser"
    )
    connector_name: str | None = Field(
        None, description="Connecteur spécifique (optionnel)"
    )


class SyncResponse(BaseModel):
    """Réponse de synchronisation."""

    status: str = Field(..., description="Statut de la synchronisation")
    message: str = Field(..., description="Message de statut")
    sync_summary: dict[str, Any] | None = Field(
        None, description="Résumé de la synchronisation"
    )
    timestamp: str = Field(..., description="Horodatage de la réponse")


class HealthConnectorsAPI(BaseAPI):
    """
    API REST pour les connecteurs santé ARKALIA ARIA.

    Endpoints disponibles :
    - GET /health/connectors/status : Statut des connecteurs
    - POST /health/samsung/sync : Synchronisation Samsung Health
    - POST /health/google/sync : Synchronisation Google Fit
    - POST /health/ios/sync : Synchronisation iOS Health
    - GET /health/data/activity : Données d'activité unifiées
    - GET /health/data/sleep : Données de sommeil unifiées
    - GET /health/data/stress : Données de stress unifiées
    - GET /health/data/health : Données de santé unifiées
    - GET /health/metrics/unified : Métriques unifiées pour dashboard
    """

    def __init__(self) -> None:
        """Initialise l'API des connecteurs santé."""
        super().__init__("/health", ["Health Connectors"])
        self.sync_manager = HealthSyncManager()
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Configure les routes de l'API."""

        @self.router.get(
            "/connectors/status", response_model=dict[str, HealthSyncStatus]
        )
        async def get_connectors_status():
            """Retourne le statut de tous les connecteurs santé."""
            try:
                status = await self.sync_manager.get_all_connectors_status()
                return status
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur statut connecteurs: {str(e)}"
                ) from e

        @self.router.post("/samsung/sync", response_model=SyncResponse)
        async def sync_samsung_health(request: SyncRequest):
            """Synchronise les données Samsung Health."""
            try:
                sync_summary = await self.sync_manager.sync_single_connector(
                    "samsung_health", request.days_back
                )

                if sync_summary["status"] == "success":
                    return SyncResponse(
                        status="success",
                        message="Synchronisation Samsung Health réussie",
                        sync_summary=sync_summary,
                        timestamp=datetime.now().isoformat(),
                    )
                else:
                    return SyncResponse(
                        status="error",
                        message=f"Erreur synchronisation Samsung Health: {sync_summary.get('error', 'Erreur inconnue')}",
                        sync_summary=sync_summary,
                        timestamp=datetime.now().isoformat(),
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur Samsung Health: {str(e)}"
                ) from e

        @self.router.post("/google/sync", response_model=SyncResponse)
        async def sync_google_fit(request: SyncRequest):
            """Synchronise les données Google Fit."""
            try:
                sync_summary = await self.sync_manager.sync_single_connector(
                    "google_fit", request.days_back
                )

                if sync_summary["status"] == "success":
                    return SyncResponse(
                        status="success",
                        message="Synchronisation Google Fit réussie",
                        sync_summary=sync_summary,
                        timestamp=datetime.now().isoformat(),
                    )
                else:
                    return SyncResponse(
                        status="error",
                        message=f"Erreur synchronisation Google Fit: {sync_summary.get('error', 'Erreur inconnue')}",
                        sync_summary=sync_summary,
                        timestamp=datetime.now().isoformat(),
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur Google Fit: {str(e)}"
                ) from e

        @self.router.post("/ios/sync", response_model=SyncResponse)
        async def sync_ios_health(request: SyncRequest):
            """Synchronise les données iOS Health."""
            try:
                sync_summary = await self.sync_manager.sync_single_connector(
                    "ios_health", request.days_back
                )

                if sync_summary["status"] == "success":
                    return SyncResponse(
                        status="success",
                        message="Synchronisation iOS Health réussie",
                        sync_summary=sync_summary,
                        timestamp=datetime.now().isoformat(),
                    )
                else:
                    return SyncResponse(
                        status="error",
                        message=f"Erreur synchronisation iOS Health: {sync_summary.get('error', 'Erreur inconnue')}",
                        sync_summary=sync_summary,
                        timestamp=datetime.now().isoformat(),
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur iOS Health: {str(e)}"
                ) from e

        @self.router.post("/sync/all", response_model=SyncResponse)
        async def sync_all_connectors(request: SyncRequest):
            """Synchronise tous les connecteurs santé."""
            try:
                sync_summary = await self.sync_manager.sync_all_connectors(
                    request.days_back
                )

                if sync_summary["status"] in ["success", "partial_success"]:
                    return SyncResponse(
                        status=sync_summary["status"],
                        message=f"Synchronisation complète: {sync_summary['status']}",
                        sync_summary=sync_summary,
                        timestamp=datetime.now().isoformat(),
                    )
                else:
                    return SyncResponse(
                        status="error",
                        message="Erreur synchronisation complète",
                        sync_summary=sync_summary,
                        timestamp=datetime.now().isoformat(),
                    )
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur synchronisation: {str(e)}"
                ) from e

        @self.router.get("/data/activity", response_model=list[ActivityData])
        async def get_unified_activity_data(
            days_back: int = Query(
                30, ge=1, le=365, description="Nombre de jours à récupérer"
            )
        ):
            """Retourne les données d'activité unifiées."""
            try:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_back)

                activity_data = await self.sync_manager.get_unified_activity_data(
                    start_date, end_date
                )
                return activity_data
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur données activité: {str(e)}"
                ) from e

        @self.router.get("/data/sleep", response_model=list[SleepData])
        async def get_unified_sleep_data(
            days_back: int = Query(
                30, ge=1, le=365, description="Nombre de jours à récupérer"
            )
        ):
            """Retourne les données de sommeil unifiées."""
            try:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_back)

                sleep_data = await self.sync_manager.get_unified_sleep_data(
                    start_date, end_date
                )
                return sleep_data
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur données sommeil: {str(e)}"
                ) from e

        @self.router.get("/data/stress", response_model=list[StressData])
        async def get_unified_stress_data(
            days_back: int = Query(
                30, ge=1, le=365, description="Nombre de jours à récupérer"
            )
        ):
            """Retourne les données de stress unifiées."""
            try:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_back)

                stress_data = await self.sync_manager.get_unified_stress_data(
                    start_date, end_date
                )
                return stress_data
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur données stress: {str(e)}"
                ) from e

        @self.router.get("/data/health", response_model=list[HealthData])
        async def get_unified_health_data(
            days_back: int = Query(
                30, ge=1, le=365, description="Nombre de jours à récupérer"
            )
        ):
            """Retourne les données de santé unifiées."""
            try:
                end_date = datetime.now()
                start_date = end_date - timedelta(days=days_back)

                health_data = []
                for connector in self.sync_manager.connectors.values():
                    try:
                        connector_data = await connector.get_health_data(
                            start_date, end_date
                        )
                        health_data.extend(connector_data)
                    except Exception as e:
                        connector.sync_errors.append(f"Erreur données santé: {str(e)}")

                # Trier par timestamp
                health_data.sort(key=lambda x: x.timestamp)
                return health_data
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur données santé: {str(e)}"
                ) from e

        @self.router.get("/metrics/unified", response_model=dict[str, Any])
        async def get_unified_metrics(
            days_back: int = Query(
                30, ge=1, le=365, description="Nombre de jours à analyser"
            )
        ):
            """Retourne les métriques unifiées pour le dashboard."""
            try:
                unified_metrics = await self.sync_manager._generate_unified_metrics(
                    days_back
                )
                return unified_metrics
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur métriques unifiées: {str(e)}"
                ) from e

        @self.router.get("/config", response_model=HealthConnectorConfig)
        async def get_config():
            """Retourne la configuration des connecteurs."""
            return self.sync_manager.config

        @self.router.put("/config", response_model=HealthConnectorConfig)
        async def update_config(config: HealthConnectorConfig):
            """Met à jour la configuration des connecteurs."""
            try:
                self.sync_manager.config = config
                self.sync_manager._initialize_connectors()
                return self.sync_manager.config
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur configuration: {str(e)}"
                ) from e

    def get_router(self) -> APIRouter:
        """Retourne le router FastAPI."""
        return self.router

    def integrate_with_app(self, app) -> None:
        """Intègre l'API des connecteurs santé avec une application FastAPI."""
        app.include_router(self.router)


# Instance FastAPI pour les connecteurs santé
app = FastAPI(
    title="ARKALIA ARIA - Connecteurs Santé",
    description="API pour la synchronisation des données santé",
    version="1.0.0",
)

# Créer l'instance de l'API et l'intégrer
health_api = HealthConnectorsAPI()
health_api.integrate_with_app(app)
