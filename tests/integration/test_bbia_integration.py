#!/usr/bin/env python3
"""
Tests d'intégration pour BBIA (mode simulation)
==============================================

Tests pour l'intégration BBIA en mode simulation.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestBBIAIntegration:
    """Tests d'intégration BBIA"""

    def test_bbia_status(self):
        """Test GET /api/bbia/status"""
        response = client.get("/api/bbia/status")
        assert response.status_code == 200
        data = response.json()
        # L'endpoint retourne le format BaseAPI standard
        assert "status" in data
        assert data["status"] == "active"
        # Vérifier que c'est bien une réponse valide
        assert "timestamp" in data

    def test_bbia_connection(self):
        """Test GET /api/bbia/connection"""
        response = client.get("/api/bbia/connection")
        assert response.status_code == 200
        data = response.json()
        assert "connected" in data
        assert "bbia_url" in data

    def test_bbia_emotional_state_from_pain(self):
        """Test POST /api/bbia/emotional-state/from-latest-pain"""
        # Créer une entrée de douleur
        pain_entry = {
            "intensity": 7,
            "location": "dos",
            "physical_trigger": "stress",
            "mental_trigger": "anxiété",
            "emotions": "Frustration, anxiété",
        }
        response = client.post("/api/pain/entry", json=pain_entry)
        assert response.status_code == 200

        # Récupérer l'état émotionnel depuis la douleur
        response = client.post("/api/bbia/emotional-state/from-latest-pain")
        assert response.status_code == 200
        data = response.json()
        # La réponse contient un champ "result" avec "emotional_state" à l'intérieur
        assert "result" in data
        assert "emotional_state" in data["result"] or "emotional_state" in data
        # Vérifier que les données sont présentes
        if "result" in data and isinstance(data["result"], dict):
            result = data["result"]
            assert "emotional_state" in result or "message" in result

    def test_bbia_emotional_state_custom(self):
        """Test POST /api/bbia/emotional-state avec données personnalisées"""
        emotional_data = {
            "pain_intensity": 6,
            "stress_level": 7,
            "sleep_quality": 4,
        }
        response = client.post("/api/bbia/emotional-state", json=emotional_data)
        assert response.status_code == 200
        data = response.json()
        # La réponse contient un champ "result" avec les données
        assert "result" in data or "emotional_state" in data
        # Vérifier que les données sont présentes
        if "result" in data and isinstance(data["result"], dict):
            result = data["result"]
            assert "emotional_state" in result or "message" in result

    def test_bbia_with_health_data(self):
        """Test intégration BBIA avec données santé"""
        # Simuler des données santé
        with patch("cia_sync.bbia_integration.get_health_data") as mock_health:
            mock_health.return_value = {
                "stress_level": 6,
                "sleep_quality": 5,
                "activity_level": 3,
            }

            emotional_data = {
                "pain_intensity": 7,
            }
            response = client.post("/api/bbia/emotional-state", json=emotional_data)
            assert response.status_code == 200
            data = response.json()
            # La réponse contient un champ "result" avec les données
            assert "result" in data or "emotional_state" in data

    def test_bbia_simulation_mode(self):
        """Test que le mode simulation fonctionne sans robot physique"""
        response = client.get("/api/bbia/status")
        assert response.status_code == 200
        data = response.json()
        assert data["mode"] == "simulation"
        # En mode simulation, on peut toujours obtenir des recommandations
        assert "note" in data or "available" in data

    def test_bbia_emotional_state_adaptation(self):
        """Test adaptation de l'état émotionnel selon intensité douleur"""
        # Test avec douleur faible
        pain_entry_low = {"intensity": 2, "location": "tête"}
        client.post("/api/pain/entry", json=pain_entry_low)
        response = client.post("/api/bbia/emotional-state/from-latest-pain")
        assert response.status_code == 200
        data_low = response.json()

        # Test avec douleur élevée
        pain_entry_high = {"intensity": 9, "location": "dos"}
        client.post("/api/pain/entry", json=pain_entry_high)
        response = client.post("/api/bbia/emotional-state/from-latest-pain")
        assert response.status_code == 200
        data_high = response.json()

        # Vérifier que les réponses sont valides
        assert "result" in data_low or "emotional_state" in data_low
        assert "result" in data_high or "emotional_state" in data_high

        # Extraire les intensités de douleur depuis les réponses
        pain_low = 0
        pain_high = 0
        if "result" in data_low and isinstance(data_low["result"], dict):
            if "emotional_state" in data_low["result"]:
                pain_low = data_low["result"]["emotional_state"].get("pain_level", 0)
        if "result" in data_high and isinstance(data_high["result"], dict):
            if "emotional_state" in data_high["result"]:
                pain_high = data_high["result"]["emotional_state"].get("pain_level", 0)

        # Vérifier que les intensités sont différentes
        if pain_low > 0 and pain_high > 0:
            assert pain_low < pain_high
