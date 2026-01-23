#!/usr/bin/env python3
"""
Recommandations IA - ARIA
==========================

Module de recommandations personnalisées basées sur l'IA locale (Ollama).
Analyse les données de douleur et génère des recommandations personnalisées.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from core import DatabaseManager, get_logger

from .ollama_integration import get_ollama_manager

logger = get_logger("ai_recommendations")
db = DatabaseManager()


class AIRecommendations:
    """
    Générateur de recommandations IA personnalisées.

    Analyse les données de douleur et génère des recommandations
    basées sur les patterns détectés.
    """

    def __init__(self):
        """Initialise le générateur de recommandations."""
        self.ollama = get_ollama_manager()

    def generate_pain_recommendations(self, days_back: int = 30) -> dict[str, Any]:
        """
        Génère des recommandations basées sur les données de douleur récentes.

        Args:
            days_back: Nombre de jours à analyser (par défaut: 30)

        Returns:
            Dictionnaire avec recommandations et analyse
        """
        # Récupérer les données de douleur récentes
        start_date = (datetime.now() - timedelta(days=days_back)).isoformat()

        try:
            rows = db.execute_query(
                """
                SELECT intensity, location, physical_trigger, mental_trigger,
                       timestamp, notes
                FROM pain_entries
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT 50
                """,
                (start_date,),
            )

            if not rows:
                return {
                    "recommendations": [],
                    "analysis": "Aucune donnée récente à analyser",
                    "days_analyzed": days_back,
                }

            # Convertir Row en dict
            entries = [dict(row) for row in rows]

            # Préparer un résumé des données
            total_entries = len(entries)
            avg_intensity = sum(e.get("intensity", 0) for e in entries) / total_entries
            locations = {}
            triggers = {}

            for entry in entries:
                loc = entry.get("location")
                if loc:
                    locations[loc] = locations.get(loc, 0) + 1

                trigger = entry.get("physical_trigger") or entry.get("mental_trigger")
                if trigger:
                    triggers[trigger] = triggers.get(trigger, 0) + 1

            # Créer un prompt pour Ollama
            prompt = f"""Analyse ces données de suivi de douleur et génère 3-5 recommandations personnalisées:

Données analysées:
- Nombre d'épisodes: {total_entries}
- Intensité moyenne: {avg_intensity:.1f}/10
- Localisations fréquentes: {', '.join(list(locations.keys())[:5])}
- Déclencheurs fréquents: {', '.join(list(triggers.keys())[:5])}

Génère des recommandations pratiques et personnalisées pour améliorer la gestion de la douleur.
Format: Liste numérotée, courtes et actionnables."""

            # Générer les recommandations avec Ollama
            result = self.ollama.generate(prompt)

            recommendations_text = result.get("response", "")
            recommendations = [
                rec.strip()
                for rec in recommendations_text.split("\n")
                if rec.strip()
                and (rec.strip()[0].isdigit() or rec.strip().startswith("-"))
            ]

            return {
                "recommendations": recommendations,
                "analysis": {
                    "total_entries": total_entries,
                    "avg_intensity": round(avg_intensity, 1),
                    "top_locations": dict(
                        sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]
                    ),
                    "top_triggers": dict(
                        sorted(triggers.items(), key=lambda x: x[1], reverse=True)[:5]
                    ),
                },
                "days_analyzed": days_back,
                "model_used": result.get("model", "simulation"),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Erreur génération recommandations: {e}")
            return {
                "recommendations": [],
                "analysis": f"Erreur lors de l'analyse: {e}",
                "days_analyzed": days_back,
            }

    def generate_correlation_insights(self) -> dict[str, Any]:
        """
        Génère des insights basés sur les corrélations détectées.

        Returns:
            Dictionnaire avec insights et recommandations
        """
        try:
            # Récupérer les corrélations récentes
            rows = db.execute_query("""
                SELECT correlation_type, strength, description
                FROM correlations
                WHERE strength > 0.5
                ORDER BY strength DESC
                LIMIT 10
                """)

            if not rows:
                return {
                    "insights": [],
                    "message": "Aucune corrélation forte détectée",
                }

            # Convertir Row en dict
            correlations = [dict(row) for row in rows]

            # Créer un prompt pour Ollama
            correlations_text = "\n".join(
                [
                    f"- {c.get('correlation_type', '')}: {c.get('description', '')} (force: {c.get('strength', 0):.2f})"
                    for c in correlations
                ]
            )

            prompt = f"""Analyse ces corrélations détectées dans les données de douleur et génère des insights actionnables:

Corrélations détectées:
{correlations_text}

Génère 3-5 insights pratiques basés sur ces corrélations.
Format: Liste numérotée, courtes et actionnables."""

            result = self.ollama.generate(prompt)

            insights_text = result.get("response", "")
            insights = [
                insight.strip()
                for insight in insights_text.split("\n")
                if insight.strip()
                and (insight.strip()[0].isdigit() or insight.strip().startswith("-"))
            ]

            return {
                "insights": insights,
                "correlations_analyzed": len(correlations),
                "model_used": result.get("model", "simulation"),
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Erreur génération insights: {e}")
            return {
                "insights": [],
                "message": f"Erreur lors de l'analyse: {e}",
            }

    def analyze_note_semantics(self, note_text: str) -> dict[str, Any]:
        """
        Analyse sémantique d'une note de douleur.

        Args:
            note_text: Texte de la note à analyser

        Returns:
            Analyse sémantique avec mots-clés, sentiment, etc.
        """
        ollama = get_ollama_manager()

        # Analyse avec différents types
        summary = ollama.analyze_text(note_text, "summary")
        sentiment = ollama.analyze_text(note_text, "sentiment")
        keywords = ollama.analyze_text(note_text, "keywords")

        return {
            "summary": summary.get("analysis", ""),
            "sentiment": sentiment.get("analysis", ""),
            "keywords": keywords.get("analysis", ""),
            "model_used": summary.get("model", "simulation"),
            "timestamp": datetime.now().isoformat(),
        }


# Instance globale (singleton)
_recommendations: AIRecommendations | None = None


def get_recommendations() -> AIRecommendations:
    """Récupère ou crée l'instance globale du générateur de recommandations."""
    global _recommendations
    if _recommendations is None:
        _recommendations = AIRecommendations()
    return _recommendations
