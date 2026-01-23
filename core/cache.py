#!/usr/bin/env python3
"""
ARKALIA ARIA - Gestionnaire de Cache
====================================

Système de cache intelligent avec TTL, invalidation et gestion de la mémoire.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import redis

from .exceptions import CacheError

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Gestionnaire de cache intelligent avec TTL et invalidation.

    Fournit un système de cache thread-safe avec expiration automatique
    et gestion de la mémoire.
    """

    def __init__(self, default_ttl: int = 300, max_size: int = 1000) -> None:
        """
        Initialise le gestionnaire de cache.

        Args:
            default_ttl: TTL par défaut en secondes
            max_size: Taille maximale du cache
        """
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._cache: dict[str, dict[str, Any]] = {}
        self._lock = threading.RLock()
        self._access_times: dict[str, float] = {}

        logger.info(
            f"🗄️ CacheManager initialisé (TTL: {default_ttl}s, Max: {max_size})"
        )

    def _is_expired(self, key: str) -> bool:
        """
        Vérifie si une entrée du cache a expiré.

        Args:
            key: Clé de l'entrée

        Returns:
            True si l'entrée a expiré
        """
        if key not in self._cache:
            return True

        entry = self._cache[key]
        if "expires_at" not in entry:
            return False

        return time.time() > entry["expires_at"]

    def _cleanup_expired(self) -> None:
        """Supprime les entrées expirées du cache."""
        current_time = time.time()
        expired_keys = []

        for key, entry in self._cache.items():
            if "expires_at" in entry and current_time > entry["expires_at"]:
                expired_keys.append(key)

        for key in expired_keys:
            del self._cache[key]
            self._access_times.pop(key, None)

        if expired_keys:
            logger.debug(
                f"🧹 Nettoyage cache: {len(expired_keys)} entrées expirées supprimées"
            )

    def _evict_lru(self) -> None:
        """Supprime l'entrée la moins récemment utilisée."""
        if not self._access_times:
            return

        # Trouver la clé avec le temps d'accès le plus ancien
        lru_key = min(self._access_times.keys(), key=lambda k: self._access_times[k])

        del self._cache[lru_key]
        del self._access_times[lru_key]

        logger.debug(f"🗑️ Éviction LRU: clé '{lru_key}' supprimée")

    def get(self, key: str) -> Any | None:
        """
        Récupère une valeur du cache.

        Args:
            key: Clé de la valeur

        Returns:
            Valeur mise en cache ou None si non trouvée/expirée
        """
        with self._lock:
            if key not in self._cache or self._is_expired(key):
                return None

            # Mettre à jour le temps d'accès
            self._access_times[key] = time.time()

            logger.debug(f"📥 Cache hit: {key}")
            return self._cache[key]["data"]

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """
        Définit une valeur dans le cache.

        Args:
            key: Clé de la valeur
            value: Valeur à mettre en cache
            ttl: TTL en secondes (utilise le TTL par défaut si None)
        """
        with self._lock:
            # Nettoyer les entrées expirées
            self._cleanup_expired()

            # Vérifier la taille maximale
            if len(self._cache) >= self.max_size and key not in self._cache:
                self._evict_lru()

            # Calculer le temps d'expiration
            expires_at = None
            if ttl is not None:
                expires_at = time.time() + ttl
            elif self.default_ttl > 0:
                expires_at = time.time() + self.default_ttl

            # Stocker la valeur
            self._cache[key] = {
                "data": value,
                "expires_at": expires_at,
                "created_at": time.time(),
            }
            self._access_times[key] = time.time()

            logger.debug(f"📤 Cache set: {key} (TTL: {ttl or self.default_ttl}s)")

    def get_or_set(
        self, key: str, func: Callable[[], Any], ttl: int | None = None
    ) -> Any:
        """
        Récupère une valeur du cache ou l'exécute et la met en cache.

        Args:
            key: Clé de la valeur
            func: Fonction à exécuter si la valeur n'est pas en cache
            ttl: TTL en secondes

        Returns:
            Valeur mise en cache ou nouvellement calculée
        """
        # Essayer de récupérer depuis le cache
        cached_value = self.get(key)
        if cached_value is not None:
            return cached_value

        # Exécuter la fonction et mettre en cache
        try:
            value = func()
            self.set(key, value, ttl)
            logger.debug(f"⚡ Cache miss, fonction exécutée: {key}")
            return value
        except Exception as e:
            logger.error(
                f"❌ Erreur lors de l'exécution de la fonction pour {key}: {e}"
            )
            raise CacheError(f"Erreur lors de l'exécution de la fonction: {e}") from e

    def delete(self, key: str) -> bool:
        """
        Supprime une entrée du cache.

        Args:
            key: Clé à supprimer

        Returns:
            True si l'entrée existait et a été supprimée
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._access_times.pop(key, None)
                logger.debug(f"🗑️ Cache delete: {key}")
                return True
            return False

    def clear(self) -> None:
        """Vide complètement le cache."""
        with self._lock:
            self._cache.clear()
            self._access_times.clear()
            logger.info("🧹 Cache vidé complètement")

    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalide toutes les entrées correspondant à un pattern.

        Args:
            pattern: Pattern à rechercher dans les clés

        Returns:
            Nombre d'entrées invalidées
        """
        with self._lock:
            keys_to_delete = [key for key in self._cache.keys() if pattern in key]

            for key in keys_to_delete:
                del self._cache[key]
                self._access_times.pop(key, None)

            logger.debug(
                f"🔄 Invalidation pattern '{pattern}': {len(keys_to_delete)} entrées"
            )
            return len(keys_to_delete)

    def get_stats(self) -> dict[str, Any]:
        """
        Retourne les statistiques du cache.

        Returns:
            Dictionnaire contenant les statistiques
        """
        with self._lock:
            current_time = time.time()
            active_entries = sum(
                1
                for entry in self._cache.values()
                if not entry.get("expires_at") or current_time <= entry["expires_at"]
            )

            return {
                "total_entries": len(self._cache),
                "active_entries": active_entries,
                "expired_entries": len(self._cache) - active_entries,
                "max_size": self.max_size,
                "default_ttl": self.default_ttl,
                "memory_usage_estimate": len(str(self._cache)),
            }

    def __len__(self) -> int:
        """Retourne le nombre d'entrées actives dans le cache."""
        with self._lock:
            current_time = time.time()
            return sum(
                1
                for entry in self._cache.values()
                if not entry.get("expires_at") or current_time <= entry["expires_at"]
            )

    def __contains__(self, key: str) -> bool:
        """Vérifie si une clé existe dans le cache et n'a pas expiré."""
        return self.get(key) is not None


class RedisCacheManager(CacheManager):
    """
    Gestionnaire de cache avec support Redis optionnel.

    Utilise Redis si disponible, sinon fallback sur cache mémoire.
    """

    def __init__(
        self,
        default_ttl: int = 300,
        max_size: int = 1000,
        redis_url: str | None = None,
        redis_enabled: bool = True,
    ) -> None:
        """
        Initialise le gestionnaire de cache avec support Redis.

        Args:
            default_ttl: TTL par défaut en secondes
            max_size: Taille maximale du cache mémoire (fallback)
            redis_url: URL Redis (ex: redis://localhost:6379/0)
            redis_enabled: Activer Redis si disponible
        """
        # Initialiser le cache mémoire comme fallback
        super().__init__(default_ttl, max_size)

        self.redis_enabled = redis_enabled
        self.redis_url = redis_url or "redis://localhost:6379/0"
        self._redis_client: redis.Redis[bytes] | None = None
        self._redis_available = False

        # Essayer de se connecter à Redis si activé
        if self.redis_enabled:
            self._init_redis()

    def _init_redis(self) -> None:
        """Initialise la connexion Redis."""
        try:
            import redis

            # Parser l'URL Redis
            self._redis_client = redis.from_url(
                self.redis_url, decode_responses=False, socket_connect_timeout=2
            )

            # Tester la connexion
            if self._redis_client is not None:
                self._redis_client.ping()
                self._redis_available = True
                logger.info(f"✅ Redis connecté: {self.redis_url}")
            else:
                self._redis_available = False
        except ImportError:
            logger.debug("Redis non installé (pip install redis)")
            self._redis_available = False
            self._redis_client = None
        except Exception as e:
            logger.warning(f"⚠️ Redis indisponible, utilisation cache mémoire: {e}")
            self._redis_available = False
            if self._redis_client is not None:
                try:
                    self._redis_client.close()
                except Exception as e:
                    # Ignorer les erreurs de fermeture lors de l'initialisation
                    logger.debug(f"Erreur lors de la fermeture Redis: {e}")
            self._redis_client = None

    def _serialize_value(self, value: Any) -> bytes:
        """Sérialise une valeur pour Redis."""
        import json

        try:
            # Essayer JSON d'abord (plus rapide pour types simples)
            return json.dumps(value).encode("utf-8")
        except (TypeError, ValueError):
            # Essayer msgpack si disponible (plus sécurisé que pickle)
            try:
                import msgpack

                return msgpack.packb(value, use_bin_type=True)
            except ImportError:
                # Si msgpack n'est pas disponible, lever une exception
                # plutôt que d'utiliser pickle qui est dangereux
                raise CacheError(
                    "Impossible de sérialiser la valeur. "
                    "Installez msgpack (pip install msgpack) pour supporter les types complexes, "
                    "ou utilisez uniquement des types JSON-sérialisables."
                ) from None

    def _deserialize_value(self, data: bytes) -> Any:
        """Désérialise une valeur depuis Redis."""
        import json

        try:
            # Essayer JSON d'abord
            return json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Essayer msgpack si disponible (plus sécurisé que pickle)
            try:
                import msgpack

                return msgpack.unpackb(data, raw=False)
            except ImportError:
                # Si msgpack n'est pas disponible, lever une exception
                # plutôt que d'utiliser pickle qui est dangereux
                raise CacheError(
                    "Impossible de désérialiser la valeur. "
                    "Les données semblent avoir été sérialisées avec msgpack. "
                    "Installez msgpack (pip install msgpack) pour les désérialiser."
                ) from None

    def get(self, key: str) -> Any | None:
        """
        Récupère une valeur du cache (Redis ou mémoire).

        Args:
            key: Clé de la valeur

        Returns:
            Valeur mise en cache ou None si non trouvée/expirée
        """
        # Essayer Redis d'abord
        if self._redis_available and self._redis_client is not None:
            try:
                data = self._redis_client.get(key)
                if data is not None:
                    value = self._deserialize_value(data)
                    logger.debug(f"📥 Redis cache hit: {key}")
                    # Mettre aussi en cache mémoire pour accès rapide
                    super().set(key, value, ttl=self.default_ttl)
                    return value
            except Exception as e:
                logger.debug(f"Erreur Redis get, fallback mémoire: {e}")
                self._redis_available = False

        # Fallback sur cache mémoire
        return super().get(key)

    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """
        Définit une valeur dans le cache (Redis et mémoire).

        Args:
            key: Clé de la valeur
            value: Valeur à mettre en cache
            ttl: TTL en secondes (utilise le TTL par défaut si None)
        """
        ttl_to_use = ttl if ttl is not None else self.default_ttl

        # Mettre en cache mémoire (toujours)
        super().set(key, value, ttl=ttl_to_use)

        # Mettre aussi en Redis si disponible
        if self._redis_available and self._redis_client is not None:
            try:
                serialized = self._serialize_value(value)
                if ttl_to_use and ttl_to_use > 0:
                    self._redis_client.setex(key, ttl_to_use, serialized)
                else:
                    self._redis_client.set(key, serialized)
                logger.debug(f"📤 Redis cache set: {key} (TTL: {ttl_to_use}s)")
            except Exception as e:
                logger.debug(f"Erreur Redis set, fallback mémoire: {e}")
                self._redis_available = False

    def delete(self, key: str) -> bool:
        """
        Supprime une entrée du cache (Redis et mémoire).

        Args:
            key: Clé à supprimer

        Returns:
            True si l'entrée existait et a été supprimée
        """
        deleted_memory = super().delete(key)

        # Supprimer aussi de Redis si disponible
        if self._redis_available and self._redis_client is not None:
            try:
                deleted_redis = self._redis_client.delete(key) > 0
                return deleted_memory or deleted_redis
            except Exception as e:
                logger.debug(f"Erreur Redis delete: {e}")
                return deleted_memory

        return deleted_memory

    def clear(self) -> None:
        """Vide complètement le cache (Redis et mémoire)."""
        super().clear()

        # Vider aussi Redis si disponible
        if self._redis_available and self._redis_client is not None:
            try:
                self._redis_client.flushdb()
                logger.info("🧹 Redis cache vidé")
            except Exception as e:
                logger.warning(f"Erreur vidage Redis: {e}")

    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalide toutes les entrées correspondant à un pattern (Redis et mémoire).

        Args:
            pattern: Pattern à rechercher dans les clés

        Returns:
            Nombre d'entrées invalidées
        """
        count_memory = super().invalidate_pattern(pattern)

        # Invalider aussi dans Redis si disponible
        if self._redis_available and self._redis_client is not None:
            try:
                # Utiliser SCAN pour trouver les clés correspondant au pattern
                count_redis = 0
                cursor = 0
                while True:
                    cursor, keys = self._redis_client.scan(
                        cursor=cursor, match=f"*{pattern}*", count=100
                    )
                    if keys:
                        count_redis += self._redis_client.delete(*keys)
                    if cursor == 0:
                        break
                logger.debug(
                    f"🔄 Redis invalidation pattern '{pattern}': {count_redis} entrées"
                )
                return count_memory + count_redis
            except Exception as e:
                logger.debug(f"Erreur Redis invalidate_pattern: {e}")
                return count_memory

        return count_memory

    def get_stats(self) -> dict[str, Any]:
        """
        Retourne les statistiques du cache (Redis et mémoire).

        Returns:
            Dictionnaire contenant les statistiques
        """
        stats = super().get_stats()
        stats["redis_enabled"] = self.redis_enabled
        stats["redis_available"] = self._redis_available

        if self._redis_available and self._redis_client is not None:
            try:
                info = self._redis_client.info("memory")
                stats["redis_memory_used"] = info.get("used_memory_human", "N/A")
                stats["redis_keys"] = self._redis_client.dbsize()
            except Exception as e:
                logger.debug(f"Erreur stats Redis: {e}")

        return stats

    def __del__(self) -> None:
        """Ferme la connexion Redis à la destruction."""
        if self._redis_client is not None:
            try:
                self._redis_client.close()
            except Exception as e:
                # Ignorer les erreurs de fermeture lors de la destruction
                logger.debug(f"Erreur lors de la fermeture Redis: {e}")
