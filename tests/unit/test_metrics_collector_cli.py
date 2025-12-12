"""
Tests pour le CLI des métriques ARIA
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from metrics_collector.cli import ARIA_MetricsCLI, main


class TestARIA_MetricsCLI:
    """Tests pour le CLI des métriques ARIA"""

    def test_init(self):
        """Test l'initialisation du CLI"""
        cli = ARIA_MetricsCLI()
        assert cli.collector is not None
        assert cli.exporter is not None
        assert cli.validator is not None
        assert cli.dashboard is not None

    @patch("metrics_collector.cli.ARIA_MetricsCollector")
    def test_run_collect(self, mock_collector_class):
        """Test la commande collect"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {"test": "data"}
        mock_collector_class.return_value = mock_collector

        cli = ARIA_MetricsCLI()
        cli.collector = mock_collector

        result = cli.run(["collect", "--project-root", "."])
        assert result == 0
        mock_collector.collect_all_metrics.assert_called_once()

    @patch("metrics_collector.cli.ARIA_MetricsCollector")
    def test_run_collect_with_output(self, mock_collector_class):
        """Test la commande collect avec fichier de sortie"""
        import tempfile

        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.return_value = {"test": "data"}
        mock_collector_class.return_value = mock_collector

        cli = ARIA_MetricsCLI()
        cli.collector = mock_collector

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_file = f.name

        try:
            result = cli.run(["collect", "--output", output_file])
            assert result == 0
            # Vérifier que le fichier a été créé
            assert Path(output_file).exists()
        finally:
            Path(output_file).unlink(missing_ok=True)

    @patch("metrics_collector.cli.ARIA_MetricsValidator")
    def test_run_validate(self, mock_validator_class):
        """Test la commande validate"""
        mock_validator = MagicMock()
        mock_validator.validate_metrics.return_value = {
            "is_valid": True,
            "alerts": [],
        }
        mock_validator_class.return_value = mock_validator

        cli = ARIA_MetricsCLI()
        cli.validator = mock_validator

        # Créer un fichier JSON temporaire pour les tests
        import json
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"test": "data"}, f)
            metrics_file = f.name

        try:
            result = cli.run(["validate", "--metrics-file", metrics_file])
            assert result == 0
        finally:
            Path(metrics_file).unlink(missing_ok=True)

    @patch("metrics_collector.cli.ARIA_MetricsExporter")
    def test_run_export_json(self, mock_exporter_class):
        """Test la commande export avec format JSON"""
        mock_exporter = MagicMock()
        mock_exporter.export_json.return_value = Path("/tmp/test.json")
        mock_exporter_class.return_value = mock_exporter

        cli = ARIA_MetricsCLI()
        cli.exporter = mock_exporter

        import json
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"test": "data"}, f)
            metrics_file = f.name

        try:
            result = cli.run(
                ["export", "--format", "json", "--metrics-file", metrics_file]
            )
            assert result == 0
        finally:
            Path(metrics_file).unlink(missing_ok=True)

    @patch("metrics_collector.cli.ARIA_MetricsDashboard")
    def test_run_dashboard(self, mock_dashboard_class):
        """Test la commande dashboard"""
        mock_dashboard = MagicMock()
        mock_dashboard.generate_dashboard_html.return_value = "<html>Test</html>"
        mock_dashboard_class.return_value = mock_dashboard

        cli = ARIA_MetricsCLI()
        cli.dashboard = mock_dashboard

        import json
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"test": "data"}, f)
            metrics_file = f.name

        try:
            with tempfile.TemporaryDirectory() as output_dir:
                result = cli.run(
                    [
                        "dashboard",
                        "--metrics-file",
                        metrics_file,
                        "--output-dir",
                        output_dir,
                    ]
                )
                assert result == 0
        finally:
            Path(metrics_file).unlink(missing_ok=True)

    @patch("metrics_collector.cli.ARIA_MetricsValidator")
    def test_run_health(self, mock_validator_class):
        """Test la commande health"""
        mock_validator = MagicMock()
        mock_validator.get_health_status.return_value = {
            "status": "healthy",
            "score": 95,
        }
        mock_validator_class.return_value = mock_validator

        cli = ARIA_MetricsCLI()
        cli.validator = mock_validator

        import json
        import tempfile

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"test": "data"}, f)
            metrics_file = f.name

        try:
            result = cli.run(["health", "--metrics-file", metrics_file])
            assert result == 0
        finally:
            Path(metrics_file).unlink(missing_ok=True)

    def test_run_invalid_command(self):
        """Test avec une commande invalide"""
        cli = ARIA_MetricsCLI()
        result = cli.run(["invalid_command"])
        assert result == 1

    def test_run_no_args(self):
        """Test sans arguments (affiche l'aide)"""
        cli = ARIA_MetricsCLI()
        result = cli.run([])
        assert result == 1  # Affiche l'aide et retourne 1

    @patch("metrics_collector.cli.ARIA_MetricsCLI")
    def test_main_function(self, mock_cli_class):
        """Test la fonction main()"""
        mock_cli = MagicMock()
        mock_cli.run.return_value = 0
        mock_cli_class.return_value = mock_cli

        with patch.object(sys, "argv", ["aria-metrics", "collect"]):
            result = main()
            assert result == 0

    @patch("metrics_collector.cli.ARIA_MetricsCollector")
    def test_run_collect_error_handling(self, mock_collector_class):
        """Test la gestion d'erreur dans collect"""
        mock_collector = MagicMock()
        mock_collector.collect_all_metrics.side_effect = Exception("Test error")
        mock_collector_class.return_value = mock_collector

        cli = ARIA_MetricsCLI()
        cli.collector = mock_collector

        result = cli.run(["collect"])
        assert result == 1  # Erreur retournée
