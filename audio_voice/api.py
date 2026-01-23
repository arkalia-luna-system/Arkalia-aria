#!/usr/bin/env python3
"""
Audio/Voix API - ARIA
=====================

Endpoints légers pour la synthèse vocale (TTS) et la prise de note audio.
Sans dépendance externe obligatoire: TTS simulé côté backend, stockage de note.
"""

from __future__ import annotations

import base64
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException
from pydantic import BaseModel, Field

from core import BaseAPI, get_logger

from .transcription import get_transcriber

# Créer l'API avec BaseAPI
api = BaseAPI("", ["Audio/Voice"])  # Pas de préfixe ici, il sera ajouté dans main.py
router = api.get_router()
logger = get_logger("audio_voice")


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    voice: str | None = Field(default="amelie")


class AudioNoteRequest(BaseModel):
    filename: str | None = None
    content_base64: str = Field(..., description="Audio encodé base64 (wav/mp3)")


@router.get("/status")
async def audio_status() -> dict:
    logger.info("Statut audio demandé")
    transcriber = get_transcriber()
    transcription_status = transcriber.get_status()
    return {
        "module": "audio_voice",
        "status": "ready",
        "features": ["tts_simulated", "audio_note_store", "transcription"],
        "transcription": transcription_status,
        "timestamp": datetime.now().isoformat(),
    }


@router.post("/tts")
async def synthesize_speech(req: TTSRequest) -> dict:
    """Simule la synthèse vocale: renvoie un texte de confirmation.

    Remarque: pour une vraie TTS locale, brancher pyttsx3 côté client
    ou un service local. Ici on évite toute dépendance lourde.
    """
    text = req.text.strip()
    if not text:
        logger.warning("Tentative TTS avec texte vide")
        raise HTTPException(status_code=400, detail="Texte requis")

    logger.info(f"TTS demandée: {len(text)} caractères, voix: {req.voice}")
    return {
        "status": "ok",
        "voice": req.voice or "amelie",
        "text": text,
        "message": "TTS simulée côté serveur - aucune dépendance installée",
    }


@router.post("/note")
async def save_audio_note(req: AudioNoteRequest) -> dict:
    """Enregistre une note audio encodée en base64 dans `dacc/audio_notes/`"""
    try:
        data = base64.b64decode(req.content_base64)
        logger.info(f"Audio décodé: {len(data)} bytes")
    except Exception as e:
        logger.error(f"Erreur décodage base64: {e}")
        raise HTTPException(
            status_code=400, detail=f"Audio base64 invalide: {e}"
        ) from e

    out_dir = Path("dacc/audio_notes")
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = (
        req.filename or f"audio_note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    out_path = out_dir / filename

    try:
        with open(out_path, "wb") as f:
            f.write(data)
        logger.info(f"Note audio sauvegardée: {out_path}")
    except Exception as e:
        logger.error(f"Erreur sauvegarde audio: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur sauvegarde: {e}") from e

    return {
        "status": "saved",
        "file_path": str(out_path.resolve()),
        "size_bytes": len(data),
        "timestamp": datetime.now().isoformat(),
    }


class TranscriptionRequest(BaseModel):
    """Requête pour transcription audio"""

    model_config = {"protected_namespaces": ()}

    audio_path: str | None = Field(
        None, description="Chemin vers fichier audio (si déjà sauvegardé)"
    )
    content_base64: str | None = Field(
        None, description="Audio encodé base64 (alternative à audio_path)"
    )
    whisper_model_size: str | None = Field(
        default="base",
        description="Taille modèle Whisper (tiny, base, small, medium, large)",
    )


@router.post("/transcribe")
async def transcribe_audio(req: TranscriptionRequest) -> dict:
    """Transcrit un fichier audio en texte utilisant Whisper.

    Args:
        req: Requête avec audio_path ou content_base64

    Returns:
        Texte transcrit et métadonnées
    """
    transcriber = get_transcriber(model_size=req.whisper_model_size or "base")

    try:
        if req.audio_path:
            # Transcription depuis fichier
            result = transcriber.transcribe_file(req.audio_path)
        elif req.content_base64:
            # Transcription depuis base64
            result = transcriber.transcribe_base64(req.content_base64)
        else:
            raise HTTPException(
                status_code=400,
                detail="audio_path ou content_base64 requis",
            )

        logger.info(f"Transcription réussie: {len(result.get('text', ''))} caractères")
        return {
            "status": "success",
            "transcription": result,
            "timestamp": datetime.now().isoformat(),
        }

    except FileNotFoundError as e:
        logger.error(f"Fichier introuvable: {e}")
        raise HTTPException(status_code=404, detail=f"Fichier introuvable: {e}") from e
    except Exception as e:
        logger.error(f"Erreur transcription: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur transcription: {e}") from e


@router.post("/transcribe-note/{note_id}")
async def transcribe_saved_note(note_id: str) -> dict:
    """Transcrit une note audio déjà sauvegardée.

    Args:
        note_id: Nom du fichier ou ID de la note

    Returns:
        Texte transcrit et métadonnées
    """
    transcriber = get_transcriber()

    # Chercher le fichier dans dacc/audio_notes
    audio_dir = Path("dacc/audio_notes")
    audio_path = audio_dir / note_id

    if not audio_path.exists():
        # Essayer avec différents formats
        for ext in [".wav", ".mp3", ".m4a", ".ogg"]:
            test_path = audio_dir / f"{note_id}{ext}"
            if test_path.exists():
                audio_path = test_path
                break
        else:
            raise HTTPException(
                status_code=404, detail=f"Note audio introuvable: {note_id}"
            )

    try:
        result = transcriber.transcribe_file(audio_path)
        logger.info(f"Note {note_id} transcrit avec succès")

        return {
            "status": "success",
            "note_id": note_id,
            "transcription": result,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Erreur transcription note {note_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur transcription: {e}") from e
