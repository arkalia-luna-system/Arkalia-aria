"""
ARKALIA ARIA - Research Intelligence Assistant
Point d'entrée principal pour le laboratoire de recherche santé personnel
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au Python path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from audio_voice.api import router as audio_router
from cia_sync.api import router as sync_router

# Import du système DevOps
from devops_automation.api import ARIA_DevOpsAPI

# Import des connecteurs santé
from health_connectors.api import HealthConnectorsAPI

# Import du système de métriques
from metrics_collector.api import ARIA_MetricsAPI

# Import des modules ARIA
from pain_tracking.api import router as pain_router
from pattern_analysis.api import router as pattern_router
from prediction_engine.api import router as prediction_router
from research_tools.api import router as research_router
from watch_integration.api import router as watch_router

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
app.include_router(audio_router, prefix="/api/audio", tags=["Audio/Voice"])
app.include_router(watch_router, prefix="/api/watch", tags=["Watch Integration"])

# Intégration des connecteurs santé
try:
    health_api = HealthConnectorsAPI()
    health_api.integrate_with_app(app)
    print("✅ Connecteurs santé intégrés")
except Exception as e:
    print(f"⚠️ Connecteurs santé désactivés: {e}")

# Intégration du système de métriques
try:
    metrics_api = ARIA_MetricsAPI(".")
    metrics_api.integrate_with_app(app)
    print("✅ Système de métriques intégré")
except Exception as e:
    print(f"⚠️ Métriques désactivées: {e}")

# Intégration du système DevOps
try:
    devops_api = ARIA_DevOpsAPI(".")
    devops_api.integrate_with_app(app)
    print("✅ Système DevOps intégré")
except Exception as e:
    print(f"⚠️ DevOps désactivé: {e}")


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
            "audio_voice",
            "watch_integration",
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
