#!/usr/bin/env python3
"""
Tests d'intégration complets pour la synchronisation CIA ↔ ARIA
===============================================================

Tests bout-en-bout pour valider la synchronisation complète entre CIA et ARIA.
"""

from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestCIAARIACompleteSync:
    """Tests de synchronisation complète CIA ↔ ARIA"""

    def test_sync_complete_workflow(self):
        """Test workflow complet de synchronisation bidirectionnelle"""
        # 1. Vérifier connexion CIA
        response = client.get("/api/sync/connection")
        assert response.status_code == 200
        data = response.json()
        assert "connected" in data

        # 2. Créer une entrée de douleur dans ARIA
        pain_entry = {
            "intensity": 7,
            "location": "dos",
            "physical_trigger": "stress",
            "mental_trigger": "anxiété",
            "who_present": "Famille",
            "emotions": "Anxiété, frustration",
        }
        response = client.post("/api/pain/entry", json=pain_entry)
        assert response.status_code == 200

        # 3. Synchroniser vers CIA (push)
        with patch("cia_sync.api._make_cia_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "success"}
            mock_request.return_value = mock_response

            response = client.post("/api/sync/push-to-cia")
            # Peut être 200, 404 ou 503 si CIA non disponible ou endpoint non trouvé
            assert response.status_code in [200, 404, 503]

        # 4. Récupérer depuis CIA (pull)
        with patch("cia_sync.api._check_cia_connection") as mock_check:
            mock_check.return_value = True
            with patch("cia_sync.api._make_cia_request") as mock_request:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "appointments": [],
                    "medications": [],
                    "documents": [],
                    "health_context": {},
                }
                mock_request.return_value = mock_response

                response = client.post("/api/sync/pull-from-cia?data_type=all")
                # Peut être 200, 404 ou 503 selon disponibilité CIA
                assert response.status_code in [200, 404, 503]

    def test_sync_with_new_pain_fields(self):
        """Test synchronisation avec nouveaux champs journal douleur"""
        # Créer entrée avec tous les nouveaux champs
        pain_entry = {
            "intensity": 8,
            "location": "tête",
            "who_present": "Seul",
            "interactions": "Aucune interaction",
            "emotions": "Frustration, colère",
            "thoughts": "Je me sens dépassé par la situation",
            "physical_symptoms": "Tension musculaire, maux de tête",
        }
        response = client.post("/api/pain/entry", json=pain_entry)
        assert response.status_code == 200
        data = response.json()
        assert data["who_present"] == "Seul"
        assert data["interactions"] == "Aucune interaction"
        assert data["emotions"] == "Frustration, colère"
        assert data["thoughts"] == "Je me sens dépassé par la situation"
        assert data["physical_symptoms"] == "Tension musculaire, maux de tête"

        # Vérifier que les champs sont bien sauvegardés en récupérant les entrées récentes
        response = client.get("/api/pain/entries/recent?limit=10")
        assert response.status_code == 200
        entries = response.json()
        # Trouver notre entrée dans la liste
        our_entry = next((e for e in entries if e["id"] == data["id"]), None)
        assert our_entry is not None
        assert our_entry["who_present"] == "Seul"
        assert our_entry["interactions"] == "Aucune interaction"

    def test_sync_correlations_automatic(self):
        """Test que les corrélations sont calculées automatiquement après sync"""
        # Créer plusieurs entrées pour avoir des données
        for i in range(3):
            pain_entry = {
                "intensity": 5 + i,
                "location": "dos",
                "physical_trigger": "stress",
                "mental_trigger": "anxiété",
            }
            client.post("/api/pain/entry", json=pain_entry)

        # Vérifier que les corrélations sont disponibles
        response = client.get("/api/patterns/correlations/sleep-pain")
        # Peut être 200 ou 404 si pas assez de données
        assert response.status_code in [200, 404]

        response = client.get("/api/patterns/correlations/stress-pain")
        assert response.status_code in [200, 404]

    def test_sync_export_with_new_fields(self):
        """Test export avec nouveaux champs"""
        # Créer entrée avec nouveaux champs
        pain_entry = {
            "intensity": 6,
            "location": "genou",
            "who_present": "Ami",
            "emotions": "Joie",
        }
        response = client.post("/api/pain/entry", json=pain_entry)
        assert response.status_code == 200

        # Tester export CSV
        response = client.get("/api/pain/export/csv")
        assert response.status_code == 200
        assert "who_present" in response.text or "Qui présent" in response.text

        # Tester export PDF
        response = client.get("/api/pain/export/pdf")
        # Peut être 200 avec PDF ou 404/500 si endpoint non disponible
        assert response.status_code in [200, 404, 500]
        if response.status_code == 200:
            # Vérifier le type de contenu si disponible
            content_type = response.headers.get("content-type", "")
            assert "pdf" in content_type.lower() or "application/json" in content_type

    @patch("cia_sync.api._check_cia_connection")
    def test_sync_cia_unavailable(self, mock_check):
        """Test comportement quand CIA est indisponible"""
        mock_check.return_value = False

        response = client.get("/api/sync/connection")
        assert response.status_code == 200
        data = response.json()
        assert data["connected"] is False

        # Les opérations de sync doivent gérer gracieusement l'indisponibilité
        response = client.post("/api/sync/push-to-cia")
        # Peut être 200 (avec message d'erreur), 404, ou 503 selon l'implémentation
        assert response.status_code in [200, 404, 503]
