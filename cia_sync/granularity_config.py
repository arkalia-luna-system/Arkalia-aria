"""
Granularity Config - Configuration de granularité de synchronisation ARIA ↔ CIA
Contrôle fin de ce qui est synchronisé et à quel niveau de détail
"""

import json
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any

from core import DatabaseManager, get_logger

logger = get_logger("granularity_config")


class SyncLevel(Enum):
    """Niveaux de détail pour la synchronisation"""

    NONE = "none"  # Aucune synchronisation
    SUMMARY = "summary"  # Résumé agrégé uniquement
    AGGREGATED = "aggregated"  # Données agrégées (par jour/semaine)
    DETAILED = "detailed"  # Toutes les données détaillées


class DataType(Enum):
    """Types de données synchronisables"""

    PAIN_ENTRIES = "pain_entries"
    PATTERNS = "patterns"
    PREDICTIONS = "predictions"
    CORRELATIONS = "correlations"
    TRIGGERS = "triggers"
    EXPORTS = "exports"


@dataclass
class GranularityConfig:
    """
    Configuration de granularité pour chaque type de données.

    Permet de contrôler finement ce qui est synchronisé avec CIA.
    """

    # Niveaux de synchronisation par type de données
    pain_entries_level: SyncLevel = SyncLevel.AGGREGATED
    patterns_level: SyncLevel = SyncLevel.SUMMARY
    predictions_level: SyncLevel = SyncLevel.SUMMARY
    correlations_level: SyncLevel = SyncLevel.SUMMARY
    triggers_level: SyncLevel = SyncLevel.AGGREGATED
    exports_level: SyncLevel = SyncLevel.NONE

    # Options de filtrage
    anonymize_personal_data: bool = False
    anonymize_timestamps: bool = False
    anonymize_locations: bool = True
    anonymize_notes: bool = True

    # Options d'agrégation
    aggregate_by_day: bool = True
    aggregate_by_week: bool = False
    include_statistics: bool = True
    include_trends: bool = True

    # Période de synchronisation
    sync_period_days: int = 30  # Derniers N jours

    def to_dict(self) -> dict[str, Any]:
        """Convertit la configuration en dictionnaire."""
        result = asdict(self)
        # Convertir les enums en strings
        for key, value in result.items():
            if isinstance(value, SyncLevel):
                result[key] = value.value
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GranularityConfig":
        """Crée une configuration depuis un dictionnaire."""
        # Convertir les strings en enums
        for key, value in data.items():
            if key.endswith("_level") and isinstance(value, str):
                data[key] = SyncLevel(value)
        return cls(**data)

    def get_sync_level(self, data_type: DataType) -> SyncLevel:
        """
        Retourne le niveau de synchronisation pour un type de données.

        Args:
            data_type: Type de données

        Returns:
            Niveau de synchronisation
        """
        mapping = {
            DataType.PAIN_ENTRIES: self.pain_entries_level,
            DataType.PATTERNS: self.patterns_level,
            DataType.PREDICTIONS: self.predictions_level,
            DataType.CORRELATIONS: self.correlations_level,
            DataType.TRIGGERS: self.triggers_level,
            DataType.EXPORTS: self.exports_level,
        }
        return mapping.get(data_type, SyncLevel.NONE)

    def should_sync(self, data_type: DataType) -> bool:
        """
        Vérifie si un type de données doit être synchronisé.

        Args:
            data_type: Type de données

        Returns:
            True si la synchronisation est activée
        """
        return self.get_sync_level(data_type) != SyncLevel.NONE


class GranularityConfigManager:
    """
    Gestionnaire de configuration de granularité.

    Permet de sauvegarder, charger et gérer les configurations
    de granularité de synchronisation.
    """

    def __init__(self, db_path: str = "aria_pain.db"):
        """
        Initialise le gestionnaire de configuration.

        Args:
            db_path: Chemin vers la base de données
        """
        self.db = DatabaseManager(db_path)
        self._init_database()
        logger.info("⚙️ Granularity Config Manager initialisé")

    def _init_database(self) -> None:
        """Initialise la table de configuration."""
        self.db.execute_update(
            """
            CREATE TABLE IF NOT EXISTS sync_granularity_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_name TEXT NOT NULL UNIQUE,
                config_data TEXT NOT NULL,
                is_default INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        logger.debug("✅ Table sync_granularity_config initialisée")

    def save_config(
        self, config: GranularityConfig, config_name: str = "default"
    ) -> bool:
        """
        Sauvegarde une configuration de granularité.

        Args:
            config: Configuration à sauvegarder
            config_name: Nom de la configuration (défaut: "default")

        Returns:
            True si sauvegardé avec succès
        """
        try:
            config_json = json.dumps(config.to_dict())

            # Vérifier si la config existe déjà
            existing = self.db.execute_query(
                "SELECT id FROM sync_granularity_config WHERE config_name = ?",
                (config_name,),
            )

            if existing:
                # Mettre à jour
                self.db.execute_update(
                    """
                    UPDATE sync_granularity_config
                    SET config_data = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE config_name = ?
                    """,
                    (config_json, config_name),
                )
                logger.info(f"✅ Configuration '{config_name}' mise à jour")
            else:
                # Créer
                is_default = 1 if config_name == "default" else 0
                self.db.execute_update(
                    """
                    INSERT INTO sync_granularity_config
                    (config_name, config_data, is_default)
                    VALUES (?, ?, ?)
                    """,
                    (config_name, config_json, is_default),
                )
                logger.info(f"✅ Configuration '{config_name}' créée")

            return True
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde config: {e}")
            return False

    def load_config(self, config_name: str = "default") -> GranularityConfig | None:
        """
        Charge une configuration de granularité.

        Args:
            config_name: Nom de la configuration (défaut: "default")

        Returns:
            Configuration chargée ou None si non trouvée
        """
        try:
            rows = self.db.execute_query(
                "SELECT config_data FROM sync_granularity_config WHERE config_name = ?",
                (config_name,),
            )

            if not rows:
                logger.warning(f"⚠️ Configuration '{config_name}' non trouvée")
                return None

            config_data = json.loads(rows[0]["config_data"])
            config = GranularityConfig.from_dict(config_data)
            logger.debug(f"✅ Configuration '{config_name}' chargée")
            return config
        except Exception as e:
            logger.error(f"❌ Erreur chargement config: {e}")
            return None

    def get_default_config(self) -> GranularityConfig:
        """
        Retourne la configuration par défaut.

        Returns:
            Configuration par défaut
        """
        config = self.load_config("default")
        if config is None:
            # Créer une configuration par défaut
            config = GranularityConfig()
            self.save_config(config, "default")
        return config

    def list_configs(self) -> list[dict[str, Any]]:
        """
        Liste toutes les configurations disponibles.

        Returns:
            Liste des configurations avec métadonnées
        """
        try:
            rows = self.db.execute_query(
                """
                SELECT config_name, is_default, created_at, updated_at
                FROM sync_granularity_config
                ORDER BY is_default DESC, config_name
                """
            )
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"❌ Erreur liste configs: {e}")
            return []

    def delete_config(self, config_name: str) -> bool:
        """
        Supprime une configuration.

        Args:
            config_name: Nom de la configuration à supprimer

        Returns:
            True si supprimée avec succès
        """
        try:
            if config_name == "default":
                logger.warning("⚠️ Impossible de supprimer la config 'default'")
                return False

            self.db.execute_update(
                "DELETE FROM sync_granularity_config WHERE config_name = ?",
                (config_name,),
            )
            logger.info(f"✅ Configuration '{config_name}' supprimée")
            return True
        except Exception as e:
            logger.error(f"❌ Erreur suppression config: {e}")
            return False

    def apply_anonymization(
        self, data: dict[str, Any], config: GranularityConfig
    ) -> dict[str, Any]:
        """
        Applique l'anonymisation selon la configuration.

        Args:
            data: Données à anonymiser
            config: Configuration de granularité

        Returns:
            Données anonymisées
        """
        anonymized = data.copy()

        if config.anonymize_timestamps:
            # Remplacer les timestamps par des dates relatives
            if "timestamp" in anonymized:
                anonymized["timestamp"] = "anonymized"
            if "created_at" in anonymized:
                anonymized["created_at"] = "anonymized"

        if config.anonymize_locations:
            if "location" in anonymized:
                anonymized["location"] = None

        if config.anonymize_notes:
            if "notes" in anonymized:
                anonymized["notes"] = None

        if config.anonymize_personal_data:
            # Supprimer tous les identifiants personnels
            for key in ["user_id", "patient_id", "name", "email"]:
                if key in anonymized:
                    anonymized[key] = None

        return anonymized

    def aggregate_data(
        self, data_list: list[dict[str, Any]], config: GranularityConfig
    ) -> dict[str, Any]:
        """
        Agrège des données selon la configuration.

        Args:
            data_list: Liste de données à agréger
            config: Configuration de granularité

        Returns:
            Données agrégées
        """
        if not data_list:
            return {"count": 0, "summary": {}}

        aggregated: dict[str, Any] = {
            "count": len(data_list),
            "period_days": config.sync_period_days,
        }

        intensities: list[float] = []
        if config.include_statistics:
            # Calculer des statistiques
            intensities = [
                float(d.get("intensity", 0))
                for d in data_list
                if d.get("intensity") is not None
            ]
            if intensities:
                aggregated["statistics"] = {
                    "avg_intensity": sum(intensities) / len(intensities),
                    "max_intensity": max(intensities),
                    "min_intensity": min(intensities),
                }

        if config.include_trends and intensities:
            # Détecter des tendances simples
            if len(intensities) > 1:
                trend = (
                    "increasing" if intensities[-1] > intensities[0] else "decreasing"
                )
                aggregated["trend"] = trend

        # Agrégation par déclencheurs
        triggers: dict[str, int] = {}
        for data in data_list:
            trigger = data.get("physical_trigger") or data.get("mental_trigger")
            if trigger:
                triggers[trigger] = triggers.get(trigger, 0) + 1

        if triggers:
            aggregated["common_triggers"] = triggers

        return aggregated


# Instance globale (singleton)
_config_manager: GranularityConfigManager | None = None


def get_config_manager() -> GranularityConfigManager:
    """Récupère ou crée l'instance globale du gestionnaire."""
    global _config_manager
    if _config_manager is None:
        _config_manager = GranularityConfigManager()
    return _config_manager

