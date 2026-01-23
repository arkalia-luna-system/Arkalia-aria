#!/usr/bin/env python3
"""
Ollama Integration - ARIA
==========================

Gestionnaire d'intégration avec Ollama pour IA locale.
Support pour modèles locaux, recommandations et chatbot.
"""

from __future__ import annotations

import os
from typing import Any

from core import get_logger

logger = get_logger("ollama_integration")

# Ollama est optionnel - si non installé, on utilise un fallback
try:
    import ollama

    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("Ollama non disponible - installer avec: pip install ollama")


class OllamaManager:
    """
    Gestionnaire d'intégration avec Ollama.

    Supporte:
    - Modèles locaux (llama2, mistral, etc.)
    - Génération de texte
    - Chat conversationnel
    - Analyse sémantique
    """

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        """
        Initialise le gestionnaire Ollama.

        Args:
            base_url: URL de base d'Ollama (par défaut: localhost:11434)
            model: Modèle à utiliser par défaut (llama2, mistral, etc.)
        """
        self.base_url = base_url
        self.default_model = model
        self.ollama_available = OLLAMA_AVAILABLE
        self.is_connected = False

        if self.ollama_available:
            try:
                # Vérifier la connexion
                self._check_connection()
                logger.info(f"✅ Ollama initialisé - Modèle: {model}")
            except Exception as e:
                logger.warning(f"Ollama non accessible: {e}")
                self.ollama_available = False
        else:
            logger.warning("Ollama non disponible - mode simulation activé")

    def _check_connection(self) -> bool:
        """Vérifie la connexion avec Ollama."""
        if not self.ollama_available:
            return False

        try:
            # Tester la connexion en listant les modèles
            ollama.list()
            self.is_connected = True
            return True
        except Exception as e:
            logger.debug(f"Ollama non accessible: {e}")
            self.is_connected = False
            return False

    def generate(
        self, prompt: str, model: str | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Génère du texte avec Ollama.

        Args:
            prompt: Prompt à envoyer
            model: Modèle à utiliser (par défaut: self.default_model)
            **kwargs: Options supplémentaires (temperature, top_p, etc.)

        Returns:
            Dictionnaire avec le texte généré et métadonnées
        """
        if not self.ollama_available or not self.is_connected:
            return {
                "response": "[Ollama non disponible - installer et démarrer Ollama]",
                "model": "simulation",
                "warning": "Ollama non installé ou non démarré",
            }

        model_name = model or self.default_model

        try:
            logger.info(f"Génération avec Ollama - Modèle: {model_name}")
            response = ollama.generate(model=model_name, prompt=prompt, **kwargs)

            return {
                "response": response.get("response", "").strip(),
                "model": model_name,
                "done": response.get("done", True),
            }
        except Exception as e:
            logger.error(f"Erreur génération Ollama: {e}")
            raise RuntimeError(f"Erreur génération Ollama: {e}") from e

    def chat(
        self, messages: list[dict[str, str]], model: str | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        """
        Chat conversationnel avec Ollama.

        Args:
            messages: Liste de messages [{"role": "user", "content": "..."}]
            model: Modèle à utiliser
            **kwargs: Options supplémentaires

        Returns:
            Dictionnaire avec la réponse et métadonnées
        """
        if not self.ollama_available or not self.is_connected:
            return {
                "message": {
                    "role": "assistant",
                    "content": "[Ollama non disponible - installer et démarrer Ollama]",
                },
                "model": "simulation",
                "warning": "Ollama non installé ou non démarré",
            }

        model_name = model or self.default_model

        try:
            logger.info(f"Chat avec Ollama - Modèle: {model_name}")
            response = ollama.chat(model=model_name, messages=messages, **kwargs)

            return {
                "message": response.get("message", {}),
                "model": model_name,
                "done": response.get("done", True),
            }
        except Exception as e:
            logger.error(f"Erreur chat Ollama: {e}")
            raise RuntimeError(f"Erreur chat Ollama: {e}") from e

    def analyze_text(self, text: str, analysis_type: str = "summary") -> dict[str, Any]:
        """
        Analyse sémantique d'un texte.

        Args:
            text: Texte à analyser
            analysis_type: Type d'analyse (summary, sentiment, keywords, etc.)

        Returns:
            Résultat de l'analyse
        """
        if not self.ollama_available or not self.is_connected:
            return {
                "analysis": "[Ollama non disponible]",
                "type": analysis_type,
                "model": "simulation",
            }

        prompts = {
            "summary": f"Résume ce texte en 2-3 phrases:\n\n{text}",
            "sentiment": (
                f"Analyse le sentiment de ce texte (positif/négatif/neutre):\n\n{text}"
            ),
            "keywords": f"Extrais les mots-clés importants de ce texte:\n\n{text}",
            "health": (
                f"Analyse ce texte médical et identifie les points importants:\n\n{text}"
            ),
        }

        prompt = prompts.get(analysis_type, prompts["summary"])

        try:
            result = self.generate(prompt)
            return {
                "analysis": result.get("response", ""),
                "type": analysis_type,
                "model": result.get("model", self.default_model),
            }
        except Exception as e:
            logger.error(f"Erreur analyse texte: {e}")
            raise RuntimeError(f"Erreur analyse texte: {e}") from e

    def get_status(self) -> dict[str, Any]:
        """
        Retourne le statut du gestionnaire Ollama.

        Returns:
            Dictionnaire avec statut et informations
        """
        models = []
        if self.ollama_available and self.is_connected:
            try:
                response = ollama.list()
                models = [model.get("name", "") for model in response.get("models", [])]
            except Exception:
                pass

        return {
            "ollama_available": self.ollama_available,
            "is_connected": self.is_connected,
            "base_url": self.base_url,
            "default_model": self.default_model,
            "available_models": models,
            "status": (
                "ready"
                if (self.ollama_available and self.is_connected)
                else "simulation"
            ),
        }


# Instance globale (singleton)
_ollama_manager: OllamaManager | None = None


def get_ollama_manager(
    base_url: str | None = None, model: str | None = None
) -> OllamaManager:
    """
    Récupère ou crée l'instance globale du gestionnaire Ollama.

    Args:
        base_url: URL de base (optionnel, depuis env ou défaut)
        model: Modèle par défaut (optionnel, depuis env ou défaut)

    Returns:
        Instance OllamaManager
    """
    global _ollama_manager
    if _ollama_manager is None:
        base: str = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        default_model_str: str = model or os.getenv("OLLAMA_MODEL", "llama2")
        _ollama_manager = OllamaManager(base_url=base, model=default_model_str)
    return _ollama_manager
