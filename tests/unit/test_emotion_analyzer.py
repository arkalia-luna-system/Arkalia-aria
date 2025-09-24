#!/usr/bin/env python3
"""
Tests unitaires pour ARIAREmotionAnalyzer
=========================================

Tests complets pour le module d'analyse émotionnelle ARIA.
"""


import pytest

from pattern_analysis.emotion_analyzer import ARIAREmotionAnalyzer


class TestARIAREmotionAnalyzer:
    """Tests unitaires pour ARIAREmotionAnalyzer"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.analyzer = ARIAREmotionAnalyzer()

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        analyzer = ARIAREmotionAnalyzer()

        # Assert
        assert analyzer.current_emotion == "neutral"
        assert analyzer.emotion_intensity == 0.5
        assert isinstance(analyzer.emotion_history, list)
        assert isinstance(analyzer.emotions, dict)
        assert "neutral" in analyzer.emotions
        assert "stressed" in analyzer.emotions
        assert "anxious" in analyzer.emotions
        assert "fatigued" in analyzer.emotions
        assert "frustrated" in analyzer.emotions
        assert "relaxed" in analyzer.emotions
        assert "focused" in analyzer.emotions
        assert "overwhelmed" in analyzer.emotions

    def test_analyze_pain_context_success(self):
        """Test cas nominal de analyze_pain_context"""
        # Arrange
        pain_data = {
            "intensity": 7,
            "location": "back",
            "duration": "2 hours",
            "triggers": ["sitting", "stress"],
        }

        # Act
        result = self.analyzer.analyze_pain_context(pain_data)

        # Assert
        assert isinstance(result, dict)
        assert "detected_emotion" in result
        assert "emotion_intensity" in result
        assert "pain_correlation" in result
        assert "stress_level" in result
        assert "timestamp" in result

    def test_analyze_pain_context_high_intensity(self):
        """Test analyze_pain_context avec intensité élevée"""
        # Arrange
        pain_data = {
            "intensity": 9,
            "location": "head",
            "duration": "4 hours",
            "triggers": ["stress", "fatigue"],
        }

        # Act
        result = self.analyzer.analyze_pain_context(pain_data)

        # Assert
        assert isinstance(result, dict)
        assert "detected_emotion" in result
        assert "emotion_intensity" in result
        assert result["emotion_intensity"] > 0.5  # Intensité élevée

    def test_analyze_pain_context_low_intensity(self):
        """Test analyze_pain_context avec intensité faible"""
        # Arrange
        pain_data = {
            "intensity": 2,
            "location": "shoulder",
            "duration": "30 minutes",
            "triggers": [],
        }

        # Act
        result = self.analyzer.analyze_pain_context(pain_data)

        # Assert
        assert isinstance(result, dict)
        assert "detected_emotion" in result
        assert "emotion_intensity" in result
        assert result["emotion_intensity"] < 0.5  # Intensité faible

    def test_analyze_pain_context_error_handling(self):
        """Test gestion d'erreur de analyze_pain_context"""
        # Arrange
        invalid_data = None

        # Act & Assert
        with pytest.raises(AttributeError):
            self.analyzer.analyze_pain_context(invalid_data)

    def test_analyze_pain_context_edge_cases(self):
        """Test analyze_pain_context avec cas limites"""
        # Arrange
        minimal_data = {"intensity": 0}

        # Act
        result = self.analyzer.analyze_pain_context(minimal_data)

        # Assert
        assert isinstance(result, dict)
        assert "detected_emotion" in result
        assert "emotion_intensity" in result

    def test_set_emotion_success(self):
        """Test cas nominal de set_emotion"""
        # Arrange
        emotion = "stressed"
        intensity = 0.8

        # Act
        result = self.analyzer.set_emotion(emotion, intensity)

        # Assert
        assert result is True
        assert self.analyzer.current_emotion == emotion
        assert self.analyzer.emotion_intensity == intensity

    def test_set_emotion_invalid_emotion(self):
        """Test set_emotion avec émotion invalide"""
        # Arrange
        invalid_emotion = "nonexistent_emotion"
        intensity = 0.5

        # Act
        result = self.analyzer.set_emotion(invalid_emotion, intensity)

        # Assert
        assert result is False
        assert self.analyzer.current_emotion == "neutral"  # Reste inchangé

    def test_set_emotion_edge_cases(self):
        """Test set_emotion avec cas limites"""
        # Arrange
        emotion = "neutral"
        intensity = 0.0  # Intensité minimale

        # Act
        result = self.analyzer.set_emotion(emotion, intensity)

        # Assert
        assert result is True
        assert self.analyzer.current_emotion == emotion
        assert self.analyzer.emotion_intensity == intensity

    def test_get_current_emotion_success(self):
        """Test cas nominal de get_current_emotion"""
        # Arrange
        self.analyzer.set_emotion("stressed", 0.8)

        # Act
        result = self.analyzer.get_current_emotion()

        # Assert
        assert isinstance(result, dict)
        assert "name" in result
        assert "intensity" in result
        assert "description" in result
        assert "color" in result
        assert "pain_correlation" in result
        assert "stress_level" in result
        assert "timestamp" in result
        assert result["name"] == "stressed"

    def test_get_current_emotion_edge_cases(self):
        """Test get_current_emotion avec cas limites"""
        # Arrange
        # Tester avec une émotion valide mais avec intensité extrême
        self.analyzer.set_emotion("neutral", 1.0)

        # Act
        result = self.analyzer.get_current_emotion()

        # Assert
        assert isinstance(result, dict)
        assert result["name"] == "neutral"
        assert result["intensity"] == 1.0

    def test_get_emotion_history_success(self):
        """Test cas nominal de get_emotion_history"""
        # Arrange
        # Ajouter quelques émotions à l'historique
        self.analyzer.set_emotion("stressed", 0.8)
        self.analyzer.set_emotion("anxious", 0.6)
        self.analyzer.set_emotion("neutral", 0.3)

        # Act
        history = self.analyzer.get_emotion_history()

        # Assert
        assert isinstance(history, list)
        assert len(history) >= 3
        assert all("emotion" in entry for entry in history)
        assert all("intensity" in entry for entry in history)
        assert all("timestamp" in entry for entry in history)

    def test_get_emotion_history_with_limit(self):
        """Test get_emotion_history avec limite"""
        # Arrange
        # Ajouter plusieurs émotions
        self.analyzer.set_emotion("stressed", 0.8)
        self.analyzer.set_emotion("anxious", 0.6)
        self.analyzer.set_emotion("neutral", 0.3)
        self.analyzer.set_emotion("relaxed", 0.2)

        # Act
        history = self.analyzer.get_emotion_history(limit=2)

        # Assert
        assert isinstance(history, list)
        assert len(history) <= 2

    def test_get_emotion_history_empty(self):
        """Test get_emotion_history avec historique vide"""
        # Arrange
        # Créer un nouvel analyseur sans historique
        analyzer = ARIAREmotionAnalyzer()

        # Act
        history = analyzer.get_emotion_history()

        # Assert
        assert isinstance(history, list)
        assert len(history) == 0

    def test_get_emotion_patterns_success(self):
        """Test cas nominal de get_emotion_patterns"""
        # Arrange
        # Ajouter quelques émotions
        self.analyzer.set_emotion("stressed", 0.8)
        self.analyzer.set_emotion("anxious", 0.6)

        # Act
        patterns = self.analyzer.get_emotion_patterns(days=7)

        # Assert
        assert isinstance(patterns, dict)
        assert "total_entries" in patterns
        assert "emotion_distribution" in patterns
        assert "dominant_emotion" in patterns
        assert "average_stress" in patterns
        assert "stress_trend" in patterns

    def test_get_emotion_patterns_with_days(self):
        """Test get_emotion_patterns avec nombre de jours spécifique"""
        # Arrange
        self.analyzer.set_emotion("stressed", 0.8)

        # Act
        patterns = self.analyzer.get_emotion_patterns(days=3)

        # Assert
        assert isinstance(patterns, dict)
        assert "total_entries" in patterns
        assert "emotion_distribution" in patterns

    def test_predict_emotional_state_success(self):
        """Test cas nominal de predict_emotional_state"""
        # Arrange
        context = {
            "pain_level": 7,
            "stress_factors": ["work", "deadline"],
            "environment": "office",
            "time_of_day": "afternoon",
        }

        # Act
        prediction = self.analyzer.predict_emotional_state(context)

        # Assert
        assert isinstance(prediction, dict)
        assert "predicted_emotion" in prediction
        assert "confidence" in prediction
        assert "factors" in prediction
        assert "predicted_stress" in prediction

    def test_predict_emotional_state_edge_cases(self):
        """Test predict_emotional_state avec cas limites"""
        # Arrange
        minimal_context = {"pain_level": 0}

        # Act
        prediction = self.analyzer.predict_emotional_state(minimal_context)

        # Assert
        assert isinstance(prediction, dict)
        assert "predicted_emotion" in prediction
        assert "confidence" in prediction

    def test_get_emotion_stats_success(self):
        """Test cas nominal de get_emotion_stats"""
        # Arrange
        # Ajouter quelques émotions
        self.analyzer.set_emotion("stressed", 0.8)
        self.analyzer.set_emotion("anxious", 0.6)

        # Act
        stats = self.analyzer.get_emotion_stats()

        # Assert
        assert isinstance(stats, dict)
        assert "total_transitions" in stats
        assert "emotion_counts" in stats
        assert "current_emotion" in stats
        assert "current_intensity" in stats

    def test_reset_emotions_success(self):
        """Test cas nominal de reset_emotions"""
        # Arrange
        # Modifier l'état émotionnel
        self.analyzer.set_emotion("stressed", 0.8)
        self.analyzer.emotion_history = [{"emotion": "test", "intensity": 0.5}]

        # Act
        self.analyzer.reset_emotions()

        # Assert
        assert self.analyzer.current_emotion == "neutral"
        assert self.analyzer.emotion_intensity == 0.5
        assert len(self.analyzer.emotion_history) == 0

    def test_emotion_correlation_analysis(self):
        """Test analyse de corrélation émotion-douleur"""
        # Arrange
        pain_data = {
            "intensity": 8,
            "location": "head",
            "triggers": ["stress", "fatigue"],
        }

        # Act
        result = self.analyzer.analyze_pain_context(pain_data)

        # Assert
        assert isinstance(result, dict)
        assert "pain_correlation" in result
        assert isinstance(result["pain_correlation"], int | float)

    def test_recommendations_generation(self):
        """Test génération de recommandations"""
        # Arrange
        pain_data = {"intensity": 6, "location": "back", "triggers": ["sitting"]}

        # Act
        result = self.analyzer.analyze_pain_context(pain_data)

        # Assert
        assert isinstance(result, dict)
        assert "detected_emotion" in result
        assert "emotion_intensity" in result
        assert "pain_correlation" in result

    def test_emotion_intensity_validation(self):
        """Test validation de l'intensité émotionnelle"""
        # Arrange
        emotion = "stressed"

        # Act & Assert
        # Intensité valide
        assert self.analyzer.set_emotion(emotion, 0.5) is True
        assert self.analyzer.set_emotion(emotion, 0.0) is True
        assert self.analyzer.set_emotion(emotion, 1.0) is True

    def test_emotion_history_tracking(self):
        """Test suivi de l'historique émotionnel"""
        # Arrange
        emotions = ["neutral", "stressed", "anxious", "relaxed"]
        intensities = [0.3, 0.8, 0.6, 0.2]

        # Act
        for emotion, intensity in zip(emotions, intensities, strict=False):
            self.analyzer.set_emotion(emotion, intensity)

        # Assert
        history = self.analyzer.get_emotion_history()
        assert len(history) >= len(emotions)
        assert self.analyzer.current_emotion == emotions[-1]
