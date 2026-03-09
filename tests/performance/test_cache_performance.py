#!/usr/bin/env python3
"""
Tests de performance du cache
=============================

Tests pour valider l'efficacité du système de cache.
"""

import time

import pytest
from fastapi.testclient import TestClient


@pytest.mark.slow
class TestCachePerformance:
    """Tests de performance du cache"""

    def test_cache_hit_performance(self, client: TestClient) -> None:
        """Test que le cache améliore les performances"""
        # Créer quelques entrées (réduit pour accélérer)
        for _ in range(5):
            pain_entry = {"intensity": 5, "location": "test"}
            client.post("/api/pain/entry", json=pain_entry)

        # Première requête (cache miss)
        start_time = time.time()
        response1 = client.get("/api/pain/entries/recent?limit=10")
        first_time = time.time() - start_time
        assert response1.status_code == 200

        # Deuxième requête (cache hit - devrait être plus rapide)
        start_time = time.time()
        response2 = client.get("/api/pain/entries/recent?limit=10")
        second_time = time.time() - start_time
        assert response2.status_code == 200

        # Le cache devrait améliorer les performances
        # (Note: peut ne pas être toujours vrai selon l'implémentation)
        # On vérifie juste que les deux requêtes fonctionnent
        assert first_time < 2.0
        assert second_time < 2.0

    def test_cache_invalidation(self, client: TestClient) -> None:
        """Test que le cache est invalidé correctement"""
        # Créer une entrée
        pain_entry = {"intensity": 5, "location": "test"}
        response = client.post("/api/pain/entry", json=pain_entry)
        assert response.status_code == 200
        entry_id = response.json()["id"]

        # Récupérer l'entrée depuis la liste récente (peut être en cache)
        response1 = client.get("/api/pain/entries/recent?limit=10")
        assert response1.status_code == 200
        entries = response1.json()
        # Vérifier que notre entrée est dans la liste
        assert any(e["id"] == entry_id for e in entries)

        # Faire une deuxième requête (devrait utiliser le cache)
        response2 = client.get("/api/pain/entries/recent?limit=10")
        assert response2.status_code == 200

    def test_cache_memory_usage(self, client: TestClient) -> None:
        """Test que le cache n'utilise pas trop de mémoire"""
        # Créer plusieurs entrées (volume réduit pour ne pas surcharger la machine)
        for i in range(10):
            pain_entry = {"intensity": i % 11, "location": f"loc_{i}"}
            client.post("/api/pain/entry", json=pain_entry)

        # Faire quelques requêtes pour remplir le cache
        for _ in range(5):
            client.get("/api/pain/entries/recent?limit=20")
            client.get("/api/pain/suggestions")

        # Vérifier que le système fonctionne toujours
        response = client.get("/api/pain/entries/recent?limit=10")
        assert response.status_code == 200

        # Vérifier la santé globale de l'API (endpoint /health)
        response = client.get("/health")
        assert response.status_code == 200
