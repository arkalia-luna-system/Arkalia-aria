"""
Correlation Analyzer - Module d'analyse de corrélations ARIA
Analyse les corrélations entre douleur, sommeil, stress et autres facteurs
"""

import json
import statistics
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from core import DatabaseManager, get_logger

logger = get_logger("correlation_analyzer")


class CorrelationAnalyzer:
    """
    Analyseur de corrélations pour ARIA.

    Détecte les corrélations entre :
    - Douleur et sommeil (durée, qualité)
    - Douleur et stress
    - Douleur et activité physique
    - Déclencheurs récurrents
    """

    def __init__(self, db_path: str = "aria_pain.db", health_data_dir: str = "dacc"):
        """
        Initialise l'analyseur de corrélations.

        Args:
            db_path: Chemin vers la base de données de douleur
            health_data_dir: Répertoire contenant les données santé (JSON)
        """
        self.db = DatabaseManager(db_path)
        self.health_data_dir = Path(health_data_dir)
        logger.info("🔍 Correlation Analyzer initialisé")

    def _load_pain_entries(self, days_back: int = 30) -> list[dict[str, Any]]:
        """Charge les entrées de douleur des N derniers jours."""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            rows = self.db.execute_query(
                """
                SELECT * FROM pain_entries
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                """,
                (cutoff_date,),
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Erreur chargement entrées douleur: {e}")
            return []

    def _load_sleep_data(self, days_back: int = 30) -> list[dict[str, Any]]:
        """Charge les données de sommeil depuis les fichiers JSON."""
        sleep_data = []
        start_date = datetime.now() - timedelta(days=days_back)

        try:
            # Chercher dans les sous-dossiers (samsung_health_data, ios_health_data, etc.)
            for subdir in ["samsung_health_data", "ios_health_data", "google_fit_data"]:
                data_dir = self.health_data_dir / subdir
                if not data_dir.exists():
                    continue

                for json_file in data_dir.glob("sleep_*.json"):
                    try:
                        with open(json_file, encoding="utf-8") as f:
                            data = json.load(f)
                            # Convertir les timestamps string en datetime pour comparaison
                            sleep_start_str = data.get("sleep_start", "")
                            if sleep_start_str:
                                sleep_start = datetime.fromisoformat(
                                    sleep_start_str.replace("Z", "+00:00")
                                )
                                if sleep_start >= start_date:
                                    sleep_data.append(data)
                    except Exception as e:
                        logger.debug(f"Erreur lecture {json_file}: {e}")

            logger.debug(f"Chargé {len(sleep_data)} entrées de sommeil")
            return sleep_data
        except Exception as e:
            logger.error(f"Erreur chargement données sommeil: {e}")
            return []

    def _load_stress_data(self, days_back: int = 30) -> list[dict[str, Any]]:
        """Charge les données de stress depuis les fichiers JSON."""
        stress_data = []
        start_date = datetime.now() - timedelta(days=days_back)

        try:
            for subdir in ["samsung_health_data", "ios_health_data", "google_fit_data"]:
                data_dir = self.health_data_dir / subdir
                if not data_dir.exists():
                    continue

                for json_file in data_dir.glob("stress_*.json"):
                    try:
                        with open(json_file, encoding="utf-8") as f:
                            data = json.load(f)
                            timestamp_str = data.get("timestamp", "")
                            if timestamp_str:
                                timestamp = datetime.fromisoformat(
                                    timestamp_str.replace("Z", "+00:00")
                                )
                                if timestamp >= start_date:
                                    stress_data.append(data)
                    except Exception as e:
                        logger.debug(f"Erreur lecture {json_file}: {e}")

            logger.debug(f"Chargé {len(stress_data)} entrées de stress")
            return stress_data
        except Exception as e:
            logger.error(f"Erreur chargement données stress: {e}")
            return []

    def _parse_datetime(self, dt_str: str) -> datetime | None:
        """Parse une string datetime ISO en datetime object."""
        try:
            # Gérer différents formats
            dt_str = dt_str.replace("Z", "+00:00")
            if "T" in dt_str:
                return datetime.fromisoformat(dt_str)
            return None
        except Exception:
            return None

    def analyze_sleep_pain_correlation(self, days_back: int = 30) -> dict[str, Any]:
        """
        Analyse la corrélation entre sommeil et douleur.

        Returns:
            Dict avec corrélations, patterns et recommandations
        """
        pain_entries = self._load_pain_entries(days_back)
        sleep_data = self._load_sleep_data(days_back)

        if not pain_entries or not sleep_data:
            return {
                "correlation": 0.0,
                "confidence": 0.0,
                "patterns": [],
                "recommendations": [],
                "message": "Données insuffisantes pour analyse",
            }

        # Grouper par jour
        pain_by_date: dict[str, list[dict]] = defaultdict(list)
        sleep_by_date: dict[str, dict] = {}

        for entry in pain_entries:
            date_key = (
                entry["timestamp"].split("T")[0]
                if "T" in entry["timestamp"]
                else entry["timestamp"][:10]
            )
            pain_by_date[date_key].append(entry)

        for sleep in sleep_data:
            sleep_start_str = sleep.get("sleep_start", "")
            if sleep_start_str:
                sleep_start = self._parse_datetime(sleep_start_str)
                if sleep_start:
                    date_key = sleep_start.date().isoformat()
                    sleep_by_date[date_key] = sleep

        # Calculer corrélations
        correlations = []
        patterns = []

        for date_key, day_pain in pain_by_date.items():
            if date_key not in sleep_by_date:
                continue

            sleep = sleep_by_date[date_key]
            avg_pain = statistics.mean([p["intensity"] for p in day_pain])
            sleep_duration = sleep.get("duration_minutes", 0)
            sleep_quality = sleep.get("quality_score", 0.5)

            correlations.append(
                {
                    "date": date_key,
                    "avg_pain": avg_pain,
                    "sleep_duration": sleep_duration,
                    "sleep_quality": sleep_quality,
                }
            )

        if len(correlations) < 3:
            return {
                "correlation": 0.0,
                "confidence": 0.0,
                "patterns": [],
                "recommendations": [],
                "message": "Données insuffisantes (minimum 3 jours)",
            }

        # Calculer corrélation simple (Pearson simplifié)
        pain_values = [c["avg_pain"] for c in correlations]
        sleep_durations = [c["sleep_duration"] for c in correlations]

        if len(pain_values) > 1 and len(sleep_durations) > 1:
            try:
                correlation = statistics.correlation(pain_values, sleep_durations)
            except Exception:
                # Fallback si correlation() n'est pas disponible (Python < 3.10)
                correlation = self._simple_correlation(pain_values, sleep_durations)
        else:
            correlation = 0.0

        # Détecter patterns
        if correlation < -0.3:
            patterns.append(
                {
                    "type": "sleep_duration",
                    "description": (
                        "Douleur plus élevée les jours avec moins de sommeil"
                    ),
                    "strength": abs(correlation),
                }
            )

        # Recommandations
        recommendations = []
        if correlation < -0.4:
            recommendations.append(
                "Manque de sommeil corrélé avec douleur élevée. "
                "Envisager d'améliorer la durée de sommeil."
            )

        return {
            "correlation": round(correlation, 3),
            "confidence": min(len(correlations) / 30.0, 1.0),
            "data_points": len(correlations),
            "patterns": patterns,
            "recommendations": recommendations,
            "correlations": correlations[:10],  # Limiter pour la réponse
        }

    def _simple_correlation(self, x: list[float], y: list[float]) -> float:
        """Calcul simple de corrélation de Pearson."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0

        try:
            mean_x = statistics.mean(x)
            mean_y = statistics.mean(y)

            numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
            sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(len(x)))
            sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(len(y)))

            denominator = (sum_sq_x * sum_sq_y) ** 0.5
            if denominator == 0:
                return 0.0

            return numerator / denominator
        except Exception:
            return 0.0

    def analyze_stress_pain_correlation(self, days_back: int = 30) -> dict[str, Any]:
        """
        Analyse la corrélation entre stress et douleur.

        Returns:
            Dict avec corrélations, patterns et recommandations
        """
        pain_entries = self._load_pain_entries(days_back)
        stress_data = self._load_stress_data(days_back)

        if not pain_entries or not stress_data:
            return {
                "correlation": 0.0,
                "confidence": 0.0,
                "patterns": [],
                "recommendations": [],
                "message": "Données insuffisantes pour analyse",
            }

        # Grouper par jour/heure
        pain_by_hour: dict[str, list[dict]] = defaultdict(list)
        stress_by_hour: dict[str, float] = {}

        for entry in pain_entries:
            timestamp_str = entry["timestamp"]
            if "T" in timestamp_str:
                hour_key = (
                    timestamp_str.split("T")[0] + "T" + timestamp_str.split("T")[1][:2]
                )
            else:
                hour_key = timestamp_str[:13]
            pain_by_hour[hour_key].append(entry)

        for stress in stress_data:
            timestamp_str = stress.get("timestamp", "")
            if timestamp_str:
                timestamp = self._parse_datetime(timestamp_str)
                if timestamp:
                    hour_key = timestamp.strftime("%Y-%m-%dT%H")
                    stress_level = stress.get("stress_level", 0)
                    # Moyenne si plusieurs mesures à la même heure
                    if hour_key in stress_by_hour:
                        stress_by_hour[hour_key] = (
                            stress_by_hour[hour_key] + stress_level
                        ) / 2
                    else:
                        stress_by_hour[hour_key] = stress_level

        # Calculer corrélations
        correlations_data = []

        for hour_key, day_pain in pain_by_hour.items():
            if hour_key not in stress_by_hour:
                continue

            avg_pain = statistics.mean([p["intensity"] for p in day_pain])
            stress_level = stress_by_hour[hour_key]

            correlations_data.append(
                {
                    "hour": hour_key,
                    "avg_pain": avg_pain,
                    "stress_level": stress_level,
                }
            )

        if len(correlations_data) < 3:
            return {
                "correlation": 0.0,
                "confidence": 0.0,
                "patterns": [],
                "recommendations": [],
                "message": "Données insuffisantes (minimum 3 points)",
            }

        pain_values = [c["avg_pain"] for c in correlations_data]
        stress_values = [c["stress_level"] for c in correlations_data]

        correlation = self._simple_correlation(pain_values, stress_values)

        # Détecter patterns
        patterns = []
        if correlation > 0.4:
            patterns.append(
                {
                    "type": "stress_pain",
                    "description": "Stress élevé corrélé avec douleur élevée",
                    "strength": abs(correlation),
                }
            )

        # Recommandations
        recommendations = []
        if correlation > 0.5:
            recommendations.append(
                "Stress fortement corrélé avec douleur. "
                "Envisager des techniques de gestion du stress."
            )

        return {
            "correlation": round(correlation, 3),
            "confidence": min(len(correlations_data) / 30.0, 1.0),
            "data_points": len(correlations_data),
            "patterns": patterns,
            "recommendations": recommendations,
            "correlations": correlations_data[:10],
        }

    def detect_recurrent_triggers(
        self, days_back: int = 30, min_occurrences: int = 3
    ) -> dict[str, Any]:
        """
        Détecte les déclencheurs récurrents de douleur.

        Args:
            days_back: Nombre de jours à analyser
            min_occurrences: Nombre minimum d'occurrences pour considérer un pattern

        Returns:
            Dict avec déclencheurs récurrents et patterns temporels
        """
        pain_entries = self._load_pain_entries(days_back)

        if not pain_entries:
            return {
                "triggers": [],
                "temporal_patterns": [],
                "message": "Aucune donnée disponible",
            }

        # Compter les déclencheurs
        physical_triggers: Counter[str] = Counter()
        mental_triggers: Counter[str] = Counter()
        activities: Counter[str] = Counter()
        hour_patterns: Counter[str] = Counter()
        day_patterns: Counter[str] = Counter()

        for entry in pain_entries:
            if entry.get("physical_trigger"):
                physical_triggers[entry["physical_trigger"]] += 1
            if entry.get("mental_trigger"):
                mental_triggers[entry["mental_trigger"]] += 1
            if entry.get("activity"):
                activities[entry["activity"]] += 1

            # Patterns temporels
            timestamp_str = entry["timestamp"]
            if "T" in timestamp_str:
                hour = timestamp_str.split("T")[1][:2]
                hour_patterns[hour] += 1

                # Jour de la semaine (simplifié)
                try:
                    dt = self._parse_datetime(timestamp_str)
                    if dt:
                        day_name = dt.strftime("%A")
                        day_patterns[day_name] += 1
                except Exception:
                    pass

        # Filtrer les déclencheurs récurrents
        recurrent_physical = [
            {"trigger": t, "count": c}
            for t, c in physical_triggers.most_common(10)
            if c >= min_occurrences
        ]
        recurrent_mental = [
            {"trigger": t, "count": c}
            for t, c in mental_triggers.most_common(10)
            if c >= min_occurrences
        ]
        recurrent_activities = [
            {"activity": a, "count": c}
            for a, c in activities.most_common(10)
            if c >= min_occurrences
        ]

        # Patterns temporels
        top_hours = [{"hour": h, "count": c} for h, c in hour_patterns.most_common(5)]
        top_days = [{"day": d, "count": c} for d, c in day_patterns.most_common(7)]

        return {
            "triggers": {
                "physical": recurrent_physical,
                "mental": recurrent_mental,
                "activities": recurrent_activities,
            },
            "temporal_patterns": {
                "hours": top_hours,
                "days": top_days,
            },
            "total_entries": len(pain_entries),
        }

    def get_comprehensive_analysis(self, days_back: int = 30) -> dict[str, Any]:
        """
        Analyse complète : toutes les corrélations et patterns.

        Returns:
            Dict avec toutes les analyses combinées
        """
        logger.info(f"🔍 Analyse complète sur {days_back} jours")

        sleep_correlation = self.analyze_sleep_pain_correlation(days_back)
        stress_correlation = self.analyze_stress_pain_correlation(days_back)
        triggers = self.detect_recurrent_triggers(days_back)

        return {
            "period_days": days_back,
            "analysis_date": datetime.now().isoformat(),
            "sleep_pain_correlation": sleep_correlation,
            "stress_pain_correlation": stress_correlation,
            "recurrent_triggers": triggers,
            "summary": {
                "sleep_correlation_strength": abs(
                    sleep_correlation.get("correlation", 0.0)
                ),
                "stress_correlation_strength": abs(
                    stress_correlation.get("correlation", 0.0)
                ),
                "total_triggers_found": (
                    len(triggers.get("triggers", {}).get("physical", []))
                    + len(triggers.get("triggers", {}).get("mental", []))
                ),
            },
        }
