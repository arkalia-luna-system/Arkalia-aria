"""
Auto Sync Manager - Gestionnaire de synchronisation automatique ARIA ↔ CIA
Synchronisation périodique en arrière-plan avec gestion intelligente
"""

import threading
from datetime import datetime, timedelta
from typing import Any

from core import DatabaseManager, get_logger

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
        self.sync_stats = {
            "total_syncs": 0,
            "successful_syncs": 0,
            "failed_syncs": 0,
            "last_error": None,
        }
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
                    self.sync_stats["successful_syncs"] += 1
                    logger.info("✅ Synchronisation automatique réussie")
                else:
                    self.sync_stats["failed_syncs"] += 1
                    logger.warning("⚠️ Synchronisation automatique échouée")

                self.sync_stats["total_syncs"] += 1
                self.last_sync = datetime.now()

            except Exception as e:
                self.sync_stats["failed_syncs"] += 1
                self.sync_stats["last_error"] = str(e)
                logger.error(f"❌ Erreur dans la boucle de sync: {e}")

            # Attendre l'intervalle avant la prochaine sync
            if self.is_running:
                sleep_seconds = self.sync_interval_minutes * 60
                logger.debug(f"⏳ Prochaine sync dans {self.sync_interval_minutes} min")
                for _ in range(sleep_seconds):
                    if not self.is_running:
                        break
                    threading.Event().wait(1)

        logger.info("🔄 Boucle de synchronisation arrêtée")

    def _perform_sync(self) -> bool:
        """
        Effectue une synchronisation complète avec CIA.

        Returns:
            True si la synchronisation a réussi
        """
        try:
            import requests

            # Vérifier la connexion CIA
            try:
                response = requests.get(
                    f"{self.cia_base_url}/health", timeout=10
                )
                if response.status_code != 200:
                    logger.warning("CIA non disponible")
                    return False
            except Exception as e:
                logger.warning(f"CIA non accessible: {e}")
                return False

            # Récupérer les données à synchroniser (dernières 24h)
            cutoff_date = (datetime.now() - timedelta(days=1)).isoformat()
            pain_entries = self.db.execute_query(
                """
                SELECT * FROM pain_entries
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                """,
                (cutoff_date,),
            )

            # Agrégation intelligente : créer un résumé
            summary = self._create_summary(pain_entries)

            # Envoyer le résumé à CIA
            try:
                response = requests.post(
                    f"{self.cia_base_url}/api/aria/sync-summary",
                    json=summary,
                    timeout=30,
                )
                if response.status_code in [200, 201]:
                    logger.debug(f"Résumé synchronisé: {len(pain_entries)} entrées")
                    return True
                else:
                    logger.warning(f"Erreur sync CIA: {response.status_code}")
                    return False
            except Exception as e:
                logger.error(f"Erreur envoi résumé: {e}")
                return False

        except Exception as e:
            logger.error(f"Erreur lors de la synchronisation: {e}")
            return False

    def _create_summary(self, pain_entries: list) -> dict[str, Any]:
        """
        Crée un résumé agrégé des données pour la synchronisation.

        Args:
            pain_entries: Liste des entrées de douleur

        Returns:
            Dict avec résumé agrégé
        """
        if not pain_entries:
            return {
                "period": "24h",
                "total_entries": 0,
                "summary": {},
            }

        # Calculer des statistiques agrégées
        intensities = [
            entry["intensity"] for entry in pain_entries if entry.get("intensity")
        ]
        avg_intensity = sum(intensities) / len(intensities) if intensities else 0
        max_intensity = max(intensities) if intensities else 0
        min_intensity = min(intensities) if intensities else 0

        # Compter les déclencheurs les plus fréquents
        triggers: dict[str, int] = {}
        for entry in pain_entries:
            trigger = entry.get("physical_trigger") or entry.get("mental_trigger")
            if trigger:
                triggers[trigger] = triggers.get(trigger, 0) + 1

        most_common_trigger = (
            max(triggers.items(), key=lambda x: x[1])[0] if triggers else None
        )

        return {
            "period": "24h",
            "total_entries": len(pain_entries),
            "summary": {
                "avg_intensity": round(avg_intensity, 2),
                "max_intensity": max_intensity,
                "min_intensity": min_intensity,
                "most_common_trigger": most_common_trigger,
                "trigger_counts": triggers,
            },
            "timestamp": datetime.now().isoformat(),
        }

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


# Instance globale (singleton)
_auto_sync_manager: AutoSyncManager | None = None


def get_auto_sync_manager() -> AutoSyncManager:
    """Récupère ou crée l'instance globale du gestionnaire."""
    global _auto_sync_manager
    if _auto_sync_manager is None:
        _auto_sync_manager = AutoSyncManager()
    return _auto_sync_manager

