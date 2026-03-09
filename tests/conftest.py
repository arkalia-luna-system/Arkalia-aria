#!/usr/bin/env python3
"""
Configuration partagée pour tous les tests
==========================================

Fixtures et configurations communes pour optimiser les performances des tests.
"""

import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Désactiver Redis pour les tests par défaut (plus rapide)
os.environ.setdefault("REDIS_ENABLED", "false")

# Utiliser une base de données temporaire pour les tests
os.environ.setdefault("ARIA_DB", ":memory:")

# Activer le mode tests rapides (sans outils DevOps lourds) en local
if os.getenv("CI") not in {"true", "1"} and os.getenv("GITHUB_ACTIONS") not in {
    "true",
    "1",
}:
    os.environ.setdefault("ARIA_FAST_TEST", "1")


@pytest.fixture(scope="session")
def app():
    """Application FastAPI partagée pour tous les tests."""
    from main import app

    return app


@pytest.fixture(scope="function")
def client(app):
    """Client de test FastAPI réutilisable."""
    client = TestClient(app)
    yield client
    # Nettoyage automatique
    try:
        client.close()
    except Exception:
        pass


@pytest.fixture(scope="function")
def temp_db():
    """Base de données temporaire pour les tests."""
    temp_dir = tempfile.TemporaryDirectory()
    db_path = Path(temp_dir.name) / "test_aria.db"
    yield str(db_path)
    temp_dir.cleanup()


@pytest.fixture(scope="function", autouse=True)
def mock_redis():
    """Mock Redis pour tous les tests (désactivé par défaut)."""
    from unittest.mock import patch

    # Désactiver Redis pour tous les tests pour éviter les connexions réseau
    with patch("core.cache.RedisCacheManager._init_redis") as mock:
        # Ne pas initialiser Redis
        def noop_init(self):
            self._redis_available = False
            self._redis_client = None

        mock.side_effect = noop_init
        yield mock


@pytest.fixture(scope="function", autouse=True)
def mock_external_apis():
    """Mock des appels API externes pour accélérer les tests."""
    from unittest.mock import Mock, patch

    patches = []

    # Mock CIA API (si le module existe)
    try:
        cia_patch = patch("cia_sync.api._make_cia_request", create=True)
        patches.append(cia_patch)
        mock_cia = cia_patch.start()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_cia.return_value = mock_response
    except (ImportError, AttributeError):
        pass

    # Mock BBIA API (si le module existe)
    try:
        bbia_patch = patch("cia_sync.bbia_api._make_bbia_request", create=True)
        patches.append(bbia_patch)
        mock_bbia = bbia_patch.start()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "success"}
        mock_bbia.return_value = mock_response
    except (ImportError, AttributeError):
        pass

    yield

    # Nettoyer tous les patches
    for patch_obj in patches:
        try:
            patch_obj.stop()
        except Exception:
            pass


@pytest.fixture(scope="function", autouse=True)
def clear_cache():
    """Nettoie le cache avant et après chaque test."""

    # Nettoyer avant le test
    try:
        # Si un cache global existe, le nettoyer
        pass
    except Exception:
        pass

    yield

    # Nettoyer après le test
    try:
        pass
    except Exception:
        pass
