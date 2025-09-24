#!/usr/bin/env python3
"""
ARKALIA ARIA - Configuration de Logging
=======================================

Configuration centralisée du système de logging avec formatage
et gestion des handlers.
"""

import logging
import logging.handlers
import sys
from pathlib import Path

from .config import config
from .exceptions import ConfigurationError


def setup_logging(
    level: str | None = None,
    log_file: str | None = None,
    log_format: str | None = None,
) -> None:
    """
    Configure le système de logging pour ARKALIA ARIA.

    Args:
        level: Niveau de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Fichier de log (utilise la config si None)
        log_format: Format des logs (utilise la config si None)

    Raises:
        ConfigurationError: Si la configuration est invalide
    """
    # Utiliser les valeurs de configuration si non spécifiées
    level = level or config.get_log_level()
    log_file = log_file or config.get("log_file", "aria.log")
    log_format = log_format or config.get("log_format")

    # Valider le niveau de logging
    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if level.upper() not in valid_levels:
        raise ConfigurationError(f"Niveau de log invalide: {level}")

    # Créer le répertoire de logs si nécessaire
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configuration du logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[
            # Handler pour la console
            logging.StreamHandler(sys.stdout),
            # Handler pour le fichier avec rotation
            logging.handlers.RotatingFileHandler(
                log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
            ),
        ],
        force=True,  # Forcer la reconfiguration
    )

    # Configuration spécifique pour les loggers ARIA
    _configure_aria_loggers()

    # Log de démarrage
    logger = logging.getLogger(__name__)
    logger.info(f"📝 Logging configuré - Niveau: {level}, Fichier: {log_file}")


def _configure_aria_loggers() -> None:
    """Configure les loggers spécifiques à ARIA."""
    # Logger principal ARIA
    aria_logger = logging.getLogger("arkalia_aria")
    aria_logger.setLevel(logging.DEBUG)

    # Logger pour les APIs
    api_logger = logging.getLogger("arkalia_aria.api")
    api_logger.setLevel(logging.INFO)

    # Logger pour les connecteurs santé
    health_logger = logging.getLogger("arkalia_aria.health")
    health_logger.setLevel(logging.INFO)

    # Logger pour les métriques
    metrics_logger = logging.getLogger("arkalia_aria.metrics")
    metrics_logger.setLevel(logging.DEBUG)

    # Logger pour la base de données
    db_logger = logging.getLogger("arkalia_aria.database")
    db_logger.setLevel(logging.WARNING)  # Moins verbeux pour la DB

    # Logger pour le cache
    cache_logger = logging.getLogger("arkalia_aria.cache")
    cache_logger.setLevel(logging.DEBUG)


def get_logger(name: str) -> logging.Logger:
    """
    Récupère un logger avec le préfixe ARIA.

    Args:
        name: Nom du logger (sans préfixe arkalia_aria)

    Returns:
        Logger configuré
    """
    if not name.startswith("arkalia_aria"):
        name = f"arkalia_aria.{name}"

    return logging.getLogger(name)


def log_function_call(func_name: str, **kwargs) -> None:
    """
    Log une fonction appelée avec ses paramètres.

    Args:
        func_name: Nom de la fonction
        **kwargs: Paramètres de la fonction
    """
    logger = get_logger("function_calls")
    params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.debug(f"🔧 {func_name}({params})")


def log_performance(operation: str, duration: float, **metadata) -> None:
    """
    Log les performances d'une opération.

    Args:
        operation: Nom de l'opération
        duration: Durée en secondes
        **metadata: Métadonnées supplémentaires
    """
    logger = get_logger("performance")

    # Déterminer le niveau selon la durée
    if duration < 0.1:
        level = logging.DEBUG
    elif duration < 1.0:
        level = logging.INFO
    elif duration < 5.0:
        level = logging.WARNING
    else:
        level = logging.ERROR

    meta_str = ", ".join(f"{k}={v}" for k, v in metadata.items())
    message = f"⏱️ {operation}: {duration:.3f}s"
    if meta_str:
        message += f" ({meta_str})"

    logger.log(level, message)


def log_error(error: Exception, context: str = "", **metadata) -> None:
    """
    Log une erreur avec contexte et métadonnées.

    Args:
        error: Exception à logger
        context: Contexte de l'erreur
        **metadata: Métadonnées supplémentaires
    """
    logger = get_logger("errors")

    meta_str = ", ".join(f"{k}={v}" for k, v in metadata.items())
    message = f"❌ {context}: {type(error).__name__}: {str(error)}"
    if meta_str:
        message += f" ({meta_str})"

    logger.error(message, exc_info=True)


def log_security(event: str, **metadata) -> None:
    """
    Log un événement de sécurité.

    Args:
        event: Description de l'événement
        **metadata: Métadonnées supplémentaires
    """
    logger = get_logger("security")

    meta_str = ", ".join(f"{k}={v}" for k, v in metadata.items())
    message = f"🔒 {event}"
    if meta_str:
        message += f" ({meta_str})"

    logger.warning(message)


def log_api_request(
    method: str, endpoint: str, status_code: int, duration: float
) -> None:
    """
    Log une requête API.

    Args:
        method: Méthode HTTP
        endpoint: Endpoint appelé
        status_code: Code de statut de la réponse
        duration: Durée de la requête en secondes
    """
    logger = get_logger("api")

    # Déterminer le niveau selon le code de statut
    if 200 <= status_code < 300:
        level = logging.INFO
    elif 400 <= status_code < 500:
        level = logging.WARNING
    else:
        level = logging.ERROR

    # Déterminer l'emoji selon le statut
    if 200 <= status_code < 300:
        emoji = "✅"
    elif 400 <= status_code < 500:
        emoji = "⚠️"
    else:
        emoji = "❌"

    message = f"{emoji} {method} {endpoint} -> {status_code} ({duration:.3f}s)"
    logger.log(level, message)


def log_database_operation(
    operation: str, table: str, duration: float, rows_affected: int = 0
) -> None:
    """
    Log une opération de base de données.

    Args:
        operation: Type d'opération (SELECT, INSERT, UPDATE, DELETE)
        table: Nom de la table
        duration: Durée de l'opération en secondes
        rows_affected: Nombre de lignes affectées
    """
    logger = get_logger("database")

    message = f"🗄️ {operation} {table}"
    if rows_affected > 0:
        message += f" ({rows_affected} lignes)"
    message += f" ({duration:.3f}s)"

    # Log seulement si l'opération prend du temps ou affecte beaucoup de lignes
    if duration > 0.1 or rows_affected > 100:
        logger.info(message)
    else:
        logger.debug(message)
