"""
ARKALIA ARIA - Générateur de Rapports Automatiques
==================================================

Génère des rapports périodiques (hebdomadaires/mensuels) automatiquement.
"""

import json
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from core import get_logger

logger = get_logger("health_reports")


class HealthReportGenerator:
    """Générateur de rapports de santé automatiques."""

    def __init__(self, reports_dir: Path | str = "reports") -> None:
        """
        Initialise le générateur de rapports.

        Args:
            reports_dir: Répertoire pour stocker les rapports
        """
        self.reports_dir = Path(reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
        self.is_running = False
        self.report_thread: threading.Thread | None = None

    def start_weekly_reports(self) -> bool:
        """Démarre la génération de rapports hebdomadaires automatiques."""
        if self.is_running:
            return False

        self.is_running = True
        self.report_thread = threading.Thread(
            target=self._weekly_report_loop, daemon=True
        )
        self.report_thread.start()
        logger.info("✅ Génération rapports hebdomadaires démarrée")
        return True

    def stop_weekly_reports(self) -> bool:
        """Arrête la génération de rapports automatiques."""
        if not self.is_running:
            return False

        self.is_running = False
        if self.report_thread and self.report_thread.is_alive():
            self.report_thread.join(timeout=5.0)
        logger.info("⏹️ Génération rapports hebdomadaires arrêtée")
        return True

    def _weekly_report_loop(self) -> None:
        """Boucle pour générer des rapports hebdomadaires."""
        logger.info("🔄 Boucle rapports hebdomadaires démarrée")

        while self.is_running:
            try:
                # Générer rapport hebdomadaire
                self.generate_weekly_report()

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
                logger.error(f"❌ Erreur dans boucle rapports: {e}")

        logger.info("🔄 Boucle rapports hebdomadaires arrêtée")

    def generate_weekly_report(self) -> dict[str, Any]:
        """Génère un rapport hebdomadaire."""
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
                metrics = loop.run_until_complete(
                    sync_manager._generate_unified_metrics(days_back=7)
                )
            finally:
                loop.close()

            # Créer rapport
            report = {
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                    "type": "weekly",
                },
                "summary": {
                    "total_activity_days": len(activity_data),
                    "total_sleep_days": len(sleep_data),
                    "total_stress_days": len(stress_data),
                },
                "metrics": metrics,
                "generated_at": datetime.now().isoformat(),
            }

            # Sauvegarder rapport
            filename = f"weekly_report_{end_date.strftime('%Y%m%d')}.json"
            filepath = self.reports_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, default=str, indent=2)

            logger.info(f"✅ Rapport hebdomadaire généré: {filename}")
            return report

        except Exception as e:
            logger.error(f"❌ Erreur génération rapport hebdomadaire: {e}")
            return {}

    def generate_monthly_report(self) -> dict[str, Any]:
        """Génère un rapport mensuel."""
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
                metrics = loop.run_until_complete(
                    sync_manager._generate_unified_metrics(days_back=30)
                )
            finally:
                loop.close()

            # Créer rapport
            report = {
                "period": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat(),
                    "type": "monthly",
                },
                "summary": {
                    "total_activity_days": len(activity_data),
                    "total_sleep_days": len(sleep_data),
                    "total_stress_days": len(stress_data),
                },
                "metrics": metrics,
                "generated_at": datetime.now().isoformat(),
            }

            # Sauvegarder rapport
            filename = f"monthly_report_{end_date.strftime('%Y%m%d')}.json"
            filepath = self.reports_dir / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report, f, default=str, indent=2)

            logger.info(f"✅ Rapport mensuel généré: {filename}")
            return report

        except Exception as e:
            logger.error(f"❌ Erreur génération rapport mensuel: {e}")
            return {}


# Instance globale (singleton)
_report_generator: HealthReportGenerator | None = None


def get_report_generator() -> HealthReportGenerator:
    """Récupère ou crée l'instance globale du générateur."""
    global _report_generator
    if _report_generator is None:
        _report_generator = HealthReportGenerator()
    return _report_generator
