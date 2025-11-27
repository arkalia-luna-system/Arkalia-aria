"""
ARKALIA ARIA - Module Alertes
=============================

Module pour le système d'alertes automatiques.
"""

from core.alerts import (
    AlertSeverity,
    AlertType,
    ARIA_AlertsSystem,
    get_alerts_system,
)

__all__ = [
    "ARIA_AlertsSystem",
    "AlertSeverity",
    "AlertType",
    "get_alerts_system",
]
