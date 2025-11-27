"""
ARKALIA ARIA - API Alertes
==========================

API REST pour le système d'alertes automatiques.
"""

from datetime import datetime
from typing import Any

from fastapi import HTTPException, Query

from core import BaseAPI
from core.alerts import AlertType, get_alerts_system

# Créer l'API avec BaseAPI
api = BaseAPI("/api/alerts", ["Alerts"])
router = api.get_router()
logger = api.logger


@router.get("/status")
async def alerts_status() -> dict[str, Any]:
    """Statut du système d'alertes."""
    return {
        "module": "alerts",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "pattern_detection",
            "crisis_prediction",
            "correlation_alerts",
            "health_sync_notifications",
        ],
    }


@router.get("", response_model=dict)
async def get_alerts(
    limit: int = Query(50, ge=1, le=200, description="Nombre d'alertes à retourner"),
    offset: int = Query(0, ge=0, description="Offset pour pagination"),
    unread_only: bool = Query(False, description="Uniquement les non lues"),
    alert_type: str | None = Query(None, description="Filtrer par type"),
) -> dict[str, Any]:
    """
    Récupère les alertes avec pagination.

    Args:
        limit: Nombre d'alertes à retourner
        offset: Offset pour pagination
        unread_only: Uniquement les non lues
        alert_type: Type d'alerte (optionnel)

    Returns:
        Dict avec les alertes et métadonnées
    """
    try:
        alerts_system = get_alerts_system()
        alert_type_enum = None
        if alert_type:
            try:
                alert_type_enum = AlertType(alert_type)
            except ValueError as e:
                raise HTTPException(
                    status_code=400, detail=f"Type d'alerte invalide: {alert_type}"
                ) from e

        result = alerts_system.get_alerts(
            limit=limit,
            offset=offset,
            unread_only=unread_only,
            alert_type=alert_type_enum,
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur récupération alertes: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.post("/check")
async def check_alerts(days_back: int = 30) -> dict[str, Any]:
    """
    Vérifie toutes les alertes et en crée de nouvelles si nécessaire.

    Args:
        days_back: Nombre de jours à analyser

    Returns:
        Résumé des alertes créées
    """
    try:
        alerts_system = get_alerts_system()
        result = alerts_system.check_all(days_back=days_back)
        logger.info(f"✅ Vérification alertes: {result['total']} nouvelles alertes")
        return result
    except Exception as e:
        logger.error(f"❌ Erreur vérification alertes: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.post("/{alert_id}/read")
async def mark_alert_as_read(alert_id: int) -> dict[str, Any]:
    """
    Marque une alerte comme lue.

    Args:
        alert_id: ID de l'alerte

    Returns:
        Confirmation
    """
    try:
        alerts_system = get_alerts_system()
        success = alerts_system.mark_as_read(alert_id)
        if not success:
            raise HTTPException(status_code=404, detail="Alerte non trouvée")
        return {"message": "Alerte marquée comme lue", "alert_id": alert_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur marquage alerte: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.post("/read-all")
async def mark_all_alerts_as_read() -> dict[str, Any]:
    """
    Marque toutes les alertes comme lues.

    Returns:
        Nombre d'alertes marquées
    """
    try:
        alerts_system = get_alerts_system()
        count = alerts_system.mark_all_as_read()
        return {"message": "Toutes les alertes marquées comme lues", "count": count}
    except Exception as e:
        logger.error(f"❌ Erreur marquage toutes alertes: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e


@router.get("/unread/count")
async def get_unread_count() -> dict[str, Any]:
    """
    Retourne le nombre d'alertes non lues.

    Returns:
        Nombre d'alertes non lues
    """
    try:
        alerts_system = get_alerts_system()
        result = alerts_system.get_alerts(limit=1, offset=0, unread_only=True)
        return {"unread_count": result["total"]}
    except Exception as e:
        logger.error(f"❌ Erreur comptage alertes non lues: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}") from e
