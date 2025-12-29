"""
Prediction Engine API - Module de prédiction ARIA
Moteur ML local pour anticiper les crises de douleur
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Query

from core.cache import CacheManager
from core.config import Config
from core.logging import get_logger
from pattern_analysis.correlation_analyzer import CorrelationAnalyzer
from prediction_engine.ml_analyzer import ARIAMLAnalyzer

router = APIRouter()
logger = get_logger("prediction_engine")

# Instances globales (singleton pattern)
_ml_analyzer: ARIAMLAnalyzer | None = None
_correlation_analyzer: CorrelationAnalyzer | None = None

# Cache pour les prédictions (TTL 5 minutes)
_config = Config()
_cache = CacheManager(
    default_ttl=_config.get("cache_ttl", 300),
    max_size=_config.get("cache_max_size", 1000),
)


def get_ml_analyzer() -> ARIAMLAnalyzer:
    """Récupère ou crée l'instance de l'analyseur ML."""
    global _ml_analyzer
    if _ml_analyzer is None:
        _ml_analyzer = ARIAMLAnalyzer()
    return _ml_analyzer


def get_correlation_analyzer() -> CorrelationAnalyzer:
    """Récupère ou crée l'instance de l'analyseur de corrélations."""
    global _correlation_analyzer
    if _correlation_analyzer is None:
        _correlation_analyzer = CorrelationAnalyzer()
    return _correlation_analyzer


@router.get("/status")
async def prediction_engine_status() -> dict:
    """Statut du module prediction engine"""
    try:
        ml_analyzer = get_ml_analyzer()
        analytics = ml_analyzer.get_analytics_summary()
        return {
            "module": "prediction_engine",
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "features": [
                "crisis_prediction",
                "early_warnings",
                "personalized_recommendations",
                "ml_learning",
                "pattern_based_prediction",
                "correlation_based_alerts",
            ],
            "analytics": analytics,
        }
    except Exception as e:
        return {
            "module": "prediction_engine",
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
        }


@router.get("/predictions/current")
async def get_current_predictions(
    include_correlations: bool = Query(
        True, description="Inclure les corrélations dans la prédiction"
    )
) -> dict:
    """
    Prédictions actuelles basées sur les données et patterns.

    Utilise :
    - Patterns historiques (ml_analyzer)
    - Corrélations sommeil/stress (correlation_analyzer)
    - Contexte actuel (heure, jour, facteurs)
    """
    try:
        # Vérifier le cache (clé basée sur include_correlations)
        cache_key = f"predictions_current_{include_correlations}"
        cached_result = _cache.get(cache_key)
        if cached_result is not None:
            logger.debug("📦 Prédiction depuis cache")
            return cached_result

        ml_analyzer = get_ml_analyzer()

        # Contexte actuel (simplifié - à améliorer avec données santé réelles)
        context = {
            "stress_level": 0.5,  # Par défaut, à remplacer par données réelles
            "fatigue_level": 0.5,
            "activity_intensity": 0.5,
        }

        # Prédiction basée sur ML
        prediction = ml_analyzer.predict_pain_episode(context)

        # Enrichir avec corrélations si demandé
        if include_correlations:
            try:
                correlation_analyzer = get_correlation_analyzer()
                sleep_corr = correlation_analyzer.analyze_sleep_pain_correlation(
                    days_back=7
                )
                stress_corr = correlation_analyzer.analyze_stress_pain_correlation(
                    days_back=7
                )

                # Ajuster la prédiction selon les corrélations
                correlation_adjustment = 0
                if sleep_corr.get("correlation", 0) < -0.4:
                    # Manque de sommeil → risque élevé
                    correlation_adjustment += 1
                if stress_corr.get("correlation", 0) > 0.4:
                    # Stress élevé → risque élevé
                    correlation_adjustment += 1

                prediction["predicted_intensity"] = min(
                    10,
                    max(0, prediction["predicted_intensity"] + correlation_adjustment),
                )

                prediction["correlation_factors"] = {
                    "sleep_correlation": sleep_corr.get("correlation", 0.0),
                    "stress_correlation": stress_corr.get("correlation", 0.0),
                    "adjustment": correlation_adjustment,
                }
            except Exception as e:
                # Si corrélations échouent, continuer sans
                prediction["correlation_factors"] = {"error": str(e)}

        # Déterminer le niveau de risque
        intensity = prediction.get("predicted_intensity", 0)
        if intensity >= 8:
            risk_level = "high"
        elif intensity >= 6:
            risk_level = "medium"
        elif intensity >= 4:
            risk_level = "low"
        else:
            risk_level = "very_low"

        result = {
            "risk_level": risk_level,
            "predictions": [prediction],
            "confidence": prediction.get("confidence", 0.0),
            "timestamp": datetime.now().isoformat(),
        }

        # Mettre en cache (TTL 5 minutes)
        _cache.set(cache_key, result, ttl=300)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}"
        ) from e


@router.post("/predict")
async def predict_pain_episode(context: dict[str, Any]) -> dict:
    """
    Prédit un épisode de douleur basé sur un contexte fourni.

    Body attendu :
    {
        "stress_level": 0.8,  # 0.0 à 1.0
        "fatigue_level": 0.6,  # 0.0 à 1.0
        "activity_intensity": 0.4,  # 0.0 à 1.0
        "include_correlations": true  # Optionnel
    }
    """
    try:
        ml_analyzer = get_ml_analyzer()
        prediction = ml_analyzer.predict_pain_episode(context)

        # Enrichir avec corrélations si demandé
        if context.get("include_correlations", True):
            try:
                correlation_analyzer = get_correlation_analyzer()
                sleep_corr = correlation_analyzer.analyze_sleep_pain_correlation(
                    days_back=7
                )
                stress_corr = correlation_analyzer.analyze_stress_pain_correlation(
                    days_back=7
                )

                prediction["correlation_factors"] = {
                    "sleep_correlation": sleep_corr.get("correlation", 0.0),
                    "stress_correlation": stress_corr.get("correlation", 0.0),
                }
            except Exception as e:
                # Ignorer les erreurs de calcul de corrélation (données manquantes)
                logger.debug(f"Erreur calcul corrélation prédiction: {e}")

        return prediction
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}"
        ) from e


@router.get("/analytics")
async def get_analytics() -> dict:
    """Retourne les analytics du moteur de prédiction."""
    try:
        # Vérifier le cache
        cache_key = "prediction_analytics"
        cached_result = _cache.get(cache_key)
        if cached_result is not None:
            logger.debug("📦 Analytics depuis cache")
            return cached_result

        ml_analyzer = get_ml_analyzer()
        analytics = ml_analyzer.get_analytics_summary()

        # Mettre en cache (TTL 10 minutes car analytics changent moins souvent)
        _cache.set(cache_key, analytics, ttl=600)
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération analytics: {str(e)}",
        ) from e


@router.post("/train")
async def train_model(data: dict[str, Any]) -> dict:
    """
    Entraîne le modèle ML avec de nouvelles données.

    Note: Pour l'instant, le modèle s'améliore automatiquement
    avec chaque nouvelle entrée de douleur. Cet endpoint permet
    de forcer une réanalyse des patterns.
    """
    try:
        ml_analyzer = get_ml_analyzer()
        days = data.get("days_back", 14)

        # Réanalyser les patterns pour "entraîner"
        patterns = ml_analyzer.analyze_pain_patterns(days=days)

        # Invalider le cache après entraînement
        _cache.invalidate_pattern("prediction_")
        _cache.invalidate_pattern("predictions_")

        return {
            "message": "Analyse des patterns effectuée",
            "model_updated": True,
            "patterns_detected": len(patterns.get("patterns", [])),
            "confidence": patterns.get("confidence", 0.0),
            "analysis_period": f"{days} jours",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'entraînement: {str(e)}"
        ) from e
