#!/usr/bin/env python3
"""
Transcription Audio - ARIA
===========================

Module de transcription audio utilisant Whisper (OpenAI).
Support pour transcription de notes audio et saisie vocale.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from core import get_logger

logger = get_logger("audio_transcription")

# Whisper est optionnel - si non installé, on utilise un fallback
try:
    import whisper

    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logger.warning(
        "Whisper non disponible - installer avec: pip install openai-whisper"
    )


class AudioTranscriber:
    """
    Gestionnaire de transcription audio utilisant Whisper.

    Supporte:
    - Transcription de fichiers audio (wav, mp3, m4a, etc.)
    - Modèles Whisper (tiny, base, small, medium, large)
    - Fallback si Whisper non disponible
    """

    def __init__(self, model_size: str = "base"):
        """
        Initialise le transcripteur audio.

        Args:
            model_size: Taille du modèle Whisper (tiny, base, small, medium, large)
                       Par défaut: "base" (bon compromis vitesse/qualité)
        """
        self.model_size = model_size
        self.model: Any = None
        self.whisper_available = WHISPER_AVAILABLE

        if self.whisper_available:
            try:
                logger.info(f"Chargement modèle Whisper: {model_size}")
                self.model = whisper.load_model(model_size)
                logger.info("✅ Modèle Whisper chargé avec succès")
            except Exception as e:
                logger.error(f"Erreur chargement Whisper: {e}")
                self.whisper_available = False
                self.model = None
        else:
            logger.warning("Whisper non disponible - mode simulation activé")

    def transcribe_file(self, audio_path: str | Path) -> dict[str, Any]:
        """
        Transcrit un fichier audio en texte.

        Args:
            audio_path: Chemin vers le fichier audio

        Returns:
            Dictionnaire avec:
            - text: Texte transcrit
            - language: Langue détectée
            - segments: Segments détaillés (si disponible)
            - duration: Durée audio (si disponible)
            - model_used: Modèle utilisé
        """
        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(f"Fichier audio introuvable: {audio_path}")

        if not self.whisper_available or self.model is None:
            # Mode simulation si Whisper non disponible
            logger.warning("Whisper non disponible - retour simulation")
            return {
                "text": "[Transcription non disponible - installer Whisper]",
                "language": "fr",
                "segments": [],
                "duration": 0.0,
                "model_used": "simulation",
                "warning": (
                    "Whisper non installé - installer avec: pip install openai-whisper"
                ),
            }

        try:
            logger.info(f"Transcription de: {audio_path}")
            result = self.model.transcribe(str(audio_path))

            return {
                "text": result.get("text", "").strip(),
                "language": result.get("language", "fr"),
                "segments": result.get("segments", []),
                "duration": sum(
                    seg.get("end", 0) - seg.get("start", 0)
                    for seg in result.get("segments", [])
                ),
                "model_used": self.model_size,
            }
        except Exception as e:
            logger.error(f"Erreur transcription: {e}")
            raise RuntimeError(f"Erreur transcription audio: {e}") from e

    def transcribe_base64(self, audio_base64: str) -> dict[str, Any]:
        """
        Transcrit un audio encodé en base64.

        Args:
            audio_base64: Audio encodé en base64

        Returns:
            Dictionnaire avec le texte transcrit et métadonnées
        """
        import base64
        import tempfile

        try:
            # Décoder base64
            audio_data = base64.b64decode(audio_base64)

            # Créer fichier temporaire
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                tmp_file.write(audio_data)
                tmp_path = tmp_file.name

            try:
                # Transcrire
                result = self.transcribe_file(tmp_path)
                return result
            finally:
                # Nettoyer fichier temporaire
                try:
                    os.unlink(tmp_path)
                except FileNotFoundError:
                    # Le fichier a déjà été supprimé, on peut ignorer
                    pass
                except OSError as exc:
                    logger.warning(
                        "Impossible de supprimer le fichier temporaire %s: %s",
                        tmp_path,
                        exc,
                    )

        except Exception as e:
            logger.error(f"Erreur transcription base64: {e}")
            raise RuntimeError(f"Erreur transcription base64: {e}") from e

    def get_status(self) -> dict[str, Any]:
        """
        Retourne le statut du transcripteur.

        Returns:
            Dictionnaire avec statut et informations
        """
        return {
            "whisper_available": self.whisper_available,
            "model_loaded": self.model is not None,
            "model_size": self.model_size if self.whisper_available else None,
            "status": "ready" if self.whisper_available else "simulation",
        }


# Instance globale (singleton)
_transcriber: AudioTranscriber | None = None


def get_transcriber(model_size: str = "base") -> AudioTranscriber:
    """
    Récupère ou crée l'instance globale du transcripteur.

    Args:
        model_size: Taille du modèle (par défaut: "base")

    Returns:
        Instance AudioTranscriber
    """
    global _transcriber
    if _transcriber is None:
        _transcriber = AudioTranscriber(model_size=model_size)
    return _transcriber
