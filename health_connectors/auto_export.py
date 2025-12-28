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
    """
    Gestionnaire d'exports automatiques périodiques.

    Supporte :
    - Export hebdomadaire automatique (CSV/PDF)
    - Export mensuel automatique (CSV/PDF)
    - Configuration d'intervalle personnalisé
    - Stockage organisé des exports
    """

    def __init__(
        self,
        export_dir: Path | str = "exports",
        weekly_enabled: bool = True,
        monthly_enabled: bool = True,
        export_formats: list[str] | None = None,
    ) -> None:
        """
        Initialise l'exporteur automatique.

        Args:
            export_dir: Répertoire pour stocker les exports
            weekly_enabled: Activer export hebdomadaire
            monthly_enabled: Activer export mensuel
            export_formats: Formats à exporter (csv, pdf, json). Par défaut: ["csv", "pdf"]
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
        self.weekly_enabled = weekly_enabled
        self.monthly_enabled = monthly_enabled
        self.export_formats = export_formats or ["csv", "pdf"]
        self.is_running = False
        self.weekly_thread: threading.Thread | None = None
        self.monthly_thread: threading.Thread | None = None

    def start_auto_exports(self) -> bool:
        """
        Démarre les exports automatiques (hebdomadaire et mensuel).

        Returns:
            True si démarré avec succès
        """
        if self.is_running:
            logger.warning("Exports automatiques déjà en cours")
            return False

        self.is_running = True
        started = False

        # Démarrer export hebdomadaire
        if self.weekly_enabled:
            self.weekly_thread = threading.Thread(
                target=self._weekly_export_loop, daemon=True, name="WeeklyExportThread"
            )
            self.weekly_thread.start()
            logger.info("✅ Export hebdomadaire automatique démarré")
            started = True

        # Démarrer export mensuel
        if self.monthly_enabled:
            self.monthly_thread = threading.Thread(
                target=self._monthly_export_loop,
                daemon=True,
                name="MonthlyExportThread",
            )
            self.monthly_thread.start()
            logger.info("✅ Export mensuel automatique démarré")
            started = True

        return started

    def stop_auto_exports(self) -> bool:
        """
        Arrête tous les exports automatiques.

        Returns:
            True si arrêté avec succès
        """
        if not self.is_running:
            return False

        self.is_running = False

        # Arrêter export hebdomadaire
        if self.weekly_thread and self.weekly_thread.is_alive():
            self.weekly_thread.join(timeout=5.0)

        # Arrêter export mensuel
        if self.monthly_thread and self.monthly_thread.is_alive():
            self.monthly_thread.join(timeout=5.0)

        logger.info("⏹️ Exports automatiques arrêtés")
        return True

    def start_weekly_export(self) -> bool:
        """Démarre l'export hebdomadaire automatique (méthode legacy)."""
        self.weekly_enabled = True
        return self.start_auto_exports()

    def stop_weekly_export(self) -> bool:
        """Arrête l'export automatique (méthode legacy)."""
        return self.stop_auto_exports()

    def _weekly_export_loop(self) -> None:
        """Boucle pour exporter hebdomadairement."""
        logger.info("🔄 Boucle export hebdomadaire démarrée")

        while self.is_running and self.weekly_enabled:
            try:
                # Exporter dans tous les formats configurés
                for format_type in self.export_formats:
                    try:
                        self.export_weekly_data(format=format_type)
                    except Exception as e:
                        logger.warning(
                            f"⚠️ Erreur export hebdomadaire {format_type}: {e}"
                        )

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
                logger.error(f"❌ Erreur dans boucle export hebdomadaire: {e}")

        logger.info("🔄 Boucle export hebdomadaire arrêtée")

    def _monthly_export_loop(self) -> None:
        """Boucle pour exporter mensuellement."""
        logger.info("🔄 Boucle export mensuel démarrée")

        while self.is_running and self.monthly_enabled:
            try:
                # Exporter dans tous les formats configurés
                for format_type in self.export_formats:
                    try:
                        self.export_monthly_data(format=format_type)
                    except Exception as e:
                        logger.warning(f"⚠️ Erreur export mensuel {format_type}: {e}")

                # Attendre 30 jours
                wait_event = threading.Event()
                wait_seconds = 30 * 24 * 3600  # 30 jours
                remaining_seconds = wait_seconds
                while remaining_seconds > 0 and self.is_running:
                    wait_time = min(
                        3600, remaining_seconds
                    )  # Vérifier toutes les heures
                    wait_event.wait(wait_time)
                    remaining_seconds -= wait_time

            except Exception as e:
                logger.error(f"❌ Erreur dans boucle export mensuel: {e}")

        logger.info("🔄 Boucle export mensuel arrêtée")

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
            elif format == "pdf":
                filename = f"weekly_export_{end_date.strftime('%Y%m%d')}.pdf"
                filepath = self.export_dir / filename
                self._export_to_pdf(export_data, filepath, period_type="hebdomadaire")
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
            elif format == "pdf":
                filename = f"monthly_export_{end_date.strftime('%Y%m%d')}.pdf"
                filepath = self.export_dir / filename
                self._export_to_pdf(export_data, filepath, period_type="mensuel")
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

        with open(filepath, "w", newline="", encoding="utf-8") as f:
            # Export activité
            if data.get("activity"):
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "timestamp",
                        "steps",
                        "heart_rate",
                        "calories",
                        "distance",
                        "source",
                    ],
                )
                writer.writeheader()
                for item in data["activity"]:
                    writer.writerow(
                        {
                            "timestamp": str(item.get("timestamp", "")),
                            "steps": item.get("steps", ""),
                            "heart_rate": item.get("heart_rate_bpm", ""),
                            "calories": item.get("calories_burned", ""),
                            "distance": item.get("distance_meters", ""),
                            "source": item.get("source", ""),
                        }
                    )

            # Export sommeil
            if data.get("sleep"):
                f.write("\n--- SOMMEIL ---\n")
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "sleep_start",
                        "sleep_end",
                        "duration_minutes",
                        "quality_score",
                        "source",
                    ],
                )
                writer.writeheader()
                for item in data["sleep"]:
                    writer.writerow(
                        {
                            "sleep_start": str(item.get("sleep_start", "")),
                            "sleep_end": str(item.get("sleep_end", "")),
                            "duration_minutes": item.get("duration_minutes", ""),
                            "quality_score": item.get("quality_score", ""),
                            "source": item.get("source", ""),
                        }
                    )

            # Export stress
            if data.get("stress"):
                f.write("\n--- STRESS ---\n")
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "timestamp",
                        "stress_level",
                        "heart_rate_variability",
                        "source",
                    ],
                )
                writer.writeheader()
                for item in data["stress"]:
                    writer.writerow(
                        {
                            "timestamp": str(item.get("timestamp", "")),
                            "stress_level": item.get("stress_level", ""),
                            "heart_rate_variability": item.get(
                                "heart_rate_variability", ""
                            ),
                            "source": item.get("source", ""),
                        }
                    )

    def _export_to_pdf(
        self, data: dict[str, Any], filepath: Path, period_type: str = "hebdomadaire"
    ) -> None:
        """
        Exporte les données en PDF (format texte simple).

        Args:
            data: Données à exporter
            filepath: Chemin du fichier PDF
            period_type: Type de période (hebdomadaire/mensuel)
        """
        try:
            period = data.get("period", {})
            start_date = period.get("start", "")
            end_date = period.get("end", "")

            pdf_content = f"""RAPPORT SANTÉ ARKALIA ARIA - {period_type.upper()}
{'=' * 60}
Date d'export: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Période: {start_date} → {end_date}

"""
            # Résumé activité
            activity_data = data.get("activity", [])
            if activity_data:
                total_steps = sum(item.get("steps", 0) for item in activity_data)
                total_calories = sum(
                    item.get("calories_burned", 0) for item in activity_data
                )
                avg_heart_rate = (
                    sum(item.get("heart_rate_bpm", 0) for item in activity_data)
                    / len(activity_data)
                    if activity_data
                    else 0
                )
                pdf_content += f"""
ACTIVITÉ PHYSIQUE
-----------------
Total pas: {total_steps:,.0f}
Total calories: {total_calories:,.0f}
Fréquence cardiaque moyenne: {avg_heart_rate:.0f} bpm
Nombre de mesures: {len(activity_data)}

"""

            # Résumé sommeil
            sleep_data = data.get("sleep", [])
            if sleep_data:
                total_sleep_minutes = sum(
                    item.get("duration_minutes", 0) for item in sleep_data
                )
                avg_sleep_hours = (
                    (total_sleep_minutes / len(sleep_data) / 60) if sleep_data else 0
                )
                avg_quality = (
                    sum(item.get("quality_score", 0) for item in sleep_data)
                    / len(sleep_data)
                    if sleep_data
                    else 0
                )
                pdf_content += f"""
SOMMEIL
-------
Durée moyenne: {avg_sleep_hours:.1f} heures
Qualité moyenne: {avg_quality:.2f}/1.0
Nombre de nuits: {len(sleep_data)}

"""

            # Résumé stress
            stress_data = data.get("stress", [])
            if stress_data:
                avg_stress = (
                    sum(item.get("stress_level", 0) for item in stress_data)
                    / len(stress_data)
                    if stress_data
                    else 0
                )
                pdf_content += f"""
STRESS
------
Niveau moyen: {avg_stress:.1f}/100
Nombre de mesures: {len(stress_data)}

"""

            pdf_content += f"""
---
Généré automatiquement par ARKALIA ARIA
Export {period_type} - {datetime.now().strftime('%d/%m/%Y')}
"""

            # Sauvegarder en fichier texte (simulation PDF)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(pdf_content)

            logger.debug(f"✅ Export PDF généré: {filepath.name}")

        except Exception as e:
            logger.error(f"❌ Erreur export PDF: {e}")
            raise


# Instance globale (singleton)
_auto_exporter: AutoExporter | None = None


def get_auto_exporter() -> AutoExporter:
    """Récupère ou crée l'instance globale de l'exporteur."""
    global _auto_exporter
    if _auto_exporter is None:
        _auto_exporter = AutoExporter()
    return _auto_exporter
