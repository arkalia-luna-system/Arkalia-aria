#!/usr/bin/env python3
"""
IA API - ARIA
=============

Endpoints API pour l'intelligence artificielle locale (Ollama).
Recommandations, chatbot et analyse sémantique.
"""

from __future__ import annotations

from datetime import datetime

from fastapi import HTTPException
from pydantic import BaseModel, Field

from core import BaseAPI, get_logger

from .chatbot import get_chatbot
from .ollama_integration import get_ollama_manager
from .recommendations import get_recommendations

# Créer l'API avec BaseAPI
api = BaseAPI("", ["AI/Local"])
router = api.get_router()
logger = get_logger("ai_api")


class ChatRequest(BaseModel):
    """Requête pour chat avec le chatbot"""

    message: str = Field(..., min_length=1, max_length=2000)
    include_context: bool = Field(
        default=True, description="Inclure contexte utilisateur"
    )
    reset_history: bool = Field(default=False, description="Réinitialiser historique")


class AnalyzeNoteRequest(BaseModel):
    """Requête pour analyse sémantique d'une note"""

    note_text: str = Field(..., min_length=1, max_length=5000)


@router.get("/status")
async def ai_status() -> dict:
    """Statut de l'intégration IA locale"""
    ollama = get_ollama_manager()
    ollama_status = ollama.get_status()
    return {
        "module": "ai_local",
        "status": "ready",
        "ollama": ollama_status,
        "features": ["recommendations", "chatbot", "semantic_analysis"],
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/recommendations")
async def get_pain_recommendations(days_back: int = 30) -> dict:
    """Génère des recommandations IA basées sur les données de douleur récentes.

    Args:
        days_back: Nombre de jours à analyser (par défaut: 30)

    Returns:
        Recommandations personnalisées et analyse
    """
    try:
        recommendations = get_recommendations()
        result = recommendations.generate_pain_recommendations(days_back=days_back)
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Erreur génération recommandations: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erreur génération recommandations: {e}"
        ) from e


@router.get("/recommendations/correlations")
async def get_correlation_insights() -> dict:
    """Génère des insights basés sur les corrélations détectées.

    Returns:
        Insights et recommandations basées sur corrélations
    """
    try:
        recommendations = get_recommendations()
        result = recommendations.generate_correlation_insights()
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Erreur génération insights: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erreur génération insights: {e}"
        ) from e


@router.post("/chat")
async def chat_with_bot(req: ChatRequest) -> dict:
    """Chat avec le chatbot santé conversationnel.

    Args:
        req: Requête avec message utilisateur

    Returns:
        Réponse du chatbot
    """
    try:
        chatbot = get_chatbot()
        result = chatbot.chat(
            user_message=req.message,
            include_context=req.include_context,
            reset_history=req.reset_history,
        )
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Erreur chat: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur chat: {e}") from e


@router.post("/chat/reset")
async def reset_chat() -> dict:
    """Réinitialise l'historique de conversation du chatbot."""
    try:
        chatbot = get_chatbot()
        result = chatbot.reset_conversation()
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Erreur reset chat: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur reset chat: {e}") from e


@router.get("/chat/history")
async def get_chat_history() -> dict:
    """Retourne l'historique de conversation."""
    try:
        chatbot = get_chatbot()
        history = chatbot.get_conversation_history()
        return {
            "status": "success",
            "history": history,
            "count": len(history),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Erreur récupération historique: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erreur récupération historique: {e}"
        ) from e


@router.post("/analyze/note")
async def analyze_note_semantics(req: AnalyzeNoteRequest) -> dict:
    """Analyse sémantique d'une note de douleur.

    Args:
        req: Requête avec texte de la note

    Returns:
        Analyse sémantique (résumé, sentiment, mots-clés)
    """
    try:
        recommendations = get_recommendations()
        result = recommendations.analyze_note_semantics(req.note_text)
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Erreur analyse sémantique: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erreur analyse sémantique: {e}"
        ) from e
