"""
ARKALIA ARIA - Gestionnaire de Synchronisation Santé
===================================================

Gestionnaire central pour orchestrer la synchronisation de tous les connecteurs santé.
Assure la cohérence et l'unification des données entre Samsung Health, Google Fit et iOS Health.
"""

import os
import threading
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

        # Synchronisation automatique
        self.is_running = False
        self.sync_thread: threading.Thread | None = None
        self.last_sync: datetime | None = None

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

            # Créer alertes basées sur données santé après sync
            try:
                self._create_health_alerts(unified_metrics)
            except Exception as e:
                from core import get_logger

                logger = get_logger("health_sync")
                logger.warning(f"⚠️ Erreur création alertes santé après sync: {e}")
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
                "avg_daily_steps": (
                    sum(d.steps or 0 for d in activity_data) / days_back
                    if days_back > 0
                    else 0
                ),
                "data_points": len(activity_data),
            },
            "sleep": {
                "avg_duration_minutes": self._calculate_average_sleep_duration(
                    sleep_data
                ),
                "avg_duration_hours": (
                    (avg_dur_min / 60.0)
                    if (
                        avg_dur_min := self._calculate_average_sleep_duration(
                            sleep_data
                        )
                    )
                    else None
                ),
                "avg_quality_score": self._calculate_average_sleep_quality(sleep_data),
                "total_awakenings": sum(d.awakenings_count or 0 for d in sleep_data),
                "data_points": len(sleep_data),
                "trend": self._calculate_sleep_trend(sleep_data),
            },
            "stress": {
                "avg_stress_level": self._calculate_average_stress_level(stress_data),
                "avg_hrv": self._calculate_average_hrv(stress_data),
                "data_points": len(stress_data),
                "trend": self._calculate_stress_trend(stress_data),
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

    def _calculate_sleep_trend(self, sleep_data: list[SleepData]) -> str | None:
        """
        Calcule la tendance du sommeil (increasing, decreasing, stable).

        Args:
            sleep_data: Liste des données de sommeil

        Returns:
            "increasing", "decreasing", "stable" ou None
        """
        if len(sleep_data) < 7:  # Besoin d'au moins 7 jours pour une tendance
            return None

        # Trier par date (utiliser sleep_start)
        sorted_data = sorted(sleep_data, key=lambda x: x.sleep_start)

        # Diviser en deux périodes
        mid_point = len(sorted_data) // 2
        first_half = sorted_data[:mid_point]
        second_half = sorted_data[mid_point:]

        avg_first = sum(d.duration_minutes for d in first_half) / len(first_half)
        avg_second = sum(d.duration_minutes for d in second_half) / len(second_half)

        # Seuil de 5% pour considérer une tendance
        threshold = avg_first * 0.05
        if avg_second > avg_first + threshold:
            return "increasing"
        elif avg_second < avg_first - threshold:
            return "decreasing"
        else:
            return "stable"

    def _calculate_stress_trend(self, stress_data: list[StressData]) -> str | None:
        """
        Calcule la tendance du stress (increasing, decreasing, stable).

        Args:
            stress_data: Liste des données de stress

        Returns:
            "increasing", "decreasing", "stable" ou None
        """
        if len(stress_data) < 7:  # Besoin d'au moins 7 jours pour une tendance
            return None

        # Trier par date
        sorted_data = sorted(stress_data, key=lambda x: x.timestamp or datetime.min)

        # Diviser en deux périodes
        mid_point = len(sorted_data) // 2
        first_half = sorted_data[:mid_point]
        second_half = sorted_data[mid_point:]

        avg_first = sum(d.stress_level for d in first_half) / len(first_half)
        avg_second = sum(d.stress_level for d in second_half) / len(second_half)

        # Seuil de 5% pour considérer une tendance
        threshold = avg_first * 0.05
        if avg_second > avg_first + threshold:
            return "increasing"
        elif avg_second < avg_first - threshold:
            return "decreasing"
        else:
            return "stable"

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

    def start_auto_sync(self) -> bool:
        """
        Démarre la synchronisation automatique périodique.

        Returns:
            True si le démarrage a réussi, False si déjà en cours
        """
        if not self.config.auto_sync_enabled:
            return False

        if self.is_running:
            return False

        self.is_running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        self.sync_thread.start()
        return True

    def stop_auto_sync(self) -> bool:
        """
        Arrête la synchronisation automatique.

        Returns:
            True si l'arrêt a réussi
        """
        if not self.is_running:
            return False

        self.is_running = False
        if self.sync_thread and self.sync_thread.is_alive():
            self.sync_thread.join(timeout=5.0)
        return True

    def _sync_loop(self) -> None:
        """Boucle principale de synchronisation automatique."""
        from core import get_logger

        logger = get_logger("health_sync")
        logger.info("🔄 Synchronisation santé automatique démarrée")

        while self.is_running:
            try:
                # Vérifier si sync intelligente (seulement nouvelles données)
                if self._should_sync():
                    import asyncio

                    # Exécuter sync asynchrone dans un thread
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(self.sync_all_connectors())
                        self.last_sync = datetime.now()
                        logger.info("✅ Synchronisation santé automatique réussie")

                        # Corrélations automatiques après sync (seulement si activé)
                        # Désactivé par défaut pour éviter surcharge CPU
                        if os.getenv("ARIA_AUTO_CORRELATIONS_ENABLED", "0").lower() in (
                            "1",
                            "true",
                        ):
                            try:
                                self._trigger_correlations()
                            except Exception as e:
                                logger.warning(
                                    f"⚠️ Erreur corrélations automatiques: {e}"
                                )

                        # Créer alertes basées sur données santé
                        try:
                            metrics = loop.run_until_complete(
                                self._generate_unified_metrics(days_back=7)
                            )
                            self._create_health_alerts(metrics)
                        except Exception as e:
                            logger.warning(f"⚠️ Erreur création alertes santé: {e}")

                    finally:
                        loop.close()
                else:
                    logger.debug("⏭️ Pas de nouvelles données, sync ignorée")

            except Exception as e:
                logger.error(f"❌ Erreur dans la boucle de sync santé: {e}")

            # Attendre l'intervalle avant la prochaine sync
            # Utiliser wait() directement au lieu de boucle pour économiser CPU
            wait_event = threading.Event()
            wait_seconds = self.config.sync_interval_hours * 3600
            # Attendre par blocs de 60 secondes pour permettre l'arrêt rapide
            while wait_seconds > 0 and self.is_running:
                wait_time = min(60, wait_seconds)  # Vérifier toutes les 60 secondes max
                wait_event.wait(wait_time)
                wait_seconds -= wait_time

        logger.info("🔄 Synchronisation santé automatique arrêtée")

    def _should_sync(self) -> bool:
        """
        Vérifie si une synchronisation est nécessaire (sync intelligente).

        Returns:
            True si sync nécessaire, False sinon
        """
        if self.last_sync is None:
            return True

        # Sync si dernière sync > intervalle configuré
        time_since_last_sync = datetime.now() - self.last_sync
        return time_since_last_sync >= timedelta(hours=self.config.sync_interval_hours)

    def _trigger_correlations(self) -> None:
        """Déclenche l'analyse de corrélations après sync."""
        try:
            from pattern_analysis.correlation_analyzer import CorrelationAnalyzer

            analyzer = CorrelationAnalyzer()
            # Analyser corrélations avec données récentes
            analyzer.get_comprehensive_analysis(days_back=30)
        except ImportError:
            # Module non disponible, ignorer
            pass
        except Exception:
            # Erreur non critique, ignorer
            pass

    def _create_health_alerts(self, metrics: dict[str, Any]) -> None:
        """
        Crée des alertes basées sur les données de santé synchronisées.

        Vérifie :
        - Sommeil insuffisant (seuil et tendance)
        - Stress élevé (seuil et tendance)
        - Fréquence cardiaque anormale
        - Activité physique insuffisante
        - Qualité de sommeil faible

        Évite les doublons en vérifiant les alertes existantes.
        """
        from core import get_logger

        logger = get_logger("health_sync")
        try:
            from core.alerts import AlertSeverity, AlertType, ARIA_AlertsSystem

            alerts_system = ARIA_AlertsSystem()

            # Récupérer les alertes existantes pour éviter les doublons
            existing_alerts = alerts_system.get_alerts(
                limit=100, alert_type=AlertType.HEALTH_SYNC, unread_only=False
            )
            existing_alert_keys = set()
            for alert in existing_alerts.get("alerts", []):
                alert_data = alert.get("data", {})
                if isinstance(alert_data, str):
                    import json

                    try:
                        alert_data = json.loads(alert_data)
                    except Exception:
                        continue
                if isinstance(alert_data, dict):
                    alert_key = alert_data.get("alert_key")
                    if alert_key:
                        existing_alert_keys.add(alert_key)

            created_count = 0

            # Vérifier sommeil insuffisant
            sleep_metrics = metrics.get("sleep", {})
            sleep_duration_hours = sleep_metrics.get("avg_duration_hours")
            sleep_duration_minutes = sleep_metrics.get("avg_duration_minutes")
            if sleep_duration_hours is None and sleep_duration_minutes:
                sleep_duration_hours = sleep_duration_minutes / 60.0

            if sleep_duration_hours and sleep_duration_hours < 6:
                alert_key = f"sleep_insufficient_{int(sleep_duration_hours)}"
                if alert_key not in existing_alert_keys:
                    alerts_system.create_alert(
                        AlertType.HEALTH_SYNC,
                        AlertSeverity.WARNING,
                        "Sommeil Insuffisant",
                        f"Votre durée moyenne de sommeil est de {sleep_duration_hours:.1f}h, "
                        f"ce qui est inférieur à la recommandation (7-9h).",
                        {
                            "alert_key": alert_key,
                            "sleep_duration_hours": sleep_duration_hours,
                            "recommended_min": 7,
                            "threshold": 6,
                        },
                    )
                    created_count += 1

            # Vérifier qualité de sommeil faible
            sleep_quality = sleep_metrics.get("avg_quality_score")
            if sleep_quality is not None and sleep_quality < 3.0:  # Sur échelle 1-5
                alert_key = f"sleep_quality_low_{int(sleep_quality * 10)}"
                if alert_key not in existing_alert_keys:
                    alerts_system.create_alert(
                        AlertType.HEALTH_SYNC,
                        AlertSeverity.INFO,
                        "Qualité de Sommeil Faible",
                        f"Votre qualité de sommeil moyenne est de {sleep_quality:.1f}/5, "
                        f"ce qui est faible. Essayez d'améliorer votre hygiène de sommeil.",
                        {
                            "alert_key": alert_key,
                            "sleep_quality": sleep_quality,
                            "threshold": 3.0,
                        },
                    )
                    created_count += 1

            # Vérifier stress élevé
            stress_metrics = metrics.get("stress", {})
            stress_level = stress_metrics.get("avg_stress_level")
            if stress_level and stress_level > 70:
                alert_key = f"stress_high_{int(stress_level)}"
                if alert_key not in existing_alert_keys:
                    alerts_system.create_alert(
                        AlertType.HEALTH_SYNC,
                        AlertSeverity.WARNING,
                        "Niveau de Stress Élevé",
                        f"Votre niveau de stress moyen est de {stress_level:.1f}/100, "
                        f"ce qui est élevé. Considérez des techniques de relaxation.",
                        {
                            "alert_key": alert_key,
                            "stress_level": stress_level,
                            "threshold": 70,
                        },
                    )
                    created_count += 1

            # Vérifier fréquence cardiaque anormale
            activity_metrics = metrics.get("activity", {})
            heart_rate = activity_metrics.get("avg_heart_rate")
            if heart_rate:
                if heart_rate > 100:
                    alert_key = f"heart_rate_high_{int(heart_rate)}"
                    if alert_key not in existing_alert_keys:
                        alerts_system.create_alert(
                            AlertType.HEALTH_SYNC,
                            AlertSeverity.WARNING,
                            "Fréquence Cardiaque Élevée",
                            f"Votre fréquence cardiaque moyenne est de {heart_rate:.0f} bpm, "
                            f"ce qui est élevé. Consultez un médecin si cela persiste.",
                            {
                                "alert_key": alert_key,
                                "heart_rate": heart_rate,
                                "threshold": 100,
                            },
                        )
                        created_count += 1
                elif heart_rate < 50:
                    alert_key = f"heart_rate_low_{int(heart_rate)}"
                    if alert_key not in existing_alert_keys:
                        alerts_system.create_alert(
                            AlertType.HEALTH_SYNC,
                            AlertSeverity.INFO,
                            "Fréquence Cardiaque Basse",
                            f"Votre fréquence cardiaque moyenne est de {heart_rate:.0f} bpm. "
                            f"Si vous êtes sportif, c'est normal. Sinon, consultez un médecin.",
                            {
                                "alert_key": alert_key,
                                "heart_rate": heart_rate,
                                "threshold": 50,
                            },
                        )
                        created_count += 1

            # Vérifier tendances (sommeil en baisse, stress en hausse)
            sleep_trend = sleep_metrics.get("trend")
            if (
                sleep_trend == "decreasing"
                and sleep_duration_hours
                and sleep_duration_hours < 7
            ):
                alert_key = "sleep_trend_decreasing"
                if alert_key not in existing_alert_keys:
                    alerts_system.create_alert(
                        AlertType.HEALTH_SYNC,
                        AlertSeverity.WARNING,
                        "Tendance Sommeil en Baisse",
                        f"Votre durée de sommeil est en baisse et actuellement à "
                        f"{sleep_duration_hours:.1f}h. Essayez d'améliorer votre hygiène de sommeil.",
                        {
                            "alert_key": alert_key,
                            "sleep_duration_hours": sleep_duration_hours,
                            "trend": "decreasing",
                        },
                    )
                    created_count += 1

            stress_trend = stress_metrics.get("trend")
            if stress_trend == "increasing" and stress_level and stress_level > 60:
                alert_key = "stress_trend_increasing"
                if alert_key not in existing_alert_keys:
                    alerts_system.create_alert(
                        AlertType.HEALTH_SYNC,
                        AlertSeverity.WARNING,
                        "Tendance Stress en Hausse",
                        f"Votre niveau de stress est en hausse et actuellement à "
                        f"{stress_level:.1f}/100. Prenez du temps pour vous détendre.",
                        {
                            "alert_key": alert_key,
                            "stress_level": stress_level,
                            "trend": "increasing",
                        },
                    )
                    created_count += 1

            # Vérifier activité physique insuffisante
            daily_steps = activity_metrics.get("avg_daily_steps")
            if daily_steps and daily_steps < 5000:
                alert_key = f"activity_low_{int(daily_steps / 1000)}k"
                if alert_key not in existing_alert_keys:
                    alerts_system.create_alert(
                        AlertType.HEALTH_SYNC,
                        AlertSeverity.INFO,
                        "Activité Physique Insuffisante",
                        f"Votre nombre moyen de pas quotidiens est de {daily_steps:.0f}, "
                        f"ce qui est inférieur à la recommandation (10 000 pas/jour).",
                        {
                            "alert_key": alert_key,
                            "daily_steps": daily_steps,
                            "recommended": 10000,
                        },
                    )
                    created_count += 1

            if created_count > 0:
                logger.info(
                    f"✅ {created_count} alerte(s) santé créée(s) après synchronisation"
                )

        except ImportError:
            # Module alerts non disponible, ignorer
            logger.debug("Module alerts non disponible")
            pass
        except Exception as e:
            logger.warning(f"⚠️ Erreur création alertes santé: {e}")
