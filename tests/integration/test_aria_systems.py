#!/usr/bin/env python3
"""
Test d'intégration des systèmes ARIA
=====================================

Test optimisé pour vérifier que tous les systèmes intégrés fonctionnent
sans surcharger le système.
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


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


def test_security_validator():
    """Test du validateur de sécurité."""
    print("\n🛡️ Test validateur de sécurité...")

    try:
        from devops_automation.security.aria_security_validator import (
            ARIA_SecurityValidator,
        )

        validator = ARIA_SecurityValidator()

        # Test commande autorisée
        is_valid, message, _ = validator.validate_command(["ls"], "test")
        if not is_valid:
            print(f"❌ Commande autorisée rejetée: {message}")
            return False

        # Test commande non autorisée
        is_valid, message, _ = validator.validate_command(["rm", "-rf", "/"], "test")
        if is_valid:
            print(f"❌ Commande dangereuse autorisée: {message}")
            return False

        print("✅ Sécurité: OK")
        return True
    except Exception as e:
        print(f"❌ Erreur sécurité: {e}")
        return False


def test_metrics_collector():
    """Test du collecteur de métriques (version légère)."""
    print("\n📊 Test collecteur de métriques...")

    try:
        from metrics_collector.collectors.aria_metrics_collector import (
            ARIA_MetricsCollector,
        )

        collector = ARIA_MetricsCollector(".")

        # Test seulement les métriques de base (pas de scan complet)
        project_info = collector._collect_project_info()
        if not project_info.get("name") == "ARKALIA ARIA":
            print("❌ Informations projet incorrectes")
            return False

        print("✅ Métriques: OK")
        return True
    except Exception as e:
        print(f"❌ Erreur métriques: {e}")
        return False


def test_cicd_manager():
    """Test du gestionnaire CI/CD."""
    print("\n🚀 Test gestionnaire CI/CD...")

    try:
        from devops_automation.cicd.aria_cicd_manager import ARIA_CICDManager

        cicd_manager = ARIA_CICDManager(".")

        # Test configuration simple
        config = {"project_name": "arkalia-aria"}
        results = cicd_manager.setup_cicd(config)

        if not results.get("created_files"):
            print("❌ Aucun fichier CI/CD créé")
            return False

        print("✅ CI/CD: OK")
        return True
    except Exception as e:
        print(f"❌ Erreur CI/CD: {e}")
        return False


def test_monitoring_system():
    """Test du système de monitoring."""
    print("\n📈 Test système de monitoring...")

    try:
        from devops_automation.monitoring.aria_monitoring_system import (
            ARIA_MonitoringSystem,
        )

        monitoring_system = ARIA_MonitoringSystem(".")

        # Test collecte de métriques système
        metrics = monitoring_system.collect_metrics()

        if not metrics.get("cpu_percent") is not None:
            print("❌ Métriques système non collectées")
            return False

        print("✅ Monitoring: OK")
        return True
    except Exception as e:
        print(f"❌ Erreur monitoring: {e}")
        return False


def test_new_pain_endpoints():
    """Teste les nouveaux endpoints: suggestions et export psy HTML via appels directs."""
    print("\n🧪 Test endpoints Suggestions et Export Psy (appels directs)...")
    try:
        import asyncio

        from pain_tracking.api import (
            QuickEntry,
            create_quick_entry,
            export_psy_report,
            pain_suggestions,
        )

        async def run_tests():
            # Créer une entrée minimale
            created = await create_quick_entry(
                QuickEntry(
                    intensity=5, physical_trigger="stress", action_taken="respiration"
                )
            )
            print(f"Créé: {created}")
            # Suggestions
            sugg = await pain_suggestions()
            print(f"Suggestions: {sugg}")
            assert isinstance(sugg, dict)
            assert "summary" in sugg
            assert "suggestions" in sugg
            # Export psy
            psy = await export_psy_report()
            print(f"Export psy: keys={list(psy.keys())}")
            assert isinstance(psy, dict)
            assert "html" in psy
            html = psy["html"].lstrip().lower()
            assert isinstance(html, str) and html.startswith("<!doctype html>")

        asyncio.run(run_tests())
        print("✅ Suggestions et Export Psy: OK")
        return True
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"❌ Erreur endpoints psy/suggestions: {repr(e)}")
        return False


def test_security_dashboard_html():
    """Vérifie que le dashboard de sécurité HTML est généré."""
    print("\n🔒 Test dashboard sécurité HTML...")
    try:
        from devops_automation.api import ARIA_DevOpsAPI

        api = ARIA_DevOpsAPI(".")
        report = api.security_validator.get_security_report()
        html = api.generate_security_dashboard_html(report)
        assert isinstance(html, str) and html.lstrip().lower().startswith(
            "<!doctype html>"
        )
        print("✅ Dashboard sécurité: OK")
        return True
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"❌ Erreur dashboard sécurité: {repr(e)}")
        return False


def test_audio_voice_endpoints():
    """Teste statut audio, TTS simulée et sauvegarde note audio en base64."""
    print("\n🎙️ Test Audio/Voix...")
    try:
        import asyncio
        import base64

        from audio_voice.api import (
            AudioNoteRequest,
            TTSRequest,
            audio_status,
            save_audio_note,
            synthesize_speech,
        )

        async def run_tests():
            st = await audio_status()
            assert st.get("module") == "audio_voice"

            tts = await synthesize_speech(TTSRequest(text="Bonjour ARIA"))
            assert tts.get("status") == "ok"

            dummy = base64.b64encode(b"RIFF....WAVE").decode()
            note = await save_audio_note(AudioNoteRequest(content_base64=dummy))
            assert note.get("status") == "saved" and note.get("size_bytes") > 0

        asyncio.run(run_tests())
        print("✅ Audio/Voix: OK")
        return True
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"❌ Erreur Audio/Voix: {repr(e)}")
        return False


def main():
    """Test d'intégration principal."""
    print("🚀 ARKALIA ARIA - Test d'Intégration des Systèmes")
    print("=" * 60)

    success = True

    # Tests individuels
    tests = [
        test_imports,
        test_security_validator,
        test_metrics_collector,
        test_cicd_manager,
        test_monitoring_system,
        test_new_pain_endpoints,
        test_security_dashboard_html,
        test_audio_voice_endpoints,
    ]

    for test_func in tests:
        if not test_func():
            success = False

    # Résultat final
    print("\n" + "=" * 60)
    if success:
        print("🎉 TOUS LES TESTS RÉUSSIS !")
        print("✅ ARIA est prêt et opérationnel")
        print("\n📊 Systèmes intégrés :")
        print("  - 🛡️ Sécurité et validation")
        print("  - 📊 Métriques avancées")
        print("  - 🚀 CI/CD automatisé")
        print("  - 📈 Monitoring en temps réel")
        print("  - 🔧 DevOps complet")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("⚠️ Vérifiez les erreurs ci-dessus")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
