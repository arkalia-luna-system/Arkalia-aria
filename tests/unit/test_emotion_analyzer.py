#!/usr/bin/env python3
"""
Tests unitaires pour ARIAREmotionAnalyzer
=========================================

Tests complets pour l'analyseur d'émotions ARIA.
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
        assert "painful" in analyzer.emotions
        assert "relaxed" in analyzer.emotions
        assert "focused" in analyzer.emotions
        assert "overwhelmed" in analyzer.emotions

    def test_analyze_emotion_success(self):
        """Test cas nominal de analyze_emotion"""
        # Arrange
        pain_data = {
            "intensity": 7,
            "trigger": "stress",
            "duration": 30,
            "location": "head",
            "previous_emotion": "neutral",
        }

        # Act
        result = self.analyzer.analyze_emotion(pain_data)

        # Assert
        assert isinstance(result, dict)
        assert "emotion" in result
        assert "intensity" in result
        assert "confidence" in result
        assert "pain_correlation" in result
        assert "recommendations" in result
        assert "timestamp" in result
        assert result["emotion"] in self.analyzer.emotions.keys()
        assert 0.0 <= result["intensity"] <= 1.0
        assert 0.0 <= result["confidence"] <= 1.0
        assert 0.0 <= result["pain_correlation"] <= 1.0
        assert isinstance(result["recommendations"], list)

    def test_analyze_emotion_high_intensity(self):
        """Test analyze_emotion avec intensité élevée"""
        # Arrange
        pain_data = {
            "intensity": 9,
            "trigger": "physical_stress",
            "duration": 60,
            "location": "back",
            "previous_emotion": "stressed",
        }

        # Act
        result = self.analyzer.analyze_emotion(pain_data)

        # Assert
        assert result["emotion"] in ["painful", "overwhelmed", "stressed"]
        assert result["intensity"] > 0.7
        assert result["pain_correlation"] > 0.5

    def test_analyze_emotion_low_intensity(self):
        """Test analyze_emotion avec intensité faible"""
        # Arrange
        pain_data = {
            "intensity": 2,
            "trigger": "mild_discomfort",
            "duration": 5,
            "location": "arm",
            "previous_emotion": "neutral",
        }

        # Act
        result = self.analyzer.analyze_emotion(pain_data)

        # Assert
        assert result["emotion"] in ["neutral", "relaxed", "focused"]
        assert result["intensity"] < 0.5
        assert result["pain_correlation"] < 0.3

    def test_analyze_emotion_error_handling(self):
        """Test gestion d'erreur de analyze_emotion"""
        # Arrange
        invalid_data = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.analyzer.analyze_emotion(invalid_data)

    def test_analyze_emotion_edge_cases(self):
        """Test cas limites de analyze_emotion"""
        # Arrange
        minimal_data = {"intensity": 5}

        # Act
        result = self.analyzer.analyze_emotion(minimal_data)

        # Assert
        assert isinstance(result, dict)
        assert "emotion" in result
        assert "intensity" in result
        assert "confidence" in result

    def test_get_current_emotion_success(self):
        """Test cas nominal de get_current_emotion"""
        # Arrange
        self.analyzer.current_emotion = "stressed"
        self.analyzer.emotion_intensity = 0.8

        # Act
        result = self.analyzer.get_current_emotion()

        # Assert
        assert isinstance(result, dict)
        assert "emotion" in result
        assert "intensity" in result
        assert "description" in result
        assert "color" in result
        assert "pain_correlation" in result
        assert "stress_level" in result
        assert result["emotion"] == "stressed"
        assert result["intensity"] == 0.8
        assert result["pain_correlation"] == 0.7
        assert result["stress_level"] == 0.8

    def test_get_current_emotion_edge_cases(self):
        """Test cas limites de get_current_emotion"""
        # Arrange
        self.analyzer.current_emotion = "nonexistent_emotion"
        self.analyzer.emotion_intensity = 0.0

        # Act
        result = self.analyzer.get_current_emotion()

        # Assert
        assert result["emotion"] == "nonexistent_emotion"
        assert result["intensity"] == 0.0
        # Devrait gérer gracieusement les émotions inexistantes
        assert "description" in result

    def test_get_emotion_history_success(self):
        """Test cas nominal de get_emotion_history"""
        # Arrange
        self.analyzer.emotion_history = [
            {
                "emotion": "neutral",
                "intensity": 0.5,
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "emotion": "stressed",
                "intensity": 0.8,
                "timestamp": "2024-01-01T00:01:00",
            },
            {
                "emotion": "relaxed",
                "intensity": 0.3,
                "timestamp": "2024-01-01T00:02:00",
            },
        ]

        # Act
        history = self.analyzer.get_emotion_history()

        # Assert
        assert isinstance(history, list)
        assert len(history) == 3
        assert history[0]["emotion"] == "neutral"
        assert history[1]["emotion"] == "stressed"
        assert history[2]["emotion"] == "relaxed"

    def test_get_emotion_history_with_limit(self):
        """Test get_emotion_history avec limite"""
        # Arrange
        self.analyzer.emotion_history = [
            {
                "emotion": "neutral",
                "intensity": 0.5,
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "emotion": "stressed",
                "intensity": 0.8,
                "timestamp": "2024-01-01T00:01:00",
            },
            {
                "emotion": "relaxed",
                "intensity": 0.3,
                "timestamp": "2024-01-01T00:02:00",
            },
        ]

        # Act
        history = self.analyzer.get_emotion_history(limit=2)

        # Assert
        assert len(history) == 2
        assert history[0]["emotion"] == "neutral"
        assert history[1]["emotion"] == "stressed"

    def test_get_emotion_history_empty(self):
        """Test get_emotion_history vide"""
        # Arrange
        self.analyzer.emotion_history = []

        # Act
        history = self.analyzer.get_emotion_history()

        # Assert
        assert isinstance(history, list)
        assert len(history) == 0

    def test_get_recommendations_success(self):
        """Test cas nominal de get_recommendations"""
        # Arrange
        current_emotion = "stressed"
        pain_data = {"intensity": 7, "trigger": "work_stress", "duration": 45}

        # Act
        recommendations = self.analyzer.get_recommendations(current_emotion, pain_data)

        # Assert
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all("recommendation" in rec for rec in recommendations)
        assert all("priority" in rec for rec in recommendations)
        assert all("category" in rec for rec in recommendations)
        assert all(
            rec["priority"] in ["high", "medium", "low"] for rec in recommendations
        )
        assert all(
            rec["category"]
            in ["breathing", "relaxation", "movement", "mindfulness", "medical"]
            for rec in recommendations
        )

    def test_get_recommendations_high_intensity(self):
        """Test get_recommendations avec intensité élevée"""
        # Arrange
        current_emotion = "painful"
        pain_data = {"intensity": 9, "trigger": "severe_pain", "duration": 120}

        # Act
        recommendations = self.analyzer.get_recommendations(current_emotion, pain_data)

        # Assert
        assert len(recommendations) > 0
        # Devrait avoir des recommandations de priorité élevée
        high_priority_recs = [
            rec for rec in recommendations if rec["priority"] == "high"
        ]
        assert len(high_priority_recs) > 0
        # Devrait inclure des recommandations médicales
        medical_recs = [rec for rec in recommendations if rec["category"] == "medical"]
        assert len(medical_recs) > 0

    def test_get_recommendations_low_intensity(self):
        """Test get_recommendations avec intensité faible"""
        # Arrange
        current_emotion = "relaxed"
        pain_data = {"intensity": 2, "trigger": "mild_discomfort", "duration": 10}

        # Act
        recommendations = self.analyzer.get_recommendations(current_emotion, pain_data)

        # Assert
        assert len(recommendations) > 0
        # Devrait avoir des recommandations de priorité faible/moyenne
        low_priority_recs = [
            rec for rec in recommendations if rec["priority"] in ["low", "medium"]
        ]
        assert len(low_priority_recs) > 0

    def test_get_recommendations_error_handling(self):
        """Test gestion d'erreur de get_recommendations"""
        # Arrange
        current_emotion = None
        pain_data = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.analyzer.get_recommendations(current_emotion, pain_data)

    def test_calculate_emotion_score_success(self):
        """Test cas nominal de _calculate_emotion_score"""
        # Arrange
        pain_data = {
            "intensity": 6,
            "trigger": "stress",
            "duration": 30,
            "location": "head",
        }

        # Act
        score = self.analyzer._calculate_emotion_score(pain_data)

        # Assert
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_calculate_emotion_score_edge_cases(self):
        """Test cas limites de _calculate_emotion_score"""
        # Arrange
        minimal_data = {"intensity": 5}

        # Act
        score = self.analyzer._calculate_emotion_score(minimal_data)

        # Assert
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_determine_emotion_from_score_success(self):
        """Test cas nominal de _determine_emotion_from_score"""
        # Arrange
        score = 0.8
        pain_data = {"intensity": 7, "trigger": "stress"}

        # Act
        emotion = self.analyzer._determine_emotion_from_score(score, pain_data)

        # Assert
        assert emotion in self.analyzer.emotions.keys()
        assert emotion in ["stressed", "anxious", "overwhelmed", "painful"]

    def test_determine_emotion_from_score_low_score(self):
        """Test _determine_emotion_from_score avec score faible"""
        # Arrange
        score = 0.2
        pain_data = {"intensity": 2, "trigger": "mild_discomfort"}

        # Act
        emotion = self.analyzer._determine_emotion_from_score(score, pain_data)

        # Assert
        assert emotion in ["neutral", "relaxed", "focused"]

    def test_determine_emotion_from_score_edge_cases(self):
        """Test cas limites de _determine_emotion_from_score"""
        # Arrange
        score = 0.0
        pain_data = {}

        # Act
        emotion = self.analyzer._determine_emotion_from_score(score, pain_data)

        # Assert
        assert emotion in self.analyzer.emotions.keys()

    def test_update_emotion_history_success(self):
        """Test cas nominal de _update_emotion_history"""
        # Arrange
        emotion_data = {
            "emotion": "stressed",
            "intensity": 0.8,
            "confidence": 0.9,
            "pain_correlation": 0.7,
        }

        # Act
        self.analyzer._update_emotion_history(emotion_data)

        # Assert
        assert len(self.analyzer.emotion_history) == 1
        assert self.analyzer.emotion_history[0]["emotion"] == "stressed"
        assert self.analyzer.emotion_history[0]["intensity"] == 0.8
        assert "timestamp" in self.analyzer.emotion_history[0]

    def test_update_emotion_history_error_handling(self):
        """Test gestion d'erreur de _update_emotion_history"""
        # Arrange
        invalid_data = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.analyzer._update_emotion_history(invalid_data)

    def test_get_emotion_info_success(self):
        """Test cas nominal de _get_emotion_info"""
        # Arrange
        emotion = "stressed"

        # Act
        info = self.analyzer._get_emotion_info(emotion)

        # Assert
        assert isinstance(info, dict)
        assert "description" in info
        assert "color" in info
        assert "pain_correlation" in info
        assert "stress_level" in info
        assert info["description"] == "Stress, tension, pression"
        assert info["color"] == "😰"
        assert info["pain_correlation"] == 0.7
        assert info["stress_level"] == 0.8

    def test_get_emotion_info_invalid_emotion(self):
        """Test _get_emotion_info avec émotion invalide"""
        # Arrange
        invalid_emotion = "nonexistent_emotion"

        # Act
        info = self.analyzer._get_emotion_info(invalid_emotion)

        # Assert
        assert isinstance(info, dict)
        assert "description" in info
        assert "color" in info
        assert "pain_correlation" in info
        assert "stress_level" in info
        # Devrait retourner des valeurs par défaut
        assert info["pain_correlation"] == 0.0
        assert info["stress_level"] == 0.0

    def test_get_emotion_info_edge_cases(self):
        """Test cas limites de _get_emotion_info"""
        # Arrange
        empty_emotion = ""

        # Act
        info = self.analyzer._get_emotion_info(empty_emotion)

        # Assert
        assert isinstance(info, dict)
        assert "description" in info
        assert "color" in info
        assert "pain_correlation" in info
        assert "stress_level" in info

    def test_calculate_confidence_success(self):
        """Test cas nominal de _calculate_confidence"""
        # Arrange
        pain_data = {
            "intensity": 6,
            "trigger": "stress",
            "duration": 30,
            "location": "head",
            "previous_emotion": "neutral",
        }

        # Act
        confidence = self.analyzer._calculate_confidence(pain_data)

        # Assert
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_calculate_confidence_edge_cases(self):
        """Test cas limites de _calculate_confidence"""
        # Arrange
        minimal_data = {"intensity": 5}

        # Act
        confidence = self.analyzer._calculate_confidence(minimal_data)

        # Assert
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0

    def test_calculate_pain_correlation_success(self):
        """Test cas nominal de _calculate_pain_correlation"""
        # Arrange
        emotion = "stressed"
        pain_data = {"intensity": 7, "trigger": "stress"}

        # Act
        correlation = self.analyzer._calculate_pain_correlation(emotion, pain_data)

        # Assert
        assert isinstance(correlation, float)
        assert 0.0 <= correlation <= 1.0
        assert (
            correlation > 0.5
        )  # Stress devrait avoir une corrélation élevée avec la douleur

    def test_calculate_pain_correlation_relaxed_emotion(self):
        """Test _calculate_pain_correlation avec émotion relaxée"""
        # Arrange
        emotion = "relaxed"
        pain_data = {"intensity": 3, "trigger": "mild_discomfort"}

        # Act
        correlation = self.analyzer._calculate_pain_correlation(emotion, pain_data)

        # Assert
        assert isinstance(correlation, float)
        assert 0.0 <= correlation <= 1.0
        assert (
            correlation < 0.3
        )  # Relaxation devrait avoir une corrélation faible avec la douleur

    def test_calculate_pain_correlation_edge_cases(self):
        """Test cas limites de _calculate_pain_correlation"""
        # Arrange
        emotion = ""
        pain_data = {}

        # Act
        correlation = self.analyzer._calculate_pain_correlation(emotion, pain_data)

        # Assert
        assert isinstance(correlation, float)
        assert 0.0 <= correlation <= 1.0

    def test_get_emotion_statistics_success(self):
        """Test cas nominal de get_emotion_statistics"""
        # Arrange
        self.analyzer.emotion_history = [
            {
                "emotion": "neutral",
                "intensity": 0.5,
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "emotion": "stressed",
                "intensity": 0.8,
                "timestamp": "2024-01-01T00:01:00",
            },
            {
                "emotion": "stressed",
                "intensity": 0.7,
                "timestamp": "2024-01-01T00:02:00",
            },
            {
                "emotion": "relaxed",
                "intensity": 0.3,
                "timestamp": "2024-01-01T00:03:00",
            },
        ]

        # Act
        stats = self.analyzer.get_emotion_statistics()

        # Assert
        assert isinstance(stats, dict)
        assert "total_emotions" in stats
        assert "emotion_counts" in stats
        assert "average_intensity" in stats
        assert "most_common_emotion" in stats
        assert "emotion_trends" in stats
        assert stats["total_emotions"] == 4
        assert stats["emotion_counts"]["stressed"] == 2
        assert stats["emotion_counts"]["neutral"] == 1
        assert stats["emotion_counts"]["relaxed"] == 1
        assert stats["most_common_emotion"] == "stressed"
        assert isinstance(stats["average_intensity"], float)
        assert isinstance(stats["emotion_trends"], list)

    def test_get_emotion_statistics_empty_history(self):
        """Test get_emotion_statistics avec historique vide"""
        # Arrange
        self.analyzer.emotion_history = []

        # Act
        stats = self.analyzer.get_emotion_statistics()

        # Assert
        assert stats["total_emotions"] == 0
        assert stats["emotion_counts"] == {}
        assert stats["most_common_emotion"] is None
        assert stats["average_intensity"] == 0.0
        assert stats["emotion_trends"] == []

    def test_reset_emotion_state_success(self):
        """Test cas nominal de reset_emotion_state"""
        # Arrange
        self.analyzer.current_emotion = "stressed"
        self.analyzer.emotion_intensity = 0.8
        self.analyzer.emotion_history = [
            {
                "emotion": "stressed",
                "intensity": 0.8,
                "timestamp": "2024-01-01T00:00:00",
            }
        ]

        # Act
        self.analyzer.reset_emotion_state()

        # Assert
        assert self.analyzer.current_emotion == "neutral"
        assert self.analyzer.emotion_intensity == 0.5
        assert len(self.analyzer.emotion_history) == 0
