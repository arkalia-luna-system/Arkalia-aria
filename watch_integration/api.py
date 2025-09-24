#!/usr/bin/env python3
"""
Watch Integration API - ARIA
===========================

Contrat d’API pour ingestion de données montre (Health Connect):
- Fréquence cardiaque, sessions de sommeil, niveau de stress, pas.
Stockage local JSONL dans `dacc/watch_data/`.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter()


class HeartRateIn(BaseModel):
    timestamp: str = Field(..., description="ISO-8601")
    bpm: int = Field(..., ge=20, le=250)
    resting: int | None = Field(default=None, ge=20, le=200)


class SleepSessionIn(BaseModel):
    start: str
    end: str
    quality: float | None = Field(default=None, ge=0, le=1)
    duration_minutes: int | None = Field(default=None, ge=0)


class StressLevelIn(BaseModel):
    timestamp: str
    level: int = Field(..., ge=0, le=100)


class StepsIn(BaseModel):
    date: str  # YYYY-MM-DD
    steps: int = Field(..., ge=0)
    active_minutes: int | None = Field(default=0, ge=0)


def _append_jsonl(filename: str, record: dict) -> str:
    out_dir = Path("dacc/watch_data")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / filename
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return str(out_path.resolve())


@router.get("/status")
async def watch_status() -> dict:
    return {
        "module": "watch_integration",
        "status": "ready",
        "endpoints": [
            "/heart-rate",
            "/sleep-session",
            "/stress",
            "/steps",
        ],
        "timestamp": datetime.now().isoformat(),
    }


@router.post("/heart-rate")
async def ingest_heart_rate(hr: HeartRateIn) -> dict:
    rec = hr.dict()
    rec["ingested_at"] = datetime.now().isoformat()
    path = _append_jsonl("heart_rate.jsonl", rec)
    return {"status": "ok", "file": path}


@router.post("/sleep-session")
async def ingest_sleep_session(s: SleepSessionIn) -> dict:
    rec = s.dict()
    rec["ingested_at"] = datetime.now().isoformat()
    path = _append_jsonl("sleep_sessions.jsonl", rec)
    return {"status": "ok", "file": path}


@router.post("/stress")
async def ingest_stress(st: StressLevelIn) -> dict:
    rec = st.dict()
    rec["ingested_at"] = datetime.now().isoformat()
    path = _append_jsonl("stress.jsonl", rec)
    return {"status": "ok", "file": path}


@router.post("/steps")
async def ingest_steps(steps: StepsIn) -> dict:
    rec = steps.dict()
    rec["ingested_at"] = datetime.now().isoformat()
    path = _append_jsonl("steps.jsonl", rec)
    return {"status": "ok", "file": path}
