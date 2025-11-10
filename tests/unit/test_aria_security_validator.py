#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_SecurityValidator
==========================================

Tests complets pour le validateur de sécurité ARIA.
"""

import tempfile
from pathlib import Path

import pytest

from devops_automation.security.aria_security_validator import (
    ARIA_SecurityValidator,
    SecurityError,
)


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
        assert "python" in validator.allowed_commands
        assert "git" in validator.allowed_commands
        assert isinstance(validator.security_log, list)
        assert isinstance(validator.blocked_attempts, list)

    def test_validate_command_success(self):
        """Test cas nominal de validate_command"""
        # Arrange
        command = ["ls", "-la"]

        # Act
        result = self.validator.validate_command(command)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 3
        is_valid, message, security_info = result
        assert isinstance(is_valid, bool)
        assert isinstance(message, str)
        assert isinstance(security_info, dict)
        assert is_valid is True
        assert "validated" in security_info
        assert "risk_level" in security_info
        assert "command" in security_info
        assert "timestamp" in security_info
        assert security_info["validated"] is True
        assert security_info["risk_level"] in ["low", "medium", "high"]
        assert security_info["command"] == ["ls", "-la"]

    def test_validate_command_blocked_command(self):
        """Test validation avec commande bloquée"""
        # Arrange
        command = ["rm", "-rf", "/"]

        # Act
        result = self.validator.validate_command(command)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 3
        is_valid, message, security_info = result
        assert isinstance(is_valid, bool)
        assert isinstance(message, str)
        assert isinstance(security_info, dict)
        assert is_valid is False
        assert "validated" in security_info
        assert "risk_level" in security_info
        assert security_info["validated"] is False
        assert security_info["risk_level"] in ["low", "medium", "high"]

    def test_validate_command_injection_attempt(self):
        """Test validation avec tentative d'injection"""
        # Arrange
        command = ["ls; rm -rf /"]

        # Act
        result = self.validator.validate_command(command)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 3
        is_valid, message, security_info = result
        assert isinstance(is_valid, bool)
        assert isinstance(message, str)
        assert isinstance(security_info, dict)
        assert is_valid is False
        assert "validated" in security_info
        assert "risk_level" in security_info
        assert security_info["validated"] is False
        assert security_info["risk_level"] in ["low", "medium", "high"]

    def test_validate_command_edge_cases(self):
        """Test validation avec cas limites"""
        # Arrange
        command = ["python", "-c", "print('hello')"]

        # Act
        result = self.validator.validate_command(command)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 3
        is_valid, message, security_info = result
        assert isinstance(is_valid, bool)
        assert isinstance(message, str)
        assert isinstance(security_info, dict)
        assert "validated" in security_info
        assert "risk_level" in security_info
        assert "command" in security_info
        assert "timestamp" in security_info

    def test_validate_command_none_input(self):
        """Test validation avec entrée None"""
        # Arrange
        command = None

        # Act
        result = self.validator.validate_command(command)

        # Assert
        assert isinstance(result, tuple)
        assert len(result) == 3
        is_valid, message, security_info = result
        assert isinstance(is_valid, bool)
        assert isinstance(message, str)
        assert isinstance(security_info, dict)
        assert is_valid is False
        assert "validated" in security_info
        assert "risk_level" in security_info
        assert security_info["validated"] is False
        assert security_info["risk_level"] in ["low", "medium", "high"]

    def test_audit_code_security_success(self):
        """Test cas nominal de audit_code_security"""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("print('Hello World')")
            file_path = Path(f.name)

        try:
            # Act
            result = self.validator.audit_code_security(file_path)

            # Assert
            assert isinstance(result, dict)
            assert "file_path" in result
            assert "risk_score" in result
            assert "issues" in result
            assert "timestamp" in result
            assert isinstance(result["risk_score"], int)
            assert isinstance(result["issues"], list)
            assert result["file_path"] == str(file_path)
        finally:
            file_path.unlink()

    def test_audit_code_security_with_vulnerabilities(self):
        """Test audit_code_security avec vulnérabilités"""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("import subprocess\nsubprocess.run('rm -rf /')")
            file_path = Path(f.name)

        try:
            # Act
            result = self.validator.audit_code_security(file_path)

            # Assert
            assert isinstance(result, dict)
            assert "file_path" in result
            assert "risk_score" in result
            assert "issues" in result
            assert "timestamp" in result
            assert isinstance(result["risk_score"], int)
            assert isinstance(result["issues"], list)
            assert result["file_path"] == str(file_path)
        finally:
            file_path.unlink()

    def test_audit_code_security_empty_content(self):
        """Test audit_code_security avec contenu vide"""
        # Arrange
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("")
            file_path = Path(f.name)

        try:
            # Act
            result = self.validator.audit_code_security(file_path)

            # Assert
            assert isinstance(result, dict)
            assert "file_path" in result
            assert "risk_score" in result
            assert "issues" in result
            assert "timestamp" in result
            assert isinstance(result["risk_score"], int)
            assert isinstance(result["issues"], list)
            assert result["file_path"] == str(file_path)
        finally:
            file_path.unlink()

    def test_calculate_risk_summary_success(self):
        """Test cas nominal de _calculate_risk_summary"""
        # Arrange
        # Ajouter quelques entrées dans les logs
        self.validator.security_log = [
            {"timestamp": "2024-01-01T00:00:00", "event_type": "VALIDATED"},
            {"timestamp": "2024-01-01T00:01:00", "event_type": "BLOCKED"},
        ]
        self.validator.blocked_attempts = [
            {"timestamp": "2024-01-01T00:01:00", "command": ["rm", "-rf", "/"]},
        ]

        # Act
        summary = self.validator._calculate_risk_summary()

        # Assert
        assert isinstance(summary, dict)
        assert "total_events" in summary
        assert "risk_levels" in summary
        assert "risk_percentage" in summary
        assert isinstance(summary["total_events"], int)
        assert isinstance(summary["risk_levels"], dict)
        assert isinstance(summary["risk_percentage"], dict)

    def test_calculate_risk_summary_empty(self):
        """Test _calculate_risk_summary avec logs vides"""
        # Arrange
        self.validator.security_log = []
        self.validator.blocked_attempts = []

        # Act
        summary = self.validator._calculate_risk_summary()

        # Assert
        assert isinstance(summary, dict)
        assert summary["total_events"] == 0
        assert "risk_levels" in summary
        assert "risk_percentage" in summary

    def test_get_security_report_success(self):
        """Test cas nominal de get_security_report"""
        # Arrange
        # Ajouter quelques entrées dans les logs
        self.validator.security_log = [
            {"timestamp": "2024-01-01T00:00:00", "event_type": "VALIDATED"},
            {"timestamp": "2024-01-01T00:01:00", "event_type": "BLOCKED"},
        ]
        self.validator.blocked_attempts = [
            {"timestamp": "2024-01-01T00:01:00", "command": ["rm", "-rf", "/"]},
        ]

        # Act
        report = self.validator.get_security_report()

        # Assert
        assert isinstance(report, dict)
        assert "timestamp" in report
        assert "total_validations" in report
        assert "blocked_attempts" in report
        assert "security_log" in report
        assert "blocked_commands" in report
        assert "risk_summary" in report

    def test_execute_secure_command_success(self):
        """Test cas nominal de execute_secure_command"""
        # Arrange
        command = ["echo", "test"]

        # Act
        result = self.validator.execute_secure_command(command, "test_context")

        # Assert
        assert hasattr(result, "returncode")
        assert hasattr(result, "stdout")
        assert hasattr(result, "stderr")
        assert isinstance(result.returncode, int)
        assert isinstance(result.stdout, str)
        assert isinstance(result.stderr, str)

    def test_execute_secure_command_blocked(self):
        """Test execute_secure_command avec commande bloquée"""
        # Arrange
        command = ["rm", "-rf", "/"]

        # Act & Assert
        with pytest.raises(SecurityError):
            self.validator.execute_secure_command(command, "test_context")

    def test_get_security_report_empty(self):
        """Test get_security_report avec logs vides"""
        # Arrange
        self.validator.security_log = []
        self.validator.blocked_attempts = []

        # Act
        report = self.validator.get_security_report()

        # Assert
        assert isinstance(report, dict)
        assert "timestamp" in report
        assert "total_validations" in report
        assert "blocked_attempts" in report
        assert "security_log" in report
        assert "blocked_commands" in report
        assert "risk_summary" in report
        assert len(report["security_log"]) == 0
        assert len(report["blocked_commands"]) == 0

    def test_log_security_event_success(self):
        """Test cas nominal de _log_security_event"""
        # Arrange
        event_type = "TEST_EVENT"
        details = {"test": "data", "timestamp": "2024-01-01T00:00:00"}

        # Act
        self.validator._log_security_event(event_type, details)

        # Assert
        assert len(self.validator.security_log) == 1
        log_entry = self.validator.security_log[0]
        assert "timestamp" in log_entry
        assert "event_type" in log_entry
        assert "context" in log_entry
        assert "command" in log_entry
        assert "risk_level" in log_entry
        assert "reason" in log_entry
        assert log_entry["event_type"] == event_type

    def test_log_security_event_none_input(self):
        """Test _log_security_event avec entrée None"""
        # Arrange
        event_type = None
        details = None

        # Act & Assert
        with pytest.raises(TypeError):
            self.validator._log_security_event(event_type, details)

    def test_initialize_allowed_commands_success(self):
        """Test cas nominal de _initialize_allowed_commands"""
        # Act
        commands = self.validator._initialize_allowed_commands()

        # Assert
        assert isinstance(commands, set)
        assert len(commands) > 0
        assert "ls" in commands
        assert "python" in commands
        assert "git" in commands
        assert "pytest" in commands
        assert "black" in commands
        assert "ruff" in commands
        assert "mypy" in commands
        assert "bandit" in commands
        assert "safety" in commands
