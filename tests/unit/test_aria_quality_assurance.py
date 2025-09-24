#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_QualityAssurance
===========================================

Tests complets pour le système d'assurance qualité ARIA.
"""

import tempfile
from pathlib import Path

import pytest

from devops_automation.quality.aria_quality_assurance import ARIA_QualityAssurance
from devops_automation.security.aria_security_validator import ARIA_SecurityValidator


class TestARIA_QualityAssurance:
    """Tests unitaires pour ARIA_QualityAssurance"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.quality_assurance = ARIA_QualityAssurance(self.temp_dir)

    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        quality_assurance = ARIA_QualityAssurance(".")

        # Assert
        assert quality_assurance.project_root == Path(".").resolve()
        assert isinstance(quality_assurance.security_validator, ARIA_SecurityValidator)
        assert isinstance(quality_assurance.quality_reports, list)
        assert isinstance(quality_assurance.quality_tools, dict)
        assert "black" in quality_assurance.quality_tools
        assert "ruff" in quality_assurance.quality_tools
        assert "mypy" in quality_assurance.quality_tools
        assert "pytest" in quality_assurance.quality_tools

    def test_init_with_custom_root(self):
        """Test initialisation avec racine personnalisée"""
        # Arrange
        custom_root = "/custom/path"

        # Act
        quality_assurance = ARIA_QualityAssurance(custom_root)

        # Assert
        assert quality_assurance.project_root == Path(custom_root).resolve()

    def test_run_full_quality_check_success(self):
        """Test cas nominal de run_full_quality_check"""
        # Arrange
        config = {
            "run_tests": True,
            "run_linting": True,
            "run_formatting": True,
            "run_type_checking": True,
            "run_security_scan": True,
        }

        # Act
        result = self.quality_assurance.run_full_quality_check(config)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert "overall_score" in result
        assert "tests" in result
        assert "linting" in result
        assert "formatting" in result
        assert "type_checking" in result
        assert "security" in result
        assert "timestamp" in result
        assert result["status"] in ["success", "warning", "error"]
        assert isinstance(result["overall_score"], int)
        assert 0 <= result["overall_score"] <= 100

    def test_run_full_quality_check_partial(self):
        """Test run_full_quality_check avec configuration partielle"""
        # Arrange
        config = {
            "run_tests": True,
            "run_linting": False,
            "run_formatting": True,
            "run_type_checking": False,
            "run_security_scan": False,
        }

        # Act
        result = self.quality_assurance.run_full_quality_check(config)

        # Assert
        assert result["status"] in ["success", "warning", "error"]
        assert "tests" in result
        assert "formatting" in result
        assert "linting" not in result or result["linting"]["skipped"] is True
        assert (
            "type_checking" not in result or result["type_checking"]["skipped"] is True
        )
        assert "security" not in result or result["security"]["skipped"] is True

    def test_run_full_quality_check_error_handling(self):
        """Test gestion d'erreur de run_full_quality_check"""
        # Arrange
        invalid_config = None

        # Act
        result = self.quality_assurance.run_full_quality_check(invalid_config)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_check_code_quality_success(self):
        """Test cas nominal de check_code_quality"""
        # Arrange
        config = {
            "run_linting": True,
            "run_formatting": True,
            "run_type_checking": True,
        }

        # Act
        result = self.quality_assurance.check_code_quality(config)

        # Assert
        assert isinstance(result, dict)
        assert "linting" in result
        assert "formatting" in result
        assert "type_checking" in result
        assert "overall_score" in result
        assert isinstance(result["overall_score"], int)
        assert 0 <= result["overall_score"] <= 100

    def test_check_code_quality_individual_tools(self):
        """Test check_code_quality avec outils individuels"""
        # Arrange
        config = {"run_linting": True}

        # Act
        result = self.quality_assurance.check_code_quality(config)

        # Assert
        assert "linting" in result
        assert "formatting" not in result or result["formatting"]["skipped"] is True
        assert (
            "type_checking" not in result or result["type_checking"]["skipped"] is True
        )

    def test_run_linting_success(self):
        """Test cas nominal de _run_linting"""
        # Arrange
        config = {"tool": "ruff", "args": ["--check"]}

        # Act
        result = self.quality_assurance._run_linting(config)

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "status" in result
        assert "output" in result
        assert "errors_found" in result
        assert "warnings_found" in result
        assert result["tool"] == "ruff"
        assert result["status"] in ["success", "warning", "error"]
        assert isinstance(result["errors_found"], int)
        assert isinstance(result["warnings_found"], int)

    def test_run_linting_error_handling(self):
        """Test gestion d'erreur de _run_linting"""
        # Arrange
        invalid_config = {"tool": "nonexistent_tool"}

        # Act
        result = self.quality_assurance._run_linting(invalid_config)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_run_formatting_success(self):
        """Test cas nominal de _run_formatting"""
        # Arrange
        config = {"tool": "black", "args": ["--check"]}

        # Act
        result = self.quality_assurance._run_formatting(config)

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "status" in result
        assert "output" in result
        assert "files_formatted" in result
        assert "files_need_formatting" in result
        assert result["tool"] == "black"
        assert result["status"] in ["success", "warning", "error"]
        assert isinstance(result["files_formatted"], int)
        assert isinstance(result["files_need_formatting"], int)

    def test_run_formatting_error_handling(self):
        """Test gestion d'erreur de _run_formatting"""
        # Arrange
        invalid_config = {"tool": "nonexistent_tool"}

        # Act
        result = self.quality_assurance._run_formatting(invalid_config)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_run_type_checking_success(self):
        """Test cas nominal de _run_type_checking"""
        # Arrange
        config = {"tool": "mypy", "args": ["--strict"]}

        # Act
        result = self.quality_assurance._run_type_checking(config)

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "status" in result
        assert "output" in result
        assert "type_errors_found" in result
        assert "type_warnings_found" in result
        assert result["tool"] == "mypy"
        assert result["status"] in ["success", "warning", "error"]
        assert isinstance(result["type_errors_found"], int)
        assert isinstance(result["type_warnings_found"], int)

    def test_run_type_checking_error_handling(self):
        """Test gestion d'erreur de _run_type_checking"""
        # Arrange
        invalid_config = {"tool": "nonexistent_tool"}

        # Act
        result = self.quality_assurance._run_type_checking(invalid_config)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_run_tests_success(self):
        """Test cas nominal de _run_tests"""
        # Arrange
        config = {"tool": "pytest", "args": ["-v", "--tb=short"], "coverage": True}

        # Act
        result = self.quality_assurance._run_tests(config)

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "status" in result
        assert "output" in result
        assert "tests_run" in result
        assert "tests_passed" in result
        assert "tests_failed" in result
        assert "coverage_percentage" in result
        assert result["tool"] == "pytest"
        assert result["status"] in ["success", "warning", "error"]
        assert isinstance(result["tests_run"], int)
        assert isinstance(result["tests_passed"], int)
        assert isinstance(result["tests_failed"], int)
        assert isinstance(result["coverage_percentage"], float)

    def test_run_tests_error_handling(self):
        """Test gestion d'erreur de _run_tests"""
        # Arrange
        invalid_config = {"tool": "nonexistent_tool"}

        # Act
        result = self.quality_assurance._run_tests(invalid_config)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

    def test_run_security_scan_success(self):
        """Test cas nominal de _run_security_scan"""
        # Arrange
        config = {"bandit": True, "safety": True, "args": ["--recursive"]}

        # Act
        result = self.quality_assurance._run_security_scan(config)

        # Assert
        assert isinstance(result, dict)
        assert "bandit" in result
        assert "safety" in result
        assert "overall_status" in result
        assert "security_issues_found" in result
        assert result["overall_status"] in ["success", "warning", "error"]
        assert isinstance(result["security_issues_found"], int)

    def test_run_security_scan_error_handling(self):
        """Test gestion d'erreur de _run_security_scan"""
        # Arrange
        invalid_config = {"invalid": "config"}

        # Act
        result = self.quality_assurance._run_security_scan(invalid_config)

        # Assert
        assert result["overall_status"] == "error"
        assert "error" in result

    def test_generate_report_success(self):
        """Test cas nominal de generate_report"""
        # Arrange
        quality_data = {
            "tests": {"status": "success", "tests_passed": 10, "tests_failed": 0},
            "linting": {"status": "success", "errors_found": 0, "warnings_found": 2},
            "formatting": {
                "status": "success",
                "files_formatted": 5,
                "files_need_formatting": 0,
            },
            "type_checking": {
                "status": "success",
                "type_errors_found": 0,
                "type_warnings_found": 1,
            },
            "security": {"status": "success", "security_issues_found": 0},
        }

        # Act
        report = self.quality_assurance.generate_report(quality_data)

        # Assert
        assert isinstance(report, dict)
        assert "report_id" in report
        assert "timestamp" in report
        assert "overall_score" in report
        assert "summary" in report
        assert "details" in report
        assert "recommendations" in report
        assert isinstance(report["overall_score"], int)
        assert 0 <= report["overall_score"] <= 100
        assert isinstance(report["summary"], dict)
        assert isinstance(report["details"], dict)
        assert isinstance(report["recommendations"], list)

    def test_generate_report_error_handling(self):
        """Test gestion d'erreur de generate_report"""
        # Arrange
        invalid_data = None

        # Act
        report = self.quality_assurance.generate_report(invalid_data)

        # Assert
        assert report["overall_score"] == 0
        assert "error" in report["summary"]

    def test_calculate_overall_score_success(self):
        """Test cas nominal de _calculate_overall_score"""
        # Arrange
        quality_data = {
            "tests": {"tests_passed": 10, "tests_failed": 0},
            "linting": {"errors_found": 0, "warnings_found": 2},
            "formatting": {"files_formatted": 5, "files_need_formatting": 0},
            "type_checking": {"type_errors_found": 0, "type_warnings_found": 1},
            "security": {"security_issues_found": 0},
        }

        # Act
        score = self.quality_assurance._calculate_overall_score(quality_data)

        # Assert
        assert isinstance(score, int)
        assert 0 <= score <= 100
        assert score >= 80  # Score élevé pour de bonnes métriques

    def test_calculate_overall_score_poor_quality(self):
        """Test _calculate_overall_score avec qualité médiocre"""
        # Arrange
        poor_quality_data = {
            "tests": {"tests_passed": 5, "tests_failed": 5},
            "linting": {"errors_found": 10, "warnings_found": 20},
            "formatting": {"files_formatted": 2, "files_need_formatting": 8},
            "type_checking": {"type_errors_found": 5, "type_warnings_found": 10},
            "security": {"security_issues_found": 3},
        }

        # Act
        score = self.quality_assurance._calculate_overall_score(poor_quality_data)

        # Assert
        assert isinstance(score, int)
        assert 0 <= score <= 100
        assert score < 50  # Score faible pour de mauvaises métriques

    def test_calculate_overall_score_edge_cases(self):
        """Test cas limites de _calculate_overall_score"""
        # Arrange
        empty_data = {}

        # Act
        score = self.quality_assurance._calculate_overall_score(empty_data)

        # Assert
        assert score == 0

    def test_run_tool_command_success(self):
        """Test cas nominal de _run_tool_command"""
        # Arrange
        tool = "python"
        args = ["--version"]

        # Act
        result = self.quality_assurance._run_tool_command(tool, args)

        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert "execution_time" in result
        assert isinstance(result["success"], bool)
        assert isinstance(result["execution_time"], float)

    def test_run_tool_command_error_handling(self):
        """Test gestion d'erreur de _run_tool_command"""
        # Arrange
        invalid_tool = "nonexistent_tool_12345"
        args = ["--version"]

        # Act
        result = self.quality_assurance._run_tool_command(invalid_tool, args)

        # Assert
        assert result["success"] is False
        assert "error" in result["error"]

    def test_run_tool_command_edge_cases(self):
        """Test cas limites de _run_tool_command"""
        # Arrange
        tool = ""
        args = []

        # Act
        result = self.quality_assurance._run_tool_command(tool, args)

        # Assert
        assert result["success"] is False
        assert "error" in result["error"]

    def test_parse_test_output_success(self):
        """Test cas nominal de _parse_test_output"""
        # Arrange
        test_output = """
========================= test session starts =========================
test_example.py::test_function PASSED [100%]
========================= 1 passed in 0.01s =========================
"""

        # Act
        result = self.quality_assurance._parse_test_output(test_output)

        # Assert
        assert isinstance(result, dict)
        assert "tests_run" in result
        assert "tests_passed" in result
        assert "tests_failed" in result
        assert "tests_skipped" in result
        assert result["tests_run"] == 1
        assert result["tests_passed"] == 1
        assert result["tests_failed"] == 0
        assert result["tests_skipped"] == 0

    def test_parse_test_output_with_failures(self):
        """Test _parse_test_output avec échecs"""
        # Arrange
        test_output = """
========================= test session starts =========================
test_example.py::test_function PASSED [50%]
test_example.py::test_failing_function FAILED [100%]
========================= 2 passed, 1 failed in 0.02s =========================
"""

        # Act
        result = self.quality_assurance._parse_test_output(test_output)

        # Assert
        assert result["tests_run"] == 2
        assert result["tests_passed"] == 1
        assert result["tests_failed"] == 1
        assert result["tests_skipped"] == 0

    def test_parse_test_output_edge_cases(self):
        """Test cas limites de _parse_test_output"""
        # Arrange
        empty_output = ""

        # Act
        result = self.quality_assurance._parse_test_output(empty_output)

        # Assert
        assert result["tests_run"] == 0
        assert result["tests_passed"] == 0
        assert result["tests_failed"] == 0
        assert result["tests_skipped"] == 0

    def test_parse_linting_output_success(self):
        """Test cas nominal de _parse_linting_output"""
        # Arrange
        linting_output = """
src/main.py:10:1: E302 expected 2 blank lines, found 1
src/main.py:15:5: W291 trailing whitespace
Found 1 error and 1 warning.
"""

        # Act
        result = self.quality_assurance._parse_linting_output(linting_output)

        # Assert
        assert isinstance(result, dict)
        assert "errors_found" in result
        assert "warnings_found" in result
        assert result["errors_found"] == 1
        assert result["warnings_found"] == 1

    def test_parse_linting_output_no_issues(self):
        """Test _parse_linting_output sans problèmes"""
        # Arrange
        clean_output = "All checks passed! No issues found."

        # Act
        result = self.quality_assurance._parse_linting_output(clean_output)

        # Assert
        assert result["errors_found"] == 0
        assert result["warnings_found"] == 0

    def test_parse_linting_output_edge_cases(self):
        """Test cas limites de _parse_linting_output"""
        # Arrange
        empty_output = ""

        # Act
        result = self.quality_assurance._parse_linting_output(empty_output)

        # Assert
        assert result["errors_found"] == 0
        assert result["warnings_found"] == 0

    def test_get_quality_tools_config_success(self):
        """Test cas nominal de _get_quality_tools_config"""
        # Arrange
        tool_name = "black"

        # Act
        config = self.quality_assurance._get_quality_tools_config(tool_name)

        # Assert
        assert isinstance(config, dict)
        assert "command" in config
        assert "args" in config
        assert "description" in config
        assert config["command"] == "black"

    def test_get_quality_tools_config_invalid_tool(self):
        """Test _get_quality_tools_config avec outil invalide"""
        # Arrange
        invalid_tool = "nonexistent_tool"

        # Act
        config = self.quality_assurance._get_quality_tools_config(invalid_tool)

        # Assert
        assert config is None

    def test_log_quality_report_success(self):
        """Test cas nominal de _log_quality_report"""
        # Arrange
        report_data = {
            "report_id": "test_report",
            "overall_score": 85,
            "status": "success",
            "timestamp": "2024-01-01T00:00:00",
        }

        # Act
        self.quality_assurance._log_quality_report(report_data)

        # Assert
        assert len(self.quality_assurance.quality_reports) == 1
        assert self.quality_assurance.quality_reports[0]["report_id"] == "test_report"
        assert self.quality_assurance.quality_reports[0]["overall_score"] == 85
        assert self.quality_assurance.quality_reports[0]["status"] == "success"

    def test_log_quality_report_error_handling(self):
        """Test gestion d'erreur de _log_quality_report"""
        # Arrange
        invalid_report_data = None

        # Act & Assert
        with pytest.raises(Exception):
            self.quality_assurance._log_quality_report(invalid_report_data)

    def test_get_quality_history_success(self):
        """Test cas nominal de get_quality_history"""
        # Arrange
        self.quality_assurance.quality_reports = [
            {
                "report_id": "report_1",
                "overall_score": 85,
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "report_id": "report_2",
                "overall_score": 90,
                "timestamp": "2024-01-01T00:01:00",
            },
        ]

        # Act
        history = self.quality_assurance.get_quality_history()

        # Assert
        assert isinstance(history, list)
        assert len(history) == 2
        assert history[0]["report_id"] == "report_1"
        assert history[1]["report_id"] == "report_2"

    def test_get_quality_history_empty(self):
        """Test get_quality_history vide"""
        # Arrange
        self.quality_assurance.quality_reports = []

        # Act
        history = self.quality_assurance.get_quality_history()

        # Assert
        assert isinstance(history, list)
        assert len(history) == 0

    def test_get_quality_trends_success(self):
        """Test cas nominal de get_quality_trends"""
        # Arrange
        self.quality_assurance.quality_reports = [
            {"overall_score": 80, "timestamp": "2024-01-01T00:00:00"},
            {"overall_score": 85, "timestamp": "2024-01-01T00:01:00"},
            {"overall_score": 90, "timestamp": "2024-01-01T00:02:00"},
        ]

        # Act
        trends = self.quality_assurance.get_quality_trends()

        # Assert
        assert isinstance(trends, dict)
        assert "average_score" in trends
        assert "trend_direction" in trends
        assert "score_change" in trends
        assert "reports_count" in trends
        assert trends["average_score"] == 85.0
        assert trends["trend_direction"] in ["improving", "declining", "stable"]
        assert trends["reports_count"] == 3
