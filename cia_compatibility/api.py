"""
CIA Compatibility API - Endpoints de compatibilité pour CIA
============================================================

Ce module ajoute des endpoints de compatibilité pour permettre à CIA
de communiquer avec ARIA en utilisant les endpoints attendus par CIA.

Endpoints de compatibilité :
- GET /api/pain-records -> GET /api/pain/entries
- GET /api/patterns -> GET /api/patterns/patterns/recent
- GET /api/health-metrics -> GET /health/metrics/unified
- POST /api/pain/entries -> POST /api/pain/entry
"""

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

router = APIRouter(tags=["CIA Compatibility"])


@router.get("/api/pain-records")
async def get_pain_records_compat(
    request: Request,
    limit: int = Query(50, ge=1, le=200, description="Nombre d'entrées à retourner"),
    offset: int = Query(0, ge=0, description="Nombre d'entrées à sauter"),
) -> dict[str, Any]:
    """
    Endpoint de compatibilité CIA : GET /api/pain-records
    Redirige vers GET /api/pain/entries
    """
    try:
        # Faire une requête interne vers l'endpoint ARIA
        from fastapi.testclient import TestClient

        from main import app

        client = TestClient(app)
        response = client.get(
            f"/api/pain/entries?limit={limit}&offset={offset}",
            headers=dict(request.headers),
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur compatibilité pain-records: {str(e)}"
        ) from e


@router.get("/api/patterns")
async def get_patterns_compat(
    request: Request,
    days: int = Query(30, ge=1, le=365, description="Nombre de jours à analyser"),
) -> dict[str, Any]:
    """
    Endpoint de compatibilité CIA : GET /api/patterns
    Redirige vers GET /api/patterns/patterns/recent
    """
    try:
        from fastapi.testclient import TestClient

        from main import app

        client = TestClient(app)
        response = client.get(
            f"/api/patterns/patterns/recent?days={days}",
            headers=dict(request.headers),
        )

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur compatibilité patterns: {str(e)}"
        ) from e


@router.get("/api/health-metrics")
async def get_health_metrics_compat(request: Request) -> dict[str, Any]:
    """
    Endpoint de compatibilité CIA : GET /api/health-metrics
    Redirige vers GET /health/metrics/unified
    """
    try:
        from fastapi.testclient import TestClient

        from main import app

        client = TestClient(app)
        response = client.get("/health/metrics/unified", headers=dict(request.headers))

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur compatibilité health-metrics: {str(e)}"
        ) from e


@router.post("/api/pain/entries")
async def post_pain_entries_compat(
    request: Request, entry_data: dict[str, Any]
) -> dict[str, Any]:
    """
    Endpoint de compatibilité CIA : POST /api/pain/entries
    Redirige vers POST /api/pain/entry
    """
    try:
        from fastapi.testclient import TestClient

        from main import app

        client = TestClient(app)
        response = client.post(
            "/api/pain/entry",
            json=entry_data,
            headers=dict(request.headers),
        )

        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur compatibilité pain/entries: {str(e)}"
        ) from e
