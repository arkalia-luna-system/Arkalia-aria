"""
Tests unitaires pour les méthodes utilitaires de CorrelationAnalyzer
"""

import pytest

from pattern_analysis.correlation_analyzer import CorrelationAnalyzer


class TestCorrelationAnalyzerUtils:
    """Tests pour les méthodes utilitaires de CorrelationAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Fixture pour CorrelationAnalyzer."""
        return CorrelationAnalyzer()

    def test_parse_datetime_valid(self, analyzer):
        """Test parsing datetime valide."""
        # Format ISO avec T
        dt_str = "2025-12-12T10:30:00"
        result = analyzer._parse_datetime(dt_str)
        assert result is not None
        assert result.year == 2025
        assert result.month == 12
        assert result.day == 12

        # Format ISO avec Z
        dt_str_z = "2025-12-12T10:30:00Z"
        result_z = analyzer._parse_datetime(dt_str_z)
        assert result_z is not None

    def test_parse_datetime_invalid(self, analyzer):
        """Test parsing datetime invalide."""
        # Format sans T
        dt_str = "2025-12-12 10:30:00"
        result = analyzer._parse_datetime(dt_str)
        assert result is None

        # Format invalide
        dt_str_invalid = "invalid"
        result_invalid = analyzer._parse_datetime(dt_str_invalid)
        assert result_invalid is None

    def test_simple_correlation_positive(self, analyzer):
        """Test corrélation positive."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2.0, 4.0, 6.0, 8.0, 10.0]  # y = 2x (corrélation parfaite)
        result = analyzer._simple_correlation(x, y)
        assert abs(result - 1.0) < 0.01  # Corrélation parfaite = 1.0

    def test_simple_correlation_negative(self, analyzer):
        """Test corrélation négative."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [10.0, 8.0, 6.0, 4.0, 2.0]  # y = -2x + 12 (corrélation négative)
        result = analyzer._simple_correlation(x, y)
        assert abs(result - (-1.0)) < 0.01  # Corrélation négative parfaite = -1.0

    def test_simple_correlation_no_correlation(self, analyzer):
        """Test pas de corrélation."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [5.0, 2.0, 4.0, 1.0, 3.0]  # Pas de corrélation évidente
        result = analyzer._simple_correlation(x, y)
        # Résultat devrait être proche de 0 (tolérance plus large)
        assert abs(result) <= 0.5

    def test_simple_correlation_insufficient_data(self, analyzer):
        """Test avec données insuffisantes."""
        x = [1.0]
        y = [2.0]
        result = analyzer._simple_correlation(x, y)
        assert result == 0.0  # Pas assez de données

    def test_simple_correlation_different_lengths(self, analyzer):
        """Test avec listes de longueurs différentes."""
        x = [1.0, 2.0, 3.0]
        y = [2.0, 4.0]
        result = analyzer._simple_correlation(x, y)
        assert result == 0.0  # Longueurs différentes

    def test_simple_correlation_empty(self, analyzer):
        """Test avec listes vides."""
        x: list[float] = []
        y: list[float] = []
        result = analyzer._simple_correlation(x, y)
        assert result == 0.0

    def test_simple_correlation_zero_variance(self, analyzer):
        """Test avec variance nulle."""
        x = [5.0, 5.0, 5.0, 5.0, 5.0]
        y = [10.0, 10.0, 10.0, 10.0, 10.0]
        result = analyzer._simple_correlation(x, y)
        assert result == 0.0  # Variance nulle = pas de corrélation calculable
