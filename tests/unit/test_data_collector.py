#!/usr/bin/env python3
"""
Tests unitaires pour ARIADataCollector
======================================

Tests complets pour le collecteur de données ARIA.
"""

import os
import tempfile
from unittest.mock import patch

import pytest

from research_tools.data_collector import ARIADataCollector


class TestARIADataCollector:
    """Tests unitaires pour ARIADataCollector"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.data_collector = ARIADataCollector(self.temp_db.name)

    def teardown_method(self):
        """Cleanup après chaque test"""
        os.unlink(self.temp_db.name)

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        data_collector = ARIADataCollector("test.db")

        # Assert
        assert data_collector.db_path == "test.db"
        from pathlib import Path

        assert isinstance(data_collector.project_root, Path)
        assert data_collector.project_root.exists()

    def test_init_with_env_db(self):
        """Test initialisation avec base de données d'environnement"""
        # Arrange
        with patch.dict(os.environ, {"ARIA_RESEARCH_DB": "env_test.db"}):
            # Act
            data_collector = ARIADataCollector()

            # Assert
            assert data_collector.db_path == "env_test.db"

    def test_init_with_aria_db_path(self):
        """Test initialisation avec ARIA_DB_PATH"""
        # Arrange
        with patch.dict(os.environ, {"ARIA_DB_PATH": "aria_test.db"}):
            # Act
            data_collector = ARIADataCollector()

            # Assert
            assert data_collector.db_path == "aria_test.db"

    def test_create_experiment_success(self):
        """Test cas nominal de create_experiment"""
        # Arrange
        experiment_data = {
            "name": "Test Experiment",
            "description": "Test experiment for pain tracking",
            "hypothesis": "Stress increases pain intensity",
            "methodology": "Daily pain tracking with stress monitoring",
        }

        # Act
        result = self.data_collector.create_experiment(experiment_data)

        # Assert
        assert isinstance(result, dict)
        assert "experiment_id" in result
        assert "status" in result
        assert "timestamp" in result
        assert result["status"] == "success"
        assert isinstance(result["experiment_id"], int)
        assert result["experiment_id"] > 0

    def test_create_experiment_error_handling(self):
        """Test gestion d'erreur de create_experiment"""
        # Arrange
        invalid_data = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.data_collector.create_experiment(invalid_data)

    def test_create_experiment_edge_cases(self):
        """Test cas limites de create_experiment"""
        # Arrange
        minimal_data = {"name": "Minimal Experiment"}

        # Act
        result = self.data_collector.create_experiment(minimal_data)

        # Assert
        assert result["status"] == "success"
        assert isinstance(result["experiment_id"], int)

    def test_collect_pain_data_success(self):
        """Test cas nominal de collect_pain_data"""
        # Arrange
        pain_data = {
            "experiment_id": 1,
            "user_id": "test_user",
            "intensity": 7,
            "trigger": "stress",
            "location": "head",
            "duration": 30,
            "action_taken": "breathing",
            "effectiveness": 8,
            "notes": "Stressful day at work",
        }

        # Act
        result = self.data_collector.collect_pain_data(pain_data)

        # Assert
        assert isinstance(result, dict)
        assert "data_id" in result
        assert "status" in result
        assert "timestamp" in result
        assert result["status"] == "success"
        assert isinstance(result["data_id"], int)
        assert result["data_id"] > 0

    def test_collect_pain_data_error_handling(self):
        """Test gestion d'erreur de collect_pain_data"""
        # Arrange
        invalid_data = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.data_collector.collect_pain_data(invalid_data)

    def test_collect_pain_data_edge_cases(self):
        """Test cas limites de collect_pain_data"""
        # Arrange
        minimal_data = {"experiment_id": 1, "user_id": "test_user", "intensity": 5}

        # Act
        result = self.data_collector.collect_pain_data(minimal_data)

        # Assert
        assert result["status"] == "success"
        assert isinstance(result["data_id"], int)

    def test_collect_emotion_data_success(self):
        """Test cas nominal de collect_emotion_data"""
        # Arrange
        emotion_data = {
            "experiment_id": 1,
            "user_id": "test_user",
            "emotion": "stressed",
            "intensity": 0.8,
            "pain_correlation": 0.7,
            "trigger": "work_stress",
            "duration": 45,
            "notes": "Feeling overwhelmed",
        }

        # Act
        result = self.data_collector.collect_emotion_data(emotion_data)

        # Assert
        assert isinstance(result, dict)
        assert "data_id" in result
        assert "status" in result
        assert "timestamp" in result
        assert result["status"] == "success"
        assert isinstance(result["data_id"], int)
        assert result["data_id"] > 0

    def test_collect_emotion_data_error_handling(self):
        """Test gestion d'erreur de collect_emotion_data"""
        # Arrange
        invalid_data = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.data_collector.collect_emotion_data(invalid_data)

    def test_collect_emotion_data_edge_cases(self):
        """Test cas limites de collect_emotion_data"""
        # Arrange
        minimal_data = {
            "experiment_id": 1,
            "user_id": "test_user",
            "emotion": "neutral",
        }

        # Act
        result = self.data_collector.collect_emotion_data(minimal_data)

        # Assert
        assert result["status"] == "success"
        assert isinstance(result["data_id"], int)

    def test_get_research_summary_success(self):
        """Test cas nominal de get_research_summary"""
        # Arrange
        # Créer un expériment et ajouter des données
        experiment_data = {
            "name": "Test Experiment",
            "description": "Test experiment",
            "hypothesis": "Test hypothesis",
            "methodology": "Test methodology",
        }
        experiment_result = self.data_collector.create_experiment(experiment_data)
        experiment_id = experiment_result["experiment_id"]

        # Ajouter des données de douleur
        pain_data = {
            "experiment_id": experiment_id,
            "user_id": "test_user",
            "intensity": 7,
            "trigger": "stress",
        }
        self.data_collector.collect_pain_data(pain_data)

        # Ajouter des données d'émotion
        emotion_data = {
            "experiment_id": experiment_id,
            "user_id": "test_user",
            "emotion": "stressed",
            "intensity": 0.8,
        }
        self.data_collector.collect_emotion_data(emotion_data)

        # Act
        summary = self.data_collector.get_research_summary()

        # Assert
        assert isinstance(summary, dict)
        assert "total_experiments" in summary
        assert "active_experiments" in summary
        assert "total_pain_data_points" in summary
        assert "total_emotion_data_points" in summary
        assert "experiments_summary" in summary
        assert "data_quality_metrics" in summary
        assert "timestamp" in summary
        assert isinstance(summary["total_experiments"], int)
        assert isinstance(summary["active_experiments"], int)
        assert isinstance(summary["total_pain_data_points"], int)
        assert isinstance(summary["total_emotion_data_points"], int)
        assert isinstance(summary["experiments_summary"], list)
        assert isinstance(summary["data_quality_metrics"], dict)

    def test_get_research_summary_empty_data(self):
        """Test get_research_summary avec données vides"""
        # Arrange
        # Pas de données

        # Act
        summary = self.data_collector.get_research_summary()

        # Assert
        assert summary["total_experiments"] == 0
        assert summary["active_experiments"] == 0
        assert summary["total_pain_data_points"] == 0
        assert summary["total_emotion_data_points"] == 0
        assert len(summary["experiments_summary"]) == 0

    def test_get_experiment_data_success(self):
        """Test cas nominal de get_experiment_data"""
        # Arrange
        # Créer un expériment
        experiment_data = {
            "name": "Test Experiment",
            "description": "Test experiment",
            "hypothesis": "Test hypothesis",
            "methodology": "Test methodology",
        }
        experiment_result = self.data_collector.create_experiment(experiment_data)
        experiment_id = experiment_result["experiment_id"]

        # Ajouter des données
        pain_data = {
            "experiment_id": experiment_id,
            "user_id": "test_user",
            "intensity": 7,
            "trigger": "stress",
        }
        self.data_collector.collect_pain_data(pain_data)

        # Act
        data = self.data_collector.get_experiment_data(experiment_id)

        # Assert
        assert isinstance(data, dict)
        assert "experiment_info" in data
        assert "pain_data" in data
        assert "emotion_data" in data
        assert "data_summary" in data
        assert "timestamp" in data
        assert isinstance(data["pain_data"], list)
        assert isinstance(data["emotion_data"], list)
        assert isinstance(data["data_summary"], dict)
        assert len(data["pain_data"]) >= 1
        assert data["pain_data"][0]["intensity"] == 7

    def test_get_experiment_data_invalid_id(self):
        """Test get_experiment_data avec ID invalide"""
        # Arrange
        invalid_id = 99999

        # Act
        data = self.data_collector.get_experiment_data(invalid_id)

        # Assert
        assert data["experiment_info"] is None
        assert len(data["pain_data"]) == 0
        assert len(data["emotion_data"]) == 0

    def test_get_experiment_data_error_handling(self):
        """Test gestion d'erreur de get_experiment_data"""
        # Arrange
        invalid_id = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.data_collector.get_experiment_data(invalid_id)

    def test_export_data_success(self):
        """Test cas nominal de export_data"""
        # Arrange
        # Créer des données
        experiment_data = {
            "name": "Test Experiment",
            "description": "Test experiment",
            "hypothesis": "Test hypothesis",
            "methodology": "Test methodology",
        }
        experiment_result = self.data_collector.create_experiment(experiment_data)
        experiment_id = experiment_result["experiment_id"]

        pain_data = {
            "experiment_id": experiment_id,
            "user_id": "test_user",
            "intensity": 7,
            "trigger": "stress",
        }
        self.data_collector.collect_pain_data(pain_data)

        # Act
        export_result = self.data_collector.export_data(experiment_id, "csv")

        # Assert
        assert isinstance(export_result, dict)
        assert "status" in export_result
        assert "file_path" in export_result
        assert "data_count" in export_result
        assert "timestamp" in export_result
        assert export_result["status"] == "success"
        assert isinstance(export_result["file_path"], str)
        assert isinstance(export_result["data_count"], int)
        assert export_result["data_count"] > 0

    def test_export_data_json_format(self):
        """Test export_data avec format JSON"""
        # Arrange
        # Créer des données
        experiment_data = {
            "name": "Test Experiment",
            "description": "Test experiment",
            "hypothesis": "Test hypothesis",
            "methodology": "Test methodology",
        }
        experiment_result = self.data_collector.create_experiment(experiment_data)
        experiment_id = experiment_result["experiment_id"]

        pain_data = {
            "experiment_id": experiment_id,
            "user_id": "test_user",
            "intensity": 7,
            "trigger": "stress",
        }
        self.data_collector.collect_pain_data(pain_data)

        # Act
        export_result = self.data_collector.export_data(experiment_id, "json")

        # Assert
        assert export_result["status"] == "success"
        assert export_result["file_path"].endswith(".json")
        assert export_result["data_count"] > 0

    def test_export_data_error_handling(self):
        """Test gestion d'erreur de export_data"""
        # Arrange
        invalid_id = None
        invalid_format = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.data_collector.export_data(invalid_id, invalid_format)

    def test_export_data_edge_cases(self):
        """Test cas limites de export_data"""
        # Arrange
        experiment_id = 1
        unsupported_format = "xml"

        # Act
        export_result = self.data_collector.export_data(
            experiment_id, unsupported_format
        )

        # Assert
        assert export_result["status"] == "error"
        assert "error" in export_result

    def test_validate_data_quality_success(self):
        """Test cas nominal de validate_data_quality"""
        # Arrange
        # Créer des données avec différentes qualités
        experiment_data = {
            "name": "Test Experiment",
            "description": "Test experiment",
            "hypothesis": "Test hypothesis",
            "methodology": "Test methodology",
        }
        experiment_result = self.data_collector.create_experiment(experiment_data)
        experiment_id = experiment_result["experiment_id"]

        # Données de bonne qualité
        good_pain_data = {
            "experiment_id": experiment_id,
            "user_id": "test_user",
            "intensity": 7,
            "trigger": "stress",
            "location": "head",
            "duration": 30,
            "action_taken": "breathing",
            "effectiveness": 8,
            "notes": "Complete data",
        }
        self.data_collector.collect_pain_data(good_pain_data)

        # Données de qualité médiocre
        poor_pain_data = {
            "experiment_id": experiment_id,
            "user_id": "test_user",
            "intensity": 5,
            # Données incomplètes
        }
        self.data_collector.collect_pain_data(poor_pain_data)

        # Act
        quality_report = self.data_collector.validate_data_quality(experiment_id)

        # Assert
        assert isinstance(quality_report, dict)
        assert "experiment_id" in quality_report
        assert "overall_quality_score" in quality_report
        assert "completeness_score" in quality_report
        assert "consistency_score" in quality_report
        assert "accuracy_score" in quality_report
        assert "issues_found" in quality_report
        assert "recommendations" in quality_report
        assert "timestamp" in quality_report
        assert isinstance(quality_report["overall_quality_score"], float)
        assert 0.0 <= quality_report["overall_quality_score"] <= 100.0
        assert isinstance(quality_report["completeness_score"], float)
        assert isinstance(quality_report["consistency_score"], float)
        assert isinstance(quality_report["accuracy_score"], float)
        assert isinstance(quality_report["issues_found"], list)
        assert isinstance(quality_report["recommendations"], list)

    def test_validate_data_quality_invalid_id(self):
        """Test validate_data_quality avec ID invalide"""
        # Arrange
        invalid_id = 99999

        # Act
        quality_report = self.data_collector.validate_data_quality(invalid_id)

        # Assert
        assert quality_report["experiment_id"] == invalid_id
        assert quality_report["overall_quality_score"] == 0.0
        assert len(quality_report["issues_found"]) == 0
        assert len(quality_report["recommendations"]) == 0

    def test_validate_data_quality_error_handling(self):
        """Test gestion d'erreur de validate_data_quality"""
        # Arrange
        invalid_id = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.data_collector.validate_data_quality(invalid_id)

    def test_get_data_statistics_success(self):
        """Test cas nominal de get_data_statistics"""
        # Arrange
        # Créer des données
        experiment_data = {
            "name": "Test Experiment",
            "description": "Test experiment",
            "hypothesis": "Test hypothesis",
            "methodology": "Test methodology",
        }
        experiment_result = self.data_collector.create_experiment(experiment_data)
        experiment_id = experiment_result["experiment_id"]

        # Ajouter des données variées
        for i in range(10):
            pain_data = {
                "experiment_id": experiment_id,
                "user_id": f"user_{i}",
                "intensity": i % 10 + 1,
                "trigger": "stress" if i % 2 == 0 else "work",
            }
            self.data_collector.collect_pain_data(pain_data)

        # Act
        statistics = self.data_collector.get_data_statistics()

        # Assert
        assert isinstance(statistics, dict)
        assert "total_experiments" in statistics
        assert "total_pain_data_points" in statistics
        assert "total_emotion_data_points" in statistics
        assert "average_pain_intensity" in statistics
        assert "most_common_triggers" in statistics
        assert "data_collection_timeline" in statistics
        assert "user_statistics" in statistics
        assert "timestamp" in statistics
        assert isinstance(statistics["total_experiments"], int)
        assert isinstance(statistics["total_pain_data_points"], int)
        assert isinstance(statistics["total_emotion_data_points"], int)
        assert isinstance(statistics["average_pain_intensity"], float)
        assert isinstance(statistics["most_common_triggers"], list)
        assert isinstance(statistics["data_collection_timeline"], list)
        assert isinstance(statistics["user_statistics"], dict)

    def test_get_data_statistics_empty_data(self):
        """Test get_data_statistics avec données vides"""
        # Arrange
        # Pas de données

        # Act
        statistics = self.data_collector.get_data_statistics()

        # Assert
        assert statistics["total_experiments"] == 0
        assert statistics["total_pain_data_points"] == 0
        assert statistics["total_emotion_data_points"] == 0
        assert statistics["average_pain_intensity"] == 0.0
        assert len(statistics["most_common_triggers"]) == 0
        assert len(statistics["data_collection_timeline"]) == 0

    def test_backup_database_success(self):
        """Test cas nominal de backup_database"""
        # Arrange
        backup_path = tempfile.mktemp(suffix=".db")

        # Act
        result = self.data_collector.backup_database(backup_path)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "backup_path" in result
        assert "backup_size" in result
        assert "timestamp" in result
        assert result["status"] == "success"
        assert result["backup_path"] == backup_path
        assert isinstance(result["backup_size"], int)
        assert result["backup_size"] > 0

        # Cleanup
        os.unlink(backup_path)

    def test_backup_database_error_handling(self):
        """Test gestion d'erreur de backup_database"""
        # Arrange
        invalid_path = "/invalid/path/backup.db"

        # Act
        result = self.data_collector.backup_database(invalid_path)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_backup_database_edge_cases(self):
        """Test cas limites de backup_database"""
        # Arrange
        empty_path = ""

        # Act
        result = self.data_collector.backup_database(empty_path)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_restore_database_success(self):
        """Test cas nominal de restore_database"""
        # Arrange
        # Créer une sauvegarde
        backup_path = tempfile.mktemp(suffix=".db")
        self.data_collector.backup_database(backup_path)

        # Act
        result = self.data_collector.restore_database(backup_path)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "restore_path" in result
        assert "timestamp" in result
        assert result["status"] == "success"
        assert result["restore_path"] == backup_path

        # Cleanup
        os.unlink(backup_path)

    def test_restore_database_error_handling(self):
        """Test gestion d'erreur de restore_database"""
        # Arrange
        invalid_path = "/invalid/path/backup.db"

        # Act
        result = self.data_collector.restore_database(invalid_path)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_restore_database_edge_cases(self):
        """Test cas limites de restore_database"""
        # Arrange
        empty_path = ""

        # Act
        result = self.data_collector.restore_database(empty_path)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_cleanup_old_data_success(self):
        """Test cas nominal de cleanup_old_data"""
        # Arrange
        days_threshold = 30

        # Act
        result = self.data_collector.cleanup_old_data(days_threshold)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "records_deleted" in result
        assert "cleanup_date" in result
        assert "timestamp" in result
        assert result["status"] == "success"
        assert isinstance(result["records_deleted"], int)
        assert isinstance(result["cleanup_date"], str)

    def test_cleanup_old_data_error_handling(self):
        """Test gestion d'erreur de cleanup_old_data"""
        # Arrange
        invalid_threshold = None

        # Act & Assert
        with pytest.raises(ValueError):
            self.data_collector.cleanup_old_data(invalid_threshold)

    def test_cleanup_old_data_edge_cases(self):
        """Test cas limites de cleanup_old_data"""
        # Arrange
        zero_threshold = 0

        # Act
        result = self.data_collector.cleanup_old_data(zero_threshold)

        # Assert
        assert result["status"] == "success"
        assert isinstance(result["records_deleted"], int)

    def test_get_database_info_success(self):
        """Test cas nominal de get_database_info"""
        # Arrange
        # Act
        info = self.data_collector.get_database_info()

        # Assert
        assert isinstance(info, dict)
        assert "database_path" in info
        assert "database_size" in info
        assert "tables_count" in info
        assert "total_records" in info
        assert "last_backup" in info
        assert "creation_date" in info
        assert "timestamp" in info
        assert isinstance(info["database_size"], int)
        assert isinstance(info["tables_count"], int)
        assert isinstance(info["total_records"], int)
        assert isinstance(info["creation_date"], str)

    def test_get_database_info_error_handling(self):
        """Test gestion d'erreur de get_database_info"""
        # Arrange
        # Corrompre le chemin de la base de données
        self.data_collector.db_path = "/invalid/path/database.db"

        # Act
        info = self.data_collector.get_database_info()

        # Assert
        assert info["database_size"] == 0
        assert info["tables_count"] == 0
        assert info["total_records"] == 0
        assert info["creation_date"] == "unknown"

    def test_close_connection_success(self):
        """Test cas nominal de close_connection"""
        # Arrange
        # Act
        result = self.data_collector.close_connection()

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "timestamp" in result
        assert result["status"] == "success"

    def test_close_connection_error_handling(self):
        """Test gestion d'erreur de close_connection"""
        # Arrange
        # Corrompre la connexion
        self.data_collector.db_path = "/invalid/path/database.db"

        # Act
        result = self.data_collector.close_connection()

        # Assert
        assert result["status"] == "success"  # Devrait gérer gracieusement
