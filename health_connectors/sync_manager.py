"""
ARKALIA ARIA - Gestionnaire de Synchronisation Santé
===================================================

Gestionnaire central pour orchestrer la synchronisation de tous les connecteurs santé.
Assure la cohérence et l'unification des données entre Samsung Health, Google Fit et iOS Health.
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .base_connector import BaseHealthConnector
from .config import HealthConnectorConfig
from .data_models import (
    ActivityData,
    HealthSyncStatus,
    SleepData,
    StressData,
)
from .google_fit_connector import GoogleFitConnector
from .ios_health_connector import IOSHealthConnector
from .samsung_health_connector import SamsungHealthConnector


class HealthSyncManager:
    """
    Gestionnaire de synchronisation pour tous les connecteurs santé.

    Orchestre la synchronisation des données entre :
    - Samsung Health (montre)
    - Google Fit (Android S24)
    - iOS Health (iPad)
    """

    def __init__(self, config: HealthConnectorConfig | None = None) -> None:
        """
        Initialise le gestionnaire de synchronisation.

        Args:
            config: Configuration des connecteurs (optionnel)
        """
        self.config = config or HealthConnectorConfig(
            samsung_health_enabled=True,
            google_fit_enabled=True,
            apple_healthkit_enabled=True,
            sync_interval_hours=6,
            max_days_back=30,
            auto_sync_enabled=True,
        )
        self.connectors: dict[str, BaseHealthConnector] = {}
        self.sync_history: list[dict[str, Any]] = []
        self.unified_data_dir = Path("dacc/unified_health_data")
        self.unified_data_dir.mkdir(parents=True, exist_ok=True)

        # Initialiser les connecteurs selon la configuration
        self._initialize_connectors()

    def _initialize_connectors(self) -> None:
        """Initialise les connecteurs selon la configuration."""
        if self.config.samsung_health_enabled:
            self.connectors["samsung_health"] = SamsungHealthConnector()

        if self.config.google_fit_enabled:
            self.connectors["google_fit"] = GoogleFitConnector()

        if self.config.apple_healthkit_enabled:
            self.connectors["ios_health"] = IOSHealthConnector()

    async def connect_all(self) -> dict[str, bool]:
        """
        Établit la connexion avec tous les connecteurs activés.

        Returns:
            Dictionnaire avec le statut de connexion de chaque connecteur
        """
        connection_results = {}

        for name, connector in self.connectors.items():
            try:
                result = await connector.connect()
                connection_results[name] = result
            except Exception as e:
                connection_results[name] = False
                connector.sync_errors.append(f"Erreur de connexion: {str(e)}")

        return connection_results

    async def disconnect_all(self) -> None:
        """Ferme la connexion avec tous les connecteurs."""
        for connector in self.connectors.values():
            try:
                await connector.disconnect()
            except Exception as e:
                connector.sync_errors.append(f"Erreur de déconnexion: {str(e)}")

    async def sync_all_connectors(self, days_back: int | None = None) -> dict[str, Any]:
        """
        Synchronise toutes les données de tous les connecteurs.

        Args:
            days_back: Nombre de jours à synchroniser (utilise la config si None)

        Returns:
            Résumé de la synchronisation complète
        """
        days_back = days_back or self.config.max_days_back
        sync_start = datetime.now()

        sync_summary: dict[str, Any] = {
            "sync_start": sync_start.isoformat(),
            "days_back": days_back,
            "connectors": {},
            "unified_metrics": {},
            "errors": [],
            "status": "success",
        }

        # Synchroniser chaque connecteur
        for name, connector in self.connectors.items():
            try:
                connector_summary = await connector.sync_all_data(days_back)
                sync_summary["connectors"][name] = connector_summary
            except Exception as e:
                error_msg = f"Erreur synchronisation {name}: {str(e)}"
                sync_summary["errors"].append(error_msg)
                connector.sync_errors.append(error_msg)

        # Générer les métriques unifiées
        try:
            unified_metrics = await self._generate_unified_metrics(days_back)
            sync_summary["unified_metrics"] = unified_metrics
        except Exception as e:
            error_msg = f"Erreur génération métriques unifiées: {str(e)}"
            sync_summary["errors"].append(error_msg)

        sync_summary["sync_end"] = datetime.now().isoformat()
        sync_summary["duration_seconds"] = (datetime.now() - sync_start).total_seconds()

        if sync_summary["errors"]:
            sync_summary["status"] = "partial_success"

        # Sauvegarder l'historique de synchronisation
        self.sync_history.append(sync_summary)
        await self._save_sync_history(sync_summary)

        return sync_summary

    async def sync_single_connector(
        self, connector_name: str, days_back: int | None = None
    ) -> dict[str, Any]:
        """
        Synchronise un seul connecteur.

        Args:
            connector_name: Nom du connecteur à synchroniser
            days_back: Nombre de jours à synchroniser

        Returns:
            Résumé de la synchronisation du connecteur
        """
        if connector_name not in self.connectors:
            return {
                "status": "error",
                "error": f"Connecteur {connector_name} non trouvé",
            }

        connector = self.connectors[connector_name]
        days_back = days_back or self.config.max_days_back

        try:
            sync_summary = await connector.sync_all_data(days_back)
            sync_summary["connector_name"] = connector_name
            sync_summary["status"] = "success"

            # Mettre à jour les métriques unifiées
            await self._update_unified_metrics_for_connector(connector_name)

            return sync_summary

        except Exception as e:
            return {
                "status": "error",
                "connector_name": connector_name,
                "error": str(e),
            }

    async def get_all_connectors_status(self) -> dict[str, HealthSyncStatus]:
        """
        Retourne le statut de tous les connecteurs.

        Returns:
            Dictionnaire avec le statut de chaque connecteur
        """
        status_dict = {}

        for name, connector in self.connectors.items():
            connector_status = connector.get_status()
            status_dict[name] = HealthSyncStatus(
                connector_name=name,
                is_connected=connector_status["is_connected"],
                last_sync=connector_status["last_sync"],
                sync_errors=connector_status["sync_errors"],
                data_counts={},  # À implémenter si nécessaire
                status=connector_status["status"],
            )

        return status_dict

    async def get_unified_activity_data(
        self, start_date: datetime, end_date: datetime
    ) -> list[ActivityData]:
        """
        Récupère les données d'activité unifiées de tous les connecteurs.

        Args:
            start_date: Date de début
            end_date: Date de fin

        Returns:
            Liste des données d'activité unifiées
        """
        all_activity_data = []

        for connector in self.connectors.values():
            try:
                connector_data = await connector.get_activity_data(start_date, end_date)
                all_activity_data.extend(connector_data)
            except Exception as e:
                connector.sync_errors.append(f"Erreur données activité: {str(e)}")

        # Trier par timestamp
        all_activity_data.sort(key=lambda x: x.timestamp)

        return all_activity_data

    async def get_unified_sleep_data(
        self, start_date: datetime, end_date: datetime
    ) -> list[SleepData]:
        """
        Récupère les données de sommeil unifiées de tous les connecteurs.

        Args:
            start_date: Date de début
            end_date: Date de fin

        Returns:
            Liste des données de sommeil unifiées
        """
        all_sleep_data = []

        for connector in self.connectors.values():
            try:
                connector_data = await connector.get_sleep_data(start_date, end_date)
                all_sleep_data.extend(connector_data)
            except Exception as e:
                connector.sync_errors.append(f"Erreur données sommeil: {str(e)}")

        # Trier par date de début de sommeil
        all_sleep_data.sort(key=lambda x: x.sleep_start)

        return all_sleep_data

    async def get_unified_stress_data(
        self, start_date: datetime, end_date: datetime
    ) -> list[StressData]:
        """
        Récupère les données de stress unifiées de tous les connecteurs.

        Args:
            start_date: Date de début
            end_date: Date de fin

        Returns:
            Liste des données de stress unifiées
        """
        all_stress_data = []

        for connector in self.connectors.values():
            try:
                connector_data = await connector.get_stress_data(start_date, end_date)
                all_stress_data.extend(connector_data)
            except Exception as e:
                connector.sync_errors.append(f"Erreur données stress: {str(e)}")

        # Trier par timestamp
        all_stress_data.sort(key=lambda x: x.timestamp)

        return all_stress_data

    async def _generate_unified_metrics(self, days_back: int) -> dict[str, Any]:
        """
        Génère les métriques unifiées pour le dashboard.

        Args:
            days_back: Nombre de jours à analyser

        Returns:
            Métriques unifiées
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        # Récupérer toutes les données unifiées
        activity_data = await self.get_unified_activity_data(start_date, end_date)
        sleep_data = await self.get_unified_sleep_data(start_date, end_date)
        stress_data = await self.get_unified_stress_data(start_date, end_date)

        # Calculer les métriques unifiées
        unified_metrics = {
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "days": days_back,
            },
            "activity": {
                "total_steps": sum(d.steps or 0 for d in activity_data),
                "total_calories": sum(d.calories_burned or 0 for d in activity_data),
                "total_distance": sum(d.distance_meters or 0 for d in activity_data),
                "avg_heart_rate": self._calculate_average_heart_rate(activity_data),
                "data_points": len(activity_data),
            },
            "sleep": {
                "avg_duration_minutes": self._calculate_average_sleep_duration(
                    sleep_data
                ),
                "avg_quality_score": self._calculate_average_sleep_quality(sleep_data),
                "total_awakenings": sum(d.awakenings_count or 0 for d in sleep_data),
                "data_points": len(sleep_data),
            },
            "stress": {
                "avg_stress_level": self._calculate_average_stress_level(stress_data),
                "avg_hrv": self._calculate_average_hrv(stress_data),
                "data_points": len(stress_data),
            },
            "sources": list(
                {d.source for d in activity_data + sleep_data + stress_data}
            ),
        }

        # Sauvegarder les métriques unifiées
        await self._save_unified_metrics(unified_metrics)

        return unified_metrics

    async def _update_unified_metrics_for_connector(self, connector_name: str) -> None:
        """Met à jour les métriques unifiées pour un connecteur spécifique."""
        # Implémentation simplifiée - pourrait être optimisée
        await self._generate_unified_metrics(self.config.max_days_back)

    # Méthodes utilitaires pour les calculs
    def _calculate_average_heart_rate(
        self, activity_data: list[ActivityData]
    ) -> float | None:
        """Calcule la fréquence cardiaque moyenne."""
        heart_rates = [
            d.heart_rate_bpm for d in activity_data if d.heart_rate_bpm is not None
        ]
        return round(sum(heart_rates) / len(heart_rates), 1) if heart_rates else None

    def _calculate_average_sleep_duration(
        self, sleep_data: list[SleepData]
    ) -> float | None:
        """Calcule la durée moyenne de sommeil."""
        durations = [d.duration_minutes for d in sleep_data]
        return round(sum(durations) / len(durations), 1) if durations else None

    def _calculate_average_sleep_quality(
        self, sleep_data: list[SleepData]
    ) -> float | None:
        """Calcule la qualité moyenne de sommeil."""
        qualities = [d.quality_score for d in sleep_data if d.quality_score is not None]
        return round(sum(qualities) / len(qualities), 2) if qualities else None

    def _calculate_average_stress_level(
        self, stress_data: list[StressData]
    ) -> float | None:
        """Calcule le niveau de stress moyen."""
        stress_levels = [d.stress_level for d in stress_data]
        return (
            round(sum(stress_levels) / len(stress_levels), 1) if stress_levels else None
        )

    def _calculate_average_hrv(self, stress_data: list[StressData]) -> float | None:
        """Calcule la variabilité cardiaque moyenne."""
        hrv_values = [
            d.heart_rate_variability
            for d in stress_data
            if d.heart_rate_variability is not None
        ]
        return round(sum(hrv_values) / len(hrv_values), 1) if hrv_values else None

    # Méthodes de sauvegarde
    async def _save_sync_history(self, sync_summary: dict[str, Any]) -> None:
        """Sauvegarde l'historique de synchronisation."""
        import json

        file_path = (
            self.unified_data_dir
            / f"sync_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(sync_summary, f, default=str, indent=2)

    async def _save_unified_metrics(self, metrics: dict[str, Any]) -> None:
        """Sauvegarde les métriques unifiées."""
        import json

        file_path = (
            self.unified_data_dir
            / f"unified_metrics_{datetime.now().strftime('%Y%m%d')}.json"
        )
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, default=str, indent=2)
