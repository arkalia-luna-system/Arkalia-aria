#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_MetricsCollector
==========================================

Tests complets pour le collecteur de métriques ARIA.
"""

import tempfile
from pathlib import Path
from unittest.mock import patch

from metrics_collector.collectors.aria_metrics_collector import ARIA_MetricsCollector


class TestARIA_MetricsCollector:
    """Tests unitaires pour ARIA_MetricsCollector"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.collector = ARIA_MetricsCollector(".")

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange
        project_root = "."

        # Act
        collector = ARIA_MetricsCollector(project_root)

        # Assert
        assert collector.project_root == Path(".").resolve()
        assert isinstance(collector.exclude_patterns, set)
        assert "__pycache__" in collector.exclude_patterns
        assert "venv" in collector.exclude_patterns
        assert ".pytest_cache" in collector.exclude_patterns

    def test_init_with_custom_root(self):
        """Test initialisation avec racine personnalisée"""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            # Act
            collector = ARIA_MetricsCollector(temp_dir)

            # Assert
            assert collector.project_root == Path(temp_dir).resolve()

    def test_collect_all_metrics_success(self):
        """Test cas nominal de collect_all_metrics"""
        # Act
        metrics = self.collector.collect_all_metrics()

        # Assert
        assert isinstance(metrics, dict)
        assert "project_info" in metrics
        assert "python_files" in metrics
        assert "aria_specific" in metrics
        assert "ml_models" in metrics
        assert "api_endpoints" in metrics
        assert "tests" in metrics
        assert "security" in metrics
        assert "performance" in metrics

    def test_collect_all_metrics_error_handling(self):
        """Test gestion d'erreur de collect_all_metrics"""
        # Arrange
        with patch.object(
            self.collector,
            "_collect_project_info",
            return_value={"error": "Test error"},
        ):
            # Act
            metrics = self.collector.collect_all_metrics()

            # Assert
            assert isinstance(metrics, dict)
            assert "project_info" in metrics

    def test_collect_python_metrics_success(self):
        """Test cas nominal de _collect_python_metrics"""
        # Act
        python_metrics = self.collector._collect_python_metrics()

        # Assert
        assert isinstance(python_metrics, dict)
        assert "count" in python_metrics
        assert "total_lines" in python_metrics
        assert "files" in python_metrics
        assert isinstance(python_metrics["count"], int)
        assert isinstance(python_metrics["total_lines"], int)
        assert isinstance(python_metrics["files"], list)

    def test_collect_python_metrics_edge_cases(self):
        """Test cas limites de _collect_python_metrics"""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            collector = ARIA_MetricsCollector(temp_dir)

            # Act
            python_metrics = collector._collect_python_metrics()

            # Assert
            assert isinstance(python_metrics, dict)
            assert python_metrics["count"] == 0
            assert python_metrics["total_lines"] == 0

    def test_collect_test_metrics_success(self):
        """Test cas nominal de _collect_test_metrics"""
        # Act
        test_metrics = self.collector._collect_test_metrics()

        # Assert
        assert isinstance(test_metrics, dict)
        assert "test_files_count" in test_metrics
        assert "test_directories_count" in test_metrics
        assert "coverage_percentage" in test_metrics
        assert "integration_tests" in test_metrics
        assert isinstance(test_metrics["test_files_count"], int)
        assert isinstance(test_metrics["test_directories_count"], int)
        assert isinstance(test_metrics["coverage_percentage"], float)
        assert isinstance(test_metrics["integration_tests"], int)

    def test_get_test_coverage_success(self):
        """Test cas nominal de _get_test_coverage"""
        # Act
        coverage = self.collector._get_test_coverage()

        # Assert
        assert isinstance(coverage, float)
        assert 0.0 <= coverage <= 100.0

    def test_get_test_coverage_error_handling(self):
        """Test gestion d'erreur de _get_test_coverage"""
        # Arrange
        with patch("subprocess.run", side_effect=Exception("Test error")):
            # Act
            coverage = self.collector._get_test_coverage()

            # Assert
            assert coverage == 0.0

    def test_collect_security_metrics_success(self):
        """Test cas nominal de _collect_security_metrics"""
        # Act
        security_metrics = self.collector._collect_security_metrics()

        # Assert
        assert isinstance(security_metrics, dict)
        assert "bandit_scan" in security_metrics
        assert "safety_scan" in security_metrics
        assert "dependencies_count" in security_metrics
        assert "vulnerabilities" in security_metrics
        assert isinstance(security_metrics["bandit_scan"], dict)
        assert isinstance(security_metrics["safety_scan"], dict)
        assert isinstance(security_metrics["dependencies_count"], int)
        assert isinstance(security_metrics["vulnerabilities"], dict)

    def test_run_bandit_scan_success(self):
        """Test cas nominal de _run_bandit_scan"""
        # Act
        bandit_result = self.collector._run_bandit_scan()

        # Assert
        assert isinstance(bandit_result, dict)
        assert "status" in bandit_result
        assert "issues_found" in bandit_result
        assert bandit_result["status"] in [
            "skipped_during_tests",
            "skipped",
            "completed",
            "failed",
        ]

    def test_run_bandit_scan_error_handling(self):
        """Test gestion d'erreur de _run_bandit_scan"""
        # Act
        bandit_result = self.collector._run_bandit_scan()

        # Assert
        assert isinstance(bandit_result, dict)
        assert "status" in bandit_result
        assert "issues_found" in bandit_result

    def test_run_safety_scan_success(self):
        """Test cas nominal de _run_safety_scan"""
        # Act
        safety_result = self.collector._run_safety_scan()

        # Assert
        assert isinstance(safety_result, dict)
        assert "status" in safety_result
        assert "vulnerabilities_found" in safety_result
        assert safety_result["status"] in [
            "skipped_during_tests",
            "skipped",
            "completed",
            "failed",
        ]

    def test_run_safety_scan_error_handling(self):
        """Test gestion d'erreur de _run_safety_scan"""
        # Act
        safety_result = self.collector._run_safety_scan()

        # Assert
        assert isinstance(safety_result, dict)
        assert "status" in safety_result
        assert "vulnerabilities_found" in safety_result

    def test_collect_performance_metrics_success(self):
        """Test cas nominal de _collect_performance_metrics"""
        # Act
        perf_metrics = self.collector._collect_performance_metrics()

        # Assert
        assert isinstance(perf_metrics, dict)
        assert "memory_usage_mb" in perf_metrics
        assert "cpu_percent" in perf_metrics
        assert "disk_usage_percent" in perf_metrics
        assert "process_count" in perf_metrics
        assert isinstance(perf_metrics["memory_usage_mb"], float)
        assert isinstance(perf_metrics["cpu_percent"], float)
        assert isinstance(perf_metrics["disk_usage_percent"], float)
        assert isinstance(perf_metrics["process_count"], int)

    def test_should_exclude_file_success(self):
        """Test cas nominal de _should_exclude_file"""
        # Arrange
        test_file = Path("__pycache__/test.py")

        # Act
        should_exclude = self.collector._should_exclude_file(test_file)

        # Assert
        assert should_exclude is True

    def test_should_exclude_file_edge_cases(self):
        """Test cas limites de _should_exclude_file"""
        # Arrange
        test_file = Path("src/main.py")

        # Act
        should_exclude = self.collector._should_exclude_file(test_file)

        # Assert
        assert should_exclude is False

    def test_collect_project_info_success(self):
        """Test cas nominal de _collect_project_info"""
        # Act
        project_info = self.collector._collect_project_info()

        # Assert
        assert isinstance(project_info, dict)
        assert "name" in project_info
        assert "root_path" in project_info
        assert "python_version" in project_info
        assert "version" in project_info
        assert isinstance(project_info["name"], str)
        assert isinstance(project_info["root_path"], str)
        assert isinstance(project_info["python_version"], str)
        assert isinstance(project_info["version"], str)

    def test_collect_aria_specific_metrics_success(self):
        """Test cas nominal de _collect_aria_specific_metrics"""
        # Act
        aria_metrics = self.collector._collect_aria_specific_metrics()

        # Assert
        assert isinstance(aria_metrics, dict)
        assert "pain_tracking" in aria_metrics
        assert "pattern_analysis" in aria_metrics
        assert "predictions" in aria_metrics
        assert "cia_integration" in aria_metrics
        assert isinstance(aria_metrics["pain_tracking"], int)
        assert isinstance(aria_metrics["pattern_analysis"], int)
        assert isinstance(aria_metrics["predictions"], int)
        assert isinstance(aria_metrics["cia_integration"], dict)

    def test_collect_ml_metrics_success(self):
        """Test cas nominal de _collect_ml_metrics"""
        # Act
        ml_metrics = self.collector._collect_ml_metrics()

        # Assert
        assert isinstance(ml_metrics, dict)
        assert "ml_files_count" in ml_metrics
        assert "model_files_count" in ml_metrics
        assert "prediction_engine_status" in ml_metrics
        assert "emotion_analyzer_status" in ml_metrics
        assert isinstance(ml_metrics["ml_files_count"], int)
        assert isinstance(ml_metrics["model_files_count"], int)
        assert isinstance(ml_metrics["prediction_engine_status"], bool)
        assert isinstance(ml_metrics["emotion_analyzer_status"], bool)

    def test_collect_api_metrics_success(self):
        """Test cas nominal de _collect_api_metrics"""
        # Act
        api_metrics = self.collector._collect_api_metrics()

        # Assert
        assert isinstance(api_metrics, dict)
        assert "api_files_count" in api_metrics
        assert "endpoints_count" in api_metrics
        assert "pain_api_endpoints" in api_metrics
        assert "cia_sync_endpoints" in api_metrics
        assert isinstance(api_metrics["api_files_count"], int)
        assert isinstance(api_metrics["endpoints_count"], int)
        assert isinstance(api_metrics["pain_api_endpoints"], int)
        assert isinstance(api_metrics["cia_sync_endpoints"], int)

    def test_count_pain_entries_success(self):
        """Test cas nominal de _count_pain_entries"""
        # Act
        count = self.collector._count_pain_entries()

        # Assert
        assert isinstance(count, int)
        assert count >= 0

    def test_count_patterns_success(self):
        """Test cas nominal de _count_patterns"""
        # Act
        count = self.collector._count_patterns()

        # Assert
        assert isinstance(count, int)
        assert count >= 0

    def test_count_predictions_success(self):
        """Test cas nominal de _count_predictions"""
        # Act
        count = self.collector._count_predictions()

        # Assert
        assert isinstance(count, int)
        assert count >= 0

    def test_check_cia_integration_success(self):
        """Test cas nominal de _check_cia_integration"""
        # Act
        cia_info = self.collector._check_cia_integration()

        # Assert
        assert isinstance(cia_info, dict)
        assert "cia_sync_exists" in cia_info
        assert "integration_endpoints" in cia_info
        assert isinstance(cia_info["cia_sync_exists"], bool)
        assert isinstance(cia_info["integration_endpoints"], int)

    def test_check_prediction_engine_success(self):
        """Test cas nominal de _check_prediction_engine"""
        # Act
        is_active = self.collector._check_prediction_engine()

        # Assert
        assert isinstance(is_active, bool)

    def test_check_emotion_analyzer_success(self):
        """Test cas nominal de _check_emotion_analyzer"""
        # Act
        is_active = self.collector._check_emotion_analyzer()

        # Assert
        assert isinstance(is_active, bool)

    def test_count_api_endpoints_success(self):
        """Test cas nominal de _count_api_endpoints"""
        # Act
        count = self.collector._count_api_endpoints()

        # Assert
        assert isinstance(count, int)
        assert count >= 0

    def test_count_cia_sync_endpoints_success(self):
        """Test cas nominal de _count_cia_sync_endpoints"""
        # Act
        count = self.collector._count_cia_sync_endpoints()

        # Assert
        assert isinstance(count, int)
        assert count >= 0

    def test_count_pain_api_endpoints_success(self):
        """Test cas nominal de _count_pain_api_endpoints"""
        # Act
        count = self.collector._count_pain_api_endpoints()

        # Assert
        assert isinstance(count, int)
        assert count >= 0

    def test_count_integration_tests_success(self):
        """Test cas nominal de _count_integration_tests"""
        # Act
        count = self.collector._count_integration_tests()

        # Assert
        assert isinstance(count, int)
        assert count >= 0

    def test_count_dependencies_success(self):
        """Test cas nominal de _count_dependencies"""
        # Act
        count = self.collector._count_dependencies()

        # Assert
        assert isinstance(count, int)
        assert count >= 0

    def test_check_vulnerabilities_success(self):
        """Test cas nominal de _check_vulnerabilities"""
        # Act
        vuln_info = self.collector._check_vulnerabilities()

        # Assert
        assert isinstance(vuln_info, dict)
        assert "known_vulnerabilities" in vuln_info
        assert "last_check" in vuln_info
        assert isinstance(vuln_info["known_vulnerabilities"], int)
        assert isinstance(vuln_info["last_check"], str)

    def test_check_mkdocs_status_success(self):
        """Test cas nominal de _check_mkdocs_status"""
        # Act
        status = self.collector._check_mkdocs_status()

        # Assert
        assert isinstance(status, bool)
