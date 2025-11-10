#!/usr/bin/env python3
"""
ARKALIA ARIA - Configuration Centralisée
========================================

Configuration centralisée du projet avec gestion des variables d'environnement
et validation des paramètres.
"""

import os
from pathlib import Path
from typing import Any

from .exceptions import ConfigurationError


class Config:
    """
    Configuration centralisée du projet ARKALIA ARIA.

    Gère toutes les variables de configuration avec des valeurs par défaut
    et validation des paramètres critiques.
    """

    def __init__(self) -> None:
        """Initialise la configuration avec les valeurs par défaut."""
        self._config: dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Charge la configuration depuis les variables d'environnement."""
        # Configuration de base de données
        self._config["db_path"] = os.getenv("ARIA_DB_PATH", "aria_pain.db")
        self._config["db_backup_path"] = os.getenv(
            "ARIA_DB_BACKUP_PATH", "aria_pain_backup.db"
        )

        # Configuration API
        self._config["api_host"] = os.getenv("ARIA_API_HOST", "127.0.0.1")
        self._config["api_port"] = int(os.getenv("ARIA_API_PORT", "8001"))
        self._config["api_workers"] = int(os.getenv("ARIA_API_WORKERS", "1"))

        # Configuration de cache
        self._config["cache_ttl"] = int(os.getenv("ARIA_CACHE_TTL", "300"))
        self._config["cache_max_size"] = int(os.getenv("ARIA_CACHE_MAX_SIZE", "1000"))

        # Configuration de logging
        self._config["log_level"] = os.getenv("ARIA_LOG_LEVEL", "INFO")
        self._config["log_file"] = os.getenv("ARIA_LOG_FILE", "aria.log")
        self._config["log_format"] = os.getenv(
            "ARIA_LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Configuration des métriques
        self._config["metrics_perf_ttl"] = float(
            os.getenv("ARIA_METRICS_PERF_TTL", "5.0")
        )
        self._config["metrics_fast_mode"] = os.getenv("ARIA_METRICS_FAST", "0") == "1"

        # Configuration des connecteurs santé
        self._config["samsung_health_enabled"] = (
            os.getenv("SAMSUNG_HEALTH_ENABLED", "1") == "1"
        )
        self._config["google_fit_enabled"] = os.getenv("GOOGLE_FIT_ENABLED", "1") == "1"
        self._config["ios_health_enabled"] = os.getenv("IOS_HEALTH_ENABLED", "1") == "1"

        # Configuration de sécurité
        self._config["cors_origins"] = os.getenv("ARIA_CORS_ORIGINS", "*").split(",")
        self._config["max_request_size"] = int(
            os.getenv("ARIA_MAX_REQUEST_SIZE", "10485760")
        )  # 10MB

        # Configuration de l'application mobile
        self._config["mobile_app_enabled"] = (
            os.getenv("ARIA_MOBILE_APP_ENABLED", "1") == "1"
        )
        self._config["mobile_api_key"] = os.getenv("ARIA_MOBILE_API_KEY", "")

        # Configuration CIA Sync
        self._config["cia_sync_enabled"] = (
            os.getenv("ARIA_CIA_SYNC_ENABLED", "0") == "1"
        )
        self._config["cia_api_url"] = os.getenv("CIA_API_URL", "http://localhost:8000")
        self._config["cia_api_key"] = os.getenv("CIA_API_KEY", "")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Récupère une valeur de configuration.

        Args:
            key: Clé de configuration
            default: Valeur par défaut si la clé n'existe pas

        Returns:
            Valeur de configuration
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Définit une valeur de configuration.

        Args:
            key: Clé de configuration
            value: Valeur à définir
        """
        self._config[key] = value

    def get_db_path(self) -> Path:
        """
        Récupère le chemin de la base de données.

        Returns:
            Chemin vers la base de données

        Raises:
            ConfigurationError: Si le chemin n'est pas valide
        """
        db_path = Path(self._config["db_path"])
        if not db_path.parent.exists():
            try:
                db_path.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise ConfigurationError(
                    f"Impossible de créer le répertoire de la base: {e}"
                ) from e
        return db_path

    def get_log_level(self) -> str:
        """
        Récupère le niveau de logging.

        Returns:
            Niveau de logging

        Raises:
            ConfigurationError: Si le niveau n'est pas valide
        """
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        level = self._config["log_level"].upper()
        if level not in valid_levels:
            raise ConfigurationError(
                f"Niveau de log invalide: {level}. Valeurs valides: {valid_levels}"
            )
        return level

    def validate(self) -> None:
        """
        Valide la configuration.

        Raises:
            ConfigurationError: Si la configuration est invalide
        """
        # Valider le port API
        port = self._config["api_port"]
        if not (1 <= port <= 65535):
            raise ConfigurationError(f"Port API invalide: {port}")

        # Valider le TTL du cache
        cache_ttl = self._config["cache_ttl"]
        if cache_ttl < 0:
            raise ConfigurationError(f"TTL du cache invalide: {cache_ttl}")

        # Valider la taille maximale des requêtes
        max_size = self._config["max_request_size"]
        if max_size < 1024:  # Au moins 1KB
            raise ConfigurationError(
                f"Taille maximale des requêtes trop petite: {max_size}"
            )

        # Valider le chemin de la base de données
        self.get_db_path()

        # Valider le niveau de logging
        self.get_log_level()

    def to_dict(self) -> dict[str, Any]:
        """
        Retourne la configuration sous forme de dictionnaire.

        Returns:
            Dictionnaire de configuration
        """
        return self._config.copy()

    def __getitem__(self, key: str) -> Any:
        """Permet l'accès par clé avec config[key]."""
        return self._config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Permet la définition par clé avec config[key] = value."""
        self._config[key] = value

    def __contains__(self, key: str) -> bool:
        """Permet de vérifier l'existence d'une clé avec 'key in config'."""
        return key in self._config


# Instance globale de configuration
config = Config()
