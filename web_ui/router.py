from __future__ import annotations

from pathlib import Path
from typing import Any
import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter(prefix="/app", tags=["Web UI"])

WEBUI_PASSWORD = os.getenv("ARIA_WEBUI_PASSWORD")


def _needs_auth() -> bool:
    return bool(WEBUI_PASSWORD)


def _is_authenticated(request: Request) -> bool:
    return request.cookies.get("aria_webui_auth") == "1"


def _redirect_to_login() -> RedirectResponse:
    return RedirectResponse(url="/app/login", status_code=302)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request) -> Any:
    # Si aucun mot de passe n'est configuré, rediriger directement vers l'accueil
    if not _needs_auth():
        return RedirectResponse(url="/app", status_code=302)
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Connexion",
            "error": None,
        },
    )


@router.post("/login", response_class=HTMLResponse)
async def login_submit(request: Request) -> Any:
    if not _needs_auth():
        return RedirectResponse(url="/app", status_code=302)
    form = await request.form()
    password = form.get("password") or ""
    if password != WEBUI_PASSWORD:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "title": "Connexion",
                "error": "Mot de passe incorrect.",
            },
            status_code=401,
        )
    response = RedirectResponse(url="/app", status_code=302)
    response.set_cookie(
        "aria_webui_auth",
        "1",
        httponly=True,
        max_age=12 * 60 * 60,
        samesite="lax",
    )
    return response


@router.get("/", response_class=HTMLResponse)
async def app_home(request: Request) -> Any:
    if _needs_auth() and not _is_authenticated(request):
        return _redirect_to_login()
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "Tableau de bord ARIA",
        },
    )


@router.get("/journal", response_class=HTMLResponse)
async def journal_page(request: Request) -> Any:
    if _needs_auth() and not _is_authenticated(request):
        return _redirect_to_login()
    return templates.TemplateResponse(
        "journal.html",
        {
            "request": request,
            "title": "Journal de douleur",
        },
    )


@router.get("/overview", response_class=HTMLResponse)
async def overview_page(request: Request) -> Any:
    if _needs_auth() and not _is_authenticated(request):
        return _redirect_to_login()
    return templates.TemplateResponse(
        "overview.html",
        {
            "request": request,
            "title": "Vue d'ensemble",
        },
    )


@router.get("/exports", response_class=HTMLResponse)
async def exports_page(request: Request) -> Any:
    if _needs_auth() and not _is_authenticated(request):
        return _redirect_to_login()
    return templates.TemplateResponse(
        "exports.html",
        {
            "request": request,
            "title": "Préparer une consultation",
        },
    )


@router.get("/connectors", response_class=HTMLResponse)
async def connectors_page(request: Request) -> Any:
    if _needs_auth() and not _is_authenticated(request):
        return _redirect_to_login()
    return templates.TemplateResponse(
        "connectors.html",
        {
            "request": request,
            "title": "Connecteurs Santé",
        },
    )

