#!/usr/bin/env python3
"""
ARKALIA ARIA - Système de Métriques Avancé
==========================================

Système de collecte de métriques professionnel intégré à ARIA.
Collecte automatique de métriques sur la qualité du code, les tests,
la sécurité et les performances.

Usage:
    from metrics_collector import ARIA_MetricsCollector

    collector = ARIA_MetricsCollector()
    metrics = collector.collect_all_metrics()
    print(f"Fichiers Python: {metrics['python_files']['count']}")

Classes principales:
    - ARIA_MetricsCollector: Collecte des métriques ARIA
    - ARIA_MetricsExporter: Export des métriques en différents formats
    - ARIA_MetricsValidator: Validation des métriques collectées
    - ARIA_MetricsDashboard: Dashboard web interactif
"""

__version__ = "1.0.0"
__author__ = "Arkalia Luna System"
__email__ = "arkalia.luna.system@gmail.com"
__license__ = "MIT"

from .collectors.aria_metrics_collector import ARIA_MetricsCollector
from .dashboard.aria_metrics_dashboard import ARIA_MetricsDashboard
from .exporters.aria_metrics_exporter import ARIA_MetricsExporter
from .validators.aria_metrics_validator import ARIA_MetricsValidator

__all__ = [
    "ARIA_MetricsCollector",
    "ARIA_MetricsExporter",
    "ARIA_MetricsValidator",
    "ARIA_MetricsDashboard",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
