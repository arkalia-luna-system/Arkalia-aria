#!/usr/bin/env python3
"""
Tests unitaires pour ARIAMLAnalyzer
=====================================

Tests complets pour l'analyseur ML ARIA.
"""

import os
import tempfile
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from prediction_engine.ml_analyzer import ARIAMLAnalyzer, PainEvent, PainEventType


class TestARIAMLAnalyzer:
    """Tests unitaires pour ARIAMLAnalyzer"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.ml_analyzer = ARIAMLAnalyzer(self.temp_db.name)

    def teardown_method(self):
        """Cleanup après chaque test"""
        os.unlink(self.temp_db.name)

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        ml_analyzer = ARIAMLAnalyzer("test.db")

        # Assert
        assert ml_analyzer.db_path == "test.db"
        assert isinstance(ml_analyzer.total_events, int)
        assert isinstance(ml_analyzer.prediction_accuracy, float)
        assert isinstance(ml_analyzer.pattern_detection_rate, float)

    def test_init_with_env_db(self):
        """Test initialisation avec base de données d'environnement"""
        # Arrange
        with patch.dict(os.environ, {"ARIA_ML_DB": "env_test.db"}):
            # Act
            ml_analyzer = ARIAMLAnalyzer()

            # Assert
            assert ml_analyzer.db_path == "env_test.db"

    def test_track_pain_event_success(self):
        """Test cas nominal de track_pain_event"""
        # Arrange
        event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            user_id="test_user",
            intensity=7,
            trigger="stress",
            action="breathing",
            effectiveness=8,
        )

        # Act
        result = self.ml_analyzer.track_pain_event(event)

        # Assert
        assert isinstance(result, dict)
        assert "event_id" in result
        assert "status" in result
        assert "timestamp" in result
        assert result["status"] == "success"
        assert len(self.ml_analyzer.events) == 1
        assert self.ml_analyzer.events[0].event_type == PainEventType.PAIN_ENTRY
        assert self.ml_analyzer.events[0].intensity == 7

    def test_track_pain_event_error_handling(self):
        """Test gestion d'erreur de track_pain_event"""
        # Arrange
        invalid_event = None

        # Act & Assert
        with pytest.raises(Exception):
            self.ml_analyzer.track_pain_event(invalid_event)

    def test_track_pain_event_edge_cases(self):
        """Test cas limites de track_pain_event"""
        # Arrange
        minimal_event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            user_id="test_user",
        )

        # Act
        result = self.ml_analyzer.track_pain_event(minimal_event)

        # Assert
        assert result["status"] == "success"
        assert len(self.ml_analyzer.events) == 1

    def test_analyze_pain_patterns_success(self):
        """Test cas nominal de analyze_pain_patterns"""
        # Arrange
        # Ajouter quelques événements
        events = [
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=1),
                user_id="test_user",
                intensity=7,
                trigger="stress",
            ),
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=2),
                user_id="test_user",
                intensity=6,
                trigger="stress",
            ),
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=3),
                user_id="test_user",
                intensity=8,
                trigger="work",
            ),
        ]

        for event in events:
            self.ml_analyzer.track_pain_event(event)

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns()

        # Assert
        assert isinstance(patterns, dict)
        assert "patterns_found" in patterns
        assert "trigger_patterns" in patterns
        assert "intensity_patterns" in patterns
        assert "temporal_patterns" in patterns
        assert "confidence_scores" in patterns
        assert "timestamp" in patterns
        assert isinstance(patterns["patterns_found"], int)
        assert isinstance(patterns["trigger_patterns"], dict)
        assert isinstance(patterns["intensity_patterns"], dict)
        assert isinstance(patterns["temporal_patterns"], dict)
        assert isinstance(patterns["confidence_scores"], dict)

    def test_analyze_pain_patterns_empty_data(self):
        """Test analyze_pain_patterns avec données vides"""
        # Arrange
        # Pas d'événements enregistrés

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns()

        # Assert
        assert patterns["patterns_found"] == 0
        assert len(patterns["trigger_patterns"]) == 0
        assert len(patterns["intensity_patterns"]) == 0
        assert len(patterns["temporal_patterns"]) == 0

    def test_analyze_pain_patterns_error_handling(self):
        """Test gestion d'erreur de analyze_pain_patterns"""
        # Arrange
        # Corrompre les données
        self.ml_analyzer.events = [None]  # Données invalides

        # Act
        patterns = self.ml_analyzer.analyze_pain_patterns()

        # Assert
        assert patterns["patterns_found"] == 0
        assert "error" in patterns or patterns["patterns_found"] == 0

    def test_predict_pain_episode_success(self):
        """Test cas nominal de predict_pain_episode"""
        # Arrange
        context = {
            "trigger": "stress",
            "time_of_day": "morning",
            "previous_intensity": 6,
            "user_profile": {"stress_level": "high"},
        }

        # Act
        prediction = self.ml_analyzer.predict_pain_episode(context)

        # Assert
        assert isinstance(prediction, dict)
        assert "predicted_intensity" in prediction
        assert "confidence" in prediction
        assert "factors" in prediction
        assert "timestamp" in prediction
        assert isinstance(prediction["predicted_intensity"], float)
        assert 0.0 <= prediction["predicted_intensity"] <= 10.0
        assert 0.0 <= prediction["confidence"] <= 1.0
        assert isinstance(prediction["factors"], list)

    def test_predict_pain_episode_with_history(self):
        """Test predict_pain_episode avec historique"""
        # Arrange
        # Ajouter des événements historiques
        historical_events = [
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=1),
                user_id="test_user",
                intensity=7,
                trigger="stress",
            ),
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=2),
                user_id="test_user",
                intensity=6,
                trigger="stress",
            ),
        ]

        for event in historical_events:
            self.ml_analyzer.track_pain_event(event)

        context = {
            "trigger": "stress",
            "time_of_day": "morning",
            "previous_intensity": 6,
        }

        # Act
        prediction = self.ml_analyzer.predict_pain_episode(context)

        # Assert
        assert prediction["predicted_intensity"] > 0
        assert prediction["confidence"] > 0
        assert len(prediction["factors"]) > 0

    def test_predict_pain_episode_error_handling(self):
        """Test gestion d'erreur de predict_pain_episode"""
        # Arrange
        invalid_context = None

        # Act & Assert
        with pytest.raises(Exception):
            self.ml_analyzer.predict_pain_episode(invalid_context)

    def test_predict_pain_episode_edge_cases(self):
        """Test cas limites de predict_pain_episode"""
        # Arrange
        minimal_context = {"trigger": "unknown"}

        # Act
        prediction = self.ml_analyzer.predict_pain_episode(minimal_context)

        # Assert
        assert isinstance(prediction, dict)
        assert "predicted_intensity" in prediction
        assert "confidence" in prediction
        assert "factors" in prediction

    def test_get_analytics_summary_success(self):
        """Test cas nominal de get_analytics_summary"""
        # Arrange
        # Ajouter des événements et patterns
        events = [
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=1),
                user_id="test_user",
                intensity=7,
                trigger="stress",
            ),
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=2),
                user_id="test_user",
                intensity=6,
                trigger="work",
            ),
        ]

        for event in events:
            self.ml_analyzer.track_pain_event(event)

        # Act
        summary = self.ml_analyzer.get_analytics_summary()

        # Assert
        assert isinstance(summary, dict)
        assert "total_events" in summary
        assert "events_by_type" in summary
        assert "average_intensity" in summary
        assert "most_common_triggers" in summary
        assert "patterns_summary" in summary
        assert "predictions_summary" in summary
        assert "model_performance" in summary
        assert "timestamp" in summary
        assert isinstance(summary["total_events"], int)
        assert isinstance(summary["events_by_type"], dict)
        assert isinstance(summary["average_intensity"], float)
        assert isinstance(summary["most_common_triggers"], list)
        assert isinstance(summary["patterns_summary"], dict)
        assert isinstance(summary["predictions_summary"], dict)
        assert isinstance(summary["model_performance"], dict)

    def test_get_analytics_summary_empty_data(self):
        """Test get_analytics_summary avec données vides"""
        # Arrange
        # Pas de données

        # Act
        summary = self.ml_analyzer.get_analytics_summary()

        # Assert
        assert summary["total_events"] == 0
        assert summary["average_intensity"] == 0.0
        assert len(summary["most_common_triggers"]) == 0
        assert summary["patterns_summary"]["patterns_found"] == 0
        assert summary["predictions_summary"]["total_predictions"] == 0

    def test_train_model_success(self):
        """Test cas nominal de train_model"""
        # Arrange
        # Ajouter des données d'entraînement
        training_events = [
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=i),
                user_id="test_user",
                intensity=i % 10 + 1,
                trigger="stress" if i % 2 == 0 else "work",
            )
            for i in range(20)
        ]

        for event in training_events:
            self.ml_analyzer.track_pain_event(event)

        # Act
        result = self.ml_analyzer.train_model()

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "training_time" in result
        assert "model_accuracy" in result
        assert "features_used" in result
        assert "timestamp" in result
        assert result["status"] in ["success", "failed", "partial"]
        assert isinstance(result["training_time"], float)
        assert isinstance(result["model_accuracy"], float)
        assert isinstance(result["features_used"], list)

    def test_train_model_insufficient_data(self):
        """Test train_model avec données insuffisantes"""
        # Arrange
        # Pas assez de données d'entraînement

        # Act
        result = self.ml_analyzer.train_model()

        # Assert
        assert result["status"] == "failed"
        assert "error" in result or result["model_accuracy"] == 0.0

    def test_train_model_error_handling(self):
        """Test gestion d'erreur de train_model"""
        # Arrange
        # Corrompre les données
        self.ml_analyzer.events = [None]  # Données invalides

        # Act
        result = self.ml_analyzer.train_model()

        # Assert
        assert result["status"] == "failed"
        assert "error" in result

    def test_evaluate_model_success(self):
        """Test cas nominal de evaluate_model"""
        # Arrange
        # Ajouter des données de test
        test_events = [
            PainEvent(
                event_type=PainEventType.PAIN_ENTRY,
                timestamp=datetime.now() - timedelta(hours=i),
                user_id="test_user",
                intensity=i % 10 + 1,
                trigger="stress",
            )
            for i in range(10)
        ]

        for event in test_events:
            self.ml_analyzer.track_pain_event(event)

        # Act
        evaluation = self.ml_analyzer.evaluate_model()

        # Assert
        assert isinstance(evaluation, dict)
        assert "accuracy" in evaluation
        assert "precision" in evaluation
        assert "recall" in evaluation
        assert "f1_score" in evaluation
        assert "confusion_matrix" in evaluation
        assert "timestamp" in evaluation
        assert isinstance(evaluation["accuracy"], float)
        assert isinstance(evaluation["precision"], float)
        assert isinstance(evaluation["recall"], float)
        assert isinstance(evaluation["f1_score"], float)
        assert isinstance(evaluation["confusion_matrix"], list)

    def test_evaluate_model_no_data(self):
        """Test evaluate_model sans données"""
        # Arrange
        # Pas de données

        # Act
        evaluation = self.ml_analyzer.evaluate_model()

        # Assert
        assert evaluation["accuracy"] == 0.0
        assert evaluation["precision"] == 0.0
        assert evaluation["recall"] == 0.0
        assert evaluation["f1_score"] == 0.0
        assert len(evaluation["confusion_matrix"]) == 0

    def test_extract_features_success(self):
        """Test cas nominal de _extract_features"""
        # Arrange
        event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            user_id="test_user",
            intensity=7,
            trigger="stress",
            action="breathing",
            effectiveness=8,
        )

        # Act
        features = self.ml_analyzer._extract_features(event)

        # Assert
        assert isinstance(features, dict)
        assert "intensity" in features
        assert "hour_of_day" in features
        assert "day_of_week" in features
        assert "trigger_encoded" in features
        assert "action_encoded" in features
        assert isinstance(features["intensity"], float)
        assert isinstance(features["hour_of_day"], int)
        assert isinstance(features["day_of_week"], int)
        assert isinstance(features["trigger_encoded"], int)
        assert isinstance(features["action_encoded"], int)

    def test_extract_features_edge_cases(self):
        """Test cas limites de _extract_features"""
        # Arrange
        minimal_event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            user_id="test_user",
        )

        # Act
        features = self.ml_analyzer._extract_features(minimal_event)

        # Assert
        assert isinstance(features, dict)
        assert "intensity" in features
        assert "hour_of_day" in features
        assert "day_of_week" in features

    def test_calculate_pattern_confidence_success(self):
        """Test cas nominal de _calculate_pattern_confidence"""
        # Arrange
        pattern_data = {"occurrences": 10, "total_events": 20, "consistency": 0.8}

        # Act
        confidence = self.ml_analyzer._calculate_pattern_confidence(pattern_data)

        # Assert
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Devrait avoir une confiance élevée

    def test_calculate_pattern_confidence_low_occurrences(self):
        """Test _calculate_pattern_confidence avec peu d'occurrences"""
        # Arrange
        pattern_data = {"occurrences": 2, "total_events": 20, "consistency": 0.8}

        # Act
        confidence = self.ml_analyzer._calculate_pattern_confidence(pattern_data)

        # Assert
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
        assert confidence < 0.5  # Devrait avoir une confiance faible

    def test_calculate_pattern_confidence_edge_cases(self):
        """Test cas limites de _calculate_pattern_confidence"""
        # Arrange
        pattern_data = {"occurrences": 0, "total_events": 0, "consistency": 0.0}

        # Act
        confidence = self.ml_analyzer._calculate_pattern_confidence(pattern_data)

        # Assert
        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
        assert confidence == 0.0

    def test_generate_prediction_id_success(self):
        """Test cas nominal de _generate_prediction_id"""
        # Arrange
        context = {"trigger": "stress", "intensity": 7}

        # Act
        prediction_id = self.ml_analyzer._generate_prediction_id(context)

        # Assert
        assert isinstance(prediction_id, str)
        assert len(prediction_id) > 0
        assert "stress" in prediction_id or "7" in prediction_id

    def test_generate_prediction_id_edge_cases(self):
        """Test cas limites de _generate_prediction_id"""
        # Arrange
        empty_context = {}

        # Act
        prediction_id = self.ml_analyzer._generate_prediction_id(empty_context)

        # Assert
        assert isinstance(prediction_id, str)
        assert len(prediction_id) > 0

    def test_save_to_database_success(self):
        """Test cas nominal de _save_to_database"""
        # Arrange
        event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            user_id="test_user",
            intensity=7,
            trigger="stress",
        )

        # Act
        result = self.ml_analyzer._save_to_database(event)

        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "event_id" in result
        assert result["success"] is True
        assert isinstance(result["event_id"], str)

    def test_save_to_database_error_handling(self):
        """Test gestion d'erreur de _save_to_database"""
        # Arrange
        invalid_event = None

        # Act
        result = self.ml_analyzer._save_to_database(invalid_event)

        # Assert
        assert result["success"] is False
        assert "error" in result

    def test_load_from_database_success(self):
        """Test cas nominal de _load_from_database"""
        # Arrange
        # Ajouter un événement à la base de données
        event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            user_id="test_user",
            intensity=7,
            trigger="stress",
        )
        self.ml_analyzer._save_to_database(event)

        # Act
        events = self.ml_analyzer._load_from_database()

        # Assert
        assert isinstance(events, list)
        assert len(events) >= 1
        assert all(isinstance(e, PainEvent) for e in events)

    def test_load_from_database_empty(self):
        """Test _load_from_database avec base vide"""
        # Arrange
        # Base de données vide

        # Act
        events = self.ml_analyzer._load_from_database()

        # Assert
        assert isinstance(events, list)
        assert len(events) == 0

    def test_load_from_database_error_handling(self):
        """Test gestion d'erreur de _load_from_database"""
        # Arrange
        # Corrompre le chemin de la base de données
        self.ml_analyzer.db_path = "/invalid/path/database.db"

        # Act
        events = self.ml_analyzer._load_from_database()

        # Assert
        assert isinstance(events, list)
        assert len(events) == 0  # Devrait retourner une liste vide en cas d'erreur

    def test_get_model_status_success(self):
        """Test cas nominal de get_model_status"""
        # Arrange
        # Act
        status = self.ml_analyzer.get_model_status()

        # Assert
        assert isinstance(status, dict)
        assert "is_trained" in status
        assert "last_training" in status
        assert "model_accuracy" in status
        assert "total_predictions" in status
        assert "prediction_accuracy" in status
        assert "timestamp" in status
        assert isinstance(status["is_trained"], bool)
        assert isinstance(status["model_accuracy"], float)
        assert isinstance(status["total_predictions"], int)
        assert isinstance(status["prediction_accuracy"], float)

    def test_get_model_status_untrained(self):
        """Test get_model_status avec modèle non entraîné"""
        # Arrange
        # Modèle non entraîné

        # Act
        status = self.ml_analyzer.get_model_status()

        # Assert
        assert status["is_trained"] is False
        assert status["model_accuracy"] == 0.0
        assert status["total_predictions"] == 0
        assert status["prediction_accuracy"] == 0.0

    def test_reset_model_success(self):
        """Test cas nominal de reset_model"""
        # Arrange
        # Ajouter des données
        event = PainEvent(
            event_type=PainEventType.PAIN_ENTRY,
            timestamp=datetime.now(),
            user_id="test_user",
            intensity=7,
            trigger="stress",
        )
        self.ml_analyzer.track_pain_event(event)

        # Act
        result = self.ml_analyzer.reset_model()

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "timestamp" in result
        assert result["status"] == "success"
        assert len(self.ml_analyzer.events) == 0
        assert len(self.ml_analyzer.patterns) == 0
        assert len(self.ml_analyzer.predictions) == 0
        assert self.ml_analyzer.is_training is False
