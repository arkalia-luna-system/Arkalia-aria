"""
ARKALIA ARIA - Système d'Alertes Automatiques
=============================================

Système d'alertes intelligent pour :
- Patterns détectés (déclencheurs récurrents)
- Prédictions (crises anticipées)
- Corrélations importantes (sommeil-douleur, stress-douleur)
- Notifications basées sur données santé
"""

from datetime import datetime
from enum import Enum
from typing import Any

from .database import DatabaseManager
from .logging import get_logger

logger = get_logger("alerts")


class AlertSeverity(Enum):
    """Niveaux de sévérité des alertes."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types d'alertes."""

    PATTERN_DETECTED = "pattern_detected"
    PREDICTION_CRISIS = "prediction_crisis"
    CORRELATION_STRONG = "correlation_strong"
    HEALTH_SYNC = "health_sync"
    MEDICAL_APPOINTMENT = "medical_appointment"


class ARIA_AlertsSystem:
    """
    Système d'alertes automatiques ARIA.

    Détecte et génère des alertes pour :
    - Patterns récurrents dans les données de douleur
    - Prédictions de crises
    - Corrélations importantes
    - Événements santé
    """

    def __init__(self, db_path: str = "aria_pain.db") -> None:
        """Initialise le système d'alertes."""
        self.db = DatabaseManager(db_path)
        self._init_alerts_table()

    def _init_alerts_table(self) -> None:
        """Initialise la table des alertes."""
        try:
            self.db.execute_update("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    data TEXT,
                    is_read INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT (DATETIME('now'))
                )
                """)
            # Index pour requêtes fréquentes
            try:
                self.db.execute_update(
                    "CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(alert_type)"
                )
                self.db.execute_update(
                    "CREATE INDEX IF NOT EXISTS idx_alerts_created ON alerts(created_at)"
                )
                self.db.execute_update(
                    "CREATE INDEX IF NOT EXISTS idx_alerts_read ON alerts(is_read)"
                )
            except Exception as e:
                # Ignorer les erreurs de création d'index (peut déjà exister)
                logger.debug(f"Index idx_alerts_read peut déjà exister: {e}")
            logger.info("✅ Table alerts initialisée")
        except Exception as e:
            logger.error(f"❌ Erreur initialisation table alerts: {e}")

    def create_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        title: str,
        message: str,
        data: dict[str, Any] | None = None,
    ) -> int:
        """
        Crée une nouvelle alerte.

        Args:
            alert_type: Type d'alerte
            severity: Niveau de sévérité
            title: Titre de l'alerte
            message: Message détaillé
            data: Données supplémentaires (optionnel)

        Returns:
            ID de l'alerte créée
        """
        try:
            import json

            data_json = json.dumps(data) if data else None
            self.db.execute_update(
                """
                INSERT INTO alerts (alert_type, severity, title, message, data)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    alert_type.value,
                    severity.value,
                    title,
                    message,
                    data_json,
                ),
            )
            logger.info(f"✅ Alerte créée: {title}")
            # Récupérer l'ID
            rows = self.db.execute_query("SELECT last_insert_rowid() as id")
            return rows[0]["id"] if rows else 0
        except Exception as e:
            logger.error(f"❌ Erreur création alerte: {e}")
            return 0

    def check_patterns(self, days_back: int = 30) -> list[dict[str, Any]]:
        """
        Vérifie les patterns récurrents et crée des alertes.

        Args:
            days_back: Nombre de jours à analyser

        Returns:
            Liste des alertes créées
        """
        alerts_created = []
        try:
            from pattern_analysis.correlation_analyzer import CorrelationAnalyzer

            analyzer = CorrelationAnalyzer()
            triggers = analyzer.detect_recurrent_triggers(days_back=days_back)

            # Vérifier si des déclencheurs récurrents existent
            if triggers.get("triggers"):
                for trigger in triggers["triggers"][:5]:  # Top 5
                    if trigger.get("occurrences", 0) >= 3:
                        alert_id = self.create_alert(
                            alert_type=AlertType.PATTERN_DETECTED,
                            severity=AlertSeverity.WARNING,
                            title="Déclencheur récurrent détecté",
                            message=f"Le déclencheur '{trigger.get('trigger', 'inconnu')}' "
                            f"apparaît {trigger.get('occurrences', 0)} fois "
                            f"dans les {days_back} derniers jours.",
                            data={"trigger": trigger, "days_back": days_back},
                        )
                        alerts_created.append({"id": alert_id, "trigger": trigger})
        except Exception as e:
            logger.warning(f"Erreur vérification patterns: {e}")

        return alerts_created

    def check_predictions(self) -> list[dict[str, Any]]:
        """
        Vérifie les prédictions de crises et crée des alertes.

        Returns:
            Liste des alertes créées
        """
        alerts_created = []
        try:
            from prediction_engine.ml_analyzer import ARIAMLAnalyzer

            ml_analyzer = ARIAMLAnalyzer()
            context = {
                "stress_level": 0.5,
                "fatigue_level": 0.5,
                "activity_intensity": 0.5,
            }
            prediction = ml_analyzer.predict_pain_episode(context)

            # Vérifier si risque élevé
            risk_level = prediction.get("risk_level", "low")
            probability = prediction.get("probability", 0.0)

            if risk_level in ["high", "critical"] or probability > 0.7:
                severity = (
                    AlertSeverity.CRITICAL
                    if risk_level == "critical" or probability > 0.9
                    else AlertSeverity.WARNING
                )
                alert_id = self.create_alert(
                    alert_type=AlertType.PREDICTION_CRISIS,
                    severity=severity,
                    title="Risque de crise détecté",
                    message=f"Probabilité de crise: {probability:.0%} "
                    f"(Niveau de risque: {risk_level})",
                    data={"prediction": prediction},
                )
                alerts_created.append({"id": alert_id, "prediction": prediction})
        except Exception as e:
            logger.warning(f"Erreur vérification prédictions: {e}")

        return alerts_created

    def check_correlations(self, days_back: int = 30) -> list[dict[str, Any]]:
        """
        Vérifie les corrélations importantes et crée des alertes.

        Args:
            days_back: Nombre de jours à analyser

        Returns:
            Liste des alertes créées
        """
        alerts_created = []
        try:
            from pattern_analysis.correlation_analyzer import CorrelationAnalyzer

            analyzer = CorrelationAnalyzer()

            # Corrélation sommeil-douleur
            sleep_corr = analyzer.analyze_sleep_pain_correlation(days_back=days_back)
            sleep_strength = sleep_corr.get("correlation_strength", 0.0)

            if abs(sleep_strength) > 0.6:  # Corrélation forte
                alert_id = self.create_alert(
                    alert_type=AlertType.CORRELATION_STRONG,
                    severity=AlertSeverity.INFO,
                    title="Corrélation sommeil-douleur détectée",
                    message=f"Corrélation forte ({sleep_strength:.0%}) entre "
                    f"la qualité du sommeil et la douleur.",
                    data={"correlation": sleep_corr, "type": "sleep_pain"},
                )
                alerts_created.append({"id": alert_id, "correlation": sleep_corr})

            # Corrélation stress-douleur
            stress_corr = analyzer.analyze_stress_pain_correlation(days_back=days_back)
            stress_strength = stress_corr.get("correlation_strength", 0.0)

            if abs(stress_strength) > 0.6:  # Corrélation forte
                alert_id = self.create_alert(
                    alert_type=AlertType.CORRELATION_STRONG,
                    severity=AlertSeverity.INFO,
                    title="Corrélation stress-douleur détectée",
                    message=f"Corrélation forte ({stress_strength:.0%}) entre "
                    f"le niveau de stress et la douleur.",
                    data={"correlation": stress_corr, "type": "stress_pain"},
                )
                alerts_created.append({"id": alert_id, "correlation": stress_corr})
        except Exception as e:
            logger.warning(f"Erreur vérification corrélations: {e}")

        return alerts_created

    def get_alerts(
        self,
        limit: int = 50,
        offset: int = 0,
        unread_only: bool = False,
        alert_type: AlertType | None = None,
    ) -> dict[str, Any]:
        """
        Récupère les alertes.

        Args:
            limit: Nombre d'alertes à retourner
            offset: Offset pour pagination
            unread_only: Retourner uniquement les non lues
            alert_type: Filtrer par type (optionnel)

        Returns:
            Dict avec les alertes et métadonnées
        """
        try:
            query = "SELECT * FROM alerts WHERE 1=1"
            params: list[Any] = []

            if unread_only:
                query += " AND is_read = 0"
            if alert_type:
                query += " AND alert_type = ?"
                params.append(alert_type.value)

            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            rows = self.db.execute_query(query, tuple(params))

            # Compter le total
            count_query = "SELECT COUNT(*) as count FROM alerts WHERE 1=1"
            count_params: list[Any] = []
            if unread_only:
                count_query += " AND is_read = 0"
            if alert_type:
                count_query += " AND alert_type = ?"
                count_params.append(alert_type.value)

            total_rows = self.db.execute_query(count_query, tuple(count_params))
            total = total_rows[0]["count"] if total_rows else 0

            alerts = []
            for row in rows:
                import json

                alert_dict = dict(row)
                if alert_dict.get("data"):
                    try:
                        alert_dict["data"] = json.loads(alert_dict["data"])
                    except Exception as e:
                        # Ignorer les erreurs de parsing JSON pour alert data
                        logger.debug(f"Erreur parsing JSON alert data: {e}")
                alerts.append(alert_dict)

            return {
                "alerts": alerts,
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total,
            }
        except Exception as e:
            logger.error(f"❌ Erreur récupération alertes: {e}")
            return {
                "alerts": [],
                "total": 0,
                "limit": limit,
                "offset": offset,
                "has_more": False,
            }

    def mark_as_read(self, alert_id: int) -> bool:
        """
        Marque une alerte comme lue.

        Args:
            alert_id: ID de l'alerte

        Returns:
            True si succès
        """
        try:
            self.db.execute_update(
                "UPDATE alerts SET is_read = 1 WHERE id = ?", (alert_id,)
            )
            return True
        except Exception as e:
            logger.error(f"❌ Erreur marquage alerte: {e}")
            return False

    def mark_all_as_read(self) -> int:
        """
        Marque toutes les alertes comme lues.

        Returns:
            Nombre d'alertes marquées
        """
        try:
            result = self.db.execute_update(
                "UPDATE alerts SET is_read = 1 WHERE is_read = 0"
            )
            return result
        except Exception as e:
            logger.error(f"❌ Erreur marquage toutes alertes: {e}")
            return 0

    def check_all(self, days_back: int = 30) -> dict[str, Any]:
        """
        Vérifie tout et crée les alertes nécessaires.

        Args:
            days_back: Nombre de jours à analyser

        Returns:
            Résumé des alertes créées
        """
        logger.info("🔍 Vérification de toutes les alertes...")
        patterns = self.check_patterns(days_back=days_back)
        predictions = self.check_predictions()
        correlations = self.check_correlations(days_back=days_back)

        total = len(patterns) + len(predictions) + len(correlations)

        return {
            "patterns": len(patterns),
            "predictions": len(predictions),
            "correlations": len(correlations),
            "total": total,
            "timestamp": datetime.now().isoformat(),
        }


# Instance globale
_alerts_system: ARIA_AlertsSystem | None = None


def get_alerts_system() -> ARIA_AlertsSystem:
    """Récupère ou crée l'instance du système d'alertes."""
    global _alerts_system
    if _alerts_system is None:
        _alerts_system = ARIA_AlertsSystem()
    return _alerts_system
