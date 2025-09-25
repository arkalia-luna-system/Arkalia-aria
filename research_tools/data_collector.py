#!/usr/bin/env python3

"""
ARIA Data Collector - Module de collecte de données pour ARIA
Adapté de Arkalia Metrics Collector pour la recherche médicale
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from core import DatabaseManager
from core.logging import get_logger

logger = get_logger("data_collector")


class ARIADataCollector:
    """Collecteur de données pour ARIA - adapté de Metrics Collector"""

    def __init__(self, db_path: str = "aria_research.db"):
        # Exposer le chemin et s'assurer de la création du fichier
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        # Création du fichier (permet aussi de lever des erreurs sur chemin invalide)
        conn = sqlite3.connect(self.db_path)
        conn.close()

        # Utiliser le gestionnaire de base de données centralisé
        self.db = DatabaseManager(self.db_path)
        self.project_root = Path(".").resolve()
        self._init_database()

        logger.info("📊 ARIA Data Collector initialisé")

    def _init_database(self):
        """Initialise la base de données de recherche"""
        # Table des expérimentations
        self.db.execute_update(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                hypothesis TEXT,
                methodology TEXT,
                status TEXT DEFAULT 'active',
                start_date TEXT DEFAULT CURRENT_TIMESTAMP,
                end_date TEXT,
                results TEXT,
                conclusions TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Table des données collectées
        self.db.execute_update(
            """
            CREATE TABLE IF NOT EXISTS collected_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id INTEGER,
                data_type TEXT NOT NULL,
                data_value REAL,
                data_text TEXT,
                metadata TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (experiment_id) REFERENCES experiments (id)
            )
            """
        )

        # Table des métriques système
        self.db.execute_update(
            """
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                unit TEXT,
                category TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        logger.info("✅ Tables research initialisées")

    def create_experiment(
        self, name: str, description: str, hypothesis: str, methodology: str
    ) -> int:
        """Crée une nouvelle expérimentation"""
        try:
            self.db.execute_update(
                """
                INSERT INTO experiments (name, description, hypothesis, methodology)
                VALUES (?, ?, ?, ?)
                """,
                (name, description, hypothesis, methodology),
            )

            # Récupérer l'ID de l'expérimentation créée
            rows = self.db.execute_query("SELECT last_insert_rowid()")
            experiment_id = rows[0][0] if rows else -1

            logger.info(f"Expérimentation créée: {name} (ID: {experiment_id})")
            return experiment_id

        except Exception as e:
            logger.error(f"Erreur création expérimentation: {e}")
            return -1

    def collect_pain_data(self, experiment_id: int, pain_entry: dict[str, Any]) -> bool:
        """Collecte des données de douleur pour une expérimentation"""
        try:
            # Enregistrer l'intensité
            self.db.execute_update(
                """
                INSERT INTO collected_data
                (experiment_id, data_type, data_value, metadata)
                VALUES (?, ?, ?, ?)
                """,
                (
                    experiment_id,
                    "pain_intensity",
                    pain_entry.get("intensity", 0),
                    json.dumps(pain_entry),
                ),
            )

            # Enregistrer les déclencheurs
            if pain_entry.get("physical_trigger"):
                self.db.execute_update(
                    """
                    INSERT INTO collected_data
                    (experiment_id, data_type, data_text, metadata)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        experiment_id,
                        "physical_trigger",
                        pain_entry["physical_trigger"],
                        json.dumps(pain_entry),
                    ),
                )

            if pain_entry.get("mental_trigger"):
                self.db.execute_update(
                    """
                    INSERT INTO collected_data
                    (experiment_id, data_type, data_text, metadata)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        experiment_id,
                        "mental_trigger",
                        pain_entry["mental_trigger"],
                        json.dumps(pain_entry),
                    ),
                )

            # Enregistrer l'action
            if pain_entry.get("action_taken"):
                self.db.execute_update(
                    """
                    INSERT INTO collected_data
                    (experiment_id, data_type, data_text, metadata)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        experiment_id,
                        "action_taken",
                        pain_entry["action_taken"],
                        json.dumps(pain_entry),
                    ),
                )

            logger.debug(
                f"Données de douleur collectées pour expérimentation {experiment_id}"
            )
            return True

        except Exception as e:
            logger.error(f"Erreur collecte données douleur: {e}")
            return False

    def collect_emotion_data(
        self, experiment_id: int, emotion_data: dict[str, Any]
    ) -> bool:
        """Collecte des données émotionnelles pour une expérimentation"""
        try:
            # Enregistrer l'émotion
            self.db.execute_update(
                """
                INSERT INTO collected_data
                (experiment_id, data_type, data_text, data_value, metadata)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    experiment_id,
                    "emotion",
                    emotion_data.get("emotion", "unknown"),
                    emotion_data.get("intensity", 0.0),
                    json.dumps(emotion_data),
                ),
            )

            # Enregistrer le niveau de stress
            if emotion_data.get("stress_level") is not None:
                self.db.execute_update(
                    """
                    INSERT INTO collected_data
                    (experiment_id, data_type, data_value, metadata)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        experiment_id,
                        "stress_level",
                        emotion_data["stress_level"],
                        json.dumps(emotion_data),
                    ),
                )

            logger.debug(
                f"Données émotionnelles collectées pour expérimentation {experiment_id}"
            )
            return True

        except Exception as e:
            logger.error(f"Erreur collecte données émotionnelles: {e}")
            return False

    def collect_system_metrics(self) -> dict[str, Any]:
        """Collecte les métriques système ARIA"""
        try:
            metrics = {}

            # Métriques de base de données
            metrics.update(self._collect_database_metrics())

            # Métriques de performance
            metrics.update(self._collect_performance_metrics())

            # Métriques d'utilisation
            metrics.update(self._collect_usage_metrics())

            # Sauvegarder les métriques
            self._save_system_metrics(metrics)

            return metrics

        except Exception as e:
            logger.error(f"Erreur collecte métriques système: {e}")
            return {"error": str(e)}

    def _collect_database_metrics(self) -> dict[str, Any]:
        """Collecte les métriques de base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Compter les entrées de douleur
            cursor.execute(
                "SELECT COUNT(*) FROM collected_data WHERE data_type = 'pain_intensity'"
            )
            pain_entries = cursor.fetchone()[0]

            # Compter les expérimentations actives
            cursor.execute("SELECT COUNT(*) FROM experiments WHERE status = 'active'")
            active_experiments = cursor.fetchone()[0]

            # Compter les données émotionnelles
            cursor.execute(
                "SELECT COUNT(*) FROM collected_data WHERE data_type = 'emotion'"
            )
            emotion_entries = cursor.fetchone()[0]

            conn.close()

            return {
                "pain_entries_count": pain_entries,
                "active_experiments_count": active_experiments,
                "emotion_entries_count": emotion_entries,
                "database_size_mb": self._get_database_size(),
            }

        except Exception as e:
            logger.error(f"Erreur métriques base de données: {e}")
            return {}

    def _collect_performance_metrics(self) -> dict[str, Any]:
        """Collecte les métriques de performance"""
        try:
            # Temps de réponse moyen (simulation)
            response_time = 0.15  # 150ms

            # Taux de succès des prédictions (simulation)
            prediction_success_rate = 0.85  # 85%

            # Utilisation mémoire (simulation)
            memory_usage_mb = 45.2

            return {
                "avg_response_time_ms": response_time,
                "prediction_success_rate": prediction_success_rate,
                "memory_usage_mb": memory_usage_mb,
                "uptime_hours": self._get_uptime_hours(),
            }

        except Exception as e:
            logger.error(f"Erreur métriques performance: {e}")
            return {}

    def _collect_usage_metrics(self) -> dict[str, Any]:
        """Collecte les métriques d'utilisation"""
        try:
            # Sessions aujourd'hui
            today = datetime.now().date()
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                    SELECT COUNT(*) FROM collected_data
                WHERE DATE(timestamp) = ?
            """,
                (today.isoformat(),),
            )

            daily_entries = cursor.fetchone()[0]

            # Entrées cette semaine
            week_ago = (datetime.now() - timedelta(days=7)).date()
            cursor.execute(
                """
                    SELECT COUNT(*) FROM collected_data
                WHERE DATE(timestamp) >= ?
            """,
                (week_ago.isoformat(),),
            )

            weekly_entries = cursor.fetchone()[0]

            conn.close()

            return {
                "daily_entries": daily_entries,
                "weekly_entries": weekly_entries,
                "avg_entries_per_day": weekly_entries / 7,
                "most_active_hour": self._get_most_active_hour(),
            }

        except Exception as e:
            logger.error(f"Erreur métriques utilisation: {e}")
            return {}

    def _get_database_size(self) -> float:
        """Calcule la taille de la base de données en MB"""
        try:
            db_path = Path(self.db_path)
            if db_path.exists():
                size_bytes = db_path.stat().st_size
                return round(size_bytes / (1024 * 1024), 2)
            return 0.0
        except Exception:
            return 0.0

    def _get_uptime_hours(self) -> float:
        """Calcule le temps de fonctionnement en heures"""
        try:
            # Simulation basée sur la première entrée
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT MIN(timestamp) FROM collected_data")
            result = cursor.fetchone()[0]

            conn.close()

            if result:
                first_entry = datetime.fromisoformat(result)
                uptime = datetime.now() - first_entry
                return round(uptime.total_seconds() / 3600, 2)

            return 0.0

        except Exception:
            return 0.0

    def _get_most_active_hour(self) -> int:
        """Trouve l'heure la plus active"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT strftime('%H', timestamp) as hour, COUNT(*) as count
                FROM collected_data
                GROUP BY hour
                ORDER BY count DESC
                LIMIT 1
            """
            )

            result = cursor.fetchone()
            conn.close()

            return int(result[0]) if result else 12  # Défaut: midi

        except Exception:
            return 12

    def _save_system_metrics(self, metrics: dict[str, Any]):
        """Sauvegarde les métriques système"""
        try:
            for metric_name, metric_value in metrics.items():
                if isinstance(metric_value, int | float):
                    self.db.execute_update(
                        """
                        INSERT INTO system_metrics (metric_name, metric_value, category)
                        VALUES (?, ?, 'system')
                        """,
                        (metric_name, metric_value),
                    )

        except Exception as e:
            logger.error(f"Erreur sauvegarde métriques: {e}")

    def analyze_experiment(self, experiment_id: int) -> dict[str, Any]:
        """Analyse les résultats d'une expérimentation"""
        try:
            # Récupérer les données de l'expérimentation
            rows = self.db.execute_query(
                """
                SELECT data_type, data_value, data_text, timestamp
                FROM collected_data
                WHERE experiment_id = ?
                ORDER BY timestamp
                """,
                (experiment_id,),
            )

            # Convertir sqlite3.Row en tuples pour mypy
            data = [tuple(r) for r in rows]

            if not data:
                return {
                    "experiment_id": experiment_id,
                    "status": "no_data",
                    "message": "Aucune donnée collectée pour cette expérimentation",
                }

            # Analyser les données
            analysis = self._analyze_data(data)

            # Récupérer les infos de l'expérimentation
            exp_info_rows = self.db.execute_query(
                """
                SELECT name, description, hypothesis, methodology
                FROM experiments
                WHERE id = ?
                """,
                (experiment_id,),
            )

            exp_info = exp_info_rows[0] if exp_info_rows else None

            return {
                "experiment_id": experiment_id,
                "experiment_name": exp_info[0] if exp_info else "Unknown",
                "description": exp_info[1] if exp_info else "",
                "hypothesis": exp_info[2] if exp_info else "",
                "methodology": exp_info[3] if exp_info else "",
                "data_points": len(data),
                "analysis": analysis,
                "status": "completed",
            }

        except Exception as e:
            logger.error(f"Erreur analyse expérimentation: {e}")
            return {"error": str(e)}

    def _analyze_data(self, data: list[tuple]) -> dict[str, Any]:
        """Analyse les données collectées"""
        analysis = {}

        # Séparer par type de données
        pain_data = [d for d in data if d[0] == "pain_intensity"]
        emotion_data = [d for d in data if d[0] == "emotion"]
        trigger_data = [
            d for d in data if d[0] in ["physical_trigger", "mental_trigger"]
        ]

        # Analyse des données de douleur
        if pain_data:
            intensities = [d[1] for d in pain_data if d[1] is not None]
            if intensities:
                analysis["pain_analysis"] = {
                    "avg_intensity": sum(intensities) / len(intensities),
                    "max_intensity": max(intensities),
                    "min_intensity": min(intensities),
                    "total_entries": len(intensities),
                }

        # Analyse des émotions
        if emotion_data:
            emotions = [d[2] for d in emotion_data if d[2]]
            emotion_counts: dict[str, int] = {}
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

            analysis["emotion_analysis"] = {
                "dominant_emotion": (
                    max(emotion_counts.items(), key=lambda x: x[1])[0]
                    if emotion_counts
                    else "unknown"
                ),
                "emotion_distribution": emotion_counts,
                "total_emotions": len(emotions),
            }

        # Analyse des déclencheurs
        if trigger_data:
            triggers = [d[2] for d in trigger_data if d[2]]
            trigger_counts: dict[str, int] = {}
            for trigger in triggers:
                trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1

            analysis["trigger_analysis"] = {
                "most_common_trigger": (
                    max(trigger_counts.items(), key=lambda x: x[1])[0]
                    if trigger_counts
                    else "unknown"
                ),
                "trigger_distribution": trigger_counts,
                "total_triggers": len(triggers),
            }

        return analysis

    def get_research_summary(self) -> dict[str, Any]:
        """Retourne un résumé de la recherche"""
        try:
            # Statistiques générales
            total_experiments = self.db.get_count("experiments")
            active_experiments = self.db.get_count("experiments", "status = 'active'")
            total_data_points = self.db.get_count("collected_data")

            # Métriques système
            system_metrics = self.collect_system_metrics()

            return {
                "total_experiments": total_experiments,
                "active_experiments": active_experiments,
                "total_data_points": total_data_points,
                "system_metrics": system_metrics,
                "research_status": "active" if active_experiments > 0 else "inactive",
                "data_quality": "high" if total_data_points > 100 else "developing",
            }

        except Exception as e:
            logger.error(f"Erreur résumé recherche: {e}")
            return {"error": str(e)}


def main():
    """Test du module ARIA Data Collector"""
    print("🧪 Test du module ARIA Data Collector")
    print("=" * 50)

    # Créer l'instance
    collector = ARIADataCollector()

    # Test création d'expérimentation
    print("\n1️⃣ Test création expérimentation")
    exp_id = collector.create_experiment(
        name="Analyse Patterns Douleur",
        description="Étude des patterns de douleur sur 7 jours",
        hypothesis="La douleur suit des patterns temporels prévisibles",
        methodology="Collecte quotidienne + analyse ML",
    )
    print(f"Expérimentation créée avec ID: {exp_id}")

    # Test collecte de données
    print("\n2️⃣ Test collecte données douleur")
    pain_entry = {
        "intensity": 7,
        "physical_trigger": "stress",
        "mental_trigger": "anxiété",
        "action_taken": "respiration",
        "timestamp": datetime.now().isoformat(),
    }
    collector.collect_pain_data(exp_id, pain_entry)

    # Test collecte données émotionnelles
    print("\n3️⃣ Test collecte données émotionnelles")
    emotion_data = {
        "emotion": "stressed",
        "intensity": 0.8,
        "stress_level": 0.7,
        "timestamp": datetime.now().isoformat(),
    }
    collector.collect_emotion_data(exp_id, emotion_data)

    # Test métriques système
    print("\n4️⃣ Test métriques système")
    metrics = collector.collect_system_metrics()
    print(f"Métriques: {metrics}")

    # Test analyse expérimentation
    print("\n5️⃣ Test analyse expérimentation")
    analysis = collector.analyze_experiment(exp_id)
    print(f"Analyse: {analysis}")

    # Test résumé recherche
    print("\n6️⃣ Test résumé recherche")
    summary = collector.get_research_summary()
    print(f"Résumé: {summary}")

    print("\n✅ Test ARIA Data Collector terminé")


if __name__ == "__main__":
    main()
