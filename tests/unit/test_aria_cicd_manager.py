#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_CICDManager
=====================================

Tests complets pour le gestionnaire CI/CD ARIA.
"""

import tempfile
from pathlib import Path

from devops_automation.cicd.aria_cicd_manager import ARIA_CICDManager
from devops_automation.security.aria_security_validator import ARIA_SecurityValidator


class TestARIA_CICDManager:
    """Tests unitaires pour ARIA_CICDManager"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.cicd_manager = ARIA_CICDManager(self.temp_dir)

    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange & Act
        cicd_manager = ARIA_CICDManager(".")

        # Assert
        assert cicd_manager.project_root == Path(".").resolve()
        assert isinstance(cicd_manager.security_validator, ARIA_SecurityValidator)
        assert isinstance(cicd_manager.cicd_config, dict)
        assert isinstance(cicd_manager.deployment_history, list)

    def test_init_with_custom_root(self):
        """Test initialisation avec racine personnalisée"""
        # Arrange
        custom_root = "/custom/path"

        # Act
        cicd_manager = ARIA_CICDManager(custom_root)

        # Assert
        assert cicd_manager.project_root == Path(custom_root).resolve()

    def test_setup_cicd_success(self):
        """Test cas nominal de setup_cicd"""
        # Arrange
        config = {
            "project_name": "ARKALIA ARIA",
            "python_version": "3.11",
            "test_command": "pytest",
            "deploy_target": "staging",
        }

        # Act
        result = self.cicd_manager.setup_cicd(config)

        # Assert
        assert isinstance(result, dict)
        assert "github_actions" in result
        assert "docker_config" in result
        assert "deployment_config" in result
        assert "monitoring_config" in result
        assert "created_files" in result
        assert isinstance(result["github_actions"], dict)
        assert isinstance(result["docker_config"], dict)
        assert isinstance(result["deployment_config"], dict)
        assert isinstance(result["monitoring_config"], dict)
        assert isinstance(result["created_files"], list)

    def test_setup_cicd_with_default_config(self):
        """Test setup_cicd avec configuration par défaut"""
        # Arrange
        config = None

        # Act
        result = self.cicd_manager.setup_cicd(config)

        # Assert
        assert "github_actions" in result
        assert "docker_config" in result
        assert "deployment_config" in result
        assert "monitoring_config" in result

    def test_setup_cicd_error_handling(self):
        """Test gestion d'erreur de setup_cicd"""
        # Arrange
        invalid_config = {"invalid": "config"}

        # Act
        result = self.cicd_manager.setup_cicd(invalid_config)

        # Assert
        assert isinstance(result, dict)
        assert "github_actions" in result
        assert "docker_config" in result
        assert "deployment_config" in result
        assert "monitoring_config" in result

    def test_generate_github_actions_success(self):
        """Test cas nominal de _generate_github_actions"""
        # Arrange
        # Act
        workflows = self.cicd_manager._generate_github_actions()

        # Assert
        assert isinstance(workflows, dict)
        assert "ci-cd.yml" in workflows
        assert "security.yml" in workflows
        assert "docs.yml" in workflows
        assert isinstance(workflows["ci-cd.yml"], dict)
        assert "name" in workflows["ci-cd.yml"]
        assert "on" in workflows["ci-cd.yml"]
        assert "jobs" in workflows["ci-cd.yml"]

    def test_generate_github_actions_edge_cases(self):
        """Test cas limites de _generate_github_actions"""
        # Arrange
        # Act
        workflows = self.cicd_manager._generate_github_actions()

        # Assert
        assert isinstance(workflows, dict)
        assert len(workflows) > 0

    def test_generate_docker_config_success(self):
        """Test cas nominal de _generate_docker_config"""
        # Arrange
        config = {
            "project_name": "ARKALIA ARIA",
            "python_version": "3.11",
            "port": 8001,
        }
        self.cicd_manager.cicd_config = config

        # Act
        result = self.cicd_manager._generate_docker_config()

        # Assert
        assert isinstance(result, dict)
        assert "Dockerfile" in result
        assert "docker-compose.yml" in result
        assert "nginx.conf" in result
        assert isinstance(result["Dockerfile"], str)
        assert isinstance(result["docker-compose.yml"], str)
        assert isinstance(result["nginx.conf"], str)

    def test_generate_docker_config_edge_cases(self):
        """Test cas limites de _generate_docker_config"""
        # Arrange
        minimal_config = {"python_version": "3.10"}
        self.cicd_manager.cicd_config = minimal_config

        # Act
        result = self.cicd_manager._generate_docker_config()

        # Assert
        assert isinstance(result, dict)
        assert "Dockerfile" in result
        assert "docker-compose.yml" in result
        assert "nginx.conf" in result

    def test_generate_monitoring_config_success(self):
        """Test cas nominal de _generate_monitoring_config"""
        # Arrange
        # Act
        result = self.cicd_manager._generate_monitoring_config()

        # Assert
        assert isinstance(result, dict)
        assert "health_checks" in result
        assert "metrics" in result
        assert "alerts" in result
        assert "logging" in result
        assert isinstance(result["health_checks"], dict)
        assert isinstance(result["metrics"], dict)
        assert isinstance(result["alerts"], dict)
        assert isinstance(result["logging"], dict)

    def test_generate_deployment_config_success(self):
        """Test cas nominal de _generate_deployment_config"""
        # Arrange
        # Act
        result = self.cicd_manager._generate_deployment_config()

        # Assert
        assert isinstance(result, dict)
        assert "staging" in result
        assert "production" in result
        assert isinstance(result["staging"], dict)
        assert isinstance(result["production"], dict)
        assert "environment" in result["staging"]
        assert "environment" in result["production"]
        assert "url" in result["staging"]
        assert "url" in result["production"]

    def test_deploy_success(self):
        """Test cas nominal de deploy"""
        # Arrange
        environment = "staging"

        # Act
        result = self.cicd_manager.deploy(environment)

        # Assert
        assert isinstance(result, dict)
        assert "timestamp" in result
        assert "environment" in result
        assert "status" in result
        assert "steps" in result
        assert "errors" in result
        assert result["environment"] == environment
        assert result["status"] in ["in_progress", "success", "failed"]
        assert isinstance(result["steps"], list)
        assert isinstance(result["errors"], list)

    def test_deploy_error_handling(self):
        """Test gestion d'erreur de deploy"""
        # Arrange
        invalid_environment = None

        # Act
        result = self.cicd_manager.deploy(invalid_environment)

        # Assert
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] in ["in_progress", "success", "failed"]

    def test_run_security_check_success(self):
        """Test cas nominal de _run_security_check"""
        # Arrange
        # Act
        result = self.cicd_manager._run_security_check()

        # Assert
        assert isinstance(result, dict)
        assert "passed" in result
        assert "issues" in result
        assert isinstance(result["passed"], bool)
        assert isinstance(result["issues"], list)

    def test_run_tests_success(self):
        """Test cas nominal de _run_tests"""
        # Arrange
        # Act
        result = self.cicd_manager._run_tests()

        # Assert
        assert isinstance(result, dict)
        assert "passed" in result
        assert "coverage" in result
        assert isinstance(result["passed"], bool)
        assert isinstance(result["coverage"], float)

    def test_build_docker_image_success(self):
        """Test cas nominal de _build_docker_image"""
        # Arrange
        # Act
        result = self.cicd_manager._build_docker_image()

        # Assert
        assert isinstance(result, dict)
        assert "success" in result
        assert "image_id" in result
        assert isinstance(result["success"], bool)
        assert isinstance(result["image_id"], str)
