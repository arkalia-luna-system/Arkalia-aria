"""
BBIA API - Endpoints pour intégration BBIA-SIM
API REST pour communication avec le robot compagnon
"""

from datetime import datetime, timedelta

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
        latest_entry = db.execute_query("""
            SELECT intensity, physical_trigger, mental_trigger, timestamp
            FROM pain_entries
            ORDER BY timestamp DESC
            LIMIT 1
            """)

        if not latest_entry:
            raise HTTPException(
                status_code=404, detail="Aucune entrée de douleur trouvée"
            )

        entry = dict(latest_entry[0])
        pain_intensity = float(entry.get("intensity", 0))

        # Récupérer stress et sommeil depuis health_connectors si disponible
        stress_level = None
        sleep_quality = None

        try:
            from health_connectors.sync_manager import HealthSyncManager

            sync_manager = HealthSyncManager()
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1)  # Dernières 24h

            # Récupérer données stress (dernière valeur)
            try:
                stress_data = await sync_manager.get_unified_stress_data(
                    start_date, end_date
                )
                if stress_data:
                    # Prendre la dernière valeur de stress
                    latest_stress = stress_data[-1]
                    stress_level = (
                        float(latest_stress.stress_level) / 10.0
                    )  # Normaliser 0-1
            except Exception as e:
                logger.debug(f"Données stress non disponibles: {e}")

            # Récupérer données sommeil (dernière valeur)
            try:
                sleep_data = await sync_manager.get_unified_sleep_data(
                    start_date, end_date
                )
                if sleep_data:
                    # Prendre la dernière valeur de sommeil
                    latest_sleep = sleep_data[-1]
                    if latest_sleep.quality_score is not None:
                        sleep_quality = (
                            float(latest_sleep.quality_score) / 10.0
                        )  # Normaliser 0-1
            except Exception as e:
                logger.debug(f"Données sommeil non disponibles: {e}")
        except Exception as e:
            logger.debug(f"Health connectors non disponibles: {e}")

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
