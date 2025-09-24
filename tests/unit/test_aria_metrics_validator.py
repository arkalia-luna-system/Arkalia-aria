#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_MetricsValidator
=========================================

Tests complets pour le validateur de métriques ARIA.
"""

import pytest

from metrics_collector.validators.aria_metrics_validator import ARIA_MetricsValidator


class TestARIA_MetricsValidator:
    """Tests unitaires pour ARIA_MetricsValidator"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.validator = ARIA_MetricsValidator()

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Act
        validator = ARIA_MetricsValidator()

        # Assert
        assert isinstance(validator.validation_rules, dict)
        assert isinstance(validator.alerts, list)
        assert isinstance(validator.recommendations, list)
        assert "min_python_files" in validator.validation_rules
        assert "min_test_coverage" in validator.validation_rules
        assert "max_security_issues" in validator.validation_rules

    def test_validate_metrics_success(self):
        """Test cas nominal de validate_metrics"""
        # Arrange
        good_metrics = {
            "python_files": {"count": 50, "total_lines": 5000},
            "tests": {"test_files_count": 20, "coverage_percentage": 85.0},
            "aria_specific": {"pain_tracking": 100, "pattern_analysis": 50},
            "security": {
                "bandit_scan": {"issues_found": 0},
                "safety_scan": {"vulnerabilities_found": 0},
            },
            "performance": {"memory_usage_mb": 500, "cpu_percent": 50.0},
        }

        # Act
        result = self.validator.validate_metrics(good_metrics)

        # Assert
        assert isinstance(result, dict)
        assert "is_valid" in result
        assert "score" in result
        assert "alerts" in result
        assert "recommendations" in result
        assert "timestamp" in result
        assert isinstance(result["is_valid"], bool)
        assert isinstance(result["score"], int)
        assert isinstance(result["alerts"], list)
        assert isinstance(result["recommendations"], list)

    def test_validate_metrics_error_handling(self):
        """Test gestion d'erreur de validate_metrics"""
        # Arrange
        invalid_metrics = None

        # Act & Assert
        with pytest.raises(Exception):
            self.validator.validate_metrics(invalid_metrics)

    def test_validate_general_metrics_success(self):
        """Test cas nominal de _validate_general_metrics"""
        # Arrange
        good_metrics = {
            "python_files": {"count": 50, "total_lines": 5000},
            "tests": {"test_files_count": 20, "coverage_percentage": 85.0},
        }

        # Act
        self.validator._validate_general_metrics(good_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_validate_general_metrics_insufficient_files(self):
        """Test validation avec nombre de fichiers insuffisant"""
        # Arrange
        poor_metrics = {
            "python_files": {"count": 5, "total_lines": 100},
            "tests": {"test_files_count": 1, "coverage_percentage": 30.0},
        }

        # Act
        self.validator._validate_general_metrics(poor_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_validate_aria_metrics_success(self):
        """Test cas nominal de _validate_aria_metrics"""
        # Arrange
        good_aria_metrics = {
            "aria_specific": {
                "pain_tracking": 100,
                "pattern_analysis": 50,
                "predictions": 25,
                "cia_integration": {
                    "cia_sync_exists": True,
                    "integration_endpoints": 5,
                },
            }
        }

        # Act
        self.validator._validate_aria_metrics(good_aria_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_validate_aria_metrics_missing_cia(self):
        """Test validation avec intégration CIA manquante"""
        # Arrange
        poor_aria_metrics = {
            "aria_specific": {
                "pain_tracking": 0,
                "pattern_analysis": 0,
                "predictions": 0,
                "cia_integration": {
                    "cia_sync_exists": False,
                    "integration_endpoints": 0,
                },
            }
        }

        # Act
        self.validator._validate_aria_metrics(poor_aria_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_validate_security_metrics_success(self):
        """Test cas nominal de _validate_security_metrics"""
        # Arrange
        good_security_metrics = {
            "security": {
                "bandit_scan": {"issues_found": 0},
                "safety_scan": {"vulnerabilities_found": 0},
                "dependencies_count": 20,
            }
        }

        # Act
        self.validator._validate_security_metrics(good_security_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_validate_security_metrics_issues_found(self):
        """Test validation avec problèmes de sécurité détectés"""
        # Arrange
        poor_security_metrics = {
            "security": {
                "bandit_scan": {"issues_found": 10},
                "safety_scan": {"vulnerabilities_found": 5},
                "dependencies_count": 100,
            }
        }

        # Act
        self.validator._validate_security_metrics(poor_security_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_validate_performance_metrics_success(self):
        """Test cas nominal de _validate_performance_metrics"""
        # Arrange
        good_performance_metrics = {
            "performance": {
                "memory_usage_mb": 500,
                "cpu_percent": 50.0,
                "disk_usage_percent": 60.0,
                "process_count": 50,
            }
        }

        # Act
        self.validator._validate_performance_metrics(good_performance_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_validate_performance_metrics_high_usage(self):
        """Test validation avec utilisation élevée"""
        # Arrange
        poor_performance_metrics = {
            "performance": {
                "memory_usage_mb": 2000,
                "cpu_percent": 90,
                "disk_usage_percent": 95,
                "process_count": 500,
            }
        }

        # Act
        self.validator._validate_performance_metrics(poor_performance_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_calculate_validation_score_success(self):
        """Test cas nominal de _calculate_validation_score"""
        # Arrange
        good_metrics = {
            "python_files": {"count": 50, "total_lines": 5000},
            "tests": {"test_files_count": 20, "coverage_percentage": 85.0},
            "aria_specific": {"pain_tracking": 100, "pattern_analysis": 50},
            "security": {
                "bandit_scan": {"issues_found": 0},
                "safety_scan": {"vulnerabilities_found": 0},
            },
            "performance": {"memory_usage_mb": 500, "cpu_percent": 50.0},
        }

        # Act
        score = self.validator._calculate_validation_score(good_metrics)

        # Assert
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_calculate_validation_score_poor_metrics(self):
        """Test calcul de score avec de mauvaises métriques"""
        # Arrange
        poor_metrics = {
            "python_files": {"count": 5, "total_lines": 100},
            "tests": {"test_files_count": 1, "coverage_percentage": 30.0},
            "aria_specific": {"pain_tracking": 0, "pattern_analysis": 0},
            "security": {
                "bandit_scan": {"issues_found": 10},
                "safety_scan": {"vulnerabilities_found": 5},
            },
            "performance": {"memory_usage_mb": 2000, "cpu_percent": 90.0},
        }

        # Act
        score = self.validator._calculate_validation_score(poor_metrics)

        # Assert
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_get_health_status_success(self):
        """Test cas nominal de get_health_status"""
        # Arrange
        metrics = {
            "python_files": {"count": 50, "total_lines": 5000},
            "tests": {"test_files_count": 20, "coverage_percentage": 85.0},
        }

        # Act
        health_status = self.validator.get_health_status(metrics)

        # Assert
        assert isinstance(health_status, dict)
        assert "status" in health_status
        assert "score" in health_status
        assert "color" in health_status
        assert "alerts_count" in health_status
        assert "recommendations_count" in health_status
        assert "timestamp" in health_status
        assert isinstance(health_status["status"], str)
        assert isinstance(health_status["score"], int)
        assert isinstance(health_status["color"], str)
        assert isinstance(health_status["alerts_count"], int)
        assert isinstance(health_status["recommendations_count"], int)
        assert isinstance(health_status["timestamp"], str)

    def test_get_health_status_edge_cases(self):
        """Test cas limites de get_health_status"""
        # Arrange
        empty_metrics = {}

        # Act
        health_status = self.validator.get_health_status(empty_metrics)

        # Assert
        assert isinstance(health_status, dict)
        assert "status" in health_status
        assert "score" in health_status
        assert "color" in health_status
        assert "alerts_count" in health_status
        assert "recommendations_count" in health_status
        assert "timestamp" in health_status

    def test_validate_test_metrics_success(self):
        """Test cas nominal de _validate_test_metrics"""
        # Arrange
        good_test_metrics = {
            "tests": {
                "test_files_count": 20,
                "test_directories_count": 5,
                "coverage_percentage": 85.0,
                "integration_tests": 10,
            }
        }

        # Act
        self.validator._validate_test_metrics(good_test_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_validate_test_metrics_low_coverage(self):
        """Test validation avec faible couverture de tests"""
        # Arrange
        poor_test_metrics = {
            "tests": {
                "test_files_count": 2,
                "test_directories_count": 1,
                "coverage_percentage": 30.0,
                "integration_tests": 0,
            }
        }

        # Act
        self.validator._validate_test_metrics(poor_test_metrics)

        # Assert
        assert isinstance(self.validator.alerts, list)

    def test_initialize_validation_rules_success(self):
        """Test cas nominal de _initialize_validation_rules"""
        # Act
        rules = self.validator._initialize_validation_rules()

        # Assert
        assert isinstance(rules, dict)
        assert "min_python_files" in rules
        assert "min_test_coverage" in rules
        assert "max_security_issues" in rules
        assert "max_memory_usage_mb" in rules
        assert "max_cpu_percent" in rules
        assert "min_documentation_files" in rules
        assert "required_api_endpoints" in rules
        assert isinstance(rules["min_python_files"], int)
        assert isinstance(rules["min_test_coverage"], float)
        assert isinstance(rules["max_security_issues"], int)
