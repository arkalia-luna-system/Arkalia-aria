"""
BBIA Integration - Intégration avec BBIA-SIM (sans robot physique)
Préparation de l'intégration future avec le robot Reachy Mini
"""

from datetime import datetime
from typing import Any

from core import get_logger

logger = get_logger("bbia_integration")


class BBIAIntegration:
    """
    Gestionnaire d'intégration avec BBIA-SIM.
    
    Fonctionnalités (sans robot physique) :
    - Préparation des données émotionnelles pour BBIA
    - Simulation des états émotionnels basés sur ARIA
    - Interface pour communication future avec robot
    - Adaptation comportementale basée sur données santé
    """

    def __init__(
        self,
        bbia_base_url: str = "http://127.0.0.1:8002",
    ):
        """
        Initialise le gestionnaire d'intégration BBIA.

        Args:
            bbia_base_url: URL de base de BBIA-SIM (par défaut: 8002)
        """
        self.bbia_base_url = bbia_base_url
        self.is_connected = False
        logger.info("🤖 BBIA Integration initialisé (mode simulation)")

    def check_connection(self) -> bool:
        """
        Vérifie la connexion avec BBIA-SIM.

        Returns:
            True si BBIA est accessible
        """
        try:
            import requests

            response = requests.get(
                f"{self.bbia_base_url}/health", timeout=5
            )
            self.is_connected = response.status_code == 200
            return self.is_connected
        except Exception as e:
            logger.debug(f"BBIA non accessible: {e}")
            self.is_connected = False
            return False

    def prepare_emotional_state(
        self,
        pain_intensity: float,
        stress_level: float | None = None,
        sleep_quality: float | None = None,
    ) -> dict[str, Any]:
        """
        Prépare l'état émotionnel pour BBIA basé sur les données ARIA.

        Args:
            pain_intensity: Intensité de la douleur (0-10)
            stress_level: Niveau de stress (0-10, optionnel)
            sleep_quality: Qualité du sommeil (0-10, optionnel)

        Returns:
            État émotionnel structuré pour BBIA
        """
        # Calculer l'état émotionnel basé sur les données
        emotional_state = {
            "timestamp": datetime.now().isoformat(),
            "source": "aria",
            "pain_level": pain_intensity,
            "emotional_state": self._calculate_emotional_state(
                pain_intensity, stress_level, sleep_quality
            ),
            "recommended_behavior": self._recommend_behavior(
                pain_intensity, stress_level, sleep_quality
            ),
        }

        if stress_level is not None:
            emotional_state["stress_level"] = stress_level
        if sleep_quality is not None:
            emotional_state["sleep_quality"] = sleep_quality

        logger.debug(f"État émotionnel préparé: {emotional_state['emotional_state']}")
        return emotional_state

    def _calculate_emotional_state(
        self,
        pain_intensity: float,
        stress_level: float | None,
        sleep_quality: float | None,
    ) -> str:
        """
        Calcule l'état émotionnel recommandé pour BBIA.

        Returns:
            État émotionnel (empathique, neutre, encourageant, etc.)
        """
        # Logique de calcul d'état émotionnel
        if pain_intensity >= 7:
            return "empathique_high"  # Empathie renforcée pour douleur élevée
        elif pain_intensity >= 5:
            return "empathique_medium"  # Empathie modérée
        elif stress_level and stress_level >= 7:
            return "calmant"  # Comportement calmant pour stress élevé
        elif sleep_quality and sleep_quality < 5:
            return "encourageant"  # Encouragement pour sommeil de mauvaise qualité
        else:
            return "neutre"  # État neutre par défaut

    def _recommend_behavior(
        self,
        pain_intensity: float,
        stress_level: float | None,
        sleep_quality: float | None,
    ) -> dict[str, Any]:
        """
        Recommande un comportement pour BBIA.

        Returns:
            Comportement recommandé avec actions
        """
        behavior = {
            "primary_action": "observe",
            "secondary_actions": [],
            "voice_tone": "calm",
            "movement_level": "minimal",
        }

        if pain_intensity >= 7:
            behavior["primary_action"] = "comfort"
            behavior["voice_tone"] = "gentle"
            behavior["secondary_actions"] = ["show_concern", "offer_support"]
        elif pain_intensity >= 5:
            behavior["primary_action"] = "monitor"
            behavior["voice_tone"] = "supportive"
            behavior["secondary_actions"] = ["check_in"]
        elif stress_level and stress_level >= 7:
            behavior["primary_action"] = "calm"
            behavior["voice_tone"] = "soothing"
            behavior["secondary_actions"] = ["breathing_guide"]

        return behavior

    def send_emotional_state(
        self, emotional_state: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Envoie l'état émotionnel à BBIA-SIM (simulation sans robot).

        Args:
            emotional_state: État émotionnel préparé

        Returns:
            Résultat de l'envoi
        """
        if not self.check_connection():
            logger.warning("BBIA non accessible - mode simulation uniquement")
            return {
                "success": False,
                "mode": "simulation",
                "message": "BBIA non accessible, état préparé mais non envoyé",
                "emotional_state": emotional_state,
            }

        try:
            import requests

            response = requests.post(
                f"{self.bbia_base_url}/api/aria/emotional-state",
                json=emotional_state,
                timeout=10,
            )

            if response.status_code in [200, 201]:
                logger.info("✅ État émotionnel envoyé à BBIA")
                return {
                    "success": True,
                    "mode": "connected",
                    "bbia_response": response.json(),
                }
            else:
                logger.warning(f"⚠️ Erreur envoi BBIA: {response.status_code}")
                return {
                    "success": False,
                    "mode": "error",
                    "error": f"Erreur BBIA: {response.status_code}",
                }
        except Exception as e:
            logger.warning(f"⚠️ Erreur communication BBIA: {e}")
            return {
                "success": False,
                "mode": "simulation",
                "error": str(e),
                "emotional_state": emotional_state,
            }

    def get_status(self) -> dict[str, Any]:
        """
        Retourne le statut de l'intégration BBIA.

        Returns:
            Statut de connexion et configuration
        """
        return {
            "module": "bbia_integration",
            "connected": self.check_connection(),
            "bbia_url": self.bbia_base_url,
            "mode": "simulation" if not self.is_connected else "connected",
            "capabilities": [
                "emotional_state_preparation",
                "behavior_recommendation",
                "pain_based_adaptation",
                "stress_based_adaptation",
                "sleep_based_adaptation",
            ],
            "note": "Mode simulation - robot physique requis pour activation complète",
            "timestamp": datetime.now().isoformat(),
        }


# Instance globale (singleton)
_bbia_integration: BBIAIntegration | None = None


def get_bbia_integration() -> BBIAIntegration:
    """Récupère ou crée l'instance globale du gestionnaire BBIA."""
    global _bbia_integration
    if _bbia_integration is None:
        _bbia_integration = BBIAIntegration()
    return _bbia_integration

