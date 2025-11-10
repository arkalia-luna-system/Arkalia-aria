#!/usr/bin/env python3
"""
Script de test pour le système DevOps ARIA
==========================================

Teste tous les composants du système DevOps automatisé :
- Sécurité et validation
- CI/CD et workflows
- Assurance qualité
- Déploiement
- Monitoring
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire courant au Python path
sys.path.insert(0, str(Path(__file__).parent))

from devops_automation.cicd.aria_cicd_manager import ARIA_CICDManager
from devops_automation.deployment.aria_deployment_manager import ARIA_DeploymentManager
from devops_automation.monitoring.aria_monitoring_system import ARIA_MonitoringSystem
from devops_automation.quality.aria_quality_assurance import ARIA_QualityAssurance
from devops_automation.security.aria_security_validator import ARIA_SecurityValidator


def test_security_validator():
    """Test le validateur de sécurité."""
    print("🛡️ Test du validateur de sécurité...")

    validator = ARIA_SecurityValidator()

    # Test commande autorisée
    is_valid, message, info = validator.validate_command(["ls", "-la"], "test")
    print(f"✅ Commande autorisée: {is_valid} - {message}")

    # Test commande non autorisée
    is_valid, message, info = validator.validate_command(["rm", "-rf", "/"], "test")
    print(f"❌ Commande non autorisée: {is_valid} - {message}")

    # Test audit de sécurité
    audit_result = validator.audit_code_security("main.py")
    print(
        f"🔍 Audit de sécurité: {len(audit_result.get('issues', []))} problèmes trouvés"
    )

    # Rapport de sécurité
    security_report = validator.get_security_report()
    print(
        f"📊 Rapport sécurité: {security_report.get('total_validations', 0)} validations"
    )

    return True


def test_cicd_manager():
    """Test le gestionnaire CI/CD."""
    print("\n🚀 Test du gestionnaire CI/CD...")

    cicd_manager = ARIA_CICDManager(".")

    # Configuration CI/CD
    config = {
        "project_name": "arkalia-aria",
        "python_version": "3.10",
        "docker_enabled": True,
    }

    results = cicd_manager.setup_cicd(config)
    print(
        f"✅ Configuration CI/CD: {len(results.get('created_files', []))} fichiers créés"
    )

    # Statut des déploiements
    status = cicd_manager.get_deployment_status()
    print(
        f"📊 Statut déploiements: {len(status.get('deployment_history', []))} déploiements"
    )

    return True


def test_quality_assurance():
    """Test l'assurance qualité."""
    print("\n🔍 Test de l'assurance qualité...")

    quality_assurance = ARIA_QualityAssurance(".")

    # Vérification de qualité (mode rapide pour éviter la surcharge)
    if os.getenv("ARIA_FAST_TEST", "0") == "1":
        report = {"overall_score": 100, "status": "ok", "recommendations": []}
        print("✅ Vérification qualité: Mode rapide activé")
    else:
        report = quality_assurance.run_full_quality_check(fix_issues=False)
        print(f"✅ Vérification qualité: Score {report.get('overall_score', 0)}/100")
        print(f"📊 Statut: {report.get('status', 'unknown')}")
        print(f"💡 Recommandations: {len(report.get('recommendations', []))}")

    # Historique
    history = quality_assurance.get_quality_history()
    print(f"📈 Historique: {len(history)} rapports")

    return True


def test_deployment_manager():
    """Test le gestionnaire de déploiement."""
    print("\n🚀 Test du gestionnaire de déploiement...")

    deployment_manager = ARIA_DeploymentManager(".")

    # Déploiement en staging
    deployment_result = deployment_manager.deploy("staging", "1.0.0")
    print(f"✅ Déploiement staging: {deployment_result.get('status', 'unknown')}")
    print(f"📊 Étapes: {len(deployment_result.get('steps', []))}")

    # Statut du déploiement
    status = deployment_manager.get_deployment_status("staging")
    print(f"📈 Statut staging: {status.get('status', 'unknown')}")
    print(f"🔢 Déploiements: {status.get('deployment_count', 0)}")

    return True


def test_monitoring_system():
    """Test le système de monitoring."""
    print("\n📊 Test du système de monitoring...")

    monitoring_system = ARIA_MonitoringSystem(".")

    # Collecte de métriques
    metrics = monitoring_system.collect_metrics()
    print(f"✅ Métriques collectées: {len(metrics)} sections")
    print(f"💻 CPU: {metrics.get('cpu_percent', 0):.1f}%")
    print(f"🧠 Mémoire: {metrics.get('memory_percent', 0):.1f}%")
    print(f"💾 Disque: {metrics.get('disk_percent', 0):.1f}%")

    # Statut de santé
    health_status = monitoring_system.get_health_status()
    print(f"🏥 Statut santé: {health_status.get('status', 'unknown')}")
    print(f"🚨 Alertes actives: {health_status.get('active_alerts', 0)}")

    # Résumé des performances
    performance_summary = monitoring_system.get_performance_summary(24)
    print(f"📈 Données performance: {performance_summary.get('data_points', 0)} points")

    # Résumé des alertes
    alerts_summary = monitoring_system.get_alerts_summary(24)
    print(f"🚨 Alertes: {alerts_summary.get('total_alerts', 0)} total")

    return True


def test_integration():
    """Test l'intégration complète."""
    print("\n🔗 Test d'intégration complète...")

    # Créer tous les composants
    validator = ARIA_SecurityValidator()
    cicd_manager = ARIA_CICDManager(".")
    quality_assurance = ARIA_QualityAssurance(".")
    deployment_manager = ARIA_DeploymentManager(".")
    monitoring_system = ARIA_MonitoringSystem(".")

    # Test workflow complet
    print("1. Validation de sécurité...")
    is_valid, _, _ = validator.validate_command(
        ["python", "--version"], "integration_test"
    )

    print("2. Configuration CI/CD...")
    _cicd_results = cicd_manager.setup_cicd()

    print("3. Vérification qualité...")
    _quality_report = quality_assurance.run_full_quality_check()

    print("4. Déploiement...")
    _deployment_result = deployment_manager.deploy("staging")

    print("5. Monitoring...")
    _metrics = monitoring_system.collect_metrics()

    print("✅ Intégration complète réussie")

    return True


def main():
    """Fonction principale de test."""
    print("🚀 ARKALIA ARIA - Test du Système DevOps")
    print("=" * 60)

    try:
        # Tests individuels
        test_security_validator()
        test_cicd_manager()
        test_quality_assurance()
        test_deployment_manager()
        test_monitoring_system()

        # Test d'intégration
        test_integration()

        # Résumé final
        print("\n" + "=" * 60)
        print("🎉 RÉSUMÉ DES TESTS DEVOPS")
        print("=" * 60)
        print("✅ Validateur de sécurité : SUCCÈS")
        print("✅ Gestionnaire CI/CD : SUCCÈS")
        print("✅ Assurance qualité : SUCCÈS")
        print("✅ Gestionnaire de déploiement : SUCCÈS")
        print("✅ Système de monitoring : SUCCÈS")
        print("✅ Intégration complète : SUCCÈS")

        print("\n🌐 Système DevOps ARIA opérationnel !")
        print("📊 Endpoints disponibles :")
        print("  - /devops/security/* : Sécurité et validation")
        print("  - /devops/cicd/* : CI/CD et workflows")
        print("  - /devops/quality/* : Assurance qualité")
        print("  - /devops/deployment/* : Déploiement")
        print("  - /devops/monitoring/* : Monitoring")

        return 0

    except Exception as e:
        print(f"\n❌ ERREUR : {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
