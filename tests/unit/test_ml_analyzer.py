#!/usr/bin/env python3
"""
Tests unitaires pour ARIAMLAnalyzer
===================================

Tests complets pour le module d'analyse ML ARIA.
"""

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from prediction_engine.ml_analyzer import ARIAMLAnalyzer, PainEvent, PainEventType


class TestARIAMLAnalyzer:
    """Tests unitaires pour ARIAMLAnalyzer"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_aria_pain.db"
        self.ml_analyzer = ARIAMLAnalyzer(str(self.db_path))

    def teardown_method(self):
        """Cleanup après chaque test"""
        self.temp_dir.cleanup()

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        ml_analyzer = ARIAMLAnalyzer(str(self.db_path))

        # Assert
        assert ml_analyzer.db_path == str(self.db_path)

    def test_init_with_env_db(self):
        """Test initialisation avec variable d'environnement"""
        # Arrange
        env_db_path = "env_test.db"
        with patch.dict("os.environ", {"ARIA_PAIN_DB": env_db_path}):
            # Act
            ml_analyzer = ARIAMLAnalyzer()

            # Assert
            # La variable d'environnement n'est pas utilisée dans l'implémentation actuelle
            assert ml_analyzer.db_path == "aria_pain.db"

    def test_track_pain_event_success(self):
        """Test cas nominal de track_pain_event"""
        # Arrange
        event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=7,
            trigger="stress",
            action="medication",
        )

        # Act
        result = self.ml_analyzer.track_pain_event(event)

        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_track_pain_event_error_handling(self):
        """Test gestion d'erreur de track_pain_event"""
        # Arrange
        invalid_event = None

        # Act
        result = self.ml_analyzer.track_pain_event(invalid_event)

        # Assert
        assert isinstance(result, bool)
        assert result is False

    def test_track_pain_event_edge_cases(self):
        """Test track_pain_event avec cas limites"""
        # Arrange
        minimal_event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY, timestamp=datetime.now()
        )

        # Act
        result = self.ml_analyzer.track_pain_event(minimal_event)

        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_analyze_pain_patterns_success(self):
        """Test cas nominal de analyze_pain_patterns"""
        # Arrange
        # Ajouter quelques événements
        event1 = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=7,
            trigger="stress",
        )
        event2 = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=6,
            trigger="stress",
        )
        event3 = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=8,
            trigger="fatigue",
        )

        self.ml_analyzer.track_pain_event(event1)
        self.ml_analyzer.track_pain_event(event2)
        self.ml_analyzer.track_pain_event(event3)

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns(days=7)

        # Assert
        assert isinstance(patterns, dict)
        assert "total_events" in patterns
        assert "patterns" in patterns
        assert "recommendations" in patterns
        assert "confidence" in patterns
        assert "analysis_period" in patterns

    def test_analyze_pain_patterns_empty_data(self):
        """Test analyze_pain_patterns avec données vides"""
        # Arrange
        # Utiliser un nouvel analyseur sans données
        empty_analyzer = ARIAMLAnalyzer(str(Path(self.temp_dir.name) / "empty.db"))

        # Act
        patterns = empty_analyzer.analyze_pain_patterns(days=7)

        # Assert
        assert isinstance(patterns, dict)
        assert patterns["total_events"] == 0
        assert len(patterns["patterns"]) == 0

    def test_analyze_pain_patterns_error_handling(self):
        """Test gestion d'erreur de analyze_pain_patterns"""
        # Arrange
        # Simuler une erreur en fermant la connexion
        self.ml_analyzer.db_path = "/invalid/path/db.db"

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns(days=7)

        # Assert
        assert isinstance(patterns, dict)
        assert "error" in patterns or "total_events" in patterns

    def test_predict_pain_episode_success(self):
        """Test cas nominal de predict_pain_episode"""
        # Arrange
        context = {
            "time_of_day": 14,
            "day_of_week": 1,
            "stress_level": 0.7,
            "fatigue_level": 0.5,
            "activity_level": 0.3,
        }

        # Act
        prediction = self.ml_analyzer.predict_pain_episode(context)

        # Assert
        assert isinstance(prediction, dict)
        assert "predicted_intensity" in prediction
        assert "predicted_trigger" in prediction
        assert "confidence" in prediction
        assert "time_horizon" in prediction
        assert "recommendations" in prediction
        assert "context_factors" in prediction

    def test_predict_pain_episode_with_history(self):
        """Test predict_pain_episode avec historique"""
        # Arrange
        # Ajouter quelques événements pour l'historique
        event1 = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=7,
            trigger="stress",
        )
        event2 = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=6,
            trigger="fatigue",
        )

        self.ml_analyzer.track_pain_event(event1)
        self.ml_analyzer.track_pain_event(event2)

        context = {
            "time_of_day": 14,
            "day_of_week": 1,
            "stress_level": 0.7,
            "fatigue_level": 0.5,
            "activity_level": 0.3,
        }

        # Act
        prediction = self.ml_analyzer.predict_pain_episode(context)

        # Assert
        assert isinstance(prediction, dict)
        assert "predicted_intensity" in prediction
        assert "predicted_trigger" in prediction
        assert "confidence" in prediction
        assert "context_factors" in prediction

    def test_predict_pain_episode_error_handling(self):
        """Test gestion d'erreur de predict_pain_episode"""
        # Arrange
        invalid_context = None

        # Act
        prediction = self.ml_analyzer.predict_pain_episode(invalid_context)

        # Assert
        assert isinstance(prediction, dict)
        assert "error" in prediction or "predicted_intensity" in prediction

    def test_get_analytics_summary_success(self):
        """Test cas nominal de get_analytics_summary"""
        # Arrange
        # Ajouter quelques événements
        event1 = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=7,
            trigger="stress",
        )
        event2 = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=6,
            trigger="fatigue",
        )

        self.ml_analyzer.track_pain_event(event1)
        self.ml_analyzer.track_pain_event(event2)

        # Act
        summary = self.ml_analyzer.get_analytics_summary()

        # Assert
        assert isinstance(summary, dict)
        assert "total_events" in summary
        assert "total_patterns" in summary
        assert "total_predictions" in summary
        assert "prediction_accuracy" in summary
        assert "system_health" in summary

    def test_get_analytics_summary_empty_data(self):
        """Test get_analytics_summary avec données vides"""
        # Arrange
        # Utiliser un nouvel analyseur sans données
        empty_analyzer = ARIAMLAnalyzer(str(Path(self.temp_dir.name) / "empty.db"))

        # Act
        summary = empty_analyzer.get_analytics_summary()

        # Assert
        assert isinstance(summary, dict)
        assert summary["total_events"] == 0
        assert summary["total_patterns"] == 0

    def test_pain_event_creation_success(self):
        """Test création d'événement de douleur"""
        # Arrange
        event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=8,
            trigger="work_stress",
            action="stretching",
            effectiveness=7,
            emotion="frustrated",
            metadata={"location": "back", "duration": "2h"},
        )

        # Act
        result = self.ml_analyzer.track_pain_event(event)

        # Assert
        assert result is True

    def test_pain_event_creation_minimal(self):
        """Test création d'événement de douleur minimal"""
        # Arrange
        event = PainEvent(event_type=PainEventType.PAIN_ENTRY, timestamp=datetime.now())

        # Act
        result = self.ml_analyzer.track_pain_event(event)

        # Assert
        assert result is True

    def test_pattern_detection_common_trigger(self):
        """Test détection de pattern de déclencheur commun"""
        # Arrange
        # Ajouter plusieurs événements avec le même déclencheur
        for i in range(5):
            event = PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now(),
                intensity=6 + i,
                trigger="stress",
            )
            self.ml_analyzer.track_pain_event(event)

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns(days=7)

        # Assert
        assert isinstance(patterns, dict)
        assert patterns["total_events"] >= 5
        assert len(patterns["patterns"]) > 0

    def test_pattern_detection_intensity_trend(self):
        """Test détection de tendance d'intensité"""
        # Arrange
        # Ajouter des événements avec intensité croissante
        for i in range(3):
            event = PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now(),
                intensity=5 + i * 2,
                trigger="fatigue",
            )
            self.ml_analyzer.track_pain_event(event)

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns(days=7)

        # Assert
        assert isinstance(patterns, dict)
        assert patterns["total_events"] >= 3

    def test_prediction_with_different_contexts(self):
        """Test prédiction avec différents contextes"""
        # Arrange
        contexts = [
            {"time_of_day": 9, "stress_level": 0.8, "fatigue_level": 0.2},
            {"time_of_day": 18, "stress_level": 0.3, "fatigue_level": 0.9},
            {"time_of_day": 22, "stress_level": 0.1, "fatigue_level": 0.8},
        ]

        # Act & Assert
        for context in contexts:
            prediction = self.ml_analyzer.predict_pain_episode(context)
            assert isinstance(prediction, dict)
            assert "predicted_intensity" in prediction
            assert "predicted_trigger" in prediction
            assert "confidence" in prediction

    def test_recommendations_generation(self):
        """Test génération de recommandations"""
        # Arrange
        # Ajouter quelques événements
        event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            intensity=8,
            trigger="stress",
        )
        self.ml_analyzer.track_pain_event(event)

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns(days=7)

        # Assert
        assert isinstance(patterns, dict)
        assert "recommendations" in patterns
        assert isinstance(patterns["recommendations"], list)
        assert len(patterns["recommendations"]) > 0

    def test_confidence_calculation(self):
        """Test calcul de confiance"""
        # Arrange
        # Ajouter plusieurs événements similaires
        for _ in range(10):
            event = PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now(),
                intensity=7,
                trigger="stress",
            )
            self.ml_analyzer.track_pain_event(event)

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns(days=7)

        # Assert
        assert isinstance(patterns, dict)
        assert "confidence" in patterns
        assert isinstance(patterns["confidence"], int | float)
        assert 0 <= patterns["confidence"] <= 1

    def test_database_initialization(self):
        """Test initialisation de la base de données"""
        # Arrange
        new_db_path = str(Path(self.temp_dir.name) / "new_aria_pain.db")

        # Act
        analyzer = ARIAMLAnalyzer(new_db_path)

        # Assert
        assert Path(new_db_path).exists()
        assert analyzer.db_path == new_db_path

    def test_multiple_event_types(self):
        """Test avec différents types d'événements"""
        # Arrange
        event_types = [
            PainEventType.PAIN_ENTRY,
            PainEventType.TRIGGER_DETECTED,
            PainEventType.ACTION_TAKEN,
            PainEventType.EFFECTIVENESS_RECORDED,
        ]

        # Act
        for event_type in event_types:
            event = PainEvent(
                event_type=event_type,
                timestamp=datetime.now(),
                intensity=6 if event_type == PainEventType.PAIN_ENTRY else None,
            )
            result = self.ml_analyzer.track_pain_event(event)
            assert result is True

        # Assert
        patterns = self.ml_analyzer.analyze_pain_patterns(days=7)
        assert patterns["total_events"] >= 1  # Au moins un événement enregistré
