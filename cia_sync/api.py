"""
CIA Sync API - Module de synchronisation ARIA
Synchronisation bidirectionnelle optimisée avec Arkalia CIA
"""

import importlib
from datetime import datetime
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel

from core import BaseAPI, get_logger

from .auto_sync import get_auto_sync_manager

# Créer l'API avec BaseAPI
api = BaseAPI("", ["CIA Sync"])  # Pas de préfixe ici, il sera ajouté dans main.py
router = api.get_router()
logger = get_logger("cia_sync")

# Charger requests dynamiquement pour éviter les stubs mypy requis
requests: Any = importlib.import_module("requests")

# Configuration CIA
CIA_BASE_URL = "http://127.0.0.1:8000"
CIA_TIMEOUT = 10


class SyncConfig(BaseModel):
    """Configuration de synchronisation"""

    sync_pain_entries: bool = True
    sync_patterns: bool = True
    sync_predictions: bool = True
    anonymize_for_psy: bool = False
    auto_sync_interval: int | None = None  # minutes


def _check_cia_connection() -> bool:
    """Vérifie si CIA est accessible"""
    try:
        response = requests.get(f"{CIA_BASE_URL}/health", timeout=CIA_TIMEOUT)
        is_connected = response.status_code == 200
        logger.debug(f"Vérification CIA: {is_connected}")
        return is_connected
    except Exception as e:
        logger.warning(f"CIA non accessible: {e}")
        return False


def _make_cia_request(method: str, endpoint: str, **kwargs) -> Any:
    """Effectue une requête vers CIA avec gestion d'erreurs"""
    try:
        url = f"{CIA_BASE_URL}{endpoint}"
        response = requests.request(method, url, timeout=CIA_TIMEOUT, **kwargs)
        return response
    except Exception as e:
        # Créer une réponse mock simple
        response = requests.Response()
        response.status_code = 503
        response._content = (
            f'{{"error": "Impossible de contacter CIA: {str(e)}"}}'.encode()
        )
        return response


@router.get("/status")
async def cia_sync_status() -> dict:
    """Statut du module CIA sync"""
    cia_connected = _check_cia_connection()
    logger.info(f"Statut CIA sync demandé - Connecté: {cia_connected}")

    return {
        "module": "cia_sync",
        "status": "healthy" if cia_connected else "cia_unavailable",
        "timestamp": datetime.now().isoformat(),
        "cia_connected": cia_connected,
        "cia_url": CIA_BASE_URL,
        "features": [
            "selective_sync",
            "psy_presentation_mode",
            "granular_permissions",
            "data_control",
            "bidirectional_sync",
            "auto_sync_periodic",
            "intelligent_aggregation",
        ],
    }


@router.get("/connection")
async def check_cia_connection() -> dict:
    """Vérifie la connexion avec CIA"""
    cia_connected = _check_cia_connection()

    return {
        "message": "CIA sync opérationnel" if cia_connected else "CIA non disponible",
        "connected": cia_connected,
        "cia_url": CIA_BASE_URL,
        "timestamp": datetime.now().isoformat(),
    }


@router.post("/sync/selective")
async def selective_sync(config: SyncConfig) -> dict:
    """Synchronisation sélective avec CIA"""
    if not _check_cia_connection():
        raise HTTPException(status_code=503, detail="CIA non disponible")

    synced_data = []

    try:
        # Synchronisation des entrées de douleur
        if config.sync_pain_entries:
            response = _make_cia_request("GET", "/api/aria/pain-entries")
            if response.status_code == 200:
                synced_data.append(
                    {
                        "type": "pain_entries",
                        "count": len(response.json()),
                        "status": "synced",
                    }
                )

        # Synchronisation des patterns
        if config.sync_patterns:
            response = _make_cia_request("GET", "/api/aria/patterns/recent")
            if response.status_code == 200:
                synced_data.append({"type": "patterns", "status": "synced"})

        # Synchronisation des prédictions
        if config.sync_predictions:
            response = _make_cia_request("GET", "/api/aria/predictions/current")
            if response.status_code == 200:
                synced_data.append({"type": "predictions", "status": "synced"})

        return {
            "message": "Synchronisation sélective réussie",
            "synced_data": synced_data,
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la synchronisation: {str(e)}"
        ) from e


@router.get("/psy-mode")
async def psy_presentation_mode() -> dict:
    """Mode présentation pour psychologue avec données anonymisées"""
    if not _check_cia_connection():
        raise HTTPException(status_code=503, detail="CIA non disponible")

    # Récupération des données anonymisées
    response = _make_cia_request("GET", "/api/aria/export/csv")

    if response.status_code == 200:
        export_data = response.json()

        # Anonymisation supplémentaire pour psychologue
        anonymized_data = {
            "pain_entries_count": export_data.get("entries_count", 0),
            "export_filename": export_data.get("filename", ""),
            "data_available": True,
            "anonymization_level": "high",
            "export_ready": True,
        }

        return {
            "message": "Mode présentation psy activé",
            "anonymized_data": anonymized_data,
            "export_ready": True,
            "timestamp": datetime.now().isoformat(),
        }
    else:
        raise HTTPException(
            status_code=response.status_code, detail=f"Erreur CIA: {response.text}"
        )


@router.post("/sync/push-data")
async def push_data_to_cia(data: dict[str, Any]) -> dict:
    """Pousse des données d'ARIA vers CIA"""
    if not _check_cia_connection():
        raise HTTPException(status_code=503, detail="CIA non disponible")

    try:
        # Déterminer le type de données et l'endpoint approprié
        data_type = data.get("type", "unknown")

        if data_type == "pain_entry":
            response = _make_cia_request(
                "POST", "/api/aria/pain-entry", json=data.get("payload", {})
            )
        elif data_type == "quick_entry":
            response = _make_cia_request(
                "POST", "/api/aria/quick-pain-entry", json=data.get("payload", {})
            )
        else:
            raise HTTPException(
                status_code=400, detail=f"Type de données non supporté: {data_type}"
            )

        if response.status_code in [200, 201]:
            return {
                "message": f"Données {data_type} synchronisées avec CIA",
                "status": "success",
                "cia_response": response.json(),
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=response.status_code, detail=f"Erreur CIA: {response.text}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la synchronisation: {str(e)}"
        ) from e


@router.post("/auto-sync/start")
async def start_auto_sync(interval_minutes: int = 60) -> dict:
    """
    Démarre la synchronisation automatique périodique.

    Args:
        interval_minutes: Intervalle entre chaque synchronisation (défaut: 60 min)

    Returns:
        Statut de démarrage
    """
    try:
        auto_sync = get_auto_sync_manager()
        success = auto_sync.start(interval_minutes=interval_minutes)

        if success:
            return {
                "message": "Synchronisation automatique démarrée",
                "status": "started",
                "interval_minutes": interval_minutes,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=400, detail="Synchronisation automatique déjà en cours"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur démarrage auto sync: {str(e)}"
        ) from e


@router.post("/auto-sync/stop")
async def stop_auto_sync() -> dict:
    """
    Arrête la synchronisation automatique périodique.

    Returns:
        Statut d'arrêt
    """
    try:
        auto_sync = get_auto_sync_manager()
        success = auto_sync.stop()

        if success:
            return {
                "message": "Synchronisation automatique arrêtée",
                "status": "stopped",
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=400, detail="Synchronisation automatique n'est pas en cours"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur arrêt auto sync: {str(e)}"
        ) from e


@router.get("/auto-sync/status")
async def auto_sync_status() -> dict:
    """
    Retourne le statut de la synchronisation automatique.

    Returns:
        Statut, statistiques, configuration
    """
    try:
        auto_sync = get_auto_sync_manager()
        status = auto_sync.get_status()
        return status
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur récupération statut: {str(e)}"
        ) from e


@router.post("/auto-sync/sync-now")
async def sync_now() -> dict:
    """
    Force une synchronisation immédiate (hors cycle automatique).

    Returns:
        Résultat de la synchronisation
    """
    try:
        auto_sync = get_auto_sync_manager()
        success = auto_sync.sync_now()

        if success:
            return {
                "message": "Synchronisation immédiate réussie",
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=500, detail="Synchronisation immédiate échouée"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur synchronisation immédiate: {str(e)}"
        ) from e


@router.put("/auto-sync/interval")
async def update_sync_interval(interval_minutes: int) -> dict:
    """
    Met à jour l'intervalle de synchronisation automatique.

    Args:
        interval_minutes: Nouvel intervalle en minutes (minimum: 1)

    Returns:
        Confirmation de mise à jour
    """
    try:
        auto_sync = get_auto_sync_manager()
        success = auto_sync.update_interval(interval_minutes)

        if success:
            return {
                "message": f"Intervalle mis à jour: {interval_minutes} min",
                "status": "updated",
                "interval_minutes": interval_minutes,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=400, detail="Intervalle invalide (minimum: 1 minute)"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur mise à jour intervalle: {str(e)}"
        ) from e
