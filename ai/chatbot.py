#!/usr/bin/env python3
"""
Chatbot Santé - ARIA
=====================

Chatbot conversationnel pour questions santé basé sur Ollama.
Contexte: données de douleur et santé de l'utilisateur.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from core import DatabaseManager, get_logger

from .ollama_integration import get_ollama_manager

logger = get_logger("ai_chatbot")
db = DatabaseManager()


class HealthChatbot:
    """
    Chatbot santé conversationnel.

    Utilise Ollama pour répondre aux questions santé avec contexte
    basé sur les données ARIA de l'utilisateur.
    """

    def __init__(self):
        """Initialise le chatbot."""
        self.ollama = get_ollama_manager()
        self.conversation_history: list[dict[str, str]] = []

    def _get_user_context(self, days_back: int = 7) -> str:
        """
        Récupère le contexte utilisateur récent.

        Args:
            days_back: Nombre de jours à analyser

        Returns:
            Contexte formaté pour le prompt
        """
        start_date = (datetime.now() - timedelta(days=days_back)).isoformat()

        try:
            # Récupérer données récentes
            entries = db.execute_query(
                """
                SELECT intensity, location, physical_trigger, timestamp
                FROM pain_entries
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT 10
                """,
                (start_date,),
            )

            if not entries:
                return "Aucune donnée récente disponible."

            context_parts = [
                f"Épisodes récents ({len(entries)}):",
            ]

            for entry in entries[:5]:  # Limiter à 5 pour le contexte
                intensity = entry.get("intensity", 0)
                location = entry.get("location", "N/A")
                trigger = entry.get("physical_trigger") or entry.get(
                    "mental_trigger", "N/A"
                )
                context_parts.append(
                    f"- Intensité {intensity}/10, {location}, déclencheur: {trigger}"
                )

            return "\n".join(context_parts)

        except Exception as e:
            logger.error(f"Erreur récupération contexte: {e}")
            return "Erreur lors de la récupération du contexte."

    def chat(
        self,
        user_message: str,
        include_context: bool = True,
        reset_history: bool = False,
    ) -> dict[str, Any]:
        """
        Chat avec le chatbot santé.

        Args:
            user_message: Message de l'utilisateur
            include_context: Inclure le contexte utilisateur (données ARIA)
            reset_history: Réinitialiser l'historique de conversation

        Returns:
            Réponse du chatbot et métadonnées
        """
        if reset_history:
            self.conversation_history = []

        # Préparer le système prompt avec contexte
        system_prompt = """Tu es un assistant santé conversationnel pour ARIA, un système de suivi de douleur chronique.
Tu réponds aux questions de manière empathique, informative et pratique.
Tu peux t'appuyer sur les données de suivi de l'utilisateur pour donner des conseils personnalisés.
Reste factuel et encourageant."""

        if include_context:
            context = self._get_user_context()
            system_prompt += f"\n\nContexte utilisateur récent:\n{context}"

        # Construire les messages
        messages = [{"role": "system", "content": system_prompt}]

        # Ajouter l'historique
        messages.extend(
            self.conversation_history[-5:]
        )  # Garder les 5 derniers messages

        # Ajouter le nouveau message
        messages.append({"role": "user", "content": user_message})

        try:
            # Chat avec Ollama
            result = self.ollama.chat(messages)

            assistant_message = result.get("message", {}).get("content", "")

            # Ajouter à l'historique
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            return {
                "response": assistant_message,
                "model_used": result.get("model", "simulation"),
                "timestamp": datetime.now().isoformat(),
                "context_included": include_context,
            }

        except Exception as e:
            logger.error(f"Erreur chat: {e}")
            return {
                "response": f"Désolé, une erreur est survenue: {e}",
                "model_used": "simulation",
                "timestamp": datetime.now().isoformat(),
            }

    def reset_conversation(self) -> dict[str, Any]:
        """Réinitialise l'historique de conversation."""
        self.conversation_history = []
        return {
            "status": "conversation_reset",
            "timestamp": datetime.now().isoformat(),
        }

    def get_conversation_history(self) -> list[dict[str, str]]:
        """Retourne l'historique de conversation."""
        return self.conversation_history.copy()


# Instance globale (singleton)
_chatbot: HealthChatbot | None = None


def get_chatbot() -> HealthChatbot:
    """Récupère ou crée l'instance globale du chatbot."""
    global _chatbot
    if _chatbot is None:
        _chatbot = HealthChatbot()
    return _chatbot
