#!/usr/bin/env python3
"""
Tests pour les recommandations IA
"""

from unittest.mock import patch

from ai.recommendations import AIRecommendations, get_recommendations


class TestAIRecommendations:
    """Tests pour AIRecommendations"""

    def test_generate_pain_recommendations_no_data(self):
        """Test génération recommandations sans données"""
        with patch("ai.recommendations.db") as mock_db:
            mock_db.execute_query.return_value = []
            recommendations = AIRecommendations()
            result = recommendations.generate_pain_recommendations(days_back=30)
            assert "recommendations" in result
            assert result["recommendations"] == []

    def test_analyze_note_semantics(self):
        """Test analyse sémantique d'une note"""
        recommendations = AIRecommendations()
        result = recommendations.analyze_note_semantics("J'ai mal à la tête")
        assert "summary" in result
        assert "sentiment" in result
        assert "keywords" in result

    def test_get_recommendations_singleton(self):
        """Test que get_recommendations retourne un singleton"""
        rec1 = get_recommendations()
        rec2 = get_recommendations()
        # Devrait être la même instance
        assert rec1 is rec2
