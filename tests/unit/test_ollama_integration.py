#!/usr/bin/env python3
"""
Tests pour l'intégration Ollama
"""

from unittest.mock import patch

from ai.ollama_integration import OllamaManager, get_ollama_manager


class TestOllamaManager:
    """Tests pour OllamaManager"""

    def test_manager_status_without_ollama(self):
        """Test statut gestionnaire sans Ollama installé"""
        with patch("ai.ollama_integration.OLLAMA_AVAILABLE", False):
            manager = OllamaManager()
            status = manager.get_status()
            assert status["ollama_available"] is False
            assert status["status"] == "simulation"

    def test_generate_simulation_mode(self):
        """Test génération en mode simulation"""
        manager = OllamaManager()
        result = manager.generate("Test prompt")
        assert "response" in result
        assert result.get("model") == "simulation" or "warning" in result

    def test_chat_simulation_mode(self):
        """Test chat en mode simulation"""
        manager = OllamaManager()
        messages = [{"role": "user", "content": "Bonjour"}]
        result = manager.chat(messages)
        assert "message" in result
        assert result.get("model") == "simulation" or "warning" in result

    def test_analyze_text_simulation(self):
        """Test analyse texte en mode simulation"""
        manager = OllamaManager()
        result = manager.analyze_text("Test text", "summary")
        assert "analysis" in result
        assert result.get("model") == "simulation" or "simulation" in str(result)

    def test_get_ollama_manager_singleton(self):
        """Test que get_ollama_manager retourne un singleton"""
        manager1 = get_ollama_manager()
        manager2 = get_ollama_manager()
        # Devrait être la même instance
        assert manager1 is manager2
