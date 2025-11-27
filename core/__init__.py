"""
ARKALIA ARIA - Core Module
==========================

Module central contenant les abstractions communes :
- Gestionnaire de base de données
- Configuration centralisée
- Logging unifié
- Gestionnaire de cache
- Exceptions personnalisées
"""

from .alerts import AlertSeverity, AlertType, ARIA_AlertsSystem, get_alerts_system
from .api_base import BaseAPI
from .cache import CacheManager
from .config import Config
from .database import DatabaseManager
from .exceptions import APIError, ARIABaseException, DatabaseError
from .logging import get_logger, setup_logging

__all__ = [
    "ARIA_AlertsSystem",
    "AlertSeverity",
    "AlertType",
    "get_alerts_system",
    "BaseAPI",
    "DatabaseManager",
    "Config",
    "setup_logging",
    "get_logger",
    "CacheManager",
    "ARIABaseException",
    "DatabaseError",
    "APIError",
]
