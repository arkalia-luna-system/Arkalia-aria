"""
BBIA API - Endpoints pour intégration BBIA-SIM
API REST pour communication avec le robot compagnon
"""

from datetime import datetime
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel

from core import BaseAPI, get_logger

from .bbia_integration import get_bbia_integration

# Créer l'API avec BaseAPI
api = BaseAPI("", ["BBIA Integration"])
router = api.get_router()
logger = get_logger("bbia_api")


class EmotionalStateRequest(BaseModel):
    """Requête pour envoi d'état émotionnel"""

    pain_intensity: float
    stress_level: float | None = None
    sleep_quality: float | None = None


@router.get("/status")
async def get_bbia_status() -> dict:
    """
    Retourne le statut de l'intégration BBIA.

    Returns:
        Statut de connexion et configuration
    """
    try:
        bbia = get_bbia_integration()
        return bbia.get_status()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur récupération statut BBIA: {str(e)}"
        ) from e


@router.get("/connection")
async def check_bbia_connection() -> dict:
    """
    Vérifie la connexion avec BBIA-SIM.

    Returns:
        Statut de connexion
    """
    try:
        bbia = get_bbia_integration()
        is_connected = bbia.check_connection()
        return {
            "connected": is_connected,
            "bbia_url": bbia.bbia_base_url,
            "mode": "connected" if is_connected else "simulation",
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur vérification connexion: {str(e)}"
        ) from e


@router.post("/emotional-state")
async def send_emotional_state(request: EmotionalStateRequest) -> dict:
    """
    Envoie un état émotionnel à BBIA basé sur les données ARIA.

    Args:
        request: Données de douleur/stress/sommeil

    Returns:
        Résultat de l'envoi
    """
    try:
        bbia = get_bbia_integration()

        # Préparer l'état émotionnel
        emotional_state = bbia.prepare_emotional_state(
            pain_intensity=request.pain_intensity,
            stress_level=request.stress_level,
            sleep_quality=request.sleep_quality,
        )

        # Envoyer à BBIA
        result = bbia.send_emotional_state(emotional_state)

        return {
            "message": "État émotionnel préparé et envoyé à BBIA",
            "result": result,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur envoi état émotionnel: {str(e)}"
        ) from e


@router.post("/emotional-state/from-latest-pain")
async def send_emotional_state_from_latest_pain() -> dict:
    """
    Envoie un état émotionnel à BBIA basé sur la dernière entrée de douleur.

    Returns:
        Résultat de l'envoi
    """
    try:
        from core import DatabaseManager

        # Récupérer la dernière entrée de douleur
        db = DatabaseManager()
        latest_entry = db.execute_query(
            """
            SELECT intensity, physical_trigger, mental_trigger, timestamp
            FROM pain_entries
            ORDER BY timestamp DESC
            LIMIT 1
            """
        )

        if not latest_entry:
            raise HTTPException(
                status_code=404, detail="Aucune entrée de douleur trouvée"
            )

        entry = dict(latest_entry[0])
        pain_intensity = float(entry.get("intensity", 0))

        # Estimer stress et sommeil si disponibles
        stress_level = None
        sleep_quality = None

        # TODO: Récupérer depuis health_connectors si disponible

        bbia = get_bbia_integration()
        emotional_state = bbia.prepare_emotional_state(
            pain_intensity=pain_intensity,
            stress_level=stress_level,
            sleep_quality=sleep_quality,
        )

        result = bbia.send_emotional_state(emotional_state)

        return {
            "message": "État émotionnel envoyé depuis dernière entrée de douleur",
            "pain_entry": entry,
            "result": result,
            "timestamp": datetime.now().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur envoi état émotionnel depuis douleur: {str(e)}",
        ) from e

