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
from alerts.api import router as alerts_router
from audio_voice.api import router as audio_router
from cia_compatibility.api import router as cia_compat_router
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
# Support URLs complètes : localhost, IPs locales, Render.com (HTTPS)
cors_origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",  # CIA local
    "http://127.0.0.1:8000",  # CIA local
    "file://",
    "null",
]

# Ajouter origines CORS depuis variables d'environnement (pour Render.com)
env_cors_origins = os.getenv("ARIA_CORS_ORIGINS", "").split(",")
cors_origins.extend([origin.strip() for origin in env_cors_origins if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
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
app.include_router(alerts_router, tags=["Alerts"])
# Router de compatibilité CIA (endpoints attendus par CIA)
app.include_router(cia_compat_router, tags=["CIA Compatibility"])
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

# Activation automatique de la synchronisation santé si configurée
if os.getenv("ARIA_HEALTH_AUTO_SYNC_ENABLED", "0").lower() in ("1", "true"):
    try:
        from health_connectors.sync_manager import HealthSyncManager

        health_sync_manager = HealthSyncManager()
        success = health_sync_manager.start_auto_sync()
        if success:
            logger.info(
                f"✅ Synchronisation automatique santé activée "
                f"(intervalle: {health_sync_manager.config.sync_interval_hours}h)"
            )
        else:
            logger.warning("⚠️ Synchronisation automatique santé déjà en cours")
    except Exception as e:
        logger.warning(f"⚠️ Synchronisation automatique santé désactivée: {e}")
else:
    logger.info(
        "ℹ️ Synchronisation automatique santé désactivée (ARIA_HEALTH_AUTO_SYNC_ENABLED=false)"
    )

# Activation automatique des rapports si configurée
if os.getenv("ARIA_AUTO_REPORTS_ENABLED", "0").lower() in ("1", "true"):
    try:
        from health_connectors.report_generator import get_report_generator

        report_generator = get_report_generator()
        success = report_generator.start_weekly_reports()
        if success:
            logger.info("✅ Rapports hebdomadaires automatiques activés")
    except Exception as e:
        logger.warning(f"⚠️ Erreur activation rapports auto: {e}")

# Activation automatique des exports si configurée
if os.getenv("ARIA_AUTO_EXPORT_ENABLED", "0").lower() in ("1", "true"):
    try:
        from health_connectors.auto_export import get_auto_exporter

        auto_exporter = get_auto_exporter()
        success = auto_exporter.start_auto_exports()
        if success:
            logger.info("✅ Exports automatiques activés (hebdomadaire et mensuel)")
    except Exception as e:
        logger.warning(f"⚠️ Erreur activation exports auto: {e}")


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
            "cia_compatibility",
            "bbia_integration",
            "audio_voice",
            "alerts",
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
