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

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    voice: str | None = Field(default="amelie")


class AudioNoteRequest(BaseModel):
    filename: str | None = None
    content_base64: str = Field(..., description="Audio encodé base64 (wav/mp3)")


@router.get("/status")
async def audio_status() -> dict:
    return {
        "module": "audio_voice",
        "status": "ready",
        "features": ["tts_simulated", "audio_note_store"],
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
        raise HTTPException(status_code=400, detail="Texte requis")
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
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Audio base64 invalide: {e}"
        ) from e

    out_dir = Path("dacc/audio_notes")
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = (
        req.filename or f"audio_note_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    )
    out_path = out_dir / filename
    with open(out_path, "wb") as f:
        f.write(data)

    return {
        "status": "saved",
        "file_path": str(out_path.resolve()),
        "size_bytes": len(data),
        "timestamp": datetime.now().isoformat(),
    }
