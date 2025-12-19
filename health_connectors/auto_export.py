"""
ARKALIA ARIA - Export Automatique
=================================

Gère les exports automatiques périodiques (hebdomadaires/mensuels).
"""

import json
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from core import get_logger

logger = get_logger("auto_export")


class AutoExporter:
    """Gestionnaire d'exports automatiques."""

    def __init__(self, export_dir: Path | str = "exports") -> None:
        """
        Initialise l'exporteur automatique.

        Args:
            export_dir: Répertoire pour stocker les exports
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
        self.is_running = False
        self.export_thread: threading.Thread | None = None

    def start_weekly_export(self) -> bool:
        """Démarre l'export hebdomadaire automatique."""
        if self.is_running:
            return False

        self.is_running = True
        self.export_thread = threading.Thread(
            target=self._weekly_export_loop, daemon=True
        )
        self.export_thread.start()
        logger.info("✅ Export hebdomadaire automatique démarré")
        return True

    def stop_weekly_export(self) -> bool:
        """Arrête l'export automatique."""
        if not self.is_running:
            return False

        self.is_running = False
        if self.export_thread and self.export_thread.is_alive():
            self.export_thread.join(timeout=5.0)
        logger.info("⏹️ Export hebdomadaire automatique arrêté")
        return True

    def _weekly_export_loop(self) -> None:
        """Boucle pour exporter hebdomadairement."""
        logger.info("🔄 Boucle export hebdomadaire démarrée")

        while self.is_running:
            try:
                # Exporter données hebdomadaires
                self.export_weekly_data()

                # Attendre 7 jours
                wait_event = threading.Event()
                wait_seconds = 7 * 24 * 3600  # 7 jours
                remaining_seconds = wait_seconds
                while remaining_seconds > 0 and self.is_running:
                    wait_time = min(
                        3600, remaining_seconds
                    )  # Vérifier toutes les heures
                    wait_event.wait(wait_time)
                    remaining_seconds -= wait_time

            except Exception as e:
                logger.error(f"❌ Erreur dans boucle export: {e}")

        logger.info("🔄 Boucle export hebdomadaire arrêtée")

    def export_weekly_data(self, format: str = "json") -> Path | None:
        """Exporte les données de la semaine."""
        try:
            from health_connectors.sync_manager import HealthSyncManager

            sync_manager = HealthSyncManager()
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

            # Récupérer données
            import asyncio

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                activity_data = loop.run_until_complete(
                    sync_manager.get_unified_activity_data(start_date, end_date)
                )
                sleep_data = loop.run_until_complete(
                    sync_manager.get_unified_sleep_data(start_date, end_date)
                )
                stress_data = loop.run_until_complete(
                    sync_manager.get_unified_stress_data(start_date, end_date)
                )
            finally:
                loop.close()

            # Préparer données pour export
            export_data = {
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                },
                "activity": [self._serialize_activity(d) for d in activity_data],
                "sleep": [self._serialize_sleep(d) for d in sleep_data],
                "stress": [self._serialize_stress(d) for d in stress_data],
                "exported_at": datetime.now().isoformat(),
            }

            # Sauvegarder selon format
            if format == "json":
                filename = f"weekly_export_{end_date.strftime('%Y%m%d')}.json"
                filepath = self.export_dir / filename
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, default=str, indent=2)
            elif format == "csv":
                filename = f"weekly_export_{end_date.strftime('%Y%m%d')}.csv"
                filepath = self.export_dir / filename
                self._export_to_csv(export_data, filepath)
            else:
                logger.warning(f"Format non supporté: {format}")
                return None

            logger.info(f"✅ Export hebdomadaire généré: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"❌ Erreur export hebdomadaire: {e}")
            return None

    def export_monthly_data(self, format: str = "json") -> Path | None:
        """Exporte les données du mois."""
        try:
            from health_connectors.sync_manager import HealthSyncManager

            sync_manager = HealthSyncManager()
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)

            # Récupérer données
            import asyncio

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                activity_data = loop.run_until_complete(
                    sync_manager.get_unified_activity_data(start_date, end_date)
                )
                sleep_data = loop.run_until_complete(
                    sync_manager.get_unified_sleep_data(start_date, end_date)
                )
                stress_data = loop.run_until_complete(
                    sync_manager.get_unified_stress_data(start_date, end_date)
                )
            finally:
                loop.close()

            # Préparer données pour export
            export_data = {
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                },
                "activity": [self._serialize_activity(d) for d in activity_data],
                "sleep": [self._serialize_sleep(d) for d in sleep_data],
                "stress": [self._serialize_stress(d) for d in stress_data],
                "exported_at": datetime.now().isoformat(),
            }

            # Sauvegarder selon format
            if format == "json":
                filename = f"monthly_export_{end_date.strftime('%Y%m%d')}.json"
                filepath = self.export_dir / filename
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(export_data, f, default=str, indent=2)
            elif format == "csv":
                filename = f"monthly_export_{end_date.strftime('%Y%m%d')}.csv"
                filepath = self.export_dir / filename
                self._export_to_csv(export_data, filepath)
            else:
                logger.warning(f"Format non supporté: {format}")
                return None

            logger.info(f"✅ Export mensuel généré: {filename}")
            return filepath

        except Exception as e:
            logger.error(f"❌ Erreur export mensuel: {e}")
            return None

    def _serialize_activity(self, data: Any) -> dict[str, Any]:
        """Sérialise une donnée d'activité."""
        if hasattr(data, "dict"):
            return data.dict()
        if hasattr(data, "__dict__"):
            return {k: str(v) for k, v in data.__dict__.items()}
        return {"data": str(data)}

    def _serialize_sleep(self, data: Any) -> dict[str, Any]:
        """Sérialise une donnée de sommeil."""
        if hasattr(data, "dict"):
            return data.dict()
        if hasattr(data, "__dict__"):
            return {k: str(v) for k, v in data.__dict__.items()}
        return {"data": str(data)}

    def _serialize_stress(self, data: Any) -> dict[str, Any]:
        """Sérialise une donnée de stress."""
        if hasattr(data, "dict"):
            return data.dict()
        if hasattr(data, "__dict__"):
            return {k: str(v) for k, v in data.__dict__.items()}
        return {"data": str(data)}

    def _export_to_csv(self, data: dict[str, Any], filepath: Path) -> None:
        """Exporte les données en CSV."""
        import csv

        # Export simplifié - seulement activité pour l'instant
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            if data.get("activity"):
                writer = csv.DictWriter(
                    f, fieldnames=["timestamp", "steps", "heart_rate", "calories"]
                )
                writer.writeheader()
                for item in data["activity"]:
                    writer.writerow(
                        {
                            "timestamp": item.get("timestamp", ""),
                            "steps": item.get("steps", ""),
                            "heart_rate": item.get("heart_rate_bpm", ""),
                            "calories": item.get("calories_burned", ""),
                        }
                    )


# Instance globale (singleton)
_auto_exporter: AutoExporter | None = None


def get_auto_exporter() -> AutoExporter:
    """Récupère ou crée l'instance globale de l'exporteur."""
    global _auto_exporter
    if _auto_exporter is None:
        _auto_exporter = AutoExporter()
    return _auto_exporter
