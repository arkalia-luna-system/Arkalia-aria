"""
Pattern Analysis API - Module d'analyse de patterns ARIA
IA locale pour découvrir des corrélations dans les données de santé
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from .correlation_analyzer import CorrelationAnalyzer

router = APIRouter()

# Instance globale de l'analyseur (singleton pattern)
_analyzer: CorrelationAnalyzer | None = None


def get_analyzer() -> CorrelationAnalyzer:
    """Récupère ou crée l'instance de l'analyseur."""
    global _analyzer
    if _analyzer is None:
        _analyzer = CorrelationAnalyzer()
    return _analyzer


@router.get("/status")
async def pattern_analysis_status() -> dict:
    """Statut du module pattern analysis"""
    return {
        "module": "pattern_analysis",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "correlation_detection",
            "temporal_patterns",
            "trigger_analysis",
            "visual_reports",
            "sleep_pain_correlation",
            "stress_pain_correlation",
            "recurrent_triggers",
        ],
    }


@router.get("/patterns/recent")
async def get_recent_patterns(
    days: int = Query(30, ge=1, le=365, description="Nombre de jours à analyser")
) -> dict:
    """
    Analyse des patterns récents.

    Retourne une analyse complète avec :
    - Corrélations sommeil ↔ douleur
    - Corrélations stress ↔ douleur
    - Déclencheurs récurrents
    - Patterns temporels
    """
    try:
        analyzer = get_analyzer()
        analysis = analyzer.get_comprehensive_analysis(days_back=days)
        return analysis
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}"
        ) from e


@router.get("/correlations/sleep-pain")
async def get_sleep_pain_correlation(
    days: int = Query(30, ge=1, le=365, description="Nombre de jours à analyser")
) -> dict:
    """
    Analyse la corrélation entre sommeil et douleur.

    Retourne :
    - Coefficient de corrélation (-1 à 1)
    - Niveau de confiance
    - Patterns détectés
    - Recommandations
    """
    try:
        analyzer = get_analyzer()
        correlation = analyzer.analyze_sleep_pain_correlation(days_back=days)
        return correlation
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}"
        ) from e


@router.get("/correlations/stress-pain")
async def get_stress_pain_correlation(
    days: int = Query(30, ge=1, le=365, description="Nombre de jours à analyser")
) -> dict:
    """
    Analyse la corrélation entre stress et douleur.

    Retourne :
    - Coefficient de corrélation (-1 à 1)
    - Niveau de confiance
    - Patterns détectés
    - Recommandations
    """
    try:
        analyzer = get_analyzer()
        correlation = analyzer.analyze_stress_pain_correlation(days_back=days)
        return correlation
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}"
        ) from e


@router.get("/triggers/recurrent")
async def get_recurrent_triggers(
    days: int = Query(30, ge=1, le=365, description="Nombre de jours à analyser"),
    min_occurrences: int = Query(3, ge=1, description="Nombre minimum d'occurrences"),
) -> dict:
    """
    Détecte les déclencheurs récurrents de douleur.

    Retourne :
    - Déclencheurs physiques récurrents
    - Déclencheurs mentaux récurrents
    - Activités corrélées
    - Patterns temporels (heures, jours de la semaine)
    """
    try:
        analyzer = get_analyzer()
        triggers = analyzer.detect_recurrent_triggers(
            days_back=days, min_occurrences=min_occurrences
        )
        return triggers
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}"
        ) from e


@router.post("/analyze")
async def analyze_patterns(data: dict[str, Any]) -> dict:
    """
    Lance une analyse de patterns sur les données fournies.

    Body attendu :
    {
        "days_back": 30,  # Optionnel, défaut 30
        "analysis_type": "comprehensive"  # "comprehensive", "sleep", "stress", "triggers"
    }
    """
    try:
        analyzer = get_analyzer()
        days_back = data.get("days_back", 30)
        analysis_type = data.get("analysis_type", "comprehensive")

        if analysis_type == "comprehensive":
            result = analyzer.get_comprehensive_analysis(days_back=days_back)
        elif analysis_type == "sleep":
            result = analyzer.analyze_sleep_pain_correlation(days_back=days_back)
        elif analysis_type == "stress":
            result = analyzer.analyze_stress_pain_correlation(days_back=days_back)
        elif analysis_type == "triggers":
            result = analyzer.detect_recurrent_triggers(days_back=days_back)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Type d'analyse non supporté: {analysis_type}",
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}"
        ) from e
