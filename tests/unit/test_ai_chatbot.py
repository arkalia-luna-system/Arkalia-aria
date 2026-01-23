#!/usr/bin/env python3
"""
Tests pour le chatbot santé
"""

from ai.chatbot import HealthChatbot, get_chatbot


class TestHealthChatbot:
    """Tests pour HealthChatbot"""

    def test_chat_simulation_mode(self):
        """Test chat en mode simulation"""
        chatbot = HealthChatbot()
        result = chatbot.chat("Bonjour", include_context=False)
        assert "response" in result
        assert "model_used" in result

    def test_reset_conversation(self):
        """Test réinitialisation conversation"""
        chatbot = HealthChatbot()
        chatbot.chat("Message 1")
        chatbot.reset_conversation()
        assert len(chatbot.get_conversation_history()) == 0

    def test_get_conversation_history(self):
        """Test récupération historique"""
        chatbot = HealthChatbot()
        chatbot.chat("Message test")
        history = chatbot.get_conversation_history()
        assert len(history) >= 2  # user + assistant

    def test_get_chatbot_singleton(self):
        """Test que get_chatbot retourne un singleton"""
        bot1 = get_chatbot()
        bot2 = get_chatbot()
        # Devrait être la même instance
        assert bot1 is bot2
