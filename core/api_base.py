#!/usr/bin/env python3
"""
ARKALIA ARIA - Base API
=======================

Classe de base pour toutes les APIs ARIA avec fonctionnalités communes.
"""

from collections.abc import Sequence
from datetime import datetime
from enum import Enum
from typing import Any

from fastapi import APIRouter, HTTPException

from .cache import CacheManager, RedisCacheManager
from .config import Config
from .database import DatabaseManager
from .logging import get_logger


class BaseAPI:
    """
    Classe de base pour toutes les APIs ARIA.

    Fournit des fonctionnalités communes :
    - Gestionnaire de base de données
    - Cache intelligent
    - Logging structuré
    - Endpoints standardisés
    """

    def __init__(self, prefix: str, tags: Sequence[str], description: str = ""):
        """
        Initialise l'API de base.

        Args:
            prefix: Préfixe de l'API (ex: "/api/pain")
            tags: Tags OpenAPI pour la documentation
            description: Description de l'API
        """
        self.prefix = prefix
        self.tags = list(tags)
        self.description = description

        # Composants communs
        self.db = DatabaseManager()

        # Initialiser le cache (Redis si activé, sinon mémoire)
        config = Config()
        if config.get("redis_enabled", False):
            self.cache: CacheManager = RedisCacheManager(
                default_ttl=config.get("cache_ttl", 300),
                max_size=config.get("cache_max_size", 1000),
                redis_url=config.get("redis_url", "redis://localhost:6379/0"),
                redis_enabled=True,
            )
        else:
            self.cache = CacheManager(
                default_ttl=config.get("cache_ttl", 300),
                max_size=config.get("cache_max_size", 1000),
            )

        self.logger = get_logger(f"api.{prefix.replace('/api/', '')}")

        # Router FastAPI
        tags_list: list[str | Enum] = list(tags)
        self.router = APIRouter(
            prefix=prefix,
            tags=tags_list,
            responses={
                404: {"description": "Not found"},
                500: {"description": "Internal server error"},
            },
        )

        # Enregistrer les endpoints standardisés
        self._register_standard_endpoints()

    def _register_standard_endpoints(self):
        """Enregistre les endpoints standardisés."""

        @self.router.get("/health")
        async def health_check():
            """Vérification de santé de l'API"""
            try:
                # Test de la base de données
                db_status = "healthy"
                try:
                    self.db.execute_query("SELECT 1")
                except Exception:
                    db_status = "unhealthy"

                # Test du cache
                cache_status = "healthy"
                try:
                    self.cache.set("health_check", "ok", ttl=1)
                    if self.cache.get("health_check") != "ok":
                        cache_status = "unhealthy"
                except Exception:
                    cache_status = "unhealthy"

                return {
                    "status": (
                        "healthy"
                        if db_status == "healthy" and cache_status == "healthy"
                        else "degraded"
                    ),
                    "timestamp": datetime.now().isoformat(),
                    "components": {"database": db_status, "cache": cache_status},
                }
            except Exception as e:
                self.logger.error(f"Erreur health check: {e}")
                raise HTTPException(
                    status_code=500, detail="Health check failed"
                ) from e

        @self.router.get("/status")
        async def get_status():
            """Statut détaillé de l'API"""
            try:
                return {
                    "api_name": self.prefix,
                    "description": self.description,
                    "status": "active",
                    "timestamp": datetime.now().isoformat(),
                    "version": "1.0.0",
                }
            except Exception as e:
                self.logger.error(f"Erreur status: {e}")
                raise HTTPException(
                    status_code=500, detail="Status check failed"
                ) from e

        @self.router.get("/metrics")
        async def get_metrics():
            """Métriques de l'API"""
            try:
                # Récupérer les métriques depuis le cache si disponibles
                cached_metrics = self.cache.get(f"metrics_{self.prefix}")
                if cached_metrics:
                    return cached_metrics

                # Calculer les métriques
                metrics = await self._calculate_metrics()

                # Mettre en cache pour 5 minutes
                self.cache.set(f"metrics_{self.prefix}", metrics, ttl=300)

                return metrics
            except Exception as e:
                self.logger.error(f"Erreur métriques: {e}")
                raise HTTPException(
                    status_code=500, detail="Metrics calculation failed"
                ) from e

    async def _calculate_metrics(self) -> dict[str, Any]:
        """
        Calcule les métriques spécifiques à l'API.

        À surcharger dans les classes dérivées.
        """
        return {
            "api_name": self.prefix,
            "requests_count": 0,
            "error_count": 0,
            "average_response_time": 0.0,
            "cache_hit_ratio": 0.0,
        }

    def log_request(
        self, method: str, endpoint: str, status_code: int, duration: float
    ):
        """Log une requête API."""
        from .logging import log_api_request

        log_api_request(method, endpoint, status_code, duration)

    def log_error(self, error: Exception, context: str = "", **metadata):
        """Log une erreur avec contexte."""
        from .logging import log_error

        log_error(error, context, **metadata)

    def get_cached_data(self, key: str, func, ttl: int = 300):
        """Récupère des données depuis le cache ou les calcule."""
        return self.cache.get_or_set(key, func, ttl)

    def invalidate_cache(self, pattern: str = None):
        """Invalide le cache."""
        if pattern:
            self.cache.invalidate_pattern(pattern)
        else:
            self.cache.clear()

    def get_router(self) -> APIRouter:
        """Retourne le router FastAPI."""
        return self.router
