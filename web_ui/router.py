from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(prefix="/app", tags=["Web UI"])


@router.get("/", response_class=HTMLResponse)
async def app_home(request: Request) -> Any:
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Tableau de bord ARIA",
        },
    )


@router.get("/journal", response_class=HTMLResponse)
async def journal_page(request: Request) -> Any:
    return templates.TemplateResponse(
        "journal.html",
        {
            "request": request,
            "title": "Journal de douleur",
        },
    )


@router.get("/overview", response_class=HTMLResponse)
async def overview_page(request: Request) -> Any:
    return templates.TemplateResponse(
        "overview.html",
        {
            "request": request,
            "title": "Vue d'ensemble",
        },
    )


@router.get("/exports", response_class=HTMLResponse)
async def exports_page(request: Request) -> Any:
    return templates.TemplateResponse(
        "exports.html",
        {
            "request": request,
            "title": "Préparer une consultation",
        },
    )

