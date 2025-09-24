#!/usr/bin/env python3

"""
ARIA Emotion Analyzer - Module d'analyse émotionnelle pour ARIA
Adapté de BBIA Emotions pour l'analyse des patterns de douleur
"""

from datetime import datetime, timedelta


class ARIAREmotionAnalyzer:
    """Module d'analyse émotionnelle pour ARIA - adapté de BBIA"""

    def __init__(self):
        self.current_emotion = "neutral"
        self.emotion_intensity = 0.5  # 0.0 à 1.0
        self.emotion_history = []

        # Émotions adaptées pour l'analyse de douleur
        self.emotions = {
            "neutral": {
                "description": "État de repos, attention normale",
                "color": "⚪",
                "pain_correlation": 0.0,
                "stress_level": 0.0,
            },
            "stressed": {
                "description": "Stress, tension, pression",
                "color": "😰",
                "pain_correlation": 0.7,
                "stress_level": 0.8,
            },
            "anxious": {
                "description": "Anxiété, inquiétude, appréhension",
                "color": "😟",
                "pain_correlation": 0.6,
                "stress_level": 0.7,
            },
            "fatigued": {
                "description": "Fatigue, épuisement, lassitude",
                "color": "😴",
                "pain_correlation": 0.5,
                "stress_level": 0.4,
            },
            "frustrated": {
                "description": "Frustration, irritation, contrariété",
                "color": "😤",
                "pain_correlation": 0.8,
                "stress_level": 0.9,
            },
            "relaxed": {
                "description": "Détente, calme, sérénité",
                "color": "😌",
                "pain_correlation": -0.3,
                "stress_level": -0.5,
            },
            "focused": {
                "description": "Concentration, attention, focalisation",
                "color": "🤔",
                "pain_correlation": -0.2,
                "stress_level": 0.2,
            },
            "overwhelmed": {
                "description": "Débordement, surcharge, saturation",
                "color": "😵",
                "pain_correlation": 0.9,
                "stress_level": 1.0,
            },
        }

        print("🧠 ARIA Emotion Analyzer initialisé")
        print(f"   • Émotion actuelle : {self.current_emotion}")
        print(f"   • Intensité : {self.emotion_intensity}")
        print(f"   • Émotions disponibles : {len(self.emotions)}")

    def analyze_pain_context(self, pain_data: dict) -> dict:
        """Analyse le contexte émotionnel d'une entrée de douleur"""
        intensity = pain_data.get("intensity", 0)
        trigger = pain_data.get("physical_trigger", "")
        mental_trigger = pain_data.get("mental_trigger", "")
        activity = pain_data.get("activity", "")

        # Analyse basée sur les déclencheurs
        emotion_scores = {}

        # Analyse des déclencheurs physiques
        if "marche" in trigger.lower():
            emotion_scores["fatigued"] = 0.6
            emotion_scores["stressed"] = 0.4
        elif "position" in trigger.lower():
            emotion_scores["frustrated"] = 0.7
            emotion_scores["overwhelmed"] = 0.3
        elif "effort" in trigger.lower():
            emotion_scores["fatigued"] = 0.8
            emotion_scores["stressed"] = 0.5

        # Analyse des déclencheurs mentaux
        if "stress" in mental_trigger.lower():
            emotion_scores["stressed"] = 0.9
            emotion_scores["anxious"] = 0.7
        elif "anxiété" in mental_trigger.lower():
            emotion_scores["anxious"] = 0.9
            emotion_scores["overwhelmed"] = 0.6
        elif "fatigue" in mental_trigger.lower():
            emotion_scores["fatigued"] = 0.8
            emotion_scores["overwhelmed"] = 0.4

        # Analyse de l'activité
        if "travail" in activity.lower() or "mac" in activity.lower():
            emotion_scores["focused"] = 0.6
            emotion_scores["stressed"] = 0.5
        elif "repos" in activity.lower():
            emotion_scores["relaxed"] = 0.7

        # Calcul de l'émotion dominante
        if emotion_scores:
            dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
            self.set_emotion(dominant_emotion[0], dominant_emotion[1])
        else:
            # Émotion par défaut basée sur l'intensité
            if intensity >= 8:
                self.set_emotion("overwhelmed", 0.9)
            elif intensity >= 6:
                self.set_emotion("stressed", 0.7)
            elif intensity >= 4:
                self.set_emotion("anxious", 0.5)
            else:
                self.set_emotion("neutral", 0.3)

        return {
            "detected_emotion": self.current_emotion,
            "emotion_intensity": self.emotion_intensity,
            "emotion_scores": emotion_scores,
            "pain_correlation": self.emotions[self.current_emotion]["pain_correlation"],
            "stress_level": self.emotions[self.current_emotion]["stress_level"],
            "timestamp": datetime.now().isoformat(),
        }

    def set_emotion(self, emotion: str, intensity: float = 0.5) -> bool:
        """Change l'émotion analysée"""
        if emotion not in self.emotions:
            print(f"❌ Émotion inconnue : {emotion}")
            return False

        old_emotion = self.current_emotion
        self.current_emotion = emotion
        self.emotion_intensity = max(0.0, min(1.0, intensity))

        # Enregistrer dans l'historique
        self.emotion_history.append(
            {
                "emotion": emotion,
                "intensity": self.emotion_intensity,
                "timestamp": datetime.now().isoformat(),
                "previous": old_emotion,
            }
        )

        return True

    def get_emotion_patterns(self, days: int = 7) -> dict:
        """Analyse les patterns émotionnels sur une période"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_emotions = [
            entry
            for entry in self.emotion_history
            if datetime.fromisoformat(entry["timestamp"]) > cutoff_date
        ]

        if not recent_emotions:
            return {
                "total_entries": 0,
                "dominant_emotion": "neutral",
                "stress_trend": "stable",
                "recommendations": ["Pas assez de données récentes"],
            }

        # Calcul des patterns
        emotion_counts: dict[str, int] = {}
        stress_levels: list[float] = []

        for entry in recent_emotions:
            emotion = entry["emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            stress_levels.append(self.emotions[emotion]["stress_level"])

        # Émotion dominante
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0]

        # Tendance de stress
        avg_stress: float = sum(stress_levels) / len(stress_levels)
        if avg_stress > 0.7:
            stress_trend = "élevé"
        elif avg_stress > 0.4:
            stress_trend = "modéré"
        else:
            stress_trend = "faible"

        # Recommandations
        recommendations = self._generate_recommendations(dominant_emotion, avg_stress)

        return {
            "total_entries": len(recent_emotions),
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": emotion_counts,
            "average_stress": avg_stress,
            "stress_trend": stress_trend,
            "recommendations": recommendations,
            "analysis_period": f"{days} derniers jours",
        }

    def _generate_recommendations(
        self, dominant_emotion: str, avg_stress: float
    ) -> list[str]:
        """Génère des recommandations basées sur l'analyse émotionnelle"""
        recommendations = []

        if dominant_emotion == "stressed":
            recommendations.extend(
                [
                    "Techniques de relaxation recommandées",
                    "Réduction des facteurs de stress",
                    "Pauses régulières pendant le travail",
                ]
            )
        elif dominant_emotion == "anxious":
            recommendations.extend(
                [
                    "Exercices de respiration profonde",
                    "Techniques de méditation",
                    "Consultation psychologique recommandée",
                ]
            )
        elif dominant_emotion == "fatigued":
            recommendations.extend(
                [
                    "Amélioration du sommeil",
                    "Gestion de l'énergie",
                    "Réduction des activités fatigantes",
                ]
            )
        elif dominant_emotion == "overwhelmed":
            recommendations.extend(
                [
                    "Priorisation des tâches",
                    "Délégation si possible",
                    "Support psychologique urgent",
                ]
            )

        if avg_stress > 0.7:
            recommendations.append(
                "Niveau de stress élevé - attention particulière requise"
            )

        return recommendations

    def predict_emotional_state(self, context: dict) -> dict:
        """Prédit l'état émotionnel basé sur le contexte"""
        # Analyse des facteurs contextuels
        time_of_day = datetime.now().hour
        day_of_week = datetime.now().weekday()

        # Patterns temporels
        if 9 <= time_of_day <= 17:  # Heures de travail
            work_stress_factor = 0.6
        else:
            work_stress_factor = 0.2

        if day_of_week >= 5:  # Weekend
            weekend_relaxation = 0.3
        else:
            weekend_relaxation = 0.0

        # Calcul de l'état émotionnel prédit
        predicted_stress = work_stress_factor - weekend_relaxation

        if predicted_stress > 0.7:
            predicted_emotion = "overwhelmed"
        elif predicted_stress > 0.5:
            predicted_emotion = "stressed"
        elif predicted_stress > 0.3:
            predicted_emotion = "anxious"
        else:
            predicted_emotion = "neutral"

        return {
            "predicted_emotion": predicted_emotion,
            "predicted_stress": predicted_stress,
            "confidence": 0.7,  # Confiance basée sur les patterns historiques
            "factors": {
                "time_of_day": time_of_day,
                "day_of_week": day_of_week,
                "work_stress_factor": work_stress_factor,
                "weekend_relaxation": weekend_relaxation,
            },
        }

    def get_current_emotion(self) -> dict:
        """Retourne l'émotion actuelle avec ses détails"""
        emotion_data = self.emotions[self.current_emotion].copy()
        emotion_data.update(
            {
                "name": self.current_emotion,
                "intensity": self.emotion_intensity,
                "timestamp": datetime.now().isoformat(),
            }
        )
        return emotion_data

    def get_emotion_history(self, limit: int = 10) -> list[dict]:
        """Retourne l'historique des émotions"""
        return self.emotion_history[-limit:] if limit > 0 else self.emotion_history

    def get_emotion_stats(self) -> dict:
        """Retourne les statistiques des émotions"""
        emotion_counts: dict[str, int] = {}
        for entry in self.emotion_history:
            emotion = entry["emotion"]
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        return {
            "current_emotion": self.current_emotion,
            "current_intensity": self.emotion_intensity,
            "total_transitions": len(self.emotion_history),
            "emotion_counts": emotion_counts,
            "available_emotions": list(self.emotions.keys()),
        }

    def reset_emotions(self):
        """Remet l'analyseur en état neutre"""
        print("🔄 Remise à zéro de l'analyseur émotionnel")
        self.set_emotion("neutral", 0.5)
        self.emotion_history.clear()


def main():
    """Test du module ARIA Emotion Analyzer"""
    print("🧪 Test du module ARIA Emotion Analyzer")
    print("=" * 50)

    # Créer l'instance
    analyzer = ARIAREmotionAnalyzer()

    # Test d'analyse de contexte de douleur
    print("\n1️⃣ Test analyse contexte douleur")
    pain_data = {
        "intensity": 7,
        "physical_trigger": "marche prolongée",
        "mental_trigger": "stress",
        "activity": "travail sur Mac",
    }
    analysis = analyzer.analyze_pain_context(pain_data)
    print(f"Analyse: {analysis}")

    # Test de patterns émotionnels
    print("\n2️⃣ Test patterns émotionnels")
    patterns = analyzer.get_emotion_patterns(days=7)
    print(f"Patterns: {patterns}")

    # Test de prédiction
    print("\n3️⃣ Test prédiction émotionnelle")
    prediction = analyzer.predict_emotional_state({})
    print(f"Prédiction: {prediction}")

    # Test statistiques
    print("\n4️⃣ Test statistiques")
    stats = analyzer.get_emotion_stats()
    print(f"Statistiques: {stats}")

    print("\n✅ Test ARIA Emotion Analyzer terminé")


if __name__ == "__main__":
    main()
