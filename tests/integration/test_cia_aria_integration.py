#!/usr/bin/env python3
"""
Script de test pour l'intégration optimisée CIA/ARIA
Valide le fonctionnement de la communication bidirectionnelle
"""

import requests

# Configuration
CIA_URL = "http://127.0.0.1:8000"
ARIA_URL = "http://127.0.0.1:8001"


def test_cia_health():
    """Test de santé CIA"""
    print("🔍 Test de santé CIA...")
    try:
        response = requests.get(f"{CIA_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ CIA est opérationnel")
            return True
        else:
            print(f"❌ CIA répond avec le code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CIA non accessible: {e}")
        return False


def test_aria_health():
    """Test de santé ARIA"""
    print("🔍 Test de santé ARIA...")
    try:
        response = requests.get(f"{ARIA_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ ARIA est opérationnel")
            return True
        else:
            print(f"❌ ARIA répond avec le code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ ARIA non accessible: {e}")
        return False


def test_aria_integration_status():
    """Test du statut d'intégration ARIA depuis CIA"""
    print("🔍 Test du statut d'intégration ARIA...")
    try:
        response = requests.get(f"{CIA_URL}/api/aria/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Intégration ARIA: {data['status']}")
            print(f"   - ARIA connecté: {data['aria_connected']}")
            print(f"   - Fonctionnalités: {', '.join(data['features'])}")
            return data["aria_connected"]
        else:
            print(f"❌ Erreur statut intégration: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur test intégration: {e}")
        return False


def test_quick_pain_entry():
    """Test de saisie rapide de douleur"""
    print("🔍 Test de saisie rapide de douleur...")
    try:
        test_data = {"intensity": 7, "trigger": "stress", "action": "respiration"}

        response = requests.post(
            f"{CIA_URL}/api/aria/quick-pain-entry", json=test_data, timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Entrée créée avec ID: {data['id']}")
            print(f"   - Intensité: {data['intensity']}")
            print(f"   - Déclencheur: {data['physical_trigger']}")
            return True
        else:
            print(f"❌ Erreur création entrée: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur test saisie: {e}")
        return False


def test_pain_history():
    """Test de récupération de l'historique"""
    print("🔍 Test de récupération de l'historique...")
    try:
        response = requests.get(
            f"{CIA_URL}/api/aria/pain-entries/recent?limit=5", timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Historique récupéré: {len(data)} entrées")
            if data:
                latest = data[0]
                print(
                    f"   - Dernière entrée: ID {latest['id']}, intensité {latest['intensity']}"
                )
            return True
        else:
            print(f"❌ Erreur historique: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur test historique: {e}")
        return False


def test_cia_sync_status():
    """Test du statut de synchronisation CIA depuis ARIA"""
    print("🔍 Test du statut de synchronisation CIA...")
    try:
        response = requests.get(f"{ARIA_URL}/api/sync/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sync CIA: {data['status']}")
            print(f"   - CIA connecté: {data['cia_connected']}")
            print(f"   - Fonctionnalités: {', '.join(data['features'])}")
            return data["cia_connected"]
        else:
            print(f"❌ Erreur statut sync: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur test sync: {e}")
        return False


def test_export_csv():
    """Test d'export CSV"""
    print("🔍 Test d'export CSV...")
    try:
        response = requests.get(f"{CIA_URL}/api/aria/export/csv", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Export CSV généré: {data['filename']}")
            print(f"   - Entrées: {data['entries_count']}")
            return True
        else:
            print(f"❌ Erreur export: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur test export: {e}")
        return False


def main():
    """Fonction principale de test"""
    print("🚀 Test d'intégration optimisée CIA/ARIA")
    print("=" * 50)

    # Tests de base
    cia_ok = test_cia_health()
    aria_ok = test_aria_health()

    if not cia_ok or not aria_ok:
        print("\n❌ Services de base non disponibles. Arrêt des tests.")
        return

    print("\n" + "=" * 50)

    # Tests d'intégration
    integration_ok = test_aria_integration_status()
    sync_ok = test_cia_sync_status()

    if not integration_ok:
        print("\n❌ Intégration ARIA non fonctionnelle. Arrêt des tests.")
        return

    print("\n" + "=" * 50)

    # Tests fonctionnels
    test_quick_pain_entry()
    test_pain_history()
    test_export_csv()

    print("\n" + "=" * 50)
    print("✅ Tests d'intégration terminés")
    print("📊 Résumé:")
    print(f"   - CIA: {'✅' if cia_ok else '❌'}")
    print(f"   - ARIA: {'✅' if aria_ok else '❌'}")
    print(f"   - Intégration: {'✅' if integration_ok else '❌'}")
    print(f"   - Synchronisation: {'✅' if sync_ok else '❌'}")


if __name__ == "__main__":
    main()
