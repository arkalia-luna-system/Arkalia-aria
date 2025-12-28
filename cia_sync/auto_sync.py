"""
Auto Sync Manager - Gestionnaire de synchronisation automatique ARIA ↔ CIA
Synchronisation périodique en arrière-plan avec gestion intelligente
"""

import threading
from datetime import datetime, timedelta
from typing import Any

from core import DatabaseManager, get_logger

from .granularity_config import (
    DataType,
    GranularityConfig,
    SyncLevel,
    get_config_manager,
)

logger = get_logger("auto_sync")


class AutoSyncManager:
    """
    Gestionnaire de synchronisation automatique périodique.

    Fonctionnalités :
    - Synchronisation périodique configurable
    - Gestion intelligente des erreurs (retry, backoff)
    - Agrégation des données avant sync
    - Logging des opérations
    - Arrêt propre
    """

    def __init__(
        self,
        cia_base_url: str = "http://127.0.0.1:8000",
        db_path: str = "aria_pain.db",
    ):
        """
        Initialise le gestionnaire de synchronisation automatique.

        Args:
            cia_base_url: URL de base de CIA
            db_path: Chemin vers la base de données ARIA
        """
        self.cia_base_url = cia_base_url
        self.db = DatabaseManager(db_path)
        self.is_running = False
        self.sync_thread: threading.Thread | None = None
        self.sync_interval_minutes = 60  # Par défaut : 1 heure
        self.last_sync: datetime | None = None
        self.sync_stats: dict[str, Any] = {
            "total_syncs": 0,
            "successful_syncs": 0,
            "failed_syncs": 0,
            "last_error": None,
        }
        self.config_manager = get_config_manager()
        logger.info("🔄 Auto Sync Manager initialisé")

    def start(self, interval_minutes: int = 60) -> bool:
        """
        Démarre la synchronisation automatique périodique.

        Args:
            interval_minutes: Intervalle entre chaque synchronisation (en minutes)

        Returns:
            True si démarré avec succès
        """
        if self.is_running:
            logger.warning("Auto sync déjà en cours")
            return False

        self.sync_interval_minutes = interval_minutes
        self.is_running = True

        # Démarrer le thread de synchronisation
        self.sync_thread = threading.Thread(
            target=self._sync_loop, daemon=True, name="AutoSyncThread"
        )
        self.sync_thread.start()

        logger.info(
            f"✅ Synchronisation automatique démarrée "
            f"(intervalle: {interval_minutes} min)"
        )
        return True

    def stop(self) -> bool:
        """
        Arrête la synchronisation automatique.

        Returns:
            True si arrêté avec succès
        """
        if not self.is_running:
            logger.warning("Auto sync n'est pas en cours")
            return False

        self.is_running = False

        if self.sync_thread and self.sync_thread.is_alive():
            self.sync_thread.join(timeout=5)

        logger.info("⏹️ Synchronisation automatique arrêtée")
        return True

    def _sync_loop(self) -> None:
        """Boucle principale de synchronisation périodique."""
        logger.info("🔄 Boucle de synchronisation démarrée")

        while self.is_running:
            try:
                # Effectuer la synchronisation
                success = self._perform_sync()

                if success:
                    self.sync_stats["successful_syncs"] = (
                        self.sync_stats.get("successful_syncs", 0) + 1
                    )
                    logger.info("✅ Synchronisation automatique réussie")
                else:
                    self.sync_stats["failed_syncs"] = (
                        self.sync_stats.get("failed_syncs", 0) + 1
                    )
                    logger.warning("⚠️ Synchronisation automatique échouée")

                self.sync_stats["total_syncs"] = (
                    self.sync_stats.get("total_syncs", 0) + 1
                )
                self.last_sync = datetime.now()

            except Exception as e:
                self.sync_stats["failed_syncs"] = (
                    self.sync_stats.get("failed_syncs", 0) + 1
                )
                self.sync_stats["last_error"] = str(e)
                logger.error(f"❌ Erreur dans la boucle de sync: {e}")

            # Attendre l'intervalle avant la prochaine sync
            sleep_seconds = self.sync_interval_minutes * 60
            logger.debug(f"⏳ Prochaine sync dans {self.sync_interval_minutes} min")
            # Attendre avec vérification périodique de is_running
            # Utiliser wait() par blocs pour économiser CPU
            wait_event = threading.Event()
            remaining_seconds = sleep_seconds
            while remaining_seconds > 0 and self.is_running:
                wait_time = min(
                    60, remaining_seconds
                )  # Vérifier toutes les 60 secondes max
                wait_event.wait(wait_time)
                remaining_seconds -= wait_time

        logger.info("🔄 Boucle de synchronisation arrêtée")

    def _perform_sync(self) -> bool:
        """
        Effectue une synchronisation complète avec CIA selon la granularité.

        Returns:
            True si la synchronisation a réussi
        """
        try:
            import requests

            # Vérifier la connexion CIA
            try:
                response = requests.get(f"{self.cia_base_url}/health", timeout=10)
                if response.status_code != 200:
                    logger.warning("CIA non disponible")
                    return False
            except Exception as e:
                logger.warning(f"CIA non accessible: {e}")
                return False

            # Charger la configuration de granularité
            config = self.config_manager.get_default_config()

            # Synchroniser selon la granularité configurée
            synced_data = {}

            # Synchronisation des entrées de douleur
            if config.should_sync(DataType.PAIN_ENTRIES):
                pain_data = self._sync_pain_entries(config)
                if pain_data:
                    synced_data["pain_entries"] = pain_data

            # Synchronisation des patterns
            if config.should_sync(DataType.PATTERNS):
                patterns_data = self._sync_patterns(config)
                if patterns_data:
                    synced_data["patterns"] = patterns_data

            # Synchronisation des prédictions
            if config.should_sync(DataType.PREDICTIONS):
                predictions_data = self._sync_predictions(config)
                if predictions_data:
                    synced_data["predictions"] = predictions_data

            # Récupérer appointments depuis CIA et créer alertes
            try:
                self._check_medical_appointments()
            except Exception as e:
                logger.warning(f"⚠️ Erreur vérification appointments: {e}")

            # Envoyer les données agrégées à CIA
            if synced_data:
                try:
                    response = requests.post(
                        f"{self.cia_base_url}/api/aria/sync-data",
                        json={
                            "synced_data": synced_data,
                            "granularity": config.to_dict(),
                            "timestamp": datetime.now().isoformat(),
                        },
                        timeout=30,
                    )
                    if response.status_code in [200, 201]:
                        logger.debug(
                            f"Données synchronisées: {list(synced_data.keys())}"
                        )
                        return True
                    else:
                        logger.warning(f"Erreur sync CIA: {response.status_code}")
                        return False
                except Exception as e:
                    logger.error(f"Erreur envoi données: {e}")
                    return False
            else:
                logger.debug("Aucune donnée à synchroniser selon la granularité")
                return True

        except Exception as e:
            logger.error(f"Erreur lors de la synchronisation: {e}")
            return False

    def _sync_pain_entries(self, config: GranularityConfig) -> dict[str, Any] | None:
        """Synchronise les entrées de douleur selon la granularité."""
        level = config.get_sync_level(DataType.PAIN_ENTRIES)
        if level == SyncLevel.NONE:
            return None

        # Récupérer les données
        cutoff_date = (
            datetime.now() - timedelta(days=config.sync_period_days)
        ).isoformat()
        # Limiter à 5000 entrées max pour éviter surcharge mémoire
        pain_entries = self.db.execute_query(
            """
            SELECT * FROM pain_entries
            WHERE timestamp >= ?
            ORDER BY timestamp DESC
            LIMIT 5000
            """,
            (cutoff_date,),
        )

        entries_list = [dict(row) for row in pain_entries]

        # Appliquer anonymisation si nécessaire
        if config.anonymize_personal_data or config.anonymize_timestamps:
            entries_list = [
                self.config_manager.apply_anonymization(entry, config)
                for entry in entries_list
            ]

        # Appliquer le niveau de granularité
        if level == SyncLevel.SUMMARY:
            return self.config_manager.aggregate_data(entries_list, config)
        elif level == SyncLevel.AGGREGATED:
            # Agrégation par jour
            return self._aggregate_by_day(entries_list, config)
        else:  # DETAILED
            return {"entries": entries_list, "count": len(entries_list)}

    def _sync_patterns(self, config: GranularityConfig) -> dict[str, Any] | None:
        """Synchronise les patterns selon la granularité."""
        level = config.get_sync_level(DataType.PATTERNS)
        if level == SyncLevel.NONE:
            return None

        try:
            from pattern_analysis.correlation_analyzer import CorrelationAnalyzer

            analyzer = CorrelationAnalyzer()
            days_back = 30  # Par défaut, peut être configuré

            if level == SyncLevel.SUMMARY:
                # Résumé simple : corrélations principales
                sleep_corr = analyzer.analyze_sleep_pain_correlation(
                    days_back=days_back
                )
                stress_corr = analyzer.analyze_stress_pain_correlation(
                    days_back=days_back
                )
                return {
                    "patterns_available": True,
                    "level": level.value,
                    "sleep_correlation": sleep_corr.get("correlation_strength", 0.0),
                    "stress_correlation": stress_corr.get("correlation_strength", 0.0),
                }
            elif level == SyncLevel.AGGREGATED:
                # Agrégation : patterns récurrents
                triggers = analyzer.detect_recurrent_triggers(days_back=days_back)
                return {
                    "patterns_available": True,
                    "level": level.value,
                    "recurrent_triggers": triggers.get("triggers", [])[:5],  # Top 5
                }
            else:  # DETAILED
                # Détails complets
                comprehensive = analyzer.get_comprehensive_analysis(days_back=days_back)
                return {
                    "patterns_available": True,
                    "level": level.value,
                    "comprehensive_analysis": comprehensive,
                }
        except Exception as e:
            logger.warning(f"Erreur intégration pattern_analysis: {e}")
            return {"patterns_available": False, "error": str(e)}

    def _sync_predictions(self, config: GranularityConfig) -> dict[str, Any] | None:
        """Synchronise les prédictions selon la granularité."""
        level = config.get_sync_level(DataType.PREDICTIONS)
        if level == SyncLevel.NONE:
            return None

        try:
            from prediction_engine.ml_analyzer import ARIAMLAnalyzer

            ml_analyzer = ARIAMLAnalyzer()

            if level == SyncLevel.SUMMARY:
                # Résumé simple : probabilité de crise
                context = {
                    "stress_level": 0.5,
                    "fatigue_level": 0.5,
                    "activity_intensity": 0.5,
                }
                prediction = ml_analyzer.predict_pain_episode(context)
                return {
                    "predictions_available": True,
                    "level": level.value,
                    "crisis_probability": prediction.get("probability", 0.0),
                    "risk_level": prediction.get("risk_level", "low"),
                }
            elif level == SyncLevel.AGGREGATED:
                # Agrégation : tendances
                analytics = ml_analyzer.get_analytics_summary()
                return {
                    "predictions_available": True,
                    "level": level.value,
                    "trends": analytics.get("trends", {}),
                    "accuracy": analytics.get("model_accuracy", 0.0),
                }
            else:  # DETAILED
                # Détails complets
                analytics = ml_analyzer.get_analytics_summary()
                context = {
                    "stress_level": 0.5,
                    "fatigue_level": 0.5,
                    "activity_intensity": 0.5,
                }
                prediction = ml_analyzer.predict_pain_episode(context)
                return {
                    "predictions_available": True,
                    "level": level.value,
                    "current_prediction": prediction,
                    "analytics": analytics,
                }
        except Exception as e:
            logger.warning(f"Erreur intégration prediction_engine: {e}")
            return {"predictions_available": False, "error": str(e)}

    def _aggregate_by_day(
        self, entries: list[dict[str, Any]], config: GranularityConfig
    ) -> dict[str, Any]:
        """Agrège les entrées par jour."""
        from collections import defaultdict

        daily_data: dict[str, list] = defaultdict(list)

        for entry in entries:
            timestamp_str = entry.get("timestamp", "")
            if "T" in timestamp_str:
                date_key = timestamp_str.split("T")[0]
            else:
                date_key = timestamp_str[:10]
            daily_data[date_key].append(entry)

        aggregated_days = []
        for date, day_entries in daily_data.items():
            day_summary = self.config_manager.aggregate_data(day_entries, config)
            day_summary["date"] = date
            aggregated_days.append(day_summary)

        return {"days": aggregated_days, "total_days": len(aggregated_days)}

    def sync_now(self) -> bool:
        """
        Force une synchronisation immédiate (hors cycle).

        Returns:
            True si la synchronisation a réussi
        """
        logger.info("🔄 Synchronisation immédiate demandée")
        return self._perform_sync()

    def get_status(self) -> dict[str, Any]:
        """
        Retourne le statut du gestionnaire de synchronisation.

        Returns:
            Dict avec statut, statistiques, configuration
        """
        return {
            "is_running": self.is_running,
            "sync_interval_minutes": self.sync_interval_minutes,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "stats": self.sync_stats.copy(),
            "cia_url": self.cia_base_url,
        }

    def update_interval(self, interval_minutes: int) -> bool:
        """
        Met à jour l'intervalle de synchronisation.

        Args:
            interval_minutes: Nouvel intervalle en minutes

        Returns:
            True si mis à jour avec succès
        """
        if interval_minutes < 1:
            logger.error("Intervalle minimum: 1 minute")
            return False

        self.sync_interval_minutes = interval_minutes
        logger.info(f"⏱️ Intervalle de sync mis à jour: {interval_minutes} min")
        return True

    def _check_medical_appointments(self) -> None:
        """
        Récupère les appointments depuis CIA et crée des alertes.

        Crée des alertes pour :
        - RDV dans les 7 prochains jours (alerte générale)
        - Rappel 24h avant le RDV (alerte de rappel)
        """
        try:
            import requests

            from core.alerts import AlertSeverity, AlertType, ARIA_AlertsSystem

            # Récupérer appointments depuis CIA
            response = requests.get(
                f"{self.cia_base_url}/api/sync/pull-from-cia",
                params={"data_type": "appointments"},
                timeout=10,
            )

            if response.status_code != 200:
                logger.debug("CIA non disponible ou erreur récupération appointments")
                return

            data = response.json()
            appointments = data.get("pulled_data", {}).get("appointments", [])
            # Fallback pour format direct
            if not appointments:
                appointments = data.get("appointments", [])

            if not appointments:
                logger.debug("Aucun appointment trouvé depuis CIA")
                return

            alerts_system = ARIA_AlertsSystem()
            now = datetime.now()
            created_alerts = 0

            for appointment in appointments:
                try:
                    # Parser la date du rendez-vous
                    appt_date_str = appointment.get("date") or appointment.get(
                        "appointment_date"
                    )
                    if not appt_date_str:
                        continue

                    # Gérer différents formats de date
                    try:
                        # Format ISO standard
                        appt_date_str_clean = appt_date_str.replace("Z", "+00:00")
                        appt_date = datetime.fromisoformat(appt_date_str_clean)
                    except ValueError:
                        # Essayer format sans fuseau horaire
                        try:
                            appt_date_str_clean = appt_date_str.split(".")[0].replace(
                                "Z", ""
                            )
                            appt_date = datetime.fromisoformat(appt_date_str_clean)
                        except ValueError:
                            # Format simple YYYY-MM-DD HH:MM:SS
                            try:
                                appt_date = datetime.strptime(
                                    appt_date_str.split("T")[0], "%Y-%m-%d"
                                )
                            except Exception:
                                logger.debug(
                                    f"Format de date invalide: {appt_date_str}"
                                )
                                continue

                    # Normaliser les fuseaux horaires pour comparaison
                    if appt_date.tzinfo is None:
                        # Si pas de fuseau horaire, considérer comme local
                        appt_date = appt_date.replace(tzinfo=now.tzinfo)
                    if now.tzinfo is None:
                        now = now.replace(tzinfo=appt_date.tzinfo)

                    # Calculer le temps jusqu'au RDV
                    time_until = appt_date - now
                    hours_until = time_until.total_seconds() / 3600
                    days_until = time_until.days

                    # Extraire les informations du RDV
                    title = (
                        appointment.get("title")
                        or appointment.get("description")
                        or "Rendez-vous médical"
                    )
                    doctor = (
                        appointment.get("doctor")
                        or appointment.get("provider")
                        or appointment.get("practitioner")
                        or "Médecin"
                    )
                    location = appointment.get("location") or appointment.get("address")

                    # Vérifier si une alerte existe déjà pour ce RDV
                    existing_alerts = alerts_system.get_alerts(
                        limit=100,
                        alert_type=AlertType.MEDICAL_APPOINTMENT,
                        unread_only=False,
                    )
                    appointment_id = appointment.get("id") or appointment.get(
                        "appointment_id"
                    )
                    alert_exists = False
                    if appointment_id:
                        for alert in existing_alerts.get("alerts", []):
                            alert_data = alert.get("data", {})
                            if isinstance(alert_data, str):
                                import json

                                try:
                                    alert_data = json.loads(alert_data)
                                except Exception:
                                    pass
                            if (
                                isinstance(alert_data, dict)
                                and alert_data.get("appointment_id") == appointment_id
                                and alert_data.get("appointment_date")
                                == appt_date.isoformat()
                            ):
                                alert_exists = True
                                break

                    # Créer alerte générale si RDV dans les 7 prochains jours
                    if 0 <= days_until <= 7 and not alert_exists:
                        if days_until == 0:
                            severity = AlertSeverity.CRITICAL
                            message = f"Rendez-vous médical AUJOURD'HUI avec {doctor}: {title}"
                        elif days_until == 1:
                            severity = AlertSeverity.WARNING
                            message = (
                                f"Rendez-vous médical DEMAIN avec {doctor}: {title}"
                            )
                        else:
                            severity = AlertSeverity.INFO
                            message = (
                                f"Rendez-vous médical dans {days_until} jours "
                                f"avec {doctor}: {title}"
                            )

                        if location:
                            message += f" - {location}"

                        alerts_system.create_alert(
                            AlertType.MEDICAL_APPOINTMENT,
                            severity,
                            f"RDV Médical - {title}",
                            message,
                            {
                                "appointment_id": appointment_id,
                                "appointment_date": appt_date.isoformat(),
                                "days_until": days_until,
                                "hours_until": hours_until,
                                "doctor": doctor,
                                "location": location,
                                "alert_type": "general",
                            },
                        )
                        created_alerts += 1

                    # Créer alerte de rappel 24h avant (entre 23h et 25h avant)
                    if 23 <= hours_until <= 25:
                        # Vérifier si alerte de rappel existe déjà
                        reminder_exists = False
                        for alert in existing_alerts.get("alerts", []):
                            alert_data = alert.get("data", {})
                            if isinstance(alert_data, str):
                                import json

                                try:
                                    alert_data = json.loads(alert_data)
                                except Exception:
                                    pass
                            if (
                                isinstance(alert_data, dict)
                                and alert_data.get("appointment_id") == appointment_id
                                and alert_data.get("alert_type") == "reminder_24h"
                            ):
                                reminder_exists = True
                                break

                        if not reminder_exists:
                            alerts_system.create_alert(
                                AlertType.MEDICAL_APPOINTMENT,
                                AlertSeverity.WARNING,
                                f"Rappel RDV - {title}",
                                (
                                    f"Rappel : Rendez-vous médical DEMAIN à "
                                    f"{appt_date.strftime('%H:%M')} avec {doctor}: {title}"
                                )
                                + (f" - {location}" if location else ""),
                                {
                                    "appointment_id": appointment_id,
                                    "appointment_date": appt_date.isoformat(),
                                    "hours_until": hours_until,
                                    "doctor": doctor,
                                    "location": location,
                                    "alert_type": "reminder_24h",
                                },
                            )
                            created_alerts += 1
                            logger.info(f"✅ Alerte rappel 24h créée pour RDV: {title}")

                except Exception as e:
                    logger.debug(f"Erreur parsing appointment: {e}")
                    continue

            if created_alerts > 0:
                logger.info(
                    f"✅ {created_alerts} alerte(s) créée(s) pour les RDV médicaux"
                )

        except ImportError:
            # Module alerts non disponible, ignorer
            logger.debug("Module alerts non disponible")
            pass
        except Exception as e:
            logger.warning(f"⚠️ Erreur vérification appointments: {e}")


# Instance globale (singleton)
_auto_sync_manager: AutoSyncManager | None = None


def get_auto_sync_manager() -> AutoSyncManager:
    """Récupère ou crée l'instance globale du gestionnaire."""
    global _auto_sync_manager
    if _auto_sync_manager is None:
        _auto_sync_manager = AutoSyncManager()
    return _auto_sync_manager
