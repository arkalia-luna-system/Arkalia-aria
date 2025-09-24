#!/usr/bin/env python3
"""
Script de test pour le système de métriques ARIA
================================================

Teste tous les composants du système de métriques intégré.
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au Python path
sys.path.insert(0, str(Path(__file__).parent))

from metrics_collector.collectors.aria_metrics_collector import ARIA_MetricsCollector
from metrics_collector.dashboard.aria_metrics_dashboard import ARIA_MetricsDashboard
from metrics_collector.exporters.aria_metrics_exporter import ARIA_MetricsExporter
from metrics_collector.validators.aria_metrics_validator import ARIA_MetricsValidator


def test_metrics_collection():
    """Test la collecte des métriques."""
    print("🚀 Test de collecte des métriques...")

    collector = ARIA_MetricsCollector(".")
    metrics = collector.collect_all_metrics()

    print(f"✅ Métriques collectées : {len(metrics)} sections")
    print(f"📊 Fichiers Python : {metrics.get('python_files', {}).get('count', 0)}")
    print(
        f"📝 Lignes de code : {metrics.get('python_files', {}).get('total_lines', 0)}"
    )
    print(f"🧪 Tests : {metrics.get('tests', {}).get('test_files_count', 0)}")

    return metrics


def test_metrics_validation(metrics):
    """Test la validation des métriques."""
    print("\n🔍 Test de validation des métriques...")

    validator = ARIA_MetricsValidator()
    validation_results = validator.validate_metrics(metrics)

    print("✅ Validation terminée")
    print(f"📊 Score : {validation_results.get('score', 0)}/100")
    print(
        f"✅ Statut : {'Valide' if validation_results.get('is_valid', False) else 'Invalide'}"
    )
    print(f"🚨 Alertes : {len(validation_results.get('alerts', []))}")
    print(f"💡 Recommandations : {len(validation_results.get('recommendations', []))}")

    return validation_results


def test_metrics_export(metrics):
    """Test l'export des métriques."""
    print("\n📤 Test d'export des métriques...")

    exporter = ARIA_MetricsExporter("test_metrics_reports")

    # Export JSON
    json_file = exporter.export_json(metrics)
    print(f"✅ Export JSON : {json_file}")

    # Export Markdown
    md_file = exporter.export_markdown(metrics)
    print(f"✅ Export Markdown : {md_file}")

    # Export HTML
    html_file = exporter.export_html(metrics)
    print(f"✅ Export HTML : {html_file}")

    # Export CSV
    csv_file = exporter.export_csv(metrics)
    print(f"✅ Export CSV : {csv_file}")

    return [json_file, md_file, html_file, csv_file]


def test_dashboard_generation(metrics):
    """Test la génération du dashboard."""
    print("\n🎨 Test de génération du dashboard...")

    dashboard = ARIA_MetricsDashboard()
    html = dashboard.generate_dashboard_html(metrics)

    print(f"✅ Dashboard généré : {len(html)} caractères")
    print(f"🌐 Contient 'ARKALIA ARIA' : {'ARKALIA ARIA' in html}")
    print(f"📊 Contient des métriques : {'10' in html or '0' in html}")

    # Sauvegarder le dashboard
    dashboard_file = Path("test_dashboard.html")
    dashboard_file.write_text(html, encoding="utf-8")
    print(f"💾 Dashboard sauvegardé : {dashboard_file}")

    return dashboard_file


def test_health_status(metrics):
    """Test le statut de santé."""
    print("\n🏥 Test du statut de santé...")

    validator = ARIA_MetricsValidator()
    health_status = validator.get_health_status(metrics)

    print(f"✅ Statut de santé : {health_status.get('status', 'unknown').upper()}")
    print(f"📊 Score : {health_status.get('score', 0)}/100")
    print(f"🎨 Couleur : {health_status.get('color', 'unknown')}")
    print(f"🚨 Alertes : {health_status.get('alerts_count', 0)}")
    print(f"💡 Recommandations : {health_status.get('recommendations_count', 0)}")

    return health_status


def main():
    """Fonction principale de test."""
    print("🚀 ARKALIA ARIA - Test du Système de Métriques")
    print("=" * 60)

    try:
        # Test 1 : Collecte des métriques
        metrics = test_metrics_collection()

        # Test 2 : Validation des métriques
        validation_results = test_metrics_validation(metrics)

        # Test 3 : Export des métriques
        export_files = test_metrics_export(metrics)

        # Test 4 : Génération du dashboard
        dashboard_file = test_dashboard_generation(metrics)

        # Test 5 : Statut de santé
        health_status = test_health_status(metrics)

        # Résumé final
        print("\n" + "=" * 60)
        print("🎉 RÉSUMÉ DES TESTS")
        print("=" * 60)
        print("✅ Collecte des métriques : SUCCÈS")
        print("✅ Validation des métriques : SUCCÈS")
        print(f"✅ Export des métriques : SUCCÈS ({len(export_files)} fichiers)")
        print("✅ Génération du dashboard : SUCCÈS")
        print("✅ Statut de santé : SUCCÈS")

        print(f"\n📊 Score global : {validation_results.get('score', 0)}/100")
        print(f"🏥 Statut de santé : {health_status.get('status', 'unknown').upper()}")

        print("\n📁 Fichiers générés :")
        for file_path in export_files:
            print(f"  - {file_path}")
        print(f"  - {dashboard_file}")

        print(f"\n🌐 Pour voir le dashboard, ouvrez : {dashboard_file}")

        return 0

    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
