#!/usr/bin/env python3

"""
ARIA ML Analyzer - Module d'analyse ML pour ARIA
Adapté de Arkalia Quest Analytics Engine pour la prédiction de douleur
"""

import json
import threading
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from core import DatabaseManager
from core.logging import get_logger

logger = get_logger("ml_analyzer")


class PainEventType(Enum):
    """Types d'événements de douleur"""

    PAIN_ENTRY = "pain_entry"
    PAIN_INTENSITY_CHANGE = "pain_intensity_change"
    TRIGGER_DETECTED = "trigger_detected"
    ACTION_TAKEN = "action_taken"
    EFFECTIVENESS_RECORDED = "effectiveness_recorded"
    PATTERN_DETECTED = "pattern_detected"
    PREDICTION_MADE = "prediction_made"
    EMOTION_ANALYZED = "emotion_analyzed"


@dataclass
class PainEvent:
    """Structure d'un événement de douleur"""

    event_type: PainEventType
    timestamp: datetime
    user_id: str = "default_user"
    intensity: int | None = None
    trigger: str | None = None
    action: str | None = None
    effectiveness: int | None = None
    emotion: str | None = None
    metadata: dict[str, Any] | None = None


class ARIAMLAnalyzer:
    """Analyseur ML pour ARIA - adapté de Quest Analytics Engine"""

    def __init__(self, db_path: str = "aria_pain.db"):
        # Utiliser le gestionnaire de base de données centralisé
        self.db = DatabaseManager(db_path)
        self.lock = threading.Lock()
        self._init_database()

        # Métriques de performance
        self.total_events = 0
        self.prediction_accuracy = 0.0
        self.pattern_detection_rate = 0.0

        logger.info("🧠 ARIA ML Analyzer initialisé")

    def _init_database(self):
        """Initialise la base de données analytics"""
        with self.lock:
            # Table des événements de douleur
            self.db.execute_update(
                """
                CREATE TABLE IF NOT EXISTS pain_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    intensity INTEGER,
                    trigger TEXT,
                    action TEXT,
                    effectiveness INTEGER,
                    emotion TEXT,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Table des patterns détectés
            self.db.execute_update(
                """
                CREATE TABLE IF NOT EXISTS pain_patterns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    description TEXT,
                    triggers TEXT,
                    recommendations TEXT,
                    detected_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # Table des prédictions
            self.db.execute_update(
                """
                CREATE TABLE IF NOT EXISTS pain_predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    predicted_intensity INTEGER NOT NULL,
                    predicted_trigger TEXT,
                    confidence REAL NOT NULL,
                    time_horizon TEXT,
                    actual_outcome TEXT,
                    accuracy REAL,
                    predicted_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            logger.info("✅ Tables ML analytics initialisées")

    def track_pain_event(self, event: PainEvent) -> bool:
        """Enregistre un événement de douleur"""
        try:
            with self.lock:
                self.db.execute_update(
                    """
                    INSERT INTO pain_events
                    (event_type, timestamp, user_id, intensity, trigger, action,
                     effectiveness, emotion, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        event.event_type.value,
                        event.timestamp.isoformat(),
                        event.user_id,
                        event.intensity,
                        event.trigger,
                        event.action,
                        event.effectiveness,
                        event.emotion,
                        json.dumps(event.metadata) if event.metadata else None,
                    ),
                )

                self.total_events += 1
                logger.debug(f"Événement enregistré: {event.event_type.value}")
                return True

        except Exception as e:
            logger.error(f"Erreur enregistrement événement: {e}")
            return False

    def analyze_pain_patterns(self, days: int = 7) -> dict[str, Any]:
        """Analyse les patterns de douleur sur une période"""
        try:
            with self.lock:
                # Récupérer les événements récents
                cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
                events = self.db.execute_query(
                    """
                    SELECT * FROM pain_events
                    WHERE timestamp > ? AND event_type = 'pain_entry'
                    ORDER BY timestamp DESC
                    """,
                    (cutoff_date,),
                )

                if not events:
                    return {
                        "total_events": 0,
                        "patterns": [],
                        "recommendations": ["Pas assez de données récentes"],
                        "confidence": 0.0,
                    }

                # Analyse des patterns
                patterns = self._detect_patterns(events)
                recommendations = self._generate_recommendations(patterns)

                # Sauvegarder les patterns détectés
                for pattern in patterns:
                    self.db.execute_update(
                        """
                        INSERT INTO pain_patterns
                        (pattern_type, confidence, description, triggers, recommendations)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            pattern["type"],
                            pattern["confidence"],
                            pattern["description"],
                            json.dumps(pattern["triggers"]),
                            json.dumps(pattern["recommendations"]),
                        ),
                    )

                return {
                    "total_events": len(events),
                    "patterns": patterns,
                    "recommendations": recommendations,
                    "confidence": self._calculate_confidence(patterns),
                    "analysis_period": f"{days} derniers jours",
                }

        except Exception as e:
            logger.error(f"Erreur analyse patterns: {e}")
            return {"error": str(e)}

    def _detect_patterns(self, events: list[tuple]) -> list[dict[str, Any]]:
        """Détecte les patterns dans les événements"""
        patterns: list[dict[str, Any]] = []

        if len(events) < 3:
            return patterns

        # Pattern 1: Intensité croissante
        intensities = [event[4] for event in events if event[4] is not None]
        if len(intensities) >= 3:
            if all(
                intensities[i] <= intensities[i + 1]
                for i in range(len(intensities) - 1)
            ):
                patterns.append(
                    {
                        "type": "intensity_increase",
                        "confidence": 0.8,
                        "description": "Intensité de douleur en augmentation",
                        "triggers": ["stress", "fatigue", "effort"],
                        "recommendations": [
                            "Surveillance accrue recommandée",
                            "Techniques de relaxation préventives",
                            "Consultation médicale si persistance",
                        ],
                    }
                )

        # Pattern 2: Déclencheurs fréquents
        triggers = [event[5] for event in events if event[5] is not None]
        if triggers:
            trigger_counts: dict[str, int] = {}
            for trigger in triggers:
                trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1

            most_common = max(trigger_counts.items(), key=lambda x: x[1])
            if most_common[1] >= len(triggers) * 0.6:  # 60% des cas
                patterns.append(
                    {
                        "type": "common_trigger",
                        "confidence": 0.9,
                        "description": f"Déclencheur fréquent: {most_common[0]}",
                        "triggers": [most_common[0]],
                        "recommendations": [
                            f"Éviter ou réduire l'exposition à {most_common[0]}",
                            "Techniques de gestion spécifiques",
                            "Plan de prévention personnalisé",
                        ],
                    }
                )

        # Pattern 3: Actions efficaces
        actions = [(event[6], event[7]) for event in events if event[6] and event[7]]
        if actions:
            effective_actions = [action for action, eff in actions if eff and eff >= 7]
            if effective_actions:
                action_counts: dict[str, int] = {}
                for action in effective_actions:
                    action_counts[action] = action_counts.get(action, 0) + 1

                most_effective = max(action_counts.items(), key=lambda x: x[1])
                patterns.append(
                    {
                        "type": "effective_action",
                        "confidence": 0.85,
                        "description": f"Action efficace: {most_effective[0]}",
                        "triggers": ["douleur"],
                        "recommendations": [
                            f"Utiliser {most_effective[0]} en priorité",
                            "Intégrer dans la routine de gestion",
                            "Partager avec le psychologue",
                        ],
                    }
                )

        return patterns

    def _generate_recommendations(self, patterns: list[dict[str, Any]]) -> list[str]:
        """Génère des recommandations basées sur les patterns"""
        recommendations = []

        for pattern in patterns:
            recommendations.extend(pattern.get("recommendations", []))

        # Recommandations générales
        if not patterns:
            recommendations.extend(
                [
                    "Continuer la collecte de données",
                    "Surveillance régulière recommandée",
                    "Consultation psychologique préventive",
                ]
            )

        return list(set(recommendations))  # Supprimer les doublons

    def _calculate_confidence(self, patterns: list[dict[str, Any]]) -> float:
        """Calcule la confiance globale de l'analyse"""
        if not patterns:
            return 0.0

        total_confidence = sum(pattern.get("confidence", 0) for pattern in patterns)
        return total_confidence / len(patterns)

    def predict_pain_episode(self, context: dict[str, Any]) -> dict[str, Any]:
        """Prédit un épisode de douleur basé sur le contexte"""
        try:
            # Analyse du contexte
            time_of_day = datetime.now().hour
            day_of_week = datetime.now().weekday()

            # Facteurs de prédiction
            stress_factor = context.get("stress_level", 0.5)
            fatigue_factor = context.get("fatigue_level", 0.5)
            activity_factor = context.get("activity_intensity", 0.5)

            # Prédiction basée sur les patterns historiques
            historical_patterns = self.analyze_pain_patterns(days=14)

            # Calcul de la prédiction
            predicted_intensity = self._calculate_predicted_intensity(
                stress_factor, fatigue_factor, activity_factor, historical_patterns
            )

            predicted_trigger = self._predict_trigger(context, historical_patterns)
            confidence = self._calculate_prediction_confidence(historical_patterns)

            # Sauvegarder la prédiction
            self._save_prediction(predicted_intensity, predicted_trigger, confidence)

            return {
                "predicted_intensity": predicted_intensity,
                "predicted_trigger": predicted_trigger,
                "confidence": confidence,
                "time_horizon": "2-4 heures",
                "recommendations": self._get_preventive_recommendations(
                    predicted_intensity
                ),
                "context_factors": {
                    "time_of_day": time_of_day,
                    "day_of_week": day_of_week,
                    "stress_factor": stress_factor,
                    "fatigue_factor": fatigue_factor,
                    "activity_factor": activity_factor,
                },
            }

        except Exception as e:
            logger.error(f"Erreur prédiction: {e}")
            return {"error": str(e)}

    def _calculate_predicted_intensity(
        self, stress: float, fatigue: float, activity: float, patterns: dict
    ) -> int:
        """Calcule l'intensité prédite"""
        base_intensity = 3  # Intensité de base

        # Facteurs d'augmentation
        stress_impact = stress * 3
        fatigue_impact = fatigue * 2
        activity_impact = activity * 2

        # Ajustement basé sur les patterns
        pattern_adjustment = 0
        if patterns.get("patterns"):
            avg_confidence = sum(
                p.get("confidence", 0) for p in patterns["patterns"]
            ) / len(patterns["patterns"])
            pattern_adjustment = avg_confidence * 2

        predicted = (
            base_intensity
            + stress_impact
            + fatigue_impact
            + activity_impact
            + pattern_adjustment
        )
        return min(10, max(0, int(predicted)))

    def _predict_trigger(self, context: dict[str, Any], patterns: dict) -> str:
        """Prédit le déclencheur le plus probable"""
        # Déclencheurs basés sur le contexte
        if context.get("stress_level", 0) > 0.7:
            return "stress"
        elif context.get("fatigue_level", 0) > 0.7:
            return "fatigue"
        elif context.get("activity_intensity", 0) > 0.7:
            return "effort"
        else:
            return "marche"

    def _calculate_prediction_confidence(self, patterns: dict) -> float:
        """Calcule la confiance de la prédiction"""
        if patterns.get("total_events", 0) < 5:
            return 0.3  # Faible confiance avec peu de données
        elif patterns.get("confidence", 0) > 0.7:
            return 0.8  # Haute confiance avec patterns clairs
        else:
            return 0.5  # Confiance modérée

    def _save_prediction(self, intensity: int, trigger: str, confidence: float):
        """Sauvegarde une prédiction"""
        try:
            with self.lock:
                self.db.execute_update(
                    """
                    INSERT INTO pain_predictions
                    (predicted_intensity, predicted_trigger, confidence, time_horizon)
                    VALUES (?, ?, ?, ?)
                    """,
                    (intensity, trigger, confidence, "2-4 heures"),
                )

        except Exception as e:
            logger.error(f"Erreur sauvegarde prédiction: {e}")

    def _get_preventive_recommendations(self, intensity: int) -> list[str]:
        """Génère des recommandations préventives"""
        if intensity >= 8:
            return [
                "Surveillance médicale recommandée",
                "Techniques de relaxation immédiates",
                "Éviter les activités stressantes",
                "Consultation psychologique urgente",
            ]
        elif intensity >= 6:
            return [
                "Techniques de relaxation préventives",
                "Surveillance accrue",
                "Plan de gestion activé",
            ]
        elif intensity >= 4:
            return [
                "Techniques de relaxation légères",
                "Surveillance normale",
                "Continuer les bonnes pratiques",
            ]
        else:
            return [
                "Maintenir les bonnes pratiques",
                "Surveillance préventive",
                "Continuer la collecte de données",
            ]

    def get_analytics_summary(self) -> dict[str, Any]:
        """Retourne un résumé des analytics"""
        try:
            with self.lock:
                # Statistiques générales
                total_events = self.db.get_count("pain_events")
                total_patterns = self.db.get_count("pain_patterns")
                total_predictions = self.db.get_count("pain_predictions")

                # Précision des prédictions
                accuracy_rows = self.db.execute_query(
                    "SELECT AVG(accuracy) FROM pain_predictions WHERE accuracy IS NOT NULL"
                )
                avg_accuracy = (
                    accuracy_rows[0][0]
                    if accuracy_rows and accuracy_rows[0][0]
                    else 0.0
                )

                return {
                    "total_events": total_events,
                    "total_patterns": total_patterns,
                    "total_predictions": total_predictions,
                    "prediction_accuracy": avg_accuracy,
                    "pattern_detection_rate": (
                        total_patterns / max(1, total_events) * 100
                    ),
                    "system_health": (
                        "operational" if total_events > 0 else "initializing"
                    ),
                }

        except Exception as e:
            logger.error(f"Erreur résumé analytics: {e}")
            return {"error": str(e)}


def main():
    """Test du module ARIA ML Analyzer"""
    logger.info("🧪 Test du module ARIA ML Analyzer")
    logger.info("=" * 50)

    # Créer l'instance
    analyzer = ARIAMLAnalyzer()

    # Test d'enregistrement d'événements
    logger.info("\n1️⃣ Test enregistrement événements")
    events = [
        PainEvent(
            PainEventType.PAIN_ENTRY,
            datetime.now(),
            intensity=7,
            trigger="stress",
            action="respiration",
        ),
        PainEvent(
            PainEventType.PAIN_ENTRY,
            datetime.now(),
            intensity=8,
            trigger="fatigue",
            action="repos",
        ),
        PainEvent(
            PainEventType.PAIN_ENTRY,
            datetime.now(),
            intensity=6,
            trigger="marche",
            action="chaleur",
        ),
    ]

    for event in events:
        analyzer.track_pain_event(event)

    # Test d'analyse de patterns
    logger.info("\n2️⃣ Test analyse patterns")
    patterns = analyzer.analyze_pain_patterns(days=7)
    logger.info(f"Patterns détectés: {len(patterns.get('patterns', []))}")
    logger.info(f"Recommandations: {patterns.get('recommendations', [])}")

    # Test de prédiction
    logger.info("\n3️⃣ Test prédiction")
    context = {"stress_level": 0.8, "fatigue_level": 0.6, "activity_intensity": 0.4}
    prediction = analyzer.predict_pain_episode(context)
    logger.info(f"Prédiction: {prediction}")

    # Test résumé analytics
    logger.info("\n4️⃣ Test résumé analytics")
    summary = analyzer.get_analytics_summary()
    logger.info(f"Résumé: {summary}")

    logger.info("\n✅ Test ARIA ML Analyzer terminé")


if __name__ == "__main__":
    main()
