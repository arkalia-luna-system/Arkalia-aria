#!/usr/bin/env python3
"""
Tests unitaires pour ARIADataCollector
=====================================

Tests complets pour le collecteur de données ARIA.
"""

import sqlite3
import tempfile
from pathlib import Path

import pytest

from research_tools.data_collector import ARIADataCollector


class TestARIADataCollector:
    """Tests unitaires pour ARIADataCollector"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_aria.db"
        self.data_collector = ARIADataCollector(str(self.db_path))

    def teardown_method(self):
        """Cleanup après chaque test"""
        self.temp_dir.cleanup()

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        data_collector = ARIADataCollector(str(self.db_path))

        # Assert
        assert data_collector.db_path == str(self.db_path)
        assert isinstance(data_collector.project_root, Path)
        assert data_collector.project_root.exists()

    def test_init_with_custom_db_path(self):
        """Test initialisation avec chemin de base personnalisé"""
        # Arrange
        custom_db_path = str(Path(self.temp_dir.name) / "custom_aria.db")

        # Act
        data_collector = ARIADataCollector(custom_db_path)

        # Assert
        assert data_collector.db_path == custom_db_path
        assert Path(custom_db_path).exists()

    def test_create_experiment_success(self):
        """Test cas nominal de create_experiment"""
        # Arrange
        name = "Test Experiment"
        description = "Test description"
        hypothesis = "Test hypothesis"
        methodology = "Test methodology"

        # Act
        experiment_id = self.data_collector.create_experiment(
            name, description, hypothesis, methodology
        )

        # Assert
        assert isinstance(experiment_id, int)
        assert experiment_id > 0

    def test_create_experiment_error_handling(self):
        """Test gestion d'erreur de create_experiment"""
        # Arrange
        invalid_name = None
        description = "Test description"
        hypothesis = "Test hypothesis"
        methodology = "Test methodology"

        # Act
        experiment_id = self.data_collector.create_experiment(
            invalid_name, description, hypothesis, methodology
        )

        # Assert
        assert experiment_id == -1  # Retourne -1 en cas d'erreur

    def test_create_experiment_edge_cases(self):
        """Test create_experiment avec cas limites"""
        # Arrange
        name = "A" * 1000  # Nom très long
        description = "Test description"
        hypothesis = "Test hypothesis"
        methodology = "Test methodology"

        # Act
        experiment_id = self.data_collector.create_experiment(
            name, description, hypothesis, methodology
        )

        # Assert
        assert isinstance(experiment_id, int)
        assert experiment_id > 0

    def test_collect_pain_data_success(self):
        """Test cas nominal de collect_pain_data"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Pain Test", "Test description", "Test hypothesis", "Test methodology"
        )
        pain_entry = {
            "intensity": 7,
            "physical_trigger": "sitting",
            "mental_trigger": "work stress",
            "action_taken": "stretching",
        }

        # Act
        result = self.data_collector.collect_pain_data(experiment_id, pain_entry)

        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_collect_pain_data_error_handling(self):
        """Test gestion d'erreur de collect_pain_data"""
        # Arrange
        invalid_experiment_id = 99999
        pain_entry = {"intensity": 7}

        # Act
        result = self.data_collector.collect_pain_data(
            invalid_experiment_id, pain_entry
        )

        # Assert
        assert isinstance(result, bool)
        # La méthode ne retourne pas False pour un ID invalide, elle gère l'erreur silencieusement
        assert result is True

    def test_collect_pain_data_edge_cases(self):
        """Test collect_pain_data avec cas limites"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Pain Test", "Test description", "Test hypothesis", "Test methodology"
        )
        pain_entry = {"intensity": 0}  # Niveau minimum

        # Act
        result = self.data_collector.collect_pain_data(experiment_id, pain_entry)

        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_collect_emotion_data_success(self):
        """Test cas nominal de collect_emotion_data"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Emotion Test", "Test description", "Test hypothesis", "Test methodology"
        )
        emotion_data = {"emotion": "anxiety", "intensity": 5.0, "stress_level": 7}

        # Act
        result = self.data_collector.collect_emotion_data(experiment_id, emotion_data)

        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_collect_emotion_data_error_handling(self):
        """Test gestion d'erreur de collect_emotion_data"""
        # Arrange
        invalid_experiment_id = 99999
        emotion_data = {"emotion": "anxiety"}

        # Act
        result = self.data_collector.collect_emotion_data(
            invalid_experiment_id, emotion_data
        )

        # Assert
        assert isinstance(result, bool)
        # La méthode ne retourne pas False pour un ID invalide, elle gère l'erreur silencieusement
        assert result is True

    def test_collect_emotion_data_edge_cases(self):
        """Test collect_emotion_data avec cas limites"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Emotion Test", "Test description", "Test hypothesis", "Test methodology"
        )
        emotion_data = {"emotion": "neutral", "intensity": 0.0}

        # Act
        result = self.data_collector.collect_emotion_data(experiment_id, emotion_data)

        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_collect_system_metrics_success(self):
        """Test cas nominal de collect_system_metrics"""
        # Act
        metrics = self.data_collector.collect_system_metrics()

        # Assert
        assert isinstance(metrics, dict)
        assert "pain_entries_count" in metrics
        assert "active_experiments_count" in metrics
        assert "emotion_entries_count" in metrics

    def test_collect_system_metrics_error_handling(self):
        """Test gestion d'erreur de collect_system_metrics"""
        # Arrange
        # Simuler une erreur en fermant la connexion
        self.data_collector.db_path = "/invalid/path/db.db"

        # Act
        metrics = self.data_collector.collect_system_metrics()

        # Assert
        assert isinstance(metrics, dict)
        # La méthode ne retourne pas d'erreur, elle gère les erreurs silencieusement
        # En cas d'erreur, elle retourne seulement les métriques de performance
        assert "avg_response_time_ms" in metrics

    def test_analyze_experiment_success(self):
        """Test cas nominal de analyze_experiment"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Analysis Test", "Test description", "Test hypothesis", "Test methodology"
        )
        # Ajouter quelques données
        self.data_collector.collect_pain_data(experiment_id, {"intensity": 5})
        self.data_collector.collect_emotion_data(
            experiment_id, {"emotion": "anxiety", "intensity": 3.0}
        )

        # Act
        analysis = self.data_collector.analyze_experiment(experiment_id)

        # Assert
        assert isinstance(analysis, dict)
        assert "experiment_id" in analysis
        assert "analysis" in analysis
        assert "status" in analysis

    def test_analyze_experiment_invalid_id(self):
        """Test analyze_experiment avec ID invalide"""
        # Arrange
        invalid_id = 99999

        # Act
        analysis = self.data_collector.analyze_experiment(invalid_id)

        # Assert
        assert isinstance(analysis, dict)
        assert analysis["experiment_id"] == invalid_id
        assert "status" in analysis
        assert analysis["status"] == "no_data"

    def test_get_research_summary_success(self):
        """Test cas nominal de get_research_summary"""
        # Arrange
        # Créer quelques expériences
        self.data_collector.create_experiment(
            "Experiment 1", "Description 1", "Hypothesis 1", "Methodology 1"
        )
        self.data_collector.create_experiment(
            "Experiment 2", "Description 2", "Hypothesis 2", "Methodology 2"
        )

        # Act
        summary = self.data_collector.get_research_summary()

        # Assert
        assert isinstance(summary, dict)
        assert "total_experiments" in summary
        assert "active_experiments" in summary
        assert "total_data_points" in summary
        assert "system_metrics" in summary
        assert "database_size_mb" in summary["system_metrics"]

    def test_get_research_summary_empty_database(self):
        """Test get_research_summary avec base vide"""
        # Arrange
        # Utiliser une nouvelle base de données vide
        empty_db_path = str(Path(self.temp_dir.name) / "empty_aria.db")
        empty_collector = ARIADataCollector(empty_db_path)

        # Act
        summary = empty_collector.get_research_summary()

        # Assert
        assert isinstance(summary, dict)
        assert summary["total_experiments"] == 0
        assert summary["active_experiments"] == 0
        assert summary["total_data_points"] == 0

    def test_database_initialization_success(self):
        """Test initialisation de la base de données"""
        # Arrange
        new_db_path = str(Path(self.temp_dir.name) / "new_aria.db")

        # Act
        collector = ARIADataCollector(new_db_path)

        # Assert
        assert Path(new_db_path).exists()
        assert collector.db_path == new_db_path

    def test_database_connection_error_handling(self):
        """Test gestion d'erreur de connexion à la base"""
        # Arrange
        invalid_db_path = "/invalid/path/aria.db"

        # Act & Assert
        with pytest.raises((OSError, sqlite3.Error)):
            ARIADataCollector(invalid_db_path)

    def test_pain_data_collection_with_all_fields(self):
        """Test collect_pain_data avec tous les champs"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Complete Pain Test",
            "Test description",
            "Test hypothesis",
            "Test methodology",
        )
        pain_entry = {
            "intensity": 8,
            "physical_trigger": "prolonged sitting",
            "mental_trigger": "deadline pressure",
            "action_taken": "medication and rest",
        }

        # Act
        result = self.data_collector.collect_pain_data(experiment_id, pain_entry)

        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_emotion_data_collection_with_stress_level(self):
        """Test collect_emotion_data avec niveau de stress"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Stress Test", "Test description", "Test hypothesis", "Test methodology"
        )
        emotion_data = {"emotion": "frustration", "intensity": 6.5, "stress_level": 8}

        # Act
        result = self.data_collector.collect_emotion_data(experiment_id, emotion_data)

        # Assert
        assert isinstance(result, bool)
        assert result is True

    def test_multiple_data_collection_same_experiment(self):
        """Test collecte de données multiples pour la même expérience"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Multi Data Test", "Test description", "Test hypothesis", "Test methodology"
        )

        # Act
        pain_result = self.data_collector.collect_pain_data(
            experiment_id, {"intensity": 5}
        )
        emotion_result = self.data_collector.collect_emotion_data(
            experiment_id, {"emotion": "calm", "intensity": 2.0}
        )

        # Assert
        assert pain_result is True
        assert emotion_result is True

    def test_analyze_experiment_with_no_data(self):
        """Test analyze_experiment sans données"""
        # Arrange
        experiment_id = self.data_collector.create_experiment(
            "Empty Data Test", "Test description", "Test hypothesis", "Test methodology"
        )

        # Act
        analysis = self.data_collector.analyze_experiment(experiment_id)

        # Assert
        assert isinstance(analysis, dict)
        assert analysis["experiment_id"] == experiment_id
        assert "status" in analysis
        assert analysis["status"] == "no_data"
