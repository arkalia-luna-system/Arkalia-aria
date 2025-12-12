"""
Tests unitaires pour le cache dans CorrelationAnalyzer
"""

from unittest.mock import patch

import pytest

from pattern_analysis.correlation_analyzer import CorrelationAnalyzer


class TestCorrelationAnalyzerCache:
    """Tests pour le système de cache dans CorrelationAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Fixture pour CorrelationAnalyzer."""
        return CorrelationAnalyzer()

    def test_cache_initialization(self, analyzer):
        """Test que le cache est initialisé."""
        assert analyzer.cache is not None
        assert analyzer.cache.default_ttl == 3600  # 1h

    def test_sleep_pain_correlation_cache(self, analyzer):
        """Test que analyze_sleep_pain_correlation utilise le cache."""
        # Premier appel : pas de cache
        result1 = analyzer.analyze_sleep_pain_correlation(days_back=30)

        # Deuxième appel : devrait utiliser le cache
        with (
            patch.object(analyzer, "_load_pain_entries") as mock_pain,
            patch.object(analyzer, "_load_sleep_data") as mock_sleep,
        ):
            result2 = analyzer.analyze_sleep_pain_correlation(days_back=30)

            # Les méthodes de chargement ne devraient pas être appelées
            mock_pain.assert_not_called()
            mock_sleep.assert_not_called()

        # Les résultats devraient être identiques
        assert result1 == result2

    def test_stress_pain_correlation_cache(self, analyzer):
        """Test que analyze_stress_pain_correlation utilise le cache."""
        # Premier appel : pas de cache
        result1 = analyzer.analyze_stress_pain_correlation(days_back=30)

        # Deuxième appel : devrait utiliser le cache
        with (
            patch.object(analyzer, "_load_pain_entries") as mock_pain,
            patch.object(analyzer, "_load_stress_data") as mock_stress,
        ):
            result2 = analyzer.analyze_stress_pain_correlation(days_back=30)

            # Les méthodes de chargement ne devraient pas être appelées
            mock_pain.assert_not_called()
            mock_stress.assert_not_called()

        # Les résultats devraient être identiques
        assert result1 == result2

    def test_recurrent_triggers_cache(self, analyzer):
        """Test que detect_recurrent_triggers utilise le cache."""
        # Premier appel : pas de cache
        result1 = analyzer.detect_recurrent_triggers(days_back=30, min_occurrences=3)

        # Deuxième appel : devrait utiliser le cache
        with patch.object(analyzer, "_load_pain_entries") as mock_pain:
            result2 = analyzer.detect_recurrent_triggers(
                days_back=30, min_occurrences=3
            )

            # La méthode de chargement ne devrait pas être appelée
            mock_pain.assert_not_called()

        # Les résultats devraient être identiques
        assert result1 == result2

    def test_comprehensive_analysis_cache(self, analyzer):
        """Test que get_comprehensive_analysis utilise le cache."""
        # Premier appel : pas de cache
        result1 = analyzer.get_comprehensive_analysis(days_back=30)

        # Deuxième appel : devrait utiliser le cache
        with (
            patch.object(analyzer, "analyze_sleep_pain_correlation") as mock_sleep,
            patch.object(analyzer, "analyze_stress_pain_correlation") as mock_stress,
            patch.object(analyzer, "detect_recurrent_triggers") as mock_triggers,
        ):
            result2 = analyzer.get_comprehensive_analysis(days_back=30)

            # Les méthodes d'analyse ne devraient pas être appelées
            mock_sleep.assert_not_called()
            mock_stress.assert_not_called()
            mock_triggers.assert_not_called()

        # Les résultats devraient être identiques
        assert result1 == result2

    def test_cache_different_parameters(self, analyzer):
        """Test que le cache distingue les paramètres différents."""
        # Appel avec days_back=30
        analyzer.analyze_sleep_pain_correlation(days_back=30)

        # Appel avec days_back=60 : devrait recalculer (pas de cache)
        with patch.object(analyzer, "_load_pain_entries") as mock_pain:
            analyzer.analyze_sleep_pain_correlation(days_back=60)

            # Devrait être appelé car paramètre différent
            mock_pain.assert_called_once_with(60)
