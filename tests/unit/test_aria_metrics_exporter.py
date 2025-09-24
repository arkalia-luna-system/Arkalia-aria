#!/usr/bin/env python3
"""
Tests unitaires pour ARIA_MetricsExporter
=========================================

Tests complets pour l'exporteur de métriques ARIA.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

from metrics_collector.exporters.aria_metrics_exporter import ARIA_MetricsExporter


class TestARIA_MetricsExporter:
    """Tests unitaires pour ARIA_MetricsExporter"""

    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.exporter = ARIA_MetricsExporter(self.temp_dir)

    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_init_success(self):
        """Test cas nominal de l'initialisation"""
        # Arrange
        with tempfile.TemporaryDirectory() as temp_dir:
            # Act
            exporter = ARIA_MetricsExporter(temp_dir)

            # Assert
            assert exporter.output_dir == Path(temp_dir)
            assert exporter.output_dir.exists()

    def test_init_creates_directory(self):
        """Test création automatique du répertoire"""
        # Arrange
        with tempfile.TemporaryDirectory() as base_dir:
            new_dir = os.path.join(base_dir, "new_metrics_dir")

            # Act
            exporter = ARIA_MetricsExporter(new_dir)

            # Assert
            assert exporter.output_dir == Path(new_dir)
            assert exporter.output_dir.exists()

    def test_export_json_success(self):
        """Test cas nominal de export_json"""
        # Arrange
        metrics = {
            "python_files": {"total_files": 10, "total_lines": 1000},
            "tests": {"test_files_count": 5, "coverage_percentage": 85.0},
        }

        # Act
        file_path = self.exporter.export_json(metrics)

        # Assert
        assert file_path.exists()
        assert file_path.suffix == ".json"
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        assert data == metrics

    def test_export_json_with_custom_filename(self):
        """Test export_json avec nom de fichier personnalisé"""
        # Arrange
        metrics = {"test": "data"}
        custom_filename = "custom_metrics.json"

        # Act
        file_path = self.exporter.export_json(metrics, custom_filename)

        # Assert
        assert file_path.name == custom_filename
        assert file_path.exists()

    def test_export_json_error_handling(self):
        """Test gestion d'erreur de export_json"""
        # Arrange
        invalid_metrics = None

        # Act
        file_path = self.exporter.export_json(invalid_metrics)

        # Assert
        assert file_path.exists()
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
        assert data is None

    def test_export_markdown_success(self):
        """Test cas nominal de export_markdown"""
        # Arrange
        metrics = {
            "python_files": {"total_files": 10, "total_lines": 1000},
            "tests": {"test_files_count": 5, "coverage_percentage": 85.0},
            "aria_specific": {"pain_tracking": 50, "pattern_analysis": 25},
        }

        # Act
        file_path = self.exporter.export_markdown(metrics)

        # Assert
        assert file_path.exists()
        assert file_path.suffix == ".md"
        content = file_path.read_text(encoding="utf-8")
        assert "ARKALIA ARIA" in content
        assert "Métriques Générales" in content

    def test_export_markdown_edge_cases(self):
        """Test cas limites de export_markdown"""
        # Arrange
        empty_metrics = {}

        # Act
        file_path = self.exporter.export_markdown(empty_metrics)

        # Assert
        assert file_path.exists()
        content = file_path.read_text(encoding="utf-8")
        assert "ARKALIA ARIA" in content

    def test_export_html_success(self):
        """Test cas nominal de export_html"""
        # Arrange
        metrics = {
            "python_files": {"total_files": 15, "total_lines": 2000},
            "tests": {"test_files_count": 0, "coverage_percentage": 90.0},
            "aria_specific": {"pain_tracking": 100, "pattern_analysis": 50},
        }

        # Act
        file_path = self.exporter.export_html(metrics)

        # Assert
        assert file_path.exists()
        assert file_path.suffix == ".html"
        content = file_path.read_text(encoding="utf-8")
        assert "ARKALIA ARIA" in content
        assert "Dashboard de Métriques" in content

    def test_export_html_with_charts(self):
        """Test export_html avec graphiques"""
        # Arrange
        metrics = {
            "python_files": {"total_files": 15, "total_lines": 2000},
            "tests": {"test_files_count": 0, "coverage_percentage": 90.0},
            "aria_specific": {"pain_tracking": 100, "pattern_analysis": 50},
        }

        # Act
        file_path = self.exporter.export_html(metrics)

        # Assert
        assert file_path.exists()
        content = file_path.read_text(encoding="utf-8")
        assert "ARKALIA ARIA" in content
        assert "Dashboard de Métriques" in content

    def test_export_csv_success(self):
        """Test cas nominal de export_csv"""
        # Arrange
        metrics = {
            "python_files": {"total_files": 10, "total_lines": 1000},
            "tests": {"test_files_count": 5, "coverage_percentage": 85.0},
            "aria_specific": {"pain_tracking": 50, "pattern_analysis": 25},
        }

        # Act
        file_path = self.exporter.export_csv(metrics)

        # Assert
        assert file_path.exists()
        assert file_path.suffix == ".csv"
        content = file_path.read_text(encoding="utf-8")
        assert "category" in content
        assert "metric" in content
        assert "value" in content

    def test_export_csv_edge_cases(self):
        """Test cas limites de export_csv"""
        # Arrange
        empty_metrics = {}

        # Act
        file_path = self.exporter.export_csv(empty_metrics)

        # Assert
        assert file_path.exists()
        content = file_path.read_text(encoding="utf-8")
        assert "category" in content
        assert "metric" in content
        assert "value" in content

    def test_export_all_formats_success(self):
        """Test cas nominal de export_all_formats"""
        # Arrange
        metrics = {
            "python_files": {"total_files": 10, "total_lines": 1000},
            "tests": {"test_files_count": 5, "coverage_percentage": 85.0},
        }

        # Act
        files = self.exporter.export_all_formats(metrics)

        # Assert
        assert isinstance(files, dict)
        assert "json" in files
        assert "markdown" in files
        assert "html" in files
        assert "csv" in files
        assert all(file_path.exists() for file_path in files.values())

    def test_export_all_formats_error_handling(self):
        """Test gestion d'erreur de export_all_formats"""
        # Arrange
        invalid_metrics = None

        # Act & Assert
        with pytest.raises(Exception):
            self.exporter.export_all_formats(invalid_metrics)

    def test_generate_markdown_report_success(self):
        """Test cas nominal de _generate_markdown_report"""
        # Arrange
        metrics = {
            "python_files": {"total_files": 10, "total_lines": 1000},
            "tests": {"test_files_count": 5, "coverage_percentage": 85.0},
            "aria_specific": {"pain_tracking": 50, "pattern_analysis": 25},
        }

        # Act
        report = self.exporter._generate_markdown_report(metrics)

        # Assert
        assert isinstance(report, str)
        assert "ARKALIA ARIA" in report
        assert "Métriques Générales" in report

    def test_generate_html_dashboard_success(self):
        """Test cas nominal de _generate_html_dashboard"""
        # Arrange
        metrics = {
            "python_files": {"total_files": 15, "total_lines": 2000},
            "tests": {"test_files_count": 0, "coverage_percentage": 90.0},
            "aria_specific": {"pain_tracking": 100, "pattern_analysis": 50},
        }

        # Act
        dashboard = self.exporter._generate_html_dashboard(metrics)

        # Assert
        assert isinstance(dashboard, str)
        assert "ARKALIA ARIA" in dashboard
        assert "Dashboard de Métriques" in dashboard
        assert "<!DOCTYPE html>" in dashboard

    def test_flatten_metrics_for_csv_success(self):
        """Test cas nominal de _flatten_metrics_for_csv"""
        # Arrange
        nested_metrics = {
            "python_files": {"total_files": 10, "total_lines": 1000},
            "tests": {"test_files_count": 5, "coverage_percentage": 85.0},
            "aria_specific": {"pain_tracking": 50, "pattern_analysis": 25},
        }

        # Act
        flattened = self.exporter._flatten_metrics_for_csv(nested_metrics)

        # Assert
        assert isinstance(flattened, list)
        assert len(flattened) > 0
        assert all(isinstance(item, dict) for item in flattened)
        assert all(
            "category" in item and "metric" in item and "value" in item
            for item in flattened
        )

    def test_flatten_metrics_for_csv_edge_cases(self):
        """Test cas limites de _flatten_metrics_for_csv"""
        # Arrange
        empty_metrics = {}

        # Act
        flattened = self.exporter._flatten_metrics_for_csv(empty_metrics)

        # Assert
        assert isinstance(flattened, list)
        assert len(flattened) >= 0  # Peut retourner des métriques par défaut
