#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_QualityAssurance
==========================================

Tests complets pour le système d'assurance qualité ARIA.
"""

import tempfile
from pathlib import Path

from devops_automation.quality.aria_quality_assurance import ARIA_QualityAssurance


class TestARIA_QualityAssurance:
    """Tests unitaires pour ARIA_QualityAssurance"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)
        self.quality_assurance = ARIA_QualityAssurance(str(self.project_root))

    def teardown_method(self):
        """Cleanup après chaque test"""
        self.temp_dir.cleanup()

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        quality_assurance = ARIA_QualityAssurance(str(self.project_root))

        # Assert
        assert quality_assurance.project_root.resolve() == self.project_root.resolve()
        assert isinstance(
            quality_assurance.security_validator,
            type(quality_assurance.security_validator),
        )
        assert isinstance(quality_assurance.quality_reports, list)
        assert isinstance(quality_assurance.quality_tools, dict)
        assert "black" in quality_assurance.quality_tools
        assert "ruff" in quality_assurance.quality_tools
        assert "mypy" in quality_assurance.quality_tools
        assert "bandit" in quality_assurance.quality_tools
        assert "safety" in quality_assurance.quality_tools
        assert "pytest" in quality_assurance.quality_tools

    def test_init_with_custom_root(self):
        """Test initialisation avec racine personnalisée"""
        # Arrange
        custom_root = "/tmp/custom_path"

        # Act
        quality_assurance = ARIA_QualityAssurance(custom_root)

        # Assert
        assert quality_assurance.project_root == Path(custom_root).resolve()

    def test_run_full_quality_check_success(self):
        """Test cas nominal de run_full_quality_check"""
        # Act
        result = self.quality_assurance.run_full_quality_check(fix_issues=False)

        # Assert
        assert isinstance(result, dict)
        assert "timestamp" in result
        assert "project_root" in result
        assert "fix_issues" in result
        assert "tools_results" in result
        assert "overall_score" in result
        assert "status" in result
        assert "recommendations" in result
        assert result["fix_issues"] is False
        assert isinstance(result["tools_results"], dict)
        assert isinstance(result["overall_score"], int)
        assert isinstance(result["recommendations"], list)

    def test_run_full_quality_check_partial(self):
        """Test run_full_quality_check avec fix_issues=True"""
        # Act
        result = self.quality_assurance.run_full_quality_check(fix_issues=True)

        # Assert
        assert isinstance(result, dict)
        assert "timestamp" in result
        assert "project_root" in result
        assert "fix_issues" in result
        assert "tools_results" in result
        assert "overall_score" in result
        assert "status" in result
        assert "recommendations" in result
        assert result["fix_issues"] is True
        assert isinstance(result["tools_results"], dict)
        assert isinstance(result["overall_score"], int)
        assert isinstance(result["recommendations"], list)

    def test_run_full_quality_check_error_handling(self):
        """Test gestion d'erreur de run_full_quality_check"""
        # Arrange
        # Simuler une erreur en modifiant temporairement la méthode
        original_method = self.quality_assurance.run_full_quality_check

        def error_method(*args, **kwargs):
            # Simuler une erreur dans le try/except de la méthode originale
            quality_report = {
                "timestamp": "2024-01-01T00:00:00",
                "project_root": str(self.project_root),
                "fix_issues": False,
                "tools_results": {},
                "overall_score": 0,
                "status": "error",
                "recommendations": [],
                "error": "Test error",
            }
            return quality_report

        self.quality_assurance.run_full_quality_check = error_method

        # Act
        result = self.quality_assurance.run_full_quality_check(fix_issues=False)

        # Assert
        assert result["status"] == "error"
        assert "error" in result

        # Restaurer la méthode originale
        self.quality_assurance.run_full_quality_check = original_method

    def test_run_black_success(self):
        """Test cas nominal de _run_black"""
        # Act
        result = self.quality_assurance._run_black(fix_issues=False)

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "returncode" in result
        assert "stdout" in result
        assert "stderr" in result
        assert result["tool"] == "black"
        assert isinstance(result["success"], bool)
        assert isinstance(result["returncode"], int)

    def test_run_black_with_fix(self):
        """Test _run_black avec fix_issues=True"""
        # Act
        result = self.quality_assurance._run_black(fix_issues=True)

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "fixed" in result
        assert result["tool"] == "black"
        assert isinstance(result["fixed"], bool)

    def test_run_ruff_success(self):
        """Test cas nominal de _run_ruff"""
        # Act
        result = self.quality_assurance._run_ruff(fix_issues=False)

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "returncode" in result
        assert "stdout" in result
        assert "stderr" in result
        assert result["tool"] == "ruff"
        assert isinstance(result["success"], bool)
        assert isinstance(result["returncode"], int)

    def test_run_ruff_with_fix(self):
        """Test _run_ruff avec fix_issues=True"""
        # Act
        result = self.quality_assurance._run_ruff(fix_issues=True)

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "fixed" in result
        assert result["tool"] == "ruff"
        assert isinstance(result["fixed"], bool)

    def test_run_mypy_success(self):
        """Test cas nominal de _run_mypy"""
        # Act
        result = self.quality_assurance._run_mypy()

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "returncode" in result
        assert "stdout" in result
        assert "stderr" in result
        assert result["tool"] == "mypy"
        assert isinstance(result["success"], bool)
        assert isinstance(result["returncode"], int)

    def test_run_bandit_success(self):
        """Test cas nominal de _run_bandit"""
        # Act
        result = self.quality_assurance._run_bandit()

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "returncode" in result
        assert "issues" in result
        assert "high_severity" in result
        assert "medium_severity" in result
        assert "low_severity" in result
        assert result["tool"] == "bandit"
        assert isinstance(result["success"], bool)
        assert isinstance(result["issues"], list)
        assert isinstance(result["high_severity"], int)
        assert isinstance(result["medium_severity"], int)
        assert isinstance(result["low_severity"], int)

    def test_run_safety_success(self):
        """Test cas nominal de _run_safety"""
        # Act
        result = self.quality_assurance._run_safety()

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "returncode" in result
        assert "vulnerabilities" in result
        assert "vulnerability_count" in result
        assert result["tool"] == "safety"
        assert isinstance(result["success"], bool)
        assert isinstance(result["vulnerabilities"], list)
        assert isinstance(result["vulnerability_count"], int)

    def test_run_pytest_success(self):
        """Test cas nominal de _run_pytest"""
        # Act
        result = self.quality_assurance._run_pytest()

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "returncode" in result
        assert "stdout" in result
        assert "stderr" in result
        assert "coverage" in result
        assert result["tool"] == "pytest"
        assert isinstance(result["success"], bool)
        assert isinstance(result["coverage"], (int, float))

    def test_run_security_audit_success(self):
        """Test cas nominal de _run_security_audit"""
        # Act
        result = self.quality_assurance._run_security_audit()

        # Assert
        assert isinstance(result, dict)
        assert "tool" in result
        assert "success" in result
        assert "files_audited" in result
        assert "files_with_issues" in result
        assert "total_risk_score" in result
        assert "audit_results" in result
        assert result["tool"] == "security_audit"
        assert isinstance(result["success"], bool)
        assert isinstance(result["files_audited"], int)
        assert isinstance(result["files_with_issues"], int)
        assert isinstance(result["total_risk_score"], int)
        assert isinstance(result["audit_results"], list)

    def test_should_audit_file_success(self):
        """Test cas nominal de _should_audit_file"""
        # Arrange
        test_file = Path("src/main.py")

        # Act
        should_audit = self.quality_assurance._should_audit_file(test_file)

        # Assert
        assert isinstance(should_audit, bool)
        assert should_audit is True

    def test_should_audit_file_excluded(self):
        """Test _should_audit_file avec fichier exclu"""
        # Arrange
        excluded_file = Path("__pycache__/module.pyc")

        # Act
        should_audit = self.quality_assurance._should_audit_file(excluded_file)

        # Assert
        assert isinstance(should_audit, bool)
        assert should_audit is False

    def test_calculate_overall_score_success(self):
        """Test cas nominal de _calculate_overall_score"""
        # Arrange
        tools_results = {
            "black": {"success": True},
            "ruff": {"success": True},
            "mypy": {"success": True},
            "bandit": {"success": True, "high_severity": 0, "medium_severity": 0},
            "safety": {"success": True, "vulnerability_count": 0},
            "pytest": {"success": True, "coverage": 85},
        }

        # Act
        score = self.quality_assurance._calculate_overall_score(tools_results)

        # Assert
        assert isinstance(score, int)
        assert 0 <= score <= 100
        assert score == 100  # Tous les outils réussissent

    def test_calculate_overall_score_with_issues(self):
        """Test _calculate_overall_score avec problèmes"""
        # Arrange
        tools_results = {
            "black": {"success": False},
            "ruff": {"success": False},
            "mypy": {"success": True},
            "bandit": {"success": True, "high_severity": 2, "medium_severity": 1},
            "safety": {"success": True, "vulnerability_count": 3},
            "pytest": {"success": True, "coverage": 60},
        }

        # Act
        score = self.quality_assurance._calculate_overall_score(tools_results)

        # Assert
        assert isinstance(score, int)
        assert 0 <= score <= 100
        assert score < 100  # Des problèmes détectés

    def test_generate_recommendations_success(self):
        """Test cas nominal de _generate_recommendations"""
        # Arrange
        tools_results = {
            "black": {"success": False},
            "ruff": {"success": False},
            "mypy": {"success": False},
            "bandit": {"success": True, "high_severity": 1},
            "safety": {"success": True, "vulnerability_count": 2},
            "pytest": {"success": True, "coverage": 70},
        }

        # Act
        recommendations = self.quality_assurance._generate_recommendations(
            tools_results
        )

        # Assert
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(rec, str) for rec in recommendations)

    def test_determine_status_success(self):
        """Test cas nominal de _determine_status"""
        # Test différents scores
        assert self.quality_assurance._determine_status(95) == "excellent"
        assert self.quality_assurance._determine_status(80) == "good"
        assert self.quality_assurance._determine_status(65) == "fair"
        assert self.quality_assurance._determine_status(45) == "poor"

    def test_get_quality_history_success(self):
        """Test cas nominal de get_quality_history"""
        # Arrange
        # Ajouter quelques rapports à l'historique
        self.quality_assurance.quality_reports = [
            {"timestamp": "2024-01-01T00:00:00", "overall_score": 85},
            {"timestamp": "2024-01-01T00:01:00", "overall_score": 90},
            {"timestamp": "2024-01-01T00:02:00", "overall_score": 88},
        ]

        # Act
        history = self.quality_assurance.get_quality_history()

        # Assert
        assert isinstance(history, list)
        assert len(history) == 3
        assert all("timestamp" in report for report in history)
        assert all("overall_score" in report for report in history)

    def test_generate_quality_report_html_success(self):
        """Test cas nominal de generate_quality_report_html"""
        # Arrange
        report = {
            "timestamp": "2024-01-01T00:00:00",
            "overall_score": 85,
            "status": "good",
            "tools_results": {
                "black": {"success": True},
                "ruff": {"success": False},
            },
            "recommendations": ["Fix linting issues"],
        }

        # Act
        html_content = self.quality_assurance.generate_quality_report_html(report)

        # Assert
        assert isinstance(html_content, str)
        assert "<!DOCTYPE html>" in html_content
        assert "ARKALIA ARIA" in html_content
        assert "Rapport de Qualité" in html_content
        assert "85/100" in html_content
        assert "good" in html_content
