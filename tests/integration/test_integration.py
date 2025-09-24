#!/usr/bin/env python3
"""
Test d'intégration ARIA - Validation de l'architecture
"""

import importlib
from typing import Any

requests: Any = importlib.import_module("requests")


def test_aria_endpoints():
    """Test des endpoints ARIA"""
    base_url = "http://127.0.0.1:8001"

    print("🧪 Test des endpoints ARIA...")

    # Test 1: Status général
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")

    # Test 2: Status pain tracking
    try:
        response = requests.get(f"{base_url}/api/pain/status")
        print(f"✅ Pain tracking status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Pain tracking status failed: {e}")

    # Test 3: Saisie rapide
    try:
        data = {"intensity": 6, "trigger": "stress", "action": "respiration"}
        response = requests.post(f"{base_url}/api/pain/quick-entry", json=data)
        print(f"✅ Quick entry: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Quick entry failed: {e}")

    # Test 4: Historique
    try:
        response = requests.get(f"{base_url}/api/pain/entries/recent")
        print(f"✅ Recent entries: {response.status_code}")
        entries = response.json()
        print(f"   Found {len(entries)} entries")
        if entries:
            print(f"   Latest: {entries[0]}")
    except Exception as e:
        print(f"❌ Recent entries failed: {e}")

    # Test 5: Export CSV
    try:
        response = requests.get(f"{base_url}/api/pain/export/csv")
        print(f"✅ CSV export: {response.status_code}")
        export_data = response.json()
        print(f"   Filename: {export_data['filename']}")
        print(f"   Entries: {export_data['entries_count']}")
    except Exception as e:
        print(f"❌ CSV export failed: {e}")


def test_other_modules():
    """Test des autres modules ARIA"""
    base_url = "http://127.0.0.1:8001"

    print("\n🧪 Test des autres modules...")

    modules = [
        ("pattern_analysis", "/api/patterns/status"),
        ("prediction_engine", "/api/predictions/status"),
        ("research_tools", "/api/research/status"),
        ("cia_sync", "/api/sync/status"),
    ]

    for module_name, endpoint in modules:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"✅ {module_name}: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"❌ {module_name} failed: {e}")


if __name__ == "__main__":
    print("🚀 Test d'intégration ARIA")
    print("=" * 50)

    test_aria_endpoints()
    test_other_modules()

    print("\n✨ Test terminé !")
    print("\n📋 Résumé de l'architecture:")
    print("   • ARIA: Projet autonome sur port 8001")
    print(
        "   • Modules: pain_tracking, pattern_analysis, prediction_engine, research_tools, cia_sync"
    )
    print("   • CIA Integration: Pont simple via /api/aria/")
    print("   • Base de données: SQLite locale chiffrée")
    print("   • Export: CSV pour professionnels de santé")
