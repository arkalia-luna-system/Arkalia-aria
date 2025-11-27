"""
ARKALIA ARIA - Research Intelligence Assistant
Point d'entrée principal pour le laboratoire de recherche santé personnel
"""

import logging
import os
import sys
from pathlib import Path

# Ajouter le répertoire courant au Python path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Imports des modules
from audio_voice.api import router as audio_router
from cia_sync.api import router as sync_router
from cia_sync.bbia_api import router as bbia_router
from devops_automation.api import ARIA_DevOpsAPI
from health_connectors.api import HealthConnectorsAPI
from metrics_collector.api import ARIA_MetricsAPI
from pain_tracking.api import router as pain_router
from pattern_analysis.api import router as pattern_router
from prediction_engine.api import router as prediction_router
from research_tools.api import router as research_router

# Configuration du logger
logger = logging.getLogger(__name__)

# watch_integration supprimé - doublon de health_connectors

# Application FastAPI
app = FastAPI(
    title="ARKALIA ARIA",
    description="Research Intelligence Assistant - Laboratoire de recherche santé personnel",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS pour intégration mobile/web
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "file://",
        "null",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Montage des routers
app.include_router(pain_router, prefix="/api/pain", tags=["Pain Tracking"])
app.include_router(pattern_router, prefix="/api/patterns", tags=["Pattern Analysis"])
app.include_router(
    prediction_router, prefix="/api/predictions", tags=["Prediction Engine"]
)
app.include_router(research_router, prefix="/api/research", tags=["Research Tools"])
app.include_router(sync_router, prefix="/api/sync", tags=["CIA Sync"])
app.include_router(bbia_router, prefix="/api/bbia", tags=["BBIA Integration"])
app.include_router(audio_router, prefix="/api/audio", tags=["Audio/Voice"])
# watch_router supprimé - doublon de health_connectors

# Intégration des connecteurs santé
try:
    health_api = HealthConnectorsAPI()
    health_api.integrate_with_app(app)
    logger.info("✅ Connecteurs santé intégrés")
except Exception as e:
    logger.warning(f"⚠️ Connecteurs santé désactivés: {e}")

# Intégration du système de métriques (désactivé en développement pour éviter les processus lourds)
if os.getenv("ARIA_ENABLE_METRICS", "false").lower() == "true":
    try:
        metrics_api = ARIA_MetricsAPI(".")
        metrics_api.integrate_with_app(app)
        logger.info("✅ Système de métriques intégré")
    except Exception as e:
        logger.warning(f"⚠️ Métriques désactivées: {e}")
else:
    logger.info("ℹ️ Système de métriques désactivé (ARIA_ENABLE_METRICS=false)")

# Intégration du système DevOps
try:
    devops_api = ARIA_DevOpsAPI(".")
    devops_api.integrate_with_app(app)
    logger.info("✅ Système DevOps intégré")
except Exception as e:
    logger.warning(f"⚠️ DevOps désactivé: {e}")

# Activation automatique de la synchronisation CIA si configurée
if os.getenv("ARIA_CIA_SYNC_ENABLED", "0").lower() in ("1", "true"):
    try:
        from cia_sync.auto_sync import get_auto_sync_manager
        from core.config import config

        auto_sync = get_auto_sync_manager()
        sync_interval = int(os.getenv("ARIA_CIA_SYNC_INTERVAL_MINUTES", "60"))
        cia_url = config.get("cia_api_url", "http://127.0.0.1:8000")

        # Mettre à jour l'URL CIA si configurée
        if cia_url != "http://127.0.0.1:8000":
            auto_sync.cia_base_url = cia_url

        success = auto_sync.start(interval_minutes=sync_interval)
        if success:
            logger.info(
                f"✅ Synchronisation automatique CIA activée "
                f"(intervalle: {sync_interval} min, URL: {cia_url})"
            )
        else:
            logger.warning("⚠️ Synchronisation automatique CIA déjà en cours")
    except Exception as e:
        logger.warning(f"⚠️ Synchronisation automatique CIA désactivée: {e}")
else:
    logger.info(
        "ℹ️ Synchronisation automatique CIA désactivée (ARIA_CIA_SYNC_ENABLED=false)"
    )


@app.get("/")
async def root():
    """Page d'accueil ARIA"""
    return {
        "message": "ARKALIA ARIA - Research Intelligence Assistant",
        "version": "1.0.0",
        "status": "running",
        "modules": [
            "pain_tracking",
            "pattern_analysis",
            "prediction_engine",
            "research_tools",
            "cia_sync",
            "bbia_integration",
            "audio_voice",
            # "watch_integration", # supprimé - doublon de health_connectors
            "health_connectors",
        ],
    }


@app.get("/health")
async def health_check():
    """Vérification de santé globale"""
    from datetime import datetime as _dt

    return {
        "status": "healthy",
        "timestamp": _dt.now().isoformat(),
        "modules_status": "all_operational",
    }


def main() -> None:
    """Point d'entrée CLI par défaut pour démarrer l'API ARIA."""
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,  # Port différent de CIA (8000)
        reload=True,
        log_level="info",
    )


def cli() -> None:
    """Alias CLI minimal, redirige vers main()."""
    main()


if __name__ == "__main__":
    # Configuration pour développement local
    main()
