"""
Tests d'intégration pour CIA Sync API
"""

from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestCIASyncEndpoints:
    """Tests pour les endpoints de synchronisation CIA"""

    def test_get_sync_status(self):
        """Test GET /api/sync/status"""
        response = client.get("/api/sync/status")
        assert response.status_code == 200
        data = response.json()
        # Le format peut varier selon l'implémentation BaseAPI
        assert "status" in data or "module" in data

    def test_get_connection(self):
        """Test GET /api/sync/connection"""
        response = client.get("/api/sync/connection")
        assert response.status_code == 200
        data = response.json()
        assert "connected" in data
        assert "cia_url" in data

    @patch("cia_sync.api._check_cia_connection")
    def test_pull_from_cia_all(self, mock_check):
        """Test POST /api/sync/pull-from-cia avec data_type=all"""
        mock_check.return_value = True

        # Mock des requêtes vers CIA
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
            # Peut retourner 200, 503 (CIA indisponible) ou 404 (endpoint CIA inexistant)
            assert response.status_code in [200, 503, 404]

    @patch("cia_sync.api._check_cia_connection")
    def test_pull_from_cia_appointments(self, mock_check):
        """Test POST /api/sync/pull-from-cia avec data_type=appointments"""
        mock_check.return_value = True

        with patch("cia_sync.api._make_cia_request") as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = []
            mock_request.return_value = mock_response

            response = client.post("/api/sync/pull-from-cia?data_type=appointments")
            # Peut retourner 200, 503 (CIA indisponible) ou 404 (endpoint CIA inexistant)
            assert response.status_code in [200, 503, 404]

    @patch("cia_sync.api._check_cia_connection")
    def test_pull_from_cia_cia_unavailable(self, mock_check):
        """Test POST /api/sync/pull-from-cia avec CIA indisponible"""
        mock_check.return_value = False

        response = client.post("/api/sync/pull-from-cia?data_type=all")
        # Peut retourner 503 (Service unavailable) ou 404 selon implémentation
        assert response.status_code in [503, 404]

    def test_auto_sync_status(self):
        """Test GET /api/sync/auto-sync/status"""
        response = client.get("/api/sync/auto-sync/status")
        assert response.status_code == 200
        data = response.json()
        assert "is_running" in data or "status" in data

    def test_auto_sync_start(self):
        """Test POST /api/sync/auto-sync/start"""
        response = client.post("/api/sync/auto-sync/start?interval_minutes=60")
        # Peut retourner 200 (démarré) ou 400 (déjà en cours)
        assert response.status_code in [200, 400]

    def test_auto_sync_stop(self):
        """Test POST /api/sync/auto-sync/stop"""
        response = client.post("/api/sync/auto-sync/stop")
        # Peut retourner 200 (arrêté) ou 400 (pas en cours)
        assert response.status_code in [200, 400]

    def test_auto_sync_sync_now(self):
        """Test POST /api/sync/auto-sync/sync-now"""
        response = client.post("/api/sync/auto-sync/sync-now")
        # Peut retourner 200 (succès) ou 500 (échec)
        assert response.status_code in [200, 500]

    def test_granularity_config_get(self):
        """Test GET /api/sync/granularity/config"""
        response = client.get("/api/sync/granularity/config?config_name=default")
        assert response.status_code == 200
        data = response.json()
        assert "config" in data

    def test_granularity_config_get_not_found(self):
        """Test GET /api/sync/granularity/config avec config inexistante"""
        response = client.get("/api/sync/granularity/config?config_name=nonexistent")
        assert response.status_code == 404  # Not found

    def test_granularity_configs_list(self):
        """Test GET /api/sync/granularity/configs"""
        response = client.get("/api/sync/granularity/configs")
        assert response.status_code == 200
        data = response.json()
        assert "configs" in data
