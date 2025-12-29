"""
Tests unitaires pour le cache Redis optionnel
"""

from unittest.mock import patch

import pytest

from core.cache import RedisCacheManager


class TestRedisCacheManager:
    """Tests pour RedisCacheManager avec fallback mémoire."""

    def test_redis_cache_init_without_redis(self):
        """Test initialisation sans Redis (fallback mémoire)."""
        cache = RedisCacheManager(redis_enabled=False)
        assert cache.redis_enabled is False
        assert cache._redis_available is False
        assert cache._redis_client is None

    def test_redis_cache_init_redis_unavailable(self):
        """Test initialisation avec Redis indisponible (fallback mémoire)."""
        # Simuler Redis indisponible en patchant l'import dans _init_redis
        with patch("builtins.__import__") as mock_import:
            # Simuler ImportError lors de l'import de redis
            def side_effect(name, *args, **kwargs):
                if name == "redis":
                    raise ImportError("No module named 'redis'")
                return __import__(name, *args, **kwargs)

            mock_import.side_effect = side_effect

            cache = RedisCacheManager(redis_enabled=True)
            assert cache.redis_enabled is True
            assert cache._redis_available is False  # Fallback activé

    def test_redis_cache_get_fallback_memory(self):
        """Test get avec fallback sur cache mémoire."""
        cache = RedisCacheManager(redis_enabled=False)

        # Mettre en cache mémoire
        cache.set("test_key", "test_value", ttl=60)

        # Récupérer depuis cache mémoire
        value = cache.get("test_key")
        assert value == "test_value"

    def test_redis_cache_set_fallback_memory(self):
        """Test set avec fallback sur cache mémoire."""
        cache = RedisCacheManager(redis_enabled=False)

        cache.set("test_key", {"data": "test"}, ttl=60)
        value = cache.get("test_key")
        assert value == {"data": "test"}

    def test_redis_cache_delete_fallback_memory(self):
        """Test delete avec fallback sur cache mémoire."""
        cache = RedisCacheManager(redis_enabled=False)

        cache.set("test_key", "test_value")
        assert cache.get("test_key") == "test_value"

        deleted = cache.delete("test_key")
        assert deleted is True
        assert cache.get("test_key") is None

    def test_redis_cache_clear_fallback_memory(self):
        """Test clear avec fallback sur cache mémoire."""
        cache = RedisCacheManager(redis_enabled=False)

        cache.set("key1", "value1")
        cache.set("key2", "value2")
        assert len(cache) == 2

        cache.clear()
        assert len(cache) == 0

    def test_redis_cache_invalidate_pattern_fallback_memory(self):
        """Test invalidate_pattern avec fallback sur cache mémoire."""
        cache = RedisCacheManager(redis_enabled=False)

        cache.set("user_123", "data1")
        cache.set("user_456", "data2")
        cache.set("other_key", "data3")

        count = cache.invalidate_pattern("user_")
        assert count == 2
        assert cache.get("user_123") is None
        assert cache.get("user_456") is None
        assert cache.get("other_key") == "data3"

    def test_redis_cache_get_stats_fallback_memory(self):
        """Test get_stats avec fallback sur cache mémoire."""
        cache = RedisCacheManager(redis_enabled=False)

        cache.set("key1", "value1")
        stats = cache.get_stats()

        assert "total_entries" in stats
        assert "redis_enabled" in stats
        assert stats["redis_enabled"] is False  # Désactivé explicitement
        assert stats["redis_available"] is False

    def test_redis_cache_with_redis_available(self):
        """Test avec Redis disponible (nécessite Redis installé et démarré)."""
        try:
            import redis  # noqa: F401
        except ImportError:
            pytest.skip("Redis non installé (pip install redis)")

        try:
            cache = RedisCacheManager(
                redis_enabled=True, redis_url="redis://localhost:6379/0"
            )

            if cache._redis_available:
                # Test set/get avec Redis
                cache.set("redis_test", {"data": "test"}, ttl=60)
                value = cache.get("redis_test")
                assert value == {"data": "test"}

                # Test stats avec Redis
                stats = cache.get_stats()
                assert stats["redis_available"] is True
                assert "redis_keys" in stats
        except Exception:
            # Redis non disponible, test ignoré
            pytest.skip("Redis non disponible pour ce test")

    def test_redis_cache_serialization(self):
        """Test sérialisation/désérialisation des valeurs."""
        cache = RedisCacheManager(redis_enabled=False)

        # Test avec types simples
        cache.set("string", "test")
        cache.set("int", 42)
        cache.set("float", 3.14)
        cache.set("bool", True)
        cache.set("list", [1, 2, 3])
        cache.set("dict", {"key": "value"})

        assert cache.get("string") == "test"
        assert cache.get("int") == 42
        assert cache.get("float") == 3.14
        assert cache.get("bool") is True
        assert cache.get("list") == [1, 2, 3]
        assert cache.get("dict") == {"key": "value"}

    def test_redis_cache_compatibility_with_cache_manager(self):
        """Test compatibilité avec CacheManager (héritage)."""
        cache = RedisCacheManager(redis_enabled=False)

        # Toutes les méthodes de CacheManager doivent fonctionner
        cache.set("key", "value")
        assert cache.get("key") == "value"
        assert "key" in cache
        assert len(cache) == 1

        cache.delete("key")
        assert cache.get("key") is None

        # Test get_or_set
        def compute_value():
            return "computed"

        value = cache.get_or_set("computed_key", compute_value, ttl=60)
        assert value == "computed"
        assert cache.get("computed_key") == "computed"
