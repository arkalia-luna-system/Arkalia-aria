#!/usr/bin/env python3
"""
ARKALIA ARIA - Intelligence Artificielle Locale
================================================

Module d'intégration avec Ollama pour IA locale.
"""

from .ollama_integration import OllamaManager, get_ollama_manager

__all__ = ["OllamaManager", "get_ollama_manager"]
