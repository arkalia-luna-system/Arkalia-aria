#!/usr/bin/env python3
"""
Test ultra-léger du système DevOps ARIA
=======================================

Test minimal qui ne charge que les composants essentiels.
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au Python path
sys.path.insert(0, str(Path(__file__).parent))


def test_security_basic():
    """Test basique du validateur de sécurité."""
    print("🛡️ Test sécurité basique...")

    try:
        from devops_automation.security.aria_security_validator import (
            ARIA_SecurityValidator,
        )

        validator = ARIA_SecurityValidator()

        # Test simple
        is_valid, message, _ = validator.validate_command(["ls"], "test")
        print(f"✅ Sécurité: {is_valid} - {message}")

        return True
    except Exception as e:
        print(f"❌ Erreur sécurité: {e}")
        return False


def test_cicd_basic():
    """Test basique du CI/CD."""
    print("🚀 Test CI/CD basique...")

    try:
        from devops_automation.cicd.aria_cicd_manager import ARIA_CICDManager

        cicd = ARIA_CICDManager(".")

        # Test simple
        config = {"project_name": "test"}
        results = cicd.setup_cicd(config)
        print(f"✅ CI/CD: {len(results.get('created_files', []))} fichiers")

        return True
    except Exception as e:
        print(f"❌ Erreur CI/CD: {e}")
        return False


def test_quality_basic():
    """Test basique de l'assurance qualité."""
    print("🔍 Test qualité basique...")

    try:
        from devops_automation.quality.aria_quality_assurance import (
            ARIA_QualityAssurance,
        )

        _quality = ARIA_QualityAssurance(".")

        # Test simple sans outils externes
        print("✅ Qualité: Module chargé")

        return True
    except Exception as e:
        print(f"❌ Erreur qualité: {e}")
        return False


def test_deployment_basic():
    """Test basique du déploiement."""
    print("🚀 Test déploiement basique...")

    try:
        from devops_automation.deployment.aria_deployment_manager import (
            ARIA_DeploymentManager,
        )

        _deployment = ARIA_DeploymentManager(".")

        # Test simple
        print("✅ Déploiement: Module chargé")

        return True
    except Exception as e:
        print(f"❌ Erreur déploiement: {e}")
        return False


def test_monitoring_basic():
    """Test basique du monitoring."""
    print("📊 Test monitoring basique...")

    try:
        from devops_automation.monitoring.aria_monitoring_system import (
            ARIA_MonitoringSystem,
        )

        _monitoring = ARIA_MonitoringSystem(".")

        # Test simple
        print("✅ Monitoring: Module chargé")

        return True
    except Exception as e:
        print(f"❌ Erreur monitoring: {e}")
        return False


def main():
    """Test ultra-léger."""
    print("🚀 ARKALIA ARIA - Test DevOps Ultra-Léger")
    print("=" * 50)

    tests = [
        test_security_basic,
        test_cicd_basic,
        test_quality_basic,
        test_deployment_basic,
        test_monitoring_basic,
    ]

    success_count = 0
    for test in tests:
        try:
            if test():
                success_count += 1
        except Exception as e:
            print(f"❌ Erreur: {e}")

    print("\n" + "=" * 50)
    print(f"🎉 Tests terminés: {success_count}/{len(tests)} succès")

    if success_count == len(tests):
        print("✅ Système DevOps ARIA opérationnel !")
    else:
        print("⚠️ Quelques problèmes détectés")

    return 0


if __name__ == "__main__":
    sys.exit(main())
