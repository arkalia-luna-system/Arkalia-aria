#!/usr/bin/env python3
"""
ARKALIA ARIA - Validateur de Métriques
====================================

Validateur de métriques ARIA avec vérifications de cohérence,
qualité et alertes automatiques.
"""

from datetime import datetime
from typing import Any


class ARIA_MetricsValidator:
    """
    Validateur de métriques ARIA.

    Effectue des vérifications de cohérence et qualité :
    - Validation des métriques collectées
    - Détection d'anomalies
    - Alertes automatiques
    - Recommandations d'amélioration
    """

    def __init__(self) -> None:
        """Initialise le validateur de métriques."""
        self.validation_rules = self._initialize_validation_rules()
        self.alerts: list[dict[str, Any]] = []
        self.recommendations: list[dict[str, Any]] = []

    def validate_metrics(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """
        Valide les métriques collectées.

        Args:
            metrics: Métriques à valider

        Returns:
            Dict contenant les résultats de validation
        """
        self.alerts = []
        self.recommendations = []

        validation_results = {
            "is_valid": True,
            "score": 0,
            "alerts": [],
            "recommendations": [],
            "timestamp": datetime.now().isoformat(),
        }

        # Validation des métriques générales
        self._validate_general_metrics(metrics)

        # Validation des métriques ARIA spécifiques
        self._validate_aria_metrics(metrics)

        # Validation de la sécurité
        self._validate_security_metrics(metrics)

        # Validation des performances
        self._validate_performance_metrics(metrics)

        # Validation des tests
        self._validate_test_metrics(metrics)

        # Calcul du score global
        validation_results["score"] = self._calculate_validation_score(metrics)
        validation_results["is_valid"] = len(self.alerts) == 0
        validation_results["alerts"] = self.alerts
        validation_results["recommendations"] = self.recommendations

        return validation_results

    def _initialize_validation_rules(self) -> dict[str, Any]:
        """Initialise les règles de validation."""
        return {
            "min_python_files": 10,
            "min_test_coverage": 70.0,
            "max_security_issues": 5,
            "max_memory_usage_mb": 1000,
            "max_cpu_percent": 80.0,
            "min_documentation_files": 5,
            "required_api_endpoints": 5,
        }

    def _validate_general_metrics(self, metrics: dict[str, Any]) -> None:
        """Valide les métriques générales."""
        python_files = metrics.get("python_files", {})

        # Vérification du nombre minimum de fichiers Python
        if python_files.get("count", 0) < self.validation_rules["min_python_files"]:
            self.alerts.append(
                {
                    "type": "warning",
                    "category": "general",
                    "message": (
                        f"Nombre de fichiers Python insuffisant ({python_files.get('count', 0)} < {self.validation_rules['min_python_files']})"
                    ),
                    "severity": "medium",
                }
            )
            self.recommendations.append(
                {
                    "category": "general",
                    "message": (
                        "Ajouter plus de modules Python pour améliorer la structure du projet"
                    ),
                    "priority": "medium",
                }
            )

        # Vérification de la documentation
        doc_files = metrics.get("documentation", {})
        if (
            doc_files.get("markdown_files", 0)
            < self.validation_rules["min_documentation_files"]
        ):
            self.alerts.append(
                {
                    "type": "warning",
                    "category": "documentation",
                    "message": (
                        f"Documentation insuffisante ({doc_files.get('markdown_files', 0)} fichiers)"
                    ),
                    "severity": "low",
                }
            )
            self.recommendations.append(
                {
                    "category": "documentation",
                    "message": (
                        "Améliorer la documentation avec plus de fichiers Markdown"
                    ),
                    "priority": "low",
                }
            )

    def _validate_aria_metrics(self, metrics: dict[str, Any]) -> None:
        """Valide les métriques spécifiques à ARIA."""
        aria_specific = metrics.get("aria_specific", {})

        # Vérification de l'intégration CIA
        cia_integration = aria_specific.get("cia_integration", {})
        if not cia_integration.get("cia_sync_exists", False):
            self.alerts.append(
                {
                    "type": "error",
                    "category": "aria_integration",
                    "message": "Intégration CIA non configurée",
                    "severity": "high",
                }
            )
            self.recommendations.append(
                {
                    "category": "aria_integration",
                    "message": (
                        "Configurer l'intégration CIA pour la synchronisation des données"
                    ),
                    "priority": "high",
                }
            )

        # Vérification des modèles ML
        ml_models = metrics.get("ml_models", {})
        if not ml_models.get("prediction_engine_status", False):
            self.alerts.append(
                {
                    "type": "warning",
                    "category": "ml_models",
                    "message": "Moteur de prédiction non actif",
                    "severity": "medium",
                }
            )
            self.recommendations.append(
                {
                    "category": "ml_models",
                    "message": (
                        "Activer le moteur de prédiction pour les analyses avancées"
                    ),
                    "priority": "medium",
                }
            )

    def _validate_security_metrics(self, metrics: dict[str, Any]) -> None:
        """Valide les métriques de sécurité."""
        security = metrics.get("security", {})

        # Vérification des issues Bandit
        bandit_scan = security.get("bandit_scan", {})
        issues_found = bandit_scan.get("issues_found", 0)

        if issues_found > self.validation_rules["max_security_issues"]:
            self.alerts.append(
                {
                    "type": "error",
                    "category": "security",
                    "message": f"Trop d'issues de sécurité détectées ({issues_found})",
                    "severity": "high",
                }
            )
            self.recommendations.append(
                {
                    "category": "security",
                    "message": "Corriger les issues de sécurité détectées par Bandit",
                    "priority": "high",
                }
            )

        # Vérification des vulnérabilités Safety
        safety_scan = security.get("safety_scan", {})
        vulnerabilities = safety_scan.get("vulnerabilities_found", 0)

        if vulnerabilities > 0:
            self.alerts.append(
                {
                    "type": "error",
                    "category": "security",
                    "message": (
                        f"Vulnérabilités détectées dans les dépendances ({vulnerabilities})"
                    ),
                    "severity": "high",
                }
            )
            self.recommendations.append(
                {
                    "category": "security",
                    "message": "Mettre à jour les dépendances vulnérables",
                    "priority": "high",
                }
            )

    def _validate_performance_metrics(self, metrics: dict[str, Any]) -> None:
        """Valide les métriques de performance."""
        performance = metrics.get("performance", {})

        # Vérification de l'utilisation mémoire
        memory_usage = performance.get("memory_usage_mb", 0)
        if memory_usage > self.validation_rules["max_memory_usage_mb"]:
            self.alerts.append(
                {
                    "type": "warning",
                    "category": "performance",
                    "message": f"Utilisation mémoire élevée ({memory_usage:.1f} MB)",
                    "severity": "medium",
                }
            )
            self.recommendations.append(
                {
                    "category": "performance",
                    "message": "Optimiser l'utilisation mémoire du système",
                    "priority": "medium",
                }
            )

        # Vérification de l'utilisation CPU
        cpu_percent = performance.get("cpu_percent", 0)
        if cpu_percent > self.validation_rules["max_cpu_percent"]:
            self.alerts.append(
                {
                    "type": "warning",
                    "category": "performance",
                    "message": f"Utilisation CPU élevée ({cpu_percent:.1f}%)",
                    "severity": "medium",
                }
            )
            self.recommendations.append(
                {
                    "category": "performance",
                    "message": "Optimiser les performances CPU",
                    "priority": "medium",
                }
            )

    def _validate_test_metrics(self, metrics: dict[str, Any]) -> None:
        """Valide les métriques de tests."""
        tests = metrics.get("tests", {})

        # Vérification de la couverture de tests
        coverage = tests.get("coverage_percentage", 0)
        if coverage < self.validation_rules["min_test_coverage"]:
            self.alerts.append(
                {
                    "type": "warning",
                    "category": "tests",
                    "message": (
                        f"Couverture de tests insuffisante ({coverage:.1f}% < {self.validation_rules['min_test_coverage']}%)"
                    ),
                    "severity": "medium",
                }
            )
            self.recommendations.append(
                {
                    "category": "tests",
                    "message": "Améliorer la couverture de tests",
                    "priority": "medium",
                }
            )

        # Vérification du nombre de tests
        test_files = tests.get("test_files_count", 0)
        if test_files == 0:
            self.alerts.append(
                {
                    "type": "error",
                    "category": "tests",
                    "message": "Aucun fichier de test trouvé",
                    "severity": "high",
                }
            )
            self.recommendations.append(
                {
                    "category": "tests",
                    "message": "Ajouter des tests pour assurer la qualité du code",
                    "priority": "high",
                }
            )

    def _calculate_validation_score(self, metrics: dict[str, Any]) -> int:
        """Calcule un score de validation global."""
        score = 100

        # Pénalités pour les alertes
        for alert in self.alerts:
            severity = alert.get("severity", "low")
            if severity == "high":
                score -= 20
            elif severity == "medium":
                score -= 10
            elif severity == "low":
                score -= 5

        # Bonus pour les bonnes pratiques
        python_files = metrics.get("python_files", {})
        if python_files.get("count", 0) > 20:
            score += 5

        tests = metrics.get("tests", {})
        if tests.get("coverage_percentage", 0) > 80:
            score += 10

        security = metrics.get("security", {})
        if security.get("bandit_scan", {}).get("issues_found", 0) == 0:
            score += 10

        return max(0, min(100, score))

    def get_health_status(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """
        Détermine le statut de santé global du projet.

        Args:
            metrics: Métriques du projet

        Returns:
            Dict contenant le statut de santé
        """
        validation_results = self.validate_metrics(metrics)
        score = validation_results["score"]

        if score >= 90:
            status = "excellent"
            color = "green"
        elif score >= 75:
            status = "good"
            color = "blue"
        elif score >= 60:
            status = "fair"
            color = "yellow"
        else:
            status = "poor"
            color = "red"

        return {
            "status": status,
            "color": color,
            "score": score,
            "alerts_count": len(self.alerts),
            "recommendations_count": len(self.recommendations),
            "timestamp": datetime.now().isoformat(),
        }
