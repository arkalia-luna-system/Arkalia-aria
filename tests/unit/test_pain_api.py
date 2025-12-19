"""
Tests unitaires pour les endpoints Pain Tracking API
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestPainEntryEndpoints:
    """Tests pour les endpoints de création d'entrées de douleur"""

    def test_post_pain_entry_success(self):
        """Test POST /api/pain/entry avec données valides"""
        entry_data = {
            "intensity": 5,
            "physical_trigger": "stress",
            "mental_trigger": "anxiété",
            "location": "tête",
            "action_taken": "respiration",
            "effectiveness": 7,
        }
        response = client.post("/api/pain/entry", json=entry_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["intensity"] == 5
        assert data["physical_trigger"] == "stress"

    def test_post_pain_entry_invalid_intensity_high(self):
        """Test POST /api/pain/entry avec intensité > 10"""
        entry_data = {
            "intensity": 15,  # Invalide (> 10)
            "physical_trigger": "stress",
        }
        response = client.post("/api/pain/entry", json=entry_data)
        assert response.status_code == 422  # Validation error

    def test_post_pain_entry_invalid_intensity_negative(self):
        """Test POST /api/pain/entry avec intensité < 0"""
        entry_data = {
            "intensity": -1,  # Invalide (< 0)
            "physical_trigger": "stress",
        }
        response = client.post("/api/pain/entry", json=entry_data)
        assert response.status_code == 422  # Validation error

    def test_post_pain_entry_missing_required(self):
        """Test POST /api/pain/entry sans champ requis (intensity)"""
        entry_data = {
            "physical_trigger": "stress",
        }
        response = client.post("/api/pain/entry", json=entry_data)
        assert response.status_code == 422  # Validation error

    def test_post_quick_entry_success(self):
        """Test POST /api/pain/quick-entry avec données valides"""
        entry_data = {
            "intensity": 6,
            "physical_trigger": "stress",
            "action_taken": "respiration",
        }
        response = client.post("/api/pain/quick-entry", json=entry_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["intensity"] == 6

    def test_post_quick_entry_invalid(self):
        """Test POST /api/pain/quick-entry avec données invalides"""
        entry_data = {
            "intensity": 11,  # Invalide
            "physical_trigger": "stress",
            "action_taken": "respiration",
        }
        response = client.post("/api/pain/quick-entry", json=entry_data)
        assert response.status_code == 422  # Validation error

    def test_get_entries_empty(self):
        """Test GET /api/pain/entries avec base vide"""
        # Supprimer toutes les entrées pour test
        client.delete("/api/pain/entries")
        response = client.get("/api/pain/entries?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "entries" in data
        assert "total" in data
        assert data["total"] >= 0

    def test_get_entries_pagination(self):
        """Test GET /api/pain/entries avec pagination"""
        # Créer quelques entrées
        for _ in range(5):
            client.post(
                "/api/pain/quick-entry",
                json={
                    "intensity": 5,
                    "physical_trigger": "test",
                    "action_taken": "test",
                },
            )

        response = client.get("/api/pain/entries?limit=2&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert len(data["entries"]) <= 2
        assert "has_more" in data

    def test_get_entries_invalid_limit(self):
        """Test GET /api/pain/entries avec limit invalide"""
        response = client.get("/api/pain/entries?limit=300")  # > 200 max
        assert response.status_code == 422  # Validation error (Pydantic valide le max)

    def test_delete_entry_not_found(self):
        """Test DELETE /api/pain/entries/{id} avec ID inexistant"""
        response = client.delete("/api/pain/entries/99999")
        assert response.status_code == 404  # Not found

    def test_delete_entry_success(self):
        """Test DELETE /api/pain/entries/{id} avec ID valide"""
        # Créer une entrée
        create_response = client.post(
            "/api/pain/quick-entry",
            json={"intensity": 5, "physical_trigger": "test", "action_taken": "test"},
        )
        entry_id = create_response.json()["id"]

        # Supprimer l'entrée
        delete_response = client.delete(f"/api/pain/entries/{entry_id}")
        assert delete_response.status_code == 200
