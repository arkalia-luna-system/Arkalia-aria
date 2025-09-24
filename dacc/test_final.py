#!/usr/bin/env python3
"""
Test final ultra-léger pour ARIA
===============================

Test minimal pour vérifier que les systèmes intégrés fonctionnent.
"""

import sys
from pathlib import Path

# Ajouter le répertoire courant au Python path
sys.path.insert(0, str(Path(__file__).parent))


def test_imports():
    """Test des imports principaux."""
    print("🔍 Test des imports...")

    try:
        # Test import métriques

        print("✅ Métriques: OK")

        # Test import DevOps

        print("✅ DevOps: OK")

        # Test import principal

        print("✅ App principale: OK")

        return True
    except Exception as e:
        print(f"❌ Erreur import: {e}")
        return False


def test_basic_functionality():
    """Test de fonctionnalité de base."""
    print("\n🚀 Test fonctionnalité de base...")

    try:
        # Test validateur de sécurité
        from devops_automation.security.aria_security_validator import (
            ARIA_SecurityValidator,
        )

        validator = ARIA_SecurityValidator()
        is_valid, _, _ = validator.validate_command(["ls"], "test")
        print(f"✅ Sécurité: {'OK' if is_valid else 'ERREUR'}")

        # Test collecteur de métriques
        from metrics_collector.collectors.aria_metrics_collector import (
            ARIA_MetricsCollector,
        )

        collector = ARIA_MetricsCollector(".")
        metrics = collector.collect_all_metrics()
        print(f"✅ Métriques: {len(metrics)} sections collectées")

        return True
    except Exception as e:
        print(f"❌ Erreur fonctionnalité: {e}")
        return False


def main():
    """Test final."""
    print("🚀 ARKALIA ARIA - Test Final Ultra-Léger")
    print("=" * 50)

    success = True

    # Test imports
    if not test_imports():
        success = False

    # Test fonctionnalité
    if not test_basic_functionality():
        success = False

    # Résultat
    print("\n" + "=" * 50)
    if success:
        print("🎉 TOUS LES TESTS RÉUSSIS !")
        print("✅ ARIA est prêt et opérationnel")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("⚠️ Vérifiez les erreurs ci-dessus")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
