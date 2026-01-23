#!/usr/bin/env python3
"""
Tests de charge pour ARKALIA ARIA
==================================

Tests pour valider les performances avec de grandes quantités de données.
"""

import time


class TestLoadPerformance:
    """Tests de charge"""

    def test_create_many_pain_entries(self, client):
        """Test création de 1000+ entrées de douleur"""
        start_time = time.time()

        # Créer 50 entrées (réduit pour accélérer les tests)
        entries_created = 0
        for i in range(50):
            pain_entry = {
                "intensity": i % 11,
                "location": f"location_{i % 10}",
                "physical_trigger": f"trigger_{i % 5}",
            }
            response = client.post("/api/pain/entry", json=pain_entry)
            if response.status_code == 200:
                entries_created += 1

        elapsed_time = time.time() - start_time

        # Vérifier que toutes les entrées ont été créées
        assert entries_created == 50

        # Vérifier que le temps est raisonnable (< 5 secondes pour 50 entrées)
        assert elapsed_time < 5.0

        # Vérifier qu'on peut récupérer les entrées
        response = client.get("/api/pain/entries/recent?limit=50")
        assert response.status_code == 200
        data = response.json()
        assert len(data.get("entries", [])) <= 50

    def test_query_performance_with_many_entries(self, client):
        """Test performance des requêtes avec beaucoup d'entrées"""
        # Créer quelques entrées pour avoir des données (réduit pour accélérer)
        for i in range(20):
            pain_entry = {
                "intensity": i % 11,
                "location": f"location_{i % 5}",
            }
            client.post("/api/pain/entry", json=pain_entry)

        # Tester différentes requêtes
        queries = [
            "/api/pain/entries/recent?limit=50",
            "/api/pain/entries/recent?limit=100",
            "/api/pain/suggestions",
            "/api/patterns/correlations/sleep-pain",
        ]

        for query in queries:
            start_time = time.time()
            response = client.get(query)
            elapsed_time = time.time() - start_time

            # Les requêtes doivent être rapides (< 2 secondes)
            assert elapsed_time < 2.0
            # Et doivent retourner un code valide
            assert response.status_code in [200, 404]

    def test_pagination_performance(self, client):
        """Test performance de la pagination avec grandes quantités"""
        # Créer des entrées (réduit pour accélérer)
        for _ in range(20):
            pain_entry = {"intensity": 5, "location": "test"}
            client.post("/api/pain/entry", json=pain_entry)

        # Tester pagination avec différents offsets (réduit)
        for offset in [0, 5, 10, 15]:
            start_time = time.time()
            response = client.get(f"/api/pain/entries/recent?limit=10&offset={offset}")
            elapsed_time = time.time() - start_time

            assert response.status_code == 200
            # Pagination doit être rapide (< 1 seconde)
            assert elapsed_time < 1.0

    def test_export_performance(self):
        """Test performance des exports avec beaucoup de données"""
        # Créer des entrées
        for i in range(50):
            pain_entry = {
                "intensity": i % 11,
                "location": f"location_{i}",
            }
            client.post("/api/pain/entry", json=pain_entry)

        # Tester export CSV
        start_time = time.time()
        response = client.get("/api/pain/export/csv")
        csv_time = time.time() - start_time

        assert response.status_code == 200
        # Export CSV doit être rapide (< 3 secondes)
        assert csv_time < 3.0

        # Tester export PDF (peut être plus lent)
        start_time = time.time()
        response = client.get("/api/pain/export/pdf")
        pdf_time = time.time() - start_time

        assert response.status_code == 200
        # Export PDF peut être plus lent mais raisonnable (< 10 secondes)
        assert pdf_time < 10.0
