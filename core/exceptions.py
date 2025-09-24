#!/usr/bin/env python3
"""
ARKALIA ARIA - Exceptions Personnalisées
========================================

Exceptions centralisées pour une gestion d'erreurs cohérente
à travers tout le projet ARKALIA ARIA.
"""


class ARIABaseException(Exception):
    """
    Exception de base pour toutes les erreurs ARIA.

    Toutes les exceptions personnalisées héritent de cette classe
    pour permettre une gestion centralisée des erreurs.
    """

    def __init__(self, message: str, error_code: str = "ARIA_ERROR") -> None:
        """
        Initialise l'exception ARIA.

        Args:
            message: Message d'erreur descriptif
            error_code: Code d'erreur pour identification
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class DatabaseError(ARIABaseException):
    """
    Exception pour les erreurs de base de données.

    Levée lors de problèmes de connexion, requêtes SQL,
    ou opérations de base de données.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, "DATABASE_ERROR")


class APIError(ARIABaseException):
    """
    Exception pour les erreurs d'API.

    Levée lors de problèmes de validation, authentification,
    ou traitement des requêtes API.
    """

    def __init__(self, message: str, status_code: int = 500) -> None:
        """
        Initialise l'erreur API.

        Args:
            message: Message d'erreur
            status_code: Code de statut HTTP
        """
        super().__init__(message, "API_ERROR")
        self.status_code = status_code


class ValidationError(ARIABaseException):
    """
    Exception pour les erreurs de validation.

    Levée lors de problèmes de validation des données
    d'entrée ou de format.
    """

    def __init__(self, message: str, field: str = None) -> None:
        """
        Initialise l'erreur de validation.

        Args:
            message: Message d'erreur
            field: Champ qui a échoué à la validation
        """
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field


class ConfigurationError(ARIABaseException):
    """
    Exception pour les erreurs de configuration.

    Levée lors de problèmes de configuration,
    variables d'environnement manquantes, etc.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, "CONFIGURATION_ERROR")


class CacheError(ARIABaseException):
    """
    Exception pour les erreurs de cache.

    Levée lors de problèmes d'opérations de cache,
    invalidation, ou récupération de données.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, "CACHE_ERROR")


class HealthConnectorError(ARIABaseException):
    """
    Exception pour les erreurs de connecteurs santé.

    Levée lors de problèmes de connexion ou synchronisation
    avec les services de santé externes.
    """

    def __init__(self, message: str, connector_name: str = None) -> None:
        """
        Initialise l'erreur de connecteur.

        Args:
            message: Message d'erreur
            connector_name: Nom du connecteur qui a échoué
        """
        super().__init__(message, "HEALTH_CONNECTOR_ERROR")
        self.connector_name = connector_name


class MetricsError(ARIABaseException):
    """
    Exception pour les erreurs de métriques.

    Levée lors de problèmes de collecte, traitement,
    ou export de métriques.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message, "METRICS_ERROR")
