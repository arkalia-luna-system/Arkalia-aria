"""
ARKALIA ARIA - Modèles de Données Santé
=======================================

Modèles de données unifiés pour tous les connecteurs santé.
Assure la cohérence des données entre Samsung Health, Google Fit et Apple HealthKit.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ActivityData(BaseModel):
    """Données d'activité physique unifiées."""

    timestamp: datetime = Field(..., description="Horodatage de la mesure")
    steps: int | None = Field(None, ge=0, description="Nombre de pas")
    calories_burned: float | None = Field(None, ge=0, description="Calories brûlées")
    distance_meters: float | None = Field(None, ge=0, description="Distance en mètres")
    active_minutes: int | None = Field(None, ge=0, description="Minutes d'activité")
    heart_rate_bpm: int | None = Field(
        None, ge=30, le=220, description="Fréquence cardiaque"
    )
    source: str = Field(..., description="Source des données (samsung/google/apple)")
    raw_data: dict[str, Any] | None = Field(
        None, description="Données brutes du connecteur"
    )


class SleepData(BaseModel):
    """Données de sommeil unifiées."""

    sleep_start: datetime = Field(..., description="Heure de début de sommeil")
    sleep_end: datetime = Field(..., description="Heure de fin de sommeil")
    duration_minutes: int = Field(..., ge=0, description="Durée du sommeil en minutes")
    quality_score: float | None = Field(
        None, ge=0, le=1, description="Score de qualité (0-1)"
    )
    deep_sleep_minutes: int | None = Field(
        None, ge=0, description="Sommeil profond en minutes"
    )
    light_sleep_minutes: int | None = Field(
        None, ge=0, description="Sommeil léger en minutes"
    )
    rem_sleep_minutes: int | None = Field(
        None, ge=0, description="Sommeil REM en minutes"
    )
    awakenings_count: int | None = Field(None, ge=0, description="Nombre de réveils")
    source: str = Field(..., description="Source des données (samsung/google/apple)")
    raw_data: dict[str, Any] | None = Field(
        None, description="Données brutes du connecteur"
    )


class StressData(BaseModel):
    """Données de stress unifiées."""

    timestamp: datetime = Field(..., description="Horodatage de la mesure")
    stress_level: float = Field(
        ..., ge=0, le=100, description="Niveau de stress (0-100)"
    )
    heart_rate_variability: float | None = Field(
        None, ge=0, description="Variabilité cardiaque"
    )
    resting_heart_rate: int | None = Field(
        None, ge=30, le=220, description="Fréquence cardiaque au repos"
    )
    source: str = Field(..., description="Source des données (samsung/google/apple)")
    raw_data: dict[str, Any] | None = Field(
        None, description="Données brutes du connecteur"
    )


class HealthData(BaseModel):
    """Données de santé générales unifiées."""

    timestamp: datetime = Field(..., description="Horodatage de la mesure")
    weight_kg: float | None = Field(None, ge=0, description="Poids en kg")
    height_cm: float | None = Field(None, ge=0, description="Taille en cm")
    bmi: float | None = Field(None, ge=0, description="Indice de masse corporelle")
    blood_pressure_systolic: int | None = Field(
        None, ge=50, le=300, description="Pression systolique"
    )
    blood_pressure_diastolic: int | None = Field(
        None, ge=30, le=200, description="Pression diastolique"
    )
    blood_glucose: float | None = Field(None, ge=0, description="Glycémie")
    body_temperature: float | None = Field(
        None, ge=30, le=45, description="Température corporelle"
    )
    source: str = Field(..., description="Source des données (samsung/google/apple)")
    raw_data: dict[str, Any] | None = Field(
        None, description="Données brutes du connecteur"
    )


class UnifiedHealthMetrics(BaseModel):
    """Métriques de santé unifiées pour le dashboard."""

    date: datetime = Field(..., description="Date des métriques")
    total_steps: int = Field(0, ge=0, description="Total des pas")
    total_calories: float = Field(0, ge=0, description="Total des calories")
    total_distance: float = Field(0, ge=0, description="Total de la distance")
    avg_heart_rate: float | None = Field(
        None, ge=0, description="Fréquence cardiaque moyenne"
    )
    sleep_duration: int | None = Field(
        None, ge=0, description="Durée du sommeil en minutes"
    )
    sleep_quality: float | None = Field(
        None, ge=0, le=1, description="Qualité du sommeil"
    )
    stress_level: float | None = Field(
        None, ge=0, le=100, description="Niveau de stress"
    )
    sources: list[str] = Field(default_factory=list, description="Sources des données")


class HealthSyncStatus(BaseModel):
    """Statut de synchronisation des connecteurs santé."""

    connector_name: str = Field(..., description="Nom du connecteur")
    is_connected: bool = Field(..., description="Connexion établie")
    last_sync: datetime | None = Field(None, description="Dernière synchronisation")
    sync_errors: list[str] = Field(
        default_factory=list, description="Erreurs de synchronisation"
    )
    data_counts: dict[str, int] = Field(
        default_factory=dict, description="Compteurs de données"
    )
    status: str = Field(..., description="Statut du connecteur")


class HealthConnectorConfig(BaseModel):
    """Configuration des connecteurs santé."""

    samsung_health_enabled: bool = Field(False, description="Activer Samsung Health")
    google_fit_enabled: bool = Field(False, description="Activer Google Fit")
    apple_healthkit_enabled: bool = Field(False, description="Activer Apple HealthKit")
    sync_interval_hours: int = Field(
        6, ge=1, le=24, description="Intervalle de synchronisation en heures"
    )
    max_days_back: int = Field(
        30, ge=1, le=365, description="Nombre maximum de jours à synchroniser"
    )
    auto_sync_enabled: bool = Field(
        True, description="Synchronisation automatique activée"
    )
