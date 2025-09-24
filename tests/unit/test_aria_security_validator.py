#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_SecurityValidator
===========================================

Tests complets pour le validateur de sécurité ARIA.
"""


import pytest

from devops_automation.security.aria_security_validator import ARIA_SecurityValidator


class TestARIA_SecurityValidator:
    """Tests unitaires pour ARIA_SecurityValidator"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.validator = ARIA_SecurityValidator()

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        validator = ARIA_SecurityValidator()

        # Assert
        assert isinstance(validator.allowed_commands, set)
        assert len(validator.allowed_commands) > 0
        assert "ls" in validator.allowed_commands
        assert "find" in validator.allowed_commands
        assert "grep" in validator.allowed_commands
        assert isinstance(validator.security_log, list)
        assert isinstance(validator.blocked_attempts, list)

    def test_validate_command_success(self):
        """Test cas nominal de validate_command"""
        # Arrange
        command = ["ls", "-la"]

        # Act
        result = self.validator.validate_command(command)

        # Assert
        assert isinstance(result, dict)
        assert "is_valid" in result
        assert "risk_score" in result
        assert "reason" in result
        assert result["is_valid"] is True
        assert result["risk_score"] == 0
        assert "ls" in result["reason"]

    def test_validate_command_blocked_command(self):
        """Test validation avec commande bloquée"""
        # Arrange
        command = ["rm", "-rf", "/"]

        # Act
        result = self.validator.validate_command(command)

        # Assert
        assert result["is_valid"] is False
        assert result["risk_score"] > 0
        assert (
            "dangerous" in result["reason"].lower()
            or "blocked" in result["reason"].lower()
        )

    def test_validate_command_injection_attempt(self):
        """Test validation avec tentative d'injection"""
        # Arrange
        command = ["ls", ";", "rm", "-rf", "/"]

        # Act
        result = self.validator.validate_command(command)

        # Assert
        assert result["is_valid"] is False
        assert result["risk_score"] > 0
        assert (
            "injection" in result["reason"].lower()
            or "dangerous" in result["reason"].lower()
        )

    def test_validate_command_edge_cases(self):
        """Test cas limites de validate_command"""
        # Arrange
        empty_command = []

        # Act
        result = self.validator.validate_command(empty_command)

        # Assert
        assert result["is_valid"] is False
        assert result["risk_score"] > 0

    def test_validate_command_none_input(self):
        """Test validation avec entrée None"""
        # Arrange
        command = None

        # Act & Assert
        with pytest.raises(Exception):
            self.validator.validate_command(command)

    def test_audit_code_success(self):
        """Test cas nominal de audit_code"""
        # Arrange
        code_content = """
def safe_function():
    return "Hello World"

def another_safe_function():
    import os
    return os.getcwd()
"""

        # Act
        audit_result = self.validator.audit_code(code_content)

        # Assert
        assert isinstance(audit_result, dict)
        assert "security_score" in audit_result
        assert "issues_found" in audit_result
        assert "recommendations" in audit_result
        assert "timestamp" in audit_result
        assert isinstance(audit_result["security_score"], int)
        assert 0 <= audit_result["security_score"] <= 100
        assert isinstance(audit_result["issues_found"], list)
        assert isinstance(audit_result["recommendations"], list)

    def test_audit_code_with_vulnerabilities(self):
        """Test audit_code avec vulnérabilités"""
        # Arrange
        vulnerable_code = """
import subprocess
import os

def dangerous_function():
    user_input = input("Enter command: ")
    subprocess.run(user_input, shell=True)  # Dangerous!
    
def another_dangerous_function():
    os.system("rm -rf /")  # Very dangerous!
"""

        # Act
        audit_result = self.validator.audit_code(vulnerable_code)

        # Assert
        assert audit_result["security_score"] < 50  # Score faible
        assert len(audit_result["issues_found"]) > 0
        assert len(audit_result["recommendations"]) > 0
        assert any(
            "subprocess" in issue["description"]
            for issue in audit_result["issues_found"]
        )

    def test_audit_code_empty_content(self):
        """Test audit_code avec contenu vide"""
        # Arrange
        empty_code = ""

        # Act
        audit_result = self.validator.audit_code(empty_code)

        # Assert
        assert audit_result["security_score"] == 100  # Score parfait pour code vide
        assert len(audit_result["issues_found"]) == 0
        assert len(audit_result["recommendations"]) == 0

    def test_calculate_risk_score_success(self):
        """Test cas nominal de calculate_risk_score"""
        # Arrange
        command = ["ls", "-la"]

        # Act
        risk_score = self.validator.calculate_risk_score(command)

        # Assert
        assert isinstance(risk_score, int)
        assert 0 <= risk_score <= 100
        assert risk_score == 0  # Commande sûre

    def test_calculate_risk_score_dangerous_command(self):
        """Test calculate_risk_score avec commande dangereuse"""
        # Arrange
        dangerous_command = ["rm", "-rf", "/"]

        # Act
        risk_score = self.validator.calculate_risk_score(dangerous_command)

        # Assert
        assert risk_score > 50  # Score élevé pour commande dangereuse
        assert risk_score <= 100

    def test_calculate_risk_score_edge_cases(self):
        """Test cas limites de calculate_risk_score"""
        # Arrange
        empty_command = []

        # Act
        risk_score = self.validator.calculate_risk_score(empty_command)

        # Assert
        assert risk_score > 0  # Score non nul pour commande vide

    def test_execute_safely_success(self):
        """Test cas nominal de execute_safely"""
        # Arrange
        command = ["ls", "-la"]

        # Act
        result = self.validator.execute_safely(command)

        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "output" in result
        assert "error" in result
        assert "execution_time" in result
        assert isinstance(result["success"], bool)
        assert isinstance(result["execution_time"], float)

    def test_execute_safely_blocked_command(self):
        """Test execute_safely avec commande bloquée"""
        # Arrange
        blocked_command = ["rm", "-rf", "/"]

        # Act
        result = self.validator.execute_safely(blocked_command)

        # Assert
        assert result["success"] is False
        assert (
            "blocked" in result["error"].lower()
            or "dangerous" in result["error"].lower()
        )
        assert result["output"] == ""

    def test_execute_safely_invalid_command(self):
        """Test execute_safely avec commande invalide"""
        # Arrange
        invalid_command = ["nonexistentcommand12345"]

        # Act
        result = self.validator.execute_safely(invalid_command)

        # Assert
        assert result["success"] is False
        assert (
            "error" in result["error"].lower() or "not found" in result["error"].lower()
        )

    def test_execute_safely_edge_cases(self):
        """Test cas limites de execute_safely"""
        # Arrange
        empty_command = []

        # Act
        result = self.validator.execute_safely(empty_command)

        # Assert
        assert result["success"] is False
        assert (
            "empty" in result["error"].lower() or "invalid" in result["error"].lower()
        )

    def test_log_security_event_success(self):
        """Test cas nominal de _log_security_event"""
        # Arrange
        event_type = "command_execution"
        details = {"command": ["ls", "-la"], "risk_score": 0}

        # Act
        self.validator._log_security_event(event_type, details)

        # Assert
        assert len(self.validator.security_log) == 1
        assert self.validator.security_log[0]["event_type"] == event_type
        assert self.validator.security_log[0]["details"] == details
        assert "timestamp" in self.validator.security_log[0]

    def test_log_security_event_error_handling(self):
        """Test gestion d'erreur de _log_security_event"""
        # Arrange
        event_type = None
        details = None

        # Act & Assert
        with pytest.raises(Exception):
            self.validator._log_security_event(event_type, details)

    def test_get_security_report_success(self):
        """Test cas nominal de get_security_report"""
        # Arrange
        self.validator.security_log = [
            {
                "event_type": "command_execution",
                "details": {"command": ["ls"]},
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "event_type": "command_blocked",
                "details": {"command": ["rm", "-rf"]},
                "timestamp": "2024-01-01T00:01:00",
            },
        ]
        self.validator.blocked_attempts = [
            {
                "command": ["rm", "-rf"],
                "reason": "dangerous",
                "timestamp": "2024-01-01T00:01:00",
            },
        ]

        # Act
        report = self.validator.get_security_report()

        # Assert
        assert isinstance(report, dict)
        assert "total_events" in report
        assert "blocked_attempts" in report
        assert "security_score" in report
        assert "recommendations" in report
        assert "timestamp" in report
        assert report["total_events"] == 2
        assert report["blocked_attempts"] == 1
        assert isinstance(report["security_score"], int)
        assert 0 <= report["security_score"] <= 100

    def test_get_security_report_empty_logs(self):
        """Test get_security_report avec logs vides"""
        # Arrange
        self.validator.security_log = []
        self.validator.blocked_attempts = []

        # Act
        report = self.validator.get_security_report()

        # Assert
        assert report["total_events"] == 0
        assert report["blocked_attempts"] == 0
        assert report["security_score"] == 100  # Score parfait sans événements

    def test_check_command_patterns_success(self):
        """Test cas nominal de _check_command_patterns"""
        # Arrange
        safe_command = ["ls", "-la"]

        # Act
        result = self.validator._check_command_patterns(safe_command)

        # Assert
        assert isinstance(result, dict)
        assert "is_safe" in result
        assert "risk_factors" in result
        assert result["is_safe"] is True
        assert len(result["risk_factors"]) == 0

    def test_check_command_patterns_dangerous_patterns(self):
        """Test _check_command_patterns avec patterns dangereux"""
        # Arrange
        dangerous_command = ["rm", "-rf", "/", "*"]

        # Act
        result = self.validator._check_command_patterns(dangerous_command)

        # Assert
        assert result["is_safe"] is False
        assert len(result["risk_factors"]) > 0
        assert any("rm" in factor for factor in result["risk_factors"])

    def test_check_command_patterns_edge_cases(self):
        """Test cas limites de _check_command_patterns"""
        # Arrange
        empty_command = []

        # Act
        result = self.validator._check_command_patterns(empty_command)

        # Assert
        assert result["is_safe"] is False
        assert len(result["risk_factors"]) > 0

    def test_scan_code_patterns_success(self):
        """Test cas nominal de _scan_code_patterns"""
        # Arrange
        safe_code = """
def safe_function():
    return "Hello World"
"""

        # Act
        issues = self.validator._scan_code_patterns(safe_code)

        # Assert
        assert isinstance(issues, list)
        assert len(issues) == 0  # Code sûr

    def test_scan_code_patterns_vulnerable_code(self):
        """Test _scan_code_patterns avec code vulnérable"""
        # Arrange
        vulnerable_code = """
import subprocess
import os

def dangerous_function():
    subprocess.run("rm -rf /", shell=True)
    os.system("ls")
"""

        # Act
        issues = self.validator._scan_code_patterns(vulnerable_code)

        # Assert
        assert len(issues) > 0
        assert any("subprocess" in issue["description"] for issue in issues)
        assert any("os.system" in issue["description"] for issue in issues)

    def test_scan_code_patterns_edge_cases(self):
        """Test cas limites de _scan_code_patterns"""
        # Arrange
        empty_code = ""

        # Act
        issues = self.validator._scan_code_patterns(empty_code)

        # Assert
        assert isinstance(issues, list)
        assert len(issues) == 0

    def test_generate_security_recommendations_success(self):
        """Test cas nominal de _generate_security_recommendations"""
        # Arrange
        issues = [
            {
                "type": "subprocess",
                "description": "Use of subprocess.run with shell=True",
            },
            {"type": "os.system", "description": "Use of os.system"},
        ]

        # Act
        recommendations = self.validator._generate_security_recommendations(issues)

        # Assert
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all("recommendation" in rec for rec in recommendations)
        assert all("priority" in rec for rec in recommendations)

    def test_generate_security_recommendations_no_issues(self):
        """Test _generate_security_recommendations sans issues"""
        # Arrange
        issues = []

        # Act
        recommendations = self.validator._generate_security_recommendations(issues)

        # Assert
        assert isinstance(recommendations, list)
        assert len(recommendations) == 0

    def test_initialize_allowed_commands_success(self):
        """Test cas nominal de _initialize_allowed_commands"""
        # Arrange & Act
        commands = self.validator._initialize_allowed_commands()

        # Assert
        assert isinstance(commands, set)
        assert len(commands) > 50  # Devrait avoir beaucoup de commandes autorisées
        assert "ls" in commands
        assert "find" in commands
        assert "grep" in commands
        assert "cat" in commands
        assert "head" in commands
        assert "tail" in commands
        assert "python" in commands
        assert "pip" in commands
        assert "git" in commands
