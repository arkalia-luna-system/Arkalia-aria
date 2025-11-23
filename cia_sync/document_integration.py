"""
Document Integration - Intégration avec documents CIA
Génération et synchronisation de rapports médicaux ARIA → CIA
"""

import importlib
from datetime import datetime, timedelta
from typing import Any

from core import DatabaseManager, get_logger

logger = get_logger("document_integration")

# Charger requests dynamiquement
requests: Any = importlib.import_module("requests")


class DocumentIntegration:
    """
    Gestionnaire d'intégration avec les documents CIA.

    Fonctionnalités :
    - Génération de rapports médicaux depuis données ARIA
    - Synchronisation avec documents CIA
    - Préparation de rapports pour consultations
    - Export formaté pour professionnels de santé
    """

    def __init__(
        self,
        cia_base_url: str = "http://127.0.0.1:8000",
        db_path: str = "aria_pain.db",
    ):
        """
        Initialise le gestionnaire d'intégration documents.

        Args:
            cia_base_url: URL de base de CIA
            db_path: Chemin vers la base de données ARIA
        """
        self.cia_base_url = cia_base_url
        self.db = DatabaseManager(db_path)
        logger.info("📄 Document Integration initialisé")

    def generate_medical_report(
        self,
        period_days: int = 30,
        include_patterns: bool = True,
        include_predictions: bool = True,
        anonymize: bool = False,
    ) -> dict[str, Any]:
        """
        Génère un rapport médical complet depuis les données ARIA.

        Args:
            period_days: Nombre de jours à inclure
            include_patterns: Inclure les patterns détectés
            include_predictions: Inclure les prédictions
            anonymize: Anonymiser les données personnelles

        Returns:
            Rapport médical structuré
        """
        try:
            cutoff_date = (
                datetime.now() - timedelta(days=period_days)
            ).isoformat()

            # Récupérer les entrées de douleur
            pain_entries = self.db.execute_query(
                """
                SELECT * FROM pain_entries
                WHERE timestamp >= ?
                ORDER BY timestamp DESC
                """,
                (cutoff_date,),
            )

            entries_list = [dict(row) for row in pain_entries]

            # Calculer des statistiques
            statistics = self._calculate_statistics(entries_list)

            # Préparer le rapport
            report = {
                "report_type": "medical",
                "period_days": period_days,
                "generated_at": datetime.now().isoformat(),
                "summary": {
                    "total_entries": len(entries_list),
                    "period_start": cutoff_date,
                    "period_end": datetime.now().isoformat(),
                },
                "statistics": statistics,
                "data": {
                    "pain_entries": entries_list[:50],  # Limiter pour taille
                },
            }

            # Ajouter patterns si demandé
            if include_patterns:
                try:
                    from pattern_analysis.correlation_analyzer import (
                        CorrelationAnalyzer,
                    )

                    analyzer = CorrelationAnalyzer()
                    patterns = analyzer.get_comprehensive_analysis(
                        days_back=period_days
                    )
                    report["patterns"] = patterns
                except Exception as e:
                    logger.warning(f"Erreur récupération patterns: {e}")
                    report["patterns"] = {"error": str(e)}

            # Ajouter prédictions si demandé
            if include_predictions:
                try:
                    from prediction_engine.ml_analyzer import ARIAMLAnalyzer

                    ml_analyzer = ARIAMLAnalyzer()
                    predictions = ml_analyzer.get_analytics_summary()
                    report["predictions"] = predictions
                except Exception as e:
                    logger.warning(f"Erreur récupération prédictions: {e}")
                    report["predictions"] = {"error": str(e)}

            # Anonymiser si demandé
            if anonymize:
                report = self._anonymize_report(report)

            logger.info(f"✅ Rapport médical généré ({len(entries_list)} entrées)")
            return report

        except Exception as e:
            logger.error(f"❌ Erreur génération rapport: {e}")
            return {"error": str(e)}

    def _calculate_statistics(
        self, entries: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Calcule des statistiques depuis les entrées."""
        if not entries:
            return {
                "avg_intensity": 0,
                "max_intensity": 0,
                "min_intensity": 0,
                "total_entries": 0,
            }

        intensities = [
            float(e.get("intensity", 0))
            for e in entries
            if e.get("intensity") is not None
        ]

        # Déclencheurs
        triggers: dict[str, int] = {}
        for entry in entries:
            trigger = entry.get("physical_trigger") or entry.get("mental_trigger")
            if trigger:
                triggers[trigger] = triggers.get(trigger, 0) + 1

        # Actions efficaces
        actions: dict[str, int] = {}
        for entry in entries:
            action = entry.get("action_taken")
            effectiveness = entry.get("effectiveness")
            if action and effectiveness and effectiveness >= 7:
                actions[action] = actions.get(action, 0) + 1

        return {
            "avg_intensity": round(sum(intensities) / len(intensities), 2)
            if intensities
            else 0,
            "max_intensity": max(intensities) if intensities else 0,
            "min_intensity": min(intensities) if intensities else 0,
            "total_entries": len(entries),
            "most_common_triggers": dict(
                sorted(triggers.items(), key=lambda x: x[1], reverse=True)[:5]
            ),
            "most_effective_actions": dict(
                sorted(actions.items(), key=lambda x: x[1], reverse=True)[:5]
            ),
        }

    def _anonymize_report(self, report: dict[str, Any]) -> dict[str, Any]:
        """Anonymise un rapport médical."""
        anonymized = report.copy()

        # Anonymiser les entrées
        if "data" in anonymized and "pain_entries" in anonymized["data"]:
            anonymized_entries = []
            for entry in anonymized["data"]["pain_entries"]:
                anonymized_entry = entry.copy()
                anonymized_entry["location"] = None
                anonymized_entry["notes"] = None
                if "timestamp" in anonymized_entry:
                    # Garder seulement la date, pas l'heure
                    timestamp_str = anonymized_entry["timestamp"]
                    if "T" in timestamp_str:
                        anonymized_entry["timestamp"] = timestamp_str.split("T")[0]
                anonymized_entries.append(anonymized_entry)
            anonymized["data"]["pain_entries"] = anonymized_entries

        anonymized["anonymized"] = True
        return anonymized

    def sync_report_to_cia(
        self, report: dict[str, Any], document_type: str = "pain_report"
    ) -> dict[str, Any]:
        """
        Synchronise un rapport avec les documents CIA.

        Args:
            report: Rapport médical à synchroniser
            document_type: Type de document (pain_report, consultation, etc.)

        Returns:
            Résultat de la synchronisation
        """
        try:
            # Vérifier la connexion CIA
            try:
                response = requests.get(
                    f"{self.cia_base_url}/health", timeout=10
                )
                if response.status_code != 200:
                    return {
                        "success": False,
                        "error": "CIA non disponible",
                    }
            except Exception as e:
                return {
                    "success": False,
                    "error": f"CIA non accessible: {e}",
                }

            # Envoyer le rapport à CIA
            try:
                response = requests.post(
                    f"{self.cia_base_url}/api/aria/documents",
                    json={
                        "document_type": document_type,
                        "report_data": report,
                        "timestamp": datetime.now().isoformat(),
                    },
                    timeout=30,
                )

                if response.status_code in [200, 201]:
                    logger.info("✅ Rapport synchronisé avec CIA")
                    return {
                        "success": True,
                        "message": "Rapport synchronisé avec CIA",
                        "cia_response": response.json(),
                    }
                else:
                    logger.warning(f"⚠️ Erreur sync CIA: {response.status_code}")
                    return {
                        "success": False,
                        "error": f"Erreur CIA: {response.status_code}",
                    }
            except Exception as e:
                logger.error(f"❌ Erreur envoi rapport: {e}")
                return {
                    "success": False,
                    "error": str(e),
                }

        except Exception as e:
            logger.error(f"❌ Erreur synchronisation rapport: {e}")
            return {
                "success": False,
                "error": str(e),
            }

    def prepare_consultation_report(
        self, days_before: int = 7, anonymize: bool = True
    ) -> dict[str, Any]:
        """
        Prépare un rapport pour une consultation médicale.

        Args:
            days_before: Nombre de jours avant la consultation
            anonymize: Anonymiser les données

        Returns:
            Rapport formaté pour consultation
        """
        report = self.generate_medical_report(
            period_days=days_before,
            include_patterns=True,
            include_predictions=True,
            anonymize=anonymize,
        )

        # Format spécifique pour consultation
        consultation_report = {
            "report_type": "consultation",
            "prepared_for": "medical_consultation",
            "prepared_at": datetime.now().isoformat(),
            "period_days": days_before,
            "summary": report.get("summary", {}),
            "statistics": report.get("statistics", {}),
            "key_findings": {
                "average_pain_intensity": report.get("statistics", {}).get(
                    "avg_intensity", 0
                ),
                "most_common_triggers": report.get("statistics", {}).get(
                    "most_common_triggers", {}
                ),
                "effective_actions": report.get("statistics", {}).get(
                    "most_effective_actions", {}
                ),
            },
            "patterns": report.get("patterns", {}),
            "recommendations": self._generate_recommendations(report),
        }

        return consultation_report

    def _generate_recommendations(
        self, report: dict[str, Any]
    ) -> list[str]:
        """Génère des recommandations basées sur le rapport."""
        recommendations = []

        statistics = report.get("statistics", {})
        avg_intensity = statistics.get("avg_intensity", 0)

        if avg_intensity >= 7:
            recommendations.append(
                "Douleur moyenne élevée. Consultation médicale recommandée."
            )
        elif avg_intensity >= 5:
            recommendations.append(
                "Douleur modérée. Surveiller l'évolution."
            )

        # Recommandations basées sur patterns
        patterns = report.get("patterns", {})
        sleep_corr = patterns.get("sleep_pain_correlation", {})
        if sleep_corr.get("correlation", 0) < -0.4:
            recommendations.append(
                "Corrélation négative entre sommeil et douleur. "
                "Améliorer la qualité du sommeil recommandé."
            )

        stress_corr = patterns.get("stress_pain_correlation", {})
        if stress_corr.get("correlation", 0) > 0.5:
            recommendations.append(
                "Corrélation positive entre stress et douleur. "
                "Techniques de gestion du stress recommandées."
            )

        return recommendations


# Instance globale (singleton)
_document_integration: DocumentIntegration | None = None


def get_document_integration() -> DocumentIntegration:
    """Récupère ou crée l'instance globale."""
    global _document_integration
    if _document_integration is None:
        _document_integration = DocumentIntegration()
    return _document_integration

