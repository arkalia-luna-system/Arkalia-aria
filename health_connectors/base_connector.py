"""
ARKALIA ARIA - Connecteur Santé de Base
=======================================

Classe abstraite commune pour tous les connecteurs santé.
Définit l'interface standardisée pour la synchronisation des données.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any

from .data_models import ActivityData, HealthData, SleepData, StressData


class BaseHealthConnector(ABC):
    """
    Classe abstraite pour les connecteurs santé.

    Tous les connecteurs doivent implémenter cette interface
    pour assurer la compatibilité avec le système ARIA.
    """

    def __init__(self, connector_name: str) -> None:
        """
        Initialise le connecteur.

        Args:
            connector_name: Nom du connecteur (ex: "samsung_health")
        """
        self.connector_name = connector_name
        self.is_connected = False
        self.last_sync: datetime | None = None
        self.sync_errors: list[str] = []

    @abstractmethod
    async def connect(self) -> bool:
        """
        Établit la connexion avec le service de santé.

        Returns:
            True si la connexion est établie, False sinon
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Ferme la connexion avec le service de santé."""
        pass

    @abstractmethod
    async def get_activity_data(
        self, start_date: datetime, end_date: datetime
    ) -> list[ActivityData]:
        """
        Récupère les données d'activité.

        Args:
            start_date: Date de début
            end_date: Date de fin

        Returns:
            Liste des données d'activité
        """
        pass

    @abstractmethod
    async def get_sleep_data(
        self, start_date: datetime, end_date: datetime
    ) -> list[SleepData]:
        """
        Récupère les données de sommeil.

        Args:
            start_date: Date de début
            end_date: Date de fin

        Returns:
            Liste des données de sommeil
        """
        pass

    @abstractmethod
    async def get_stress_data(
        self, start_date: datetime, end_date: datetime
    ) -> list[StressData]:
        """
        Récupère les données de stress.

        Args:
            start_date: Date de début
            end_date: Date de fin

        Returns:
            Liste des données de stress
        """
        pass

    @abstractmethod
    async def get_health_data(
        self, start_date: datetime, end_date: datetime
    ) -> list[HealthData]:
        """
        Récupère les données de santé générales.

        Args:
            start_date: Date de début
            end_date: Date de fin

        Returns:
            Liste des données de santé
        """
        pass

    async def sync_all_data(self, days_back: int = 30) -> dict[str, Any]:
        """
        Synchronise toutes les données disponibles.

        Args:
            days_back: Nombre de jours à synchroniser en arrière

        Returns:
            Dictionnaire avec le résumé de la synchronisation
        """
        if not self.is_connected:
            await self.connect()

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        sync_summary = {
            "connector": self.connector_name,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "sync_timestamp": datetime.now().isoformat(),
            "data_counts": {},
            "errors": [],
        }

        try:
            # Synchronisation des données d'activité
            activity_data = await self.get_activity_data(start_date, end_date)
            sync_summary["data_counts"]["activity"] = len(activity_data)

            # Synchronisation des données de sommeil
            sleep_data = await self.get_sleep_data(start_date, end_date)
            sync_summary["data_counts"]["sleep"] = len(sleep_data)

            # Synchronisation des données de stress
            stress_data = await self.get_stress_data(start_date, end_date)
            sync_summary["data_counts"]["stress"] = len(stress_data)

            # Synchronisation des données de santé
            health_data = await self.get_health_data(start_date, end_date)
            sync_summary["data_counts"]["health"] = len(health_data)

            self.last_sync = datetime.now()
            sync_summary["status"] = "success"

        except Exception as e:
            error_msg = f"Erreur de synchronisation: {str(e)}"
            self.sync_errors.append(error_msg)
            sync_summary["errors"].append(error_msg)
            sync_summary["status"] = "error"

        return sync_summary

    def get_status(self) -> dict[str, Any]:
        """
        Retourne le statut du connecteur.

        Returns:
            Dictionnaire avec le statut du connecteur
        """
        return {
            "connector_name": self.connector_name,
            "is_connected": self.is_connected,
            "last_sync": self.last_sync.isoformat() if self.last_sync else None,
            "sync_errors": self.sync_errors,
            "status": "connected" if self.is_connected else "disconnected",
        }

    def clear_errors(self) -> None:
        """Efface la liste des erreurs de synchronisation."""
        self.sync_errors.clear()
