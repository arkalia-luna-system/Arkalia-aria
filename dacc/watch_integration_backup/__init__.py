"""
ARKALIA ARIA - Connecteurs Santé
===============================

Module de connecteurs santé pour intégration avec :
- Samsung Health
- Google Fit
- Apple HealthKit

Fournit une interface unifiée pour la synchronisation des données de santé.
"""

from .base_connector import BaseHealthConnector
from .data_models import (
    ActivityData,
    HealthData,
    SleepData,
    StressData,
    UnifiedHealthMetrics,
)
from .google_fit_connector import GoogleFitConnector
from .ios_health_connector import IOSHealthConnector
from .samsung_health_connector import SamsungHealthConnector
from .sync_manager import HealthSyncManager

__all__ = [
    "BaseHealthConnector",
    "HealthData",
    "ActivityData",
    "SleepData",
    "StressData",
    "UnifiedHealthMetrics",
    "HealthSyncManager",
    "SamsungHealthConnector",
    "GoogleFitConnector",
    "IOSHealthConnector",
]
