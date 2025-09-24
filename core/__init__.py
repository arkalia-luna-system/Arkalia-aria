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

from .cache import CacheManager
from .config import Config
from .database import DatabaseManager
from .exceptions import APIError, ARIABaseException, DatabaseError
from .logging import setup_logging

__all__ = [
    "DatabaseManager",
    "Config",
    "setup_logging",
    "CacheManager",
    "ARIABaseException",
    "DatabaseError",
    "APIError",
]
