#!/usr/bin/env python3
"""
ARKALIA ARIA - DevOps Automation
===============================

Système DevOps automatisé intégré à ARIA basé sur athalia-dev-setup.
Fournit des outils de sécurité, validation, CI/CD et automatisation.

Modules principaux:
    - ARIA_SecurityValidator: Validation sécurisée des commandes
    - ARIA_CICDManager: Gestionnaire CI/CD automatisé
    - ARIA_QualityAssurance: Assurance qualité automatisée
    - ARIA_DeploymentManager: Gestionnaire de déploiement
    - ARIA_MonitoringSystem: Système de monitoring
"""

__version__ = "1.0.0"
__author__ = "Arkalia Luna System"
__email__ = "contact@arkalia-luna.com"
__license__ = "MIT"

from .cicd.aria_cicd_manager import ARIA_CICDManager
from .deployment.aria_deployment_manager import ARIA_DeploymentManager
from .monitoring.aria_monitoring_system import ARIA_MonitoringSystem
from .quality.aria_quality_assurance import ARIA_QualityAssurance
from .security.aria_security_validator import ARIA_SecurityValidator

__all__ = [
    "ARIA_SecurityValidator",
    "ARIA_CICDManager",
    "ARIA_QualityAssurance",
    "ARIA_DeploymentManager",
    "ARIA_MonitoringSystem",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
