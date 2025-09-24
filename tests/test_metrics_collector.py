#!/usr/bin/env python3
"""
Tests pour le système de métriques ARIA
=======================================

Tests complets pour tous les composants du système de métriques :
- Collecteur de métriques
- Exporteur de métriques
- Validateur de métriques
- Dashboard
- API
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from metrics_collector.collectors.aria_metrics_collector import ARIA_MetricsCollector
from metrics_collector.dashboard.aria_metrics_dashboard import ARIA_MetricsDashboard
from metrics_collector.exporters.aria_metrics_exporter import ARIA_MetricsExporter
from metrics_collector.validators.aria_metrics_validator import ARIA_MetricsValidator


class TestARIA_MetricsCollector:
    """Tests pour le collecteur de métriques ARIA."""

    def test_init(self):
        """Test l'initialisation du collecteur."""
        collector = ARIA_MetricsCollector(".")
        assert collector.project_root == Path(".").resolve()
        assert isinstance(collector.exclude_patterns, set)
        assert "__pycache__" in collector.exclude_patterns
        assert "venv" in collector.exclude_patterns

    def test_collect_all_metrics(self):
        """Test la collecte complète des métriques."""
        collector = ARIA_MetricsCollector(".")
        metrics = collector.collect_all_metrics()

        # Vérifier la structure des métriques
        assert "project_info" in metrics
        assert "python_files" in metrics
        assert "aria_specific" in metrics
        assert "ml_models" in metrics
        assert "api_endpoints" in metrics
        assert "tests" in metrics
        assert "security" in metrics
        assert "performance" in metrics
        assert "documentation" in metrics
        assert "timestamp" in metrics

    def test_collect_project_info(self):
        """Test la collecte des informations du projet."""
        collector = ARIA_MetricsCollector(".")
        project_info = collector._collect_project_info()

        assert project_info["name"] == "ARKALIA ARIA"
        assert project_info["version"] == "1.0.0"
        assert "python_version" in project_info
        assert "platform" in project_info

    def test_collect_python_metrics(self):
        """Test la collecte des métriques Python."""
        collector = ARIA_MetricsCollector(".")
        python_metrics = collector._collect_python_metrics()

        assert "count" in python_metrics
        assert "core_files" in python_metrics
        assert "test_files" in python_metrics
        assert "total_lines" in python_metrics
        assert "files" in python_metrics
        assert isinstance(python_metrics["count"], int)
        assert isinstance(python_metrics["total_lines"], int)

    def test_should_exclude_file(self):
        """Test la logique d'exclusion des fichiers."""
        collector = ARIA_MetricsCollector(".")

        # Fichiers à exclure
        assert collector._should_exclude_file(Path("__pycache__/test.py"))
        assert collector._should_exclude_file(Path("venv/lib/test.py"))
        assert collector._should_exclude_file(Path(".pytest_cache/test.py"))

        # Fichiers à inclure
        assert not collector._should_exclude_file(Path("main.py"))
        assert not collector._should_exclude_file(Path("src/module.py"))

    @patch("subprocess.run")
    def test_get_test_coverage(self, mock_run):
        """Test l'obtention de la couverture de tests."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "TOTAL 85%"

        collector = ARIA_MetricsCollector(".")
        coverage = collector._get_test_coverage()

        assert isinstance(coverage, float)
        assert 0 <= coverage <= 100

    @patch("subprocess.run")
    def test_run_bandit_scan(self, mock_run):
        """Test l'exécution du scan Bandit."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = '{"results": []}'

        collector = ARIA_MetricsCollector(".")
        bandit_result = collector._run_bandit_scan()

        assert "status" in bandit_result
        assert "issues_found" in bandit_result

    @patch("subprocess.run")
    def test_run_safety_scan(self, mock_run):
        """Test l'exécution du scan Safety."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "[]"

        collector = ARIA_MetricsCollector(".")
        safety_result = collector._run_safety_scan()

        assert "status" in safety_result
        assert "vulnerabilities_found" in safety_result


class TestARIA_MetricsExporter:
    """Tests pour l'exporteur de métriques ARIA."""

    def test_init(self):
        """Test l'initialisation de l'exporteur."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = ARIA_MetricsExporter(temp_dir)
            assert exporter.output_dir == Path(temp_dir)
            assert exporter.output_dir.exists()

    def test_export_json(self):
        """Test l'export JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = ARIA_MetricsExporter(temp_dir)
            metrics = {"test": "data", "count": 42}

            file_path = exporter.export_json(metrics)

            assert file_path.exists()
            assert file_path.suffix == ".json"

            with open(file_path) as f:
                data = json.load(f)
            assert data == metrics

    def test_export_markdown(self):
        """Test l'export Markdown."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = ARIA_MetricsExporter(temp_dir)
            metrics = {
                "python_files": {"count": 10, "total_lines": 1000},
                "tests": {"test_files_count": 5, "coverage_percentage": 85.0},
                "aria_specific": {"pain_tracking": 50, "pattern_analysis": 25},
                "timestamp": "2024-01-01T00:00:00",
            }

            file_path = exporter.export_markdown(metrics)

            assert file_path.exists()
            assert file_path.suffix == ".md"

            content = file_path.read_text(encoding="utf-8")
            assert "ARKALIA ARIA" in content
            assert "Fichiers Python" in content
            assert "10" in content

    def test_export_html(self):
        """Test l'export HTML."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = ARIA_MetricsExporter(temp_dir)
            metrics = {
                "python_files": {"count": 10, "total_lines": 1000},
                "timestamp": "2024-01-01T00:00:00",
            }

            file_path = exporter.export_html(metrics)

            assert file_path.exists()
            assert file_path.suffix == ".html"

            content = file_path.read_text(encoding="utf-8")
            assert "<!DOCTYPE html>" in content
            assert "ARKALIA ARIA" in content
            assert "Dashboard" in content

    def test_export_csv(self):
        """Test l'export CSV."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = ARIA_MetricsExporter(temp_dir)
            metrics = {
                "python_files": {"count": 10, "total_lines": 1000},
                "aria_specific": {"pain_tracking": 50},
                "timestamp": "2024-01-01T00:00:00",
            }

            file_path = exporter.export_csv(metrics)

            assert file_path.exists()
            assert file_path.suffix == ".csv"

            content = file_path.read_text(encoding="utf-8")
            assert "category" in content
            assert "metric" in content
            assert "value" in content

    def test_export_all_formats(self):
        """Test l'export dans tous les formats."""
        with tempfile.TemporaryDirectory() as temp_dir:
            exporter = ARIA_MetricsExporter(temp_dir)
            metrics = {"test": "data"}

            files = exporter.export_all_formats(metrics)

            assert "json" in files
            assert "markdown" in files
            assert "html" in files
            assert "csv" in files

            for file_path in files.values():
                assert file_path.exists()


class TestARIA_MetricsValidator:
    """Tests pour le validateur de métriques ARIA."""

    def test_init(self):
        """Test l'initialisation du validateur."""
        validator = ARIA_MetricsValidator()
        assert isinstance(validator.validation_rules, dict)
        assert "min_python_files" in validator.validation_rules
        assert "min_test_coverage" in validator.validation_rules

    def test_validate_metrics(self):
        """Test la validation des métriques."""
        validator = ARIA_MetricsValidator()
        metrics = {
            "python_files": {"count": 20, "total_lines": 2000},
            "tests": {"test_files_count": 10, "coverage_percentage": 85.0},
            "aria_specific": {"cia_integration": {"cia_sync_exists": True}},
            "ml_models": {"prediction_engine_status": True},
            "security": {"bandit_scan": {"issues_found": 0}},
            "performance": {"memory_usage_mb": 500, "cpu_percent": 30},
            "documentation": {"markdown_files": 10},
        }

        results = validator.validate_metrics(metrics)

        assert "is_valid" in results
        assert "score" in results
        assert "alerts" in results
        assert "recommendations" in results
        assert "timestamp" in results
        assert isinstance(results["score"], int)
        assert 0 <= results["score"] <= 100

    def test_validate_general_metrics(self):
        """Test la validation des métriques générales."""
        validator = ARIA_MetricsValidator()

        # Test avec peu de fichiers Python
        metrics = {"python_files": {"count": 5}}
        validator._validate_general_metrics(metrics)
        assert len(validator.alerts) > 0
        assert any("insuffisant" in alert["message"] for alert in validator.alerts)

    def test_validate_aria_metrics(self):
        """Test la validation des métriques ARIA spécifiques."""
        validator = ARIA_MetricsValidator()

        # Test sans intégration CIA
        metrics = {"aria_specific": {"cia_integration": {"cia_sync_exists": False}}}
        validator._validate_aria_metrics(metrics)
        assert len(validator.alerts) > 0
        assert any("CIA" in alert["message"] for alert in validator.alerts)

    def test_validate_security_metrics(self):
        """Test la validation des métriques de sécurité."""
        validator = ARIA_MetricsValidator()

        # Test avec beaucoup d'issues de sécurité
        metrics = {"security": {"bandit_scan": {"issues_found": 10}}}
        validator._validate_security_metrics(metrics)
        assert len(validator.alerts) > 0
        assert any("sécurité" in alert["message"] for alert in validator.alerts)

    def test_calculate_validation_score(self):
        """Test le calcul du score de validation."""
        validator = ARIA_MetricsValidator()
        metrics = {
            "python_files": {"count": 25},
            "tests": {"coverage_percentage": 85},
            "security": {"bandit_scan": {"issues_found": 0}},
        }

        score = validator._calculate_validation_score(metrics)
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_get_health_status(self):
        """Test l'obtention du statut de santé."""
        validator = ARIA_MetricsValidator()
        metrics = {
            "python_files": {"count": 20},
            "tests": {"coverage_percentage": 80},
            "security": {"bandit_scan": {"issues_found": 0}},
        }

        health_status = validator.get_health_status(metrics)

        assert "status" in health_status
        assert "color" in health_status
        assert "score" in health_status
        assert "alerts_count" in health_status
        assert "recommendations_count" in health_status
        assert health_status["status"] in ["excellent", "good", "fair", "poor"]


class TestARIA_MetricsDashboard:
    """Tests pour le dashboard de métriques ARIA."""

    def test_init(self):
        """Test l'initialisation du dashboard."""
        dashboard = ARIA_MetricsDashboard()
        assert dashboard.templates_dir.exists()
        assert dashboard.static_dir.exists()

    def test_generate_dashboard_html(self):
        """Test la génération du HTML du dashboard."""
        dashboard = ARIA_MetricsDashboard()
        metrics = {
            "python_files": {"count": 10, "total_lines": 1000},
            "aria_specific": {"pain_tracking": 50},
            "timestamp": "2024-01-01T00:00:00",
        }

        html = dashboard.generate_dashboard_html(metrics)

        assert "<!DOCTYPE html>" in html
        assert "ARKALIA ARIA" in html
        assert "Dashboard" in html
        assert "10" in html  # Nombre de fichiers Python
        assert "50" in html  # Entrées de douleur

    def test_create_static_files(self):
        """Test la création des fichiers statiques."""
        with tempfile.TemporaryDirectory() as temp_dir:
            dashboard = ARIA_MetricsDashboard()
            dashboard.static_dir = Path(temp_dir)

            dashboard.create_static_files()

            css_file = dashboard.static_dir / "dashboard.css"
            js_file = dashboard.static_dir / "dashboard.js"

            assert css_file.exists()
            assert js_file.exists()

            assert "dashboard-container" in css_file.read_text()
            assert "ARKALIA ARIA" in js_file.read_text()


class TestIntegration:
    """Tests d'intégration pour le système complet."""

    def test_full_workflow(self):
        """Test le workflow complet : collecte -> validation -> export."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Collecte
            collector = ARIA_MetricsCollector(".")
            metrics = collector.collect_all_metrics()

            # Validation
            validator = ARIA_MetricsValidator()
            validation_results = validator.validate_metrics(metrics)

            # Export
            exporter = ARIA_MetricsExporter(temp_dir)
            files = exporter.export_all_formats(metrics)

            # Vérifications
            assert isinstance(metrics, dict)
            assert isinstance(validation_results, dict)
            assert len(files) == 4  # json, markdown, html, csv

            for file_path in files.values():
                assert file_path.exists()

    def test_dashboard_integration(self):
        """Test l'intégration du dashboard avec les métriques."""
        collector = ARIA_MetricsCollector(".")
        metrics = collector.collect_all_metrics()

        dashboard = ARIA_MetricsDashboard()
        html = dashboard.generate_dashboard_html(metrics)

        assert isinstance(html, str)
        assert len(html) > 1000  # HTML substantiel
        assert "ARKALIA ARIA" in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
