#!/usr/bin/env python3
"""
ARKALIA ARIA - CLI des Métriques
===============================

Interface en ligne de commande pour le système de métriques ARIA.
Permet la collecte, validation et export des métriques depuis le terminal.
"""

import argparse
import json
import sys
from typing import Any

from .collectors.aria_metrics_collector import ARIA_MetricsCollector
from .dashboard.aria_metrics_dashboard import ARIA_MetricsDashboard
from .exporters.aria_metrics_exporter import ARIA_MetricsExporter
from .dashboard.aria_metrics_dashboard import ARIA_MetricsDashboard
from .validators.aria_metrics_validator import ARIA_MetricsValidator


class ARIA_MetricsCLI:
    """
    Interface en ligne de commande pour les métriques ARIA.

    Commandes disponibles :
    - collect : Collecte les métriques
    - validate : Valide les métriques
    - export : Exporte les métriques
    - dashboard : Génère le dashboard HTML
    - health : Affiche le statut de santé
    """

    def __init__(self) -> None:
        """Initialise le CLI des métriques."""
        self.collector = ARIA_MetricsCollector()
        self.exporter = ARIA_MetricsExporter()
        self.validator = ARIA_MetricsValidator()
        self.dashboard = ARIA_MetricsDashboard()
        self.dashboard = ARIA_MetricsDashboard()

    def run(self, args: list[str] | None = None) -> int:
        """
        Exécute le CLI avec les arguments fournis.

        Args:
            args: Arguments de la ligne de commande

        Returns:
            Code de sortie (0 = succès, 1 = erreur)
        """
        parser = self._create_parser()

        if args is None:
            args = sys.argv[1:]

        parsed_args = parser.parse_args(args)

        try:
            if parsed_args.command == "collect":
                return self._handle_collect(parsed_args)
            elif parsed_args.command == "validate":
                return self._handle_validate(parsed_args)
            elif parsed_args.command == "export":
                return self._handle_export(parsed_args)
            elif parsed_args.command == "dashboard":
                return self._handle_dashboard(parsed_args)
            elif parsed_args.command == "health":
                return self._handle_health(parsed_args)
            else:
                parser.print_help()
                return 1

        except Exception as e:
            print(f"❌ Erreur : {e}", file=sys.stderr)
            return 1

    def _create_parser(self) -> argparse.ArgumentParser:
        """Crée le parser d'arguments."""
        parser = argparse.ArgumentParser(
            description="ARKALIA ARIA - Système de Métriques",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Exemples d'utilisation :
  aria-metrics collect                    # Collecte les métriques
  aria-metrics validate                   # Valide les métriques
  aria-metrics export --format json       # Exporte en JSON
  aria-metrics dashboard                  # Génère le dashboard
  aria-metrics health                     # Affiche le statut de santé
            """,
        )

        subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

        # Commande collect
        collect_parser = subparsers.add_parser("collect", help="Collecte les métriques")
        collect_parser.add_argument(
            "--project-root", default=".", help="Racine du projet"
        )
        collect_parser.add_argument("--output", help="Fichier de sortie JSON")

        # Commande validate
        validate_parser = subparsers.add_parser("validate", help="Valide les métriques")
        validate_parser.add_argument(
            "--project-root", default=".", help="Racine du projet"
        )
        validate_parser.add_argument(
            "--strict", action="store_true", help="Mode strict"
        )

        # Commande export
        export_parser = subparsers.add_parser("export", help="Exporte les métriques")
        export_parser.add_argument(
            "--format",
            choices=["json", "markdown", "html", "csv"],
            default="json",
            help="Format d'export",
        )
        export_parser.add_argument(
            "--output-dir", default="metrics_reports", help="Répertoire de sortie"
        )
        export_parser.add_argument(
            "--project-root", default=".", help="Racine du projet"
        )

        # Commande dashboard
        dashboard_parser = subparsers.add_parser(
            "dashboard", help="Génère le dashboard HTML"
        )
        dashboard_parser.add_argument("--output", help="Fichier HTML de sortie")
        dashboard_parser.add_argument(
            "--project-root", default=".", help="Racine du projet"
        )

        # Commande health
        health_parser = subparsers.add_parser(
            "health", help="Affiche le statut de santé"
        )
        health_parser.add_argument(
            "--project-root", default=".", help="Racine du projet"
        )
        health_parser.add_argument("--json", action="store_true", help="Sortie JSON")

        return parser

    def _handle_collect(self, args: argparse.Namespace) -> int:
        """Gère la commande collect."""
        print("🚀 Collecte des métriques ARIA...")

        try:
            # Configurer le collecteur
            if args.project_root != ".":
                self.collector = ARIA_MetricsCollector(args.project_root)

            # Collecter les métriques
            metrics = self.collector.collect_all_metrics()

            # Afficher un résumé
            self._print_collection_summary(metrics)

            # Sauvegarder si demandé
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(metrics, f, indent=2, ensure_ascii=False)
                print(f"📁 Métriques sauvegardées dans : {args.output}")

            return 0

        except Exception as e:
            print(f"❌ Erreur lors de la collecte : {e}", file=sys.stderr)
            return 1

    def _handle_validate(self, args: argparse.Namespace) -> int:
        """Gère la commande validate."""
        print("🔍 Validation des métriques ARIA...")

        try:
            # Configurer le collecteur
            if args.project_root != ".":
                self.collector = ARIA_MetricsCollector(args.project_root)

            # Collecter et valider
            metrics = self.collector.collect_all_metrics()
            validation_results = self.validator.validate_metrics(metrics)

            # Afficher les résultats
            self._print_validation_results(validation_results, args.strict)

            return 0 if validation_results["is_valid"] else 1

        except Exception as e:
            print(f"❌ Erreur lors de la validation : {e}", file=sys.stderr)
            return 1

    def _handle_export(self, args: argparse.Namespace) -> int:
        """Gère la commande export."""
        print(f"📤 Export des métriques en format {args.format.upper()}...")

        try:
            # Configurer les composants
            if args.project_root != ".":
                self.collector = ARIA_MetricsCollector(args.project_root)

            self.exporter = ARIA_MetricsExporter(args.output_dir)

            # Collecter les métriques
            metrics = self.collector.collect_all_metrics()

            # Exporter
            if args.format == "json":
                file_path = self.exporter.export_json(metrics)
            elif args.format == "markdown":
                file_path = self.exporter.export_markdown(metrics)
            elif args.format == "html":
                file_path = self.exporter.export_html(metrics)
            elif args.format == "csv":
                file_path = self.exporter.export_csv(metrics)

            print(f"✅ Export réussi : {file_path}")
            return 0

        except Exception as e:
            print(f"❌ Erreur lors de l'export : {e}", file=sys.stderr)
            return 1

    def _handle_dashboard(self, args: argparse.Namespace) -> int:
        """Gère la commande dashboard."""
        print("🎨 Génération du dashboard HTML...")

        try:
            # Configurer le collecteur
            if args.project_root != ".":
                self.collector = ARIA_MetricsCollector(args.project_root)

            # Collecter les métriques
            metrics = self.collector.collect_all_metrics()

            # Générer le dashboard
            dashboard_html = self.dashboard.generate_dashboard_html(metrics)

            # Sauvegarder
            output_file = args.output or "aria_dashboard.html"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(dashboard_html)

            print(f"✅ Dashboard généré : {output_file}")
            print(
                "🌐 Ouvrez le fichier dans votre navigateur pour voir le dashboard interactif"
            )
            return 0

        except Exception as e:
            print(
                f"❌ Erreur lors de la génération du dashboard : {e}", file=sys.stderr
            )
            return 1

    def _handle_health(self, args: argparse.Namespace) -> int:
        """Gère la commande health."""
        print("🏥 Vérification du statut de santé...")

        try:
            # Configurer le collecteur
            if args.project_root != ".":
                self.collector = ARIA_MetricsCollector(args.project_root)

            # Collecter les métriques
            metrics = self.collector.collect_all_metrics()
            health_status = self.validator.get_health_status(metrics)

            # Afficher le statut
            if args.json:
                print(json.dumps(health_status, indent=2, ensure_ascii=False))
            else:
                self._print_health_status(health_status)

            return 0 if health_status["status"] in ["excellent", "good"] else 1

        except Exception as e:
            print(f"❌ Erreur lors de la vérification de santé : {e}", file=sys.stderr)
            return 1

    def _print_collection_summary(self, metrics: dict[str, Any]) -> None:
        """Affiche un résumé de la collecte."""
        print("\n📊 Résumé de la Collecte :")
        print("=" * 50)

        python_files = metrics.get("python_files", {})
        print(f"🐍 Fichiers Python : {python_files.get('count', 0)}")
        print(f"📝 Lignes de Code : {python_files.get('total_lines', 0)}")

        tests = metrics.get("tests", {})
        print(f"🧪 Tests : {tests.get('test_files_count', 0)}")
        print(f"📊 Couverture : {tests.get('coverage_percentage', 0):.1f}%")

        aria_specific = metrics.get("aria_specific", {})
        print(f"🎯 Entrées Douleur : {aria_specific.get('pain_tracking', 0)}")
        print(f"🔍 Patterns : {aria_specific.get('pattern_analysis', 0)}")

        security = metrics.get("security", {})
        print(
            f"🔒 Issues Sécurité : {security.get('bandit_scan', {}).get('issues_found', 0)}"
        )

        print("=" * 50)

    def _print_validation_results(
        self, results: dict[str, Any], strict: bool = False
    ) -> None:
        """Affiche les résultats de validation."""
        print("\n🔍 Résultats de Validation :")
        print("=" * 50)

        score = results.get("score", 0)
        is_valid = results.get("is_valid", False)

        print(f"📊 Score Global : {score}/100")
        print(f"✅ Statut : {'Valide' if is_valid else 'Invalide'}")

        alerts = results.get("alerts", [])
        if alerts:
            print(f"\n🚨 Alertes ({len(alerts)}) :")
            for alert in alerts:
                severity = alert.get("severity", "unknown")
                message = alert.get("message", "Message manquant")
                print(f"  - {severity.upper()}: {message}")

        recommendations = results.get("recommendations", [])
        if recommendations:
            print(f"\n💡 Recommandations ({len(recommendations)}) :")
            for rec in recommendations:
                message = rec.get("message", "Message manquant")
                print(f"  - {message}")

        print("=" * 50)

    def _print_health_status(self, status: dict[str, Any]) -> None:
        """Affiche le statut de santé."""
        print("\n🏥 Statut de Santé :")
        print("=" * 50)

        status_name = status.get("status", "unknown")
        score = status.get("score", 0)

        print(f"📊 Score : {score}/100")
        print(f"🎯 Statut : {status_name.upper()}")
        print(f"🚨 Alertes : {status.get('alerts_count', 0)}")
        print(f"💡 Recommandations : {status.get('recommendations_count', 0)}")

        print("=" * 50)


def main() -> int:
    """Point d'entrée principal du CLI."""
    cli = ARIA_MetricsCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())
