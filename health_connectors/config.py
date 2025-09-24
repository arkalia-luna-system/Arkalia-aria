"""
Configuration des connecteurs de santé pour la production
Gestion des clés API, URLs et paramètres de connexion
"""

from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class HealthConnectorConfig(BaseSettings):
    """Configuration des connecteurs de santé."""

    # Configuration générale
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Samsung Health API
    samsung_health_enabled: bool = Field(default=True, env="SAMSUNG_HEALTH_ENABLED")
    samsung_health_api_key: str | None = Field(
        default=None, env="SAMSUNG_HEALTH_API_KEY"
    )
    samsung_health_api_secret: str | None = Field(
        default=None, env="SAMSUNG_HEALTH_API_SECRET"
    )
    samsung_health_base_url: str = Field(
        default="https://api.samsunghealth.com", env="SAMSUNG_HEALTH_BASE_URL"
    )
    samsung_health_timeout: int = Field(default=30, env="SAMSUNG_HEALTH_TIMEOUT")

    # Google Fit API
    google_fit_enabled: bool = Field(default=True, env="GOOGLE_FIT_ENABLED")
    google_fit_client_id: str | None = Field(default=None, env="GOOGLE_FIT_CLIENT_ID")
    google_fit_client_secret: str | None = Field(
        default=None, env="GOOGLE_FIT_CLIENT_SECRET"
    )
    google_fit_redirect_uri: str = Field(
        default="http://localhost:8000/auth/google/callback",
        env="GOOGLE_FIT_REDIRECT_URI",
    )
    google_fit_scopes: list = Field(
        default=[
            "https://www.googleapis.com/auth/fitness.activity.read",
            "https://www.googleapis.com/auth/fitness.body.read",
            "https://www.googleapis.com/auth/fitness.sleep.read",
        ],
        env="GOOGLE_FIT_SCOPES",
    )

    # Apple HealthKit (iOS Health)
    ios_health_enabled: bool = Field(default=True, env="IOS_HEALTH_ENABLED")
    apple_healthkit_enabled: bool = Field(default=True, env="APPLE_HEALTHKIT_ENABLED")
    ios_health_team_id: str | None = Field(default=None, env="IOS_HEALTH_TEAM_ID")
    ios_health_key_id: str | None = Field(default=None, env="IOS_HEALTH_KEY_ID")
    ios_health_private_key: str | None = Field(
        default=None, env="IOS_HEALTH_PRIVATE_KEY"
    )
    ios_health_bundle_id: str = Field(
        default="com.arkalia.aria", env="IOS_HEALTH_BUNDLE_ID"
    )

    # Configuration de synchronisation
    sync_interval_hours: int = Field(default=6, env="SYNC_INTERVAL_HOURS")
    max_days_back: int = Field(default=30, env="MAX_DAYS_BACK")
    auto_sync_enabled: bool = Field(default=True, env="AUTO_SYNC_ENABLED")
    batch_size: int = Field(default=100, env="BATCH_SIZE")

    # Configuration de sécurité
    encryption_key: str | None = Field(default=None, env="ENCRYPTION_KEY")
    jwt_secret: str | None = Field(default=None, env="JWT_SECRET")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")

    # Configuration de la base de données
    database_url: str = Field(
        default="postgresql://user:pass@localhost/arkalia", env="DATABASE_URL"
    )
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")

    # Configuration des logs
    log_file: str = Field(default="logs/health_connectors.log", env="LOG_FILE")
    log_rotation: str = Field(default="daily", env="LOG_ROTATION")
    log_retention_days: int = Field(default=30, env="LOG_RETENTION_DAYS")

    # Configuration des notifications
    notification_enabled: bool = Field(default=True, env="NOTIFICATION_ENABLED")
    email_smtp_host: str | None = Field(default=None, env="EMAIL_SMTP_HOST")
    email_smtp_port: int = Field(default=587, env="EMAIL_SMTP_PORT")
    email_username: str | None = Field(default=None, env="EMAIL_USERNAME")
    email_password: str | None = Field(default=None, env="EMAIL_PASSWORD")

    # Configuration des webhooks
    webhook_enabled: bool = Field(default=False, env="WEBHOOK_ENABLED")
    webhook_url: str | None = Field(default=None, env="WEBHOOK_URL")
    webhook_secret: str | None = Field(default=None, env="WEBHOOK_SECRET")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class SamsungHealthConfig:
    """Configuration spécifique pour Samsung Health."""

    def __init__(self, config: HealthConnectorConfig):
        self.api_key = config.samsung_health_api_key
        self.api_secret = config.samsung_health_api_secret
        self.base_url = config.samsung_health_base_url
        self.timeout = config.samsung_health_timeout
        self.enabled = config.samsung_health_enabled

        # Endpoints Samsung Health
        self.endpoints = {
            "auth": f"{self.base_url}/oauth2/authorize",
            "token": f"{self.base_url}/oauth2/token",
            "user": f"{self.base_url}/v1/user",
            "activity": f"{self.base_url}/v1/activity",
            "sleep": f"{self.base_url}/v1/sleep",
            "stress": f"{self.base_url}/v1/stress",
            "health": f"{self.base_url}/v1/health",
        }

        # Scopes Samsung Health
        self.scopes = [
            "user.info.read",
            "activity.read",
            "sleep.read",
            "stress.read",
            "health.read",
        ]


class GoogleFitConfig:
    """Configuration spécifique pour Google Fit."""

    def __init__(self, config: HealthConnectorConfig):
        self.client_id = config.google_fit_client_id
        self.client_secret = config.google_fit_client_secret
        self.redirect_uri = config.google_fit_redirect_uri
        self.scopes = config.google_fit_scopes
        self.enabled = config.google_fit_enabled

        # URLs Google Fit
        self.auth_url = "https://accounts.google.com/o/oauth2/v2/auth"  # nosec B105
        self.token_url = "https://oauth2.googleapis.com/token"  # nosec B105
        self.api_base_url = "https://www.googleapis.com/fitness/v1"

        # Endpoints Google Fit
        self.endpoints = {
            "datasources": f"{self.api_base_url}/users/me/dataSources",
            "datasets": f"{self.api_base_url}/users/me/dataset:aggregate",
            "sessions": f"{self.api_base_url}/users/me/sessions",
        }

        # Types de données Google Fit
        self.data_types = {
            "steps": "com.google.step_count.delta",
            "distance": "com.google.distance.delta",
            "calories": "com.google.calories.expended",
            "heart_rate": "com.google.heart_rate.bpm",
            "sleep": "com.google.sleep.segment",
            "weight": "com.google.weight",
            "height": "com.google.height",
        }


class IOSHealthConfig:
    """Configuration spécifique pour iOS Health."""

    def __init__(self, config: HealthConnectorConfig):
        self.team_id = config.ios_health_team_id
        self.key_id = config.ios_health_key_id
        self.private_key = config.ios_health_private_key
        self.bundle_id = config.ios_health_bundle_id
        self.enabled = config.ios_health_enabled

        # URLs Apple Health
        self.base_url = "https://api.apple.com/health"  # nosec B105
        self.auth_url = "https://appleid.apple.com/auth/authorize"  # nosec B105
        self.token_url = "https://appleid.apple.com/auth/token"  # nosec B105

        # Types de données iOS Health
        self.data_types = {
            "steps": "HKQuantityTypeIdentifierStepCount",
            "distance": "HKQuantityTypeIdentifierDistanceWalkingRunning",
            "calories": "HKQuantityTypeIdentifierActiveEnergyBurned",
            "heart_rate": "HKQuantityTypeIdentifierHeartRate",
            "sleep": "HKCategoryTypeIdentifierSleepAnalysis",
            "weight": "HKQuantityTypeIdentifierBodyMass",
            "height": "HKQuantityTypeIdentifierHeight",
            "blood_pressure": "HKQuantityTypeIdentifierBloodPressureSystolic",
        }


def get_config() -> HealthConnectorConfig:
    """Récupère la configuration des connecteurs de santé."""
    return HealthConnectorConfig()


def get_samsung_config() -> SamsungHealthConfig:
    """Récupère la configuration Samsung Health."""
    config = get_config()
    return SamsungHealthConfig(config)


def get_google_fit_config() -> GoogleFitConfig:
    """Récupère la configuration Google Fit."""
    config = get_config()
    return GoogleFitConfig(config)


def get_ios_health_config() -> IOSHealthConfig:
    """Récupère la configuration iOS Health."""
    config = get_config()
    return IOSHealthConfig(config)


def validate_config() -> dict[str, Any]:
    """Valide la configuration et retourne les erreurs éventuelles."""
    config = get_config()
    errors = {}

    # Validation Samsung Health
    if config.samsung_health_enabled:
        if not config.samsung_health_api_key:
            errors["samsung_health"] = "API key manquante"
        if not config.samsung_health_api_secret:
            errors["samsung_health"] = "API secret manquant"

    # Validation Google Fit
    if config.google_fit_enabled:
        if not config.google_fit_client_id:
            errors["google_fit"] = "Client ID manquant"
        if not config.google_fit_client_secret:
            errors["google_fit"] = "Client secret manquant"

    # Validation iOS Health
    if config.ios_health_enabled:
        if not config.ios_health_team_id:
            errors["ios_health"] = "Team ID manquant"
        if not config.ios_health_key_id:
            errors["ios_health"] = "Key ID manquant"
        if not config.ios_health_private_key:
            errors["ios_health"] = "Private key manquante"

    # Validation générale
    if not config.encryption_key:
        errors["security"] = "Clé de chiffrement manquante"
    if not config.jwt_secret:
        errors["security"] = "Secret JWT manquant"

    return errors


# Instance globale de configuration
config = get_config()
samsung_config = get_samsung_config()
google_fit_config = get_google_fit_config()
ios_health_config = get_ios_health_config()
