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
from .document_integration import get_document_integration
from .granularity_config import (
    DataType,
    GranularityConfig,
    SyncLevel,
    get_config_manager,
)

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
            "document_integration",
            "medical_reports",
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


@router.get("/granularity/config")
async def get_granularity_config(config_name: str = "default") -> dict:
    """
    Récupère la configuration de granularité.

    Args:
        config_name: Nom de la configuration (défaut: "default")

    Returns:
        Configuration de granularité
    """
    try:
        config_manager = get_config_manager()
        config = config_manager.load_config(config_name)

        if config is None:
            raise HTTPException(
                status_code=404, detail=f"Configuration '{config_name}' non trouvée"
            )

        return {
            "config_name": config_name,
            "config": config.to_dict(),
            "timestamp": datetime.now().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur récupération config: {str(e)}"
        ) from e


@router.post("/granularity/config")
async def save_granularity_config(
    config: dict[str, Any], config_name: str = "default"
) -> dict:
    """
    Sauvegarde une configuration de granularité.

    Body attendu :
    {
        "pain_entries_level": "aggregated",
        "patterns_level": "summary",
        "anonymize_personal_data": false,
        "sync_period_days": 30,
        ...
    }

    Args:
        config: Configuration de granularité
        config_name: Nom de la configuration (défaut: "default")

    Returns:
        Confirmation de sauvegarde
    """
    try:
        config_manager = get_config_manager()
        granularity_config = GranularityConfig.from_dict(config)
        success = config_manager.save_config(granularity_config, config_name)

        if success:
            return {
                "message": f"Configuration '{config_name}' sauvegardée",
                "status": "saved",
                "config_name": config_name,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=500, detail="Erreur lors de la sauvegarde"
            )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur sauvegarde config: {str(e)}"
        ) from e


@router.get("/granularity/configs")
async def list_granularity_configs() -> dict:
    """
    Liste toutes les configurations de granularité disponibles.

    Returns:
        Liste des configurations
    """
    try:
        config_manager = get_config_manager()
        configs = config_manager.list_configs()

        return {
            "configs": configs,
            "total": len(configs),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur liste configs: {str(e)}"
        ) from e


@router.delete("/granularity/config")
async def delete_granularity_config(config_name: str) -> dict:
    """
    Supprime une configuration de granularité.

    Args:
        config_name: Nom de la configuration à supprimer

    Returns:
        Confirmation de suppression
    """
    try:
        if config_name == "default":
            raise HTTPException(
                status_code=400, detail="Impossible de supprimer la config 'default'"
            )

        config_manager = get_config_manager()
        success = config_manager.delete_config(config_name)

        if success:
            return {
                "message": f"Configuration '{config_name}' supprimée",
                "status": "deleted",
                "config_name": config_name,
                "timestamp": datetime.now().isoformat(),
            }
        else:
            raise HTTPException(
                status_code=500, detail="Erreur lors de la suppression"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur suppression config: {str(e)}"
        ) from e


@router.get("/granularity/sync-levels")
async def get_sync_levels() -> dict:
    """
    Retourne les niveaux de synchronisation disponibles.

    Returns:
        Liste des niveaux et types de données
    """
    return {
        "sync_levels": [level.value for level in SyncLevel],
        "data_types": [data_type.value for data_type in DataType],
        "default_config": get_config_manager().get_default_config().to_dict(),
        "timestamp": datetime.now().isoformat(),
    }


@router.post("/documents/generate-report")
async def generate_medical_report(
    period_days: int = 30,
    include_patterns: bool = True,
    include_predictions: bool = True,
    anonymize: bool = False,
) -> dict:
    """
    Génère un rapport médical complet depuis les données ARIA.

    Args:
        period_days: Nombre de jours à inclure (défaut: 30)
        include_patterns: Inclure les patterns détectés (défaut: True)
        include_predictions: Inclure les prédictions (défaut: True)
        anonymize: Anonymiser les données personnelles (défaut: False)

    Returns:
        Rapport médical structuré
    """
    try:
        doc_integration = get_document_integration()
        report = doc_integration.generate_medical_report(
            period_days=period_days,
            include_patterns=include_patterns,
            include_predictions=include_predictions,
            anonymize=anonymize,
        )

        if "error" in report:
            raise HTTPException(
                status_code=500, detail=f"Erreur génération rapport: {report['error']}"
            )

        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur génération rapport: {str(e)}"
        ) from e


@router.post("/documents/sync-report")
async def sync_report_to_cia(
    report: dict[str, Any], document_type: str = "pain_report"
) -> dict:
    """
    Synchronise un rapport médical avec les documents CIA.

    Body attendu :
    {
        "report": {...},  # Rapport généré par generate-report
        "document_type": "pain_report"  # Type de document
    }

    Args:
        report: Rapport médical à synchroniser
        document_type: Type de document (défaut: "pain_report")

    Returns:
        Résultat de la synchronisation
    """
    try:
        doc_integration = get_document_integration()
        result = doc_integration.sync_report_to_cia(report, document_type)

        if not result.get("success"):
            raise HTTPException(
                status_code=500, detail=result.get("error", "Erreur synchronisation")
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur synchronisation rapport: {str(e)}"
        ) from e


@router.post("/documents/consultation-report")
async def prepare_consultation_report(
    days_before: int = 7, anonymize: bool = True
) -> dict:
    """
    Prépare un rapport formaté pour une consultation médicale.

    Args:
        days_before: Nombre de jours avant la consultation (défaut: 7)
        anonymize: Anonymiser les données (défaut: True)

    Returns:
        Rapport formaté pour consultation
    """
    try:
        doc_integration = get_document_integration()
        report = doc_integration.prepare_consultation_report(
            days_before=days_before, anonymize=anonymize
        )

        return report
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur préparation rapport consultation: {str(e)}",
        ) from e


@router.post("/documents/generate-and-sync")
async def generate_and_sync_report(
    period_days: int = 30,
    include_patterns: bool = True,
    include_predictions: bool = True,
    anonymize: bool = False,
    document_type: str = "pain_report",
) -> dict:
    """
    Génère un rapport médical et le synchronise automatiquement avec CIA.

    Args:
        period_days: Nombre de jours à inclure (défaut: 30)
        include_patterns: Inclure les patterns (défaut: True)
        include_predictions: Inclure les prédictions (défaut: True)
        anonymize: Anonymiser les données (défaut: False)
        document_type: Type de document (défaut: "pain_report")

    Returns:
        Résultat de la génération et synchronisation
    """
    try:
        doc_integration = get_document_integration()

        # Générer le rapport
        report = doc_integration.generate_medical_report(
            period_days=period_days,
            include_patterns=include_patterns,
            include_predictions=include_predictions,
            anonymize=anonymize,
        )

        if "error" in report:
            raise HTTPException(
                status_code=500, detail=f"Erreur génération: {report['error']}"
            )

        # Synchroniser avec CIA
        sync_result = doc_integration.sync_report_to_cia(report, document_type)

        return {
            "report_generated": True,
            "report": report,
            "sync_result": sync_result,
            "timestamp": datetime.now().isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur génération et synchronisation: {str(e)}",
        ) from e
