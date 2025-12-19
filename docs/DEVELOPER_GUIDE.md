# Guide Développeur

**ARKALIA ARIA** — Documentation technique complète

**Version :** 1.0.0
*Dernière mise à jour :* Novembre 2025

---

## Table des matières

1. [Architecture Générale](#architecture-générale)
2. [Module Core](#module-core)
3. [BaseAPI](#baseapi)
4. [Installation et Configuration](#installation-et-configuration)
5. [Structure du Projet](#structure-du-projet)
6. [API Documentation](#api-documentation)
7. [Connecteurs de Santé](#connecteurs-de-santé)
8. [Dashboard Web](#dashboard-web)
9. [Application Mobile](#application-mobile)
10. [Base de Données](#base-de-données)
11. [Tests et Qualité](#tests-et-qualité)
12. [Déploiement](#déploiement)
13. [Contributions](#contributions)
14. [Troubleshooting](#troubleshooting)
15. [Performance](#performance)
16. [Sécurité](#sécurité)
17. [Monitoring](#monitoring)

---

## Module Core

### Vue d'ensemble

Le module `core/` centralise toutes les fonctionnalités communes d'ARKALIA ARIA :

```text
core/
├── __init__.py          # Exports principaux
├── api_base.py          # BaseAPI pour standardiser les APIs
├── database.py          # DatabaseManager centralisé
├── cache.py             # CacheManager intelligent
├── config.py            # Configuration centralisée
├── logging.py           # Logging unifié
└── exceptions.py        # Exceptions personnalisées

```

### DatabaseManager

Gestionnaire de base de données centralisé avec pattern Singleton :

```python
from core import DatabaseManager

db = DatabaseManager()

# Requêtes
rows = db.execute_query("SELECT * FROM pain_entries")
count = db.get_count("pain_entries")
db.execute_update("INSERT INTO pain_entries ...")

```

### CacheManager

Système de cache intelligent avec TTL et invalidation :

```python
from core import CacheManager

cache = CacheManager()

# Cache simple
cache.set("key", value, ttl=300)
value = cache.get("key")

# Cache avec fonction
value = cache.get_or_set("key", expensive_function, ttl=300)

```

### Configuration

Configuration centralisée avec validation :

```python
from core import config

# Accès aux valeurs
db_path = config.get_db_path()
log_level = config.get_log_level()
api_port = config["api_port"]

```

---

## BaseAPI

### Vue d'ensemble BaseAPI

BaseAPI standardise toutes les APIs ARIA avec des endpoints communs :

```python
from core import BaseAPI

api = BaseAPI(
    prefix="/api/pain",
    tags=["Pain Tracking"],
    description="API de suivi de la douleur"
)

router = api.get_router()

```

### Endpoints Standardisés

Toutes les APIs héritent automatiquement de :

- `GET /health` - Vérification de santé
- `GET /status` - Statut de l'API
- `GET /metrics` - Métriques de performance

### Utilisation

```python
# Dans pain_tracking/api.py
from core import BaseAPI

api = BaseAPI("/api/pain", ["Pain Tracking"])
router = api.get_router()

@router.post("/entries")
async def create_entry(entry: PainEntry):
    # Logique métier
    return api.db.execute_update(...)

```

---

## Architecture Générale

### Vue d'ensemble Architecture

ARKALIA ARIA suit une architecture microservices modulaire avec les composants suivants :

```text
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │    │  Web Dashboard  │    │  Health APIs    │
│    (Flutter)    │    │   (FastAPI)     │    │  (Samsung,      │
│                 │    │                 │    │   Google, iOS)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Core API      │
                    │   (FastAPI)     │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Database      │
                    │   (PostgreSQL)  │
                    └─────────────────┘

```

### Technologies Utilisées

#### Backend

- **FastAPI** : Framework web moderne et performant
- **PostgreSQL** : Base de données relationnelle
- **Redis** : Cache et sessions
- **Celery** : Tâches asynchrones
- **Pydantic** : Validation des données

#### Frontend Web

- **HTML5/CSS3** : Structure et styles
- **JavaScript ES6+** : Logique côté client
- **Chart.js** : Graphiques interactifs
- **Bootstrap 5** : Framework CSS
- **WebSockets** : Communication temps réel

#### Mobile

- **Flutter** : Framework cross-platform
- **Dart** : Langage de programmation
- **Riverpod** : Gestion d'état
- **Hive** : Base de données locale
- **Health** : Intégration santé

#### DevOps

- **Docker** : Conteneurisation
- **GitHub Actions** : CI/CD
- **Nginx** : Serveur web
- **Let's Encrypt** : Certificats SSL

---

## Installation et Configuration

### Prérequis

- Python 3.10+
- Node.js 18+
- Flutter 3.0+
- PostgreSQL 14+
- Redis 6+
- Docker (optionnel)

### Installation Backend

```bash
# Cloner le repository
git clone <https://github.com/arkalia-aria/arkalia-aria.git>
cd arkalia-aria

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
python -m alembic upgrade head

# Lancer l'application
uvicorn main:app --reload

```

### Installation Frontend Web

```bash
cd metrics_collector/dashboard
npm install
npm run dev

```

### Installation Mobile

```bash
cd mobile_app
flutter pub get
flutter run

```

### Configuration Docker

```bash
# Lancer tous les services
docker-compose up -d

# Vérifier les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

```

---

## Structure du Projet

```text
arkalia-aria/
├── health_connectors/          # Connecteurs de santé
│   ├── __init__.py
│   ├── base_connector.py       # Classe de base
│   ├── samsung_health_connector.py
│   ├── google_fit_connector.py
│   ├── ios_health_connector.py
│   ├── data_models.py          # Modèles de données
│   ├── sync_manager.py         # Gestionnaire de sync
│   └── api.py                  # Endpoints API
├── metrics_collector/          # Collecteur de métriques
│   ├── dashboard/              # Dashboard web
│   │   ├── templates/          # Templates HTML
│   │   ├── static/             # Assets statiques
│   │   ├── aria_metrics_dashboard.py
│   │   └── export_handlers.py
│   └── ...
├── mobile_app/                 # Application mobile Flutter
│   ├── lib/
│   │   ├── models/             # Modèles de données
│   │   ├── services/           # Services métier
│   │   ├── screens/            # Écrans de l'app
│   │   ├── widgets/            # Widgets réutilisables
│   │   └── utils/              # Utilitaires
│   ├── android/                # Configuration Android
│   ├── ios/                    # Configuration iOS
│   └── pubspec.yaml
├── tests/                      # Tests unitaires
│   ├── test_health_connectors.py
│   ├── test_dashboard_web.py
│   └── test_mobile_app.py
├── docs/                       # Documentation
│   ├── API.md
│   ├── USER_GUIDE.md
│   └── DEVELOPER_GUIDE.md
├── main.py                     # Point d'entrée FastAPI
├── requirements.txt            # Dépendances Python
├── pyproject.toml             # Configuration du projet
└── README.md

```

---

## API Documentation

### Endpoints Principaux

#### Santé

```http
POST /api/health/sync
GET  /api/health/metrics/unified
GET  /api/health/activity
GET  /api/health/sleep
GET  /api/health/stress
GET  /api/health/data
GET  /api/health/connectors/status

```

#### Dashboard

```http
GET  /dashboard
GET  /dashboard/health
GET  /dashboard/pain
GET  /dashboard/patterns
GET  /dashboard/reports
POST /dashboard/export/pdf
POST /dashboard/export/excel
POST /dashboard/export/html

```

### Modèles de Données

#### ActivityData

```python
class ActivityData(BaseModel):
    date: datetime
    steps: int
    distance_meters: float
    calories_burned: float
    active_minutes: int
    source: str
    raw_data: dict

```

#### HealthData

```python
class HealthData(BaseModel):
    date: datetime
    heart_rate: Optional[int]
    blood_pressure_systolic: Optional[int]
    blood_pressure_diastolic: Optional[int]
    weight: Optional[float]
    height: Optional[float]
    bmi: Optional[float]
    blood_glucose: Optional[float]
    body_temperature: Optional[float]
    source: str
    raw_data: dict

```

### Authentification

```python
# JWT Token
headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

```

### Gestion des Erreurs

```python
# Codes d'erreur standardisés
{
    "error_code": 1001,
    "message": "Erreur de connexion réseau",
    "details": {...}
}

```

---

## Connecteurs de Santé

### Architecture des Connecteurs

Tous les connecteurs héritent de `BaseHealthConnector` :

```python
class BaseHealthConnector(ABC):
    @abstractmethod
    async def connect(self) -> bool:
        """Établit la connexion avec le service"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Ferme la connexion"""
        pass
    
    @abstractmethod
    async def get_activity_data(self, start_date: datetime, end_date: datetime) -> List[ActivityData]:
        """Récupère les données d'activité"""
        pass

```

### Samsung Health Connector

```python
class SamsungHealthConnector(BaseHealthConnector):
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.is_connected = False
    
    async def connect(self) -> bool:
        # Implémentation de la connexion Samsung Health
        pass

```

### Google Fit Connector

```python
class GoogleFitConnector(BaseHealthConnector):
    def __init__(self, credentials_path: str):
        self.credentials_path = credentials_path
        self.is_connected = False
    
    async def connect(self) -> bool:
        # Implémentation de la connexion Google Fit
        pass

```

### iOS Health Connector

```python
class IOSHealthConnector(BaseHealthConnector):
    def __init__(self, health_store: HealthStore):
        self.health_store = health_store
        self.is_connected = False
    
    async def connect(self) -> bool:
        # Implémentation de la connexion iOS Health
        pass

```

---

## Pattern Analysis

### Vue d'ensemble Pattern Analysis

Le module `pattern_analysis/` détecte automatiquement les corrélations entre douleur, sommeil, stress et autres facteurs.

### CorrelationAnalyzer

```python
from pattern_analysis.correlation_analyzer import CorrelationAnalyzer

analyzer = CorrelationAnalyzer()

# Analyse corrélation sommeil ↔ douleur
sleep_corr = analyzer.analyze_sleep_pain_correlation(days_back=30)

# Analyse corrélation stress ↔ douleur
stress_corr = analyzer.analyze_stress_pain_correlation(days_back=30)

# Détection déclencheurs récurrents
triggers = analyzer.detect_recurrent_triggers(days_back=30, min_occurrences=3)

# Analyse complète
comprehensive = analyzer.get_comprehensive_analysis(days_back=30)
```

### Endpoints API

```python
# Analyse complète
GET /api/patterns/patterns/recent?days=30

# Corrélations spécifiques
GET /api/patterns/correlations/sleep-pain?days=30
GET /api/patterns/correlations/stress-pain?days=30

# Déclencheurs récurrents
GET /api/patterns/triggers/recurrent?days=30&min_occurrences=3

# Analyse personnalisée
POST /api/patterns/analyze
{
  "days_back": 30,
  "analysis_type": "comprehensive"  # "comprehensive", "sleep", "stress", "triggers"
}
```

### Algorithmes

- **Corrélation de Pearson** : Calcul simple et local pour corrélations sommeil/stress
- **Détection de patterns** : Comptage de déclencheurs récurrents
- **Patterns temporels** : Analyse par heure et jour de la semaine
- **100% local** : Aucune donnée externe, traitement entièrement local

---

## Prediction Engine

### Vue d'ensemble Prediction Engine

Le module `prediction_engine/` prédit les épisodes de douleur basés sur les patterns historiques et le contexte actuel.

### ARIAMLAnalyzer

```python
from prediction_engine.ml_analyzer import ARIAMLAnalyzer

ml_analyzer = ARIAMLAnalyzer()

# Prédiction basée sur contexte
context = {
    "stress_level": 0.8,
    "fatigue_level": 0.6,
    "activity_intensity": 0.4
}
prediction = ml_analyzer.predict_pain_episode(context)

# Analyse des patterns historiques
patterns = ml_analyzer.analyze_pain_patterns(days=14)

# Analytics
summary = ml_analyzer.get_analytics_summary()
```

### Intégration avec Pattern Analysis

Le `prediction_engine` utilise automatiquement les corrélations détectées par `pattern_analysis` :

```python
# Dans prediction_engine/api.py
correlation_analyzer = CorrelationAnalyzer()
sleep_corr = correlation_analyzer.analyze_sleep_pain_correlation(days_back=7)
stress_corr = correlation_analyzer.analyze_stress_pain_correlation(days_back=7)

# Ajustement de la prédiction selon corrélations
if sleep_corr.get("correlation", 0) < -0.4:
    # Manque de sommeil → risque élevé
    predicted_intensity += 1
```

### Endpoints API

```python
# Prédictions actuelles
GET /api/predictions/predictions/current?include_correlations=true

# Prédiction personnalisée
POST /api/predictions/predict
{
  "stress_level": 0.8,
  "fatigue_level": 0.6,
  "activity_intensity": 0.4,
  "include_correlations": true
}

# Analytics
GET /api/predictions/analytics

# Entraînement (réanalyse)
POST /api/predictions/train
{
  "days_back": 14
}
```

### Algorithmes de Prédiction

- **Règles basées sur patterns** : Utilise les patterns détectés historiquement
- **Facteurs contextuels** : Stress, fatigue, activité, heure, jour
- **Ajustement corrélations** : Enrichit avec corrélations sommeil/stress
- **Confiance adaptative** : Plus de données = plus de confiance

---

## Synchronisation CIA et Granularité

### Vue d'ensemble CIA Sync

Le module `cia_sync/` gère la synchronisation bidirectionnelle avec ARKALIA CIA, avec un système de granularité permettant un contrôle fin de ce qui est synchronisé.

### AutoSyncManager

```python
from cia_sync.auto_sync import get_auto_sync_manager

# Récupérer le gestionnaire
auto_sync = get_auto_sync_manager()

# Démarrer la synchronisation automatique (60 min par défaut)
auto_sync.start(interval_minutes=60)

# Forcer une synchronisation immédiate
auto_sync.sync_now()

# Arrêter la synchronisation
auto_sync.stop()

# Obtenir le statut
status = auto_sync.get_status()
```

### GranularityConfigManager

```python
from cia_sync.granularity_config import (
    GranularityConfig,
    SyncLevel,
    DataType,
    get_config_manager,
)

# Récupérer le gestionnaire
config_manager = get_config_manager()

# Créer une configuration personnalisée
config = GranularityConfig(
    pain_entries_level=SyncLevel.AGGREGATED,
    patterns_level=SyncLevel.SUMMARY,
    predictions_level=SyncLevel.NONE,
    anonymize_personal_data=True,
    anonymize_timestamps=True,
    sync_period_days=7,
)

# Sauvegarder la configuration
config_manager.save_config(config, config_name="psy_mode")

# Charger une configuration
config = config_manager.load_config("psy_mode")

# Obtenir la configuration par défaut
default_config = config_manager.get_default_config()
```

### Niveaux de Synchronisation

```python
from cia_sync.granularity_config import SyncLevel, DataType

# Vérifier si un type de données doit être synchronisé
if config.should_sync(DataType.PAIN_ENTRIES):
    # Synchroniser les entrées de douleur
    pass

# Obtenir le niveau de synchronisation
level = config.get_sync_level(DataType.PATTERNS)
# Retourne: SyncLevel.SUMMARY, AGGREGATED, DETAILED, ou NONE
```

### Anonymisation

```python
# Appliquer l'anonymisation selon la configuration
anonymized_data = config_manager.apply_anonymization(
    data={"intensity": 7, "location": "maison", "notes": "douleur"},
    config=config
)
# Résultat: {"intensity": 7, "location": None, "notes": None}
```

### Agrégation

```python
# Agrégation intelligente de données
data_list = [
    {"intensity": 7, "physical_trigger": "stress"},
    {"intensity": 8, "physical_trigger": "stress"},
    {"intensity": 6, "physical_trigger": "fatigue"},
]

aggregated = config_manager.aggregate_data(data_list, config)
# Résultat:
# {
#   "count": 3,
#   "statistics": {
#     "avg_intensity": 7.0,
#     "max_intensity": 8,
#     "min_intensity": 6
#   },
#   "common_triggers": {"stress": 2, "fatigue": 1}
# }
```

### Endpoints API

```python
# Récupérer une configuration
GET /api/sync/granularity/config?config_name=default

# Sauvegarder une configuration
POST /api/sync/granularity/config?config_name=psy_mode
{
  "pain_entries_level": "summary",
  "anonymize_personal_data": true,
  ...
}

# Liste des configurations
GET /api/sync/granularity/configs

# Supprimer une configuration
DELETE /api/sync/granularity/config?config_name=psy_mode

# Niveaux disponibles
GET /api/sync/granularity/sync-levels
```

### Intégration dans AutoSyncManager

Le `AutoSyncManager` utilise automatiquement la configuration de granularité :

```python
# Dans _perform_sync()
config = self.config_manager.get_default_config()

# Synchroniser selon la granularité
if config.should_sync(DataType.PAIN_ENTRIES):
    pain_data = self._sync_pain_entries(config)
    # Applique anonymisation et agrégation selon config
```

### Cas d'usage

**Configuration pour psychologue** :

```python
psy_config = GranularityConfig(
    pain_entries_level=SyncLevel.SUMMARY,
    patterns_level=SyncLevel.SUMMARY,
    predictions_level=SyncLevel.NONE,
    anonymize_personal_data=True,
    anonymize_timestamps=True,
    anonymize_locations=True,
    anonymize_notes=True,
    sync_period_days=7,
)
```

**Configuration pour médecin** :

```python
doctor_config = GranularityConfig(
    pain_entries_level=SyncLevel.AGGREGATED,
    patterns_level=SyncLevel.SUMMARY,
    predictions_level=SyncLevel.SUMMARY,
    anonymize_personal_data=False,
    anonymize_timestamps=False,
    anonymize_locations=False,
    anonymize_notes=False,
    sync_period_days=30,
)
```

---

## Dashboard Web

### Architecture Frontend

#### Templates Jinja2

```html
<!-- dashboard.html -->
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{{ title }} - ARKALIA ARIA</title>
    <link rel="stylesheet" href="/static/dashboard.css">
</head>
<body>
    <div class="dashboard-container">
        <!-- Contenu du dashboard -->
    </div>
    <script src="/static/dashboard.js"></script>
</body>
</html>

```

#### CSS Moderne

```css
/* Variables CSS personnalisées */
:root {
    --primary-color: #2563eb;
    --secondary-color: #64748b;
    --success-color: #10b981;
    --error-color: #ef4444;
}

/* Classes utilitaires */
.metric-card {
    background: var(--bg-primary);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-md);
}

```

#### JavaScript ES6+

```javascript
class ARKALIADashboard {
    constructor() {
        this.charts = new Map();
        this.init();
    }
    
    async syncAllData() {
        const response = await fetch('/api/health/sync', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        // Traitement de la réponse
    }
}

```

### Gestion des Exports

#### PDF Export

```python
class PDFExportHandler:
    def generate_report(self, data: dict) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        # Génération du PDF
        return buffer.getvalue()

```

#### Excel Export

```python
class ExcelExportHandler:
    def generate_report(self, data: dict) -> bytes:
        workbook = Workbook()
        worksheet = workbook.active
        # Génération du Excel
        return workbook.save()

```

---

## Application Mobile

### Architecture Flutter

#### Structure des Modèles

```dart
// models/health_data.dart
class HealthData {
  final DateTime date;
  final int? heartRate;
  final double? bloodPressureSystolic;
  final double? bloodPressureDiastolic;
  final double? weight;
  final double? height;
  final double? bmi;
  final String source;
  final Map<String, dynamic> rawData;

  const HealthData({
    required this.date,
    this.heartRate,
    this.bloodPressureSystolic,
    this.bloodPressureDiastolic,
    this.weight,
    this.height,
    this.bmi,
    required this.source,
    required this.rawData,
  });
}

```

#### Services

```dart
// services/health_connector_service.dart
class HealthConnectorService {
  static final HealthConnectorService _instance = HealthConnectorService._internal();
  factory HealthConnectorService() => _instance;
  HealthConnectorService._internal();

  Future<List<HealthData>> getHealthData(DateTime startDate, DateTime endDate) async {
    // Implémentation de la récupération des données
  }
}

```

#### Écrans

```dart
// screens/dashboard_screen.dart
class DashboardScreen extends ConsumerStatefulWidget {
  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Dashboard')),
      body: Column(
        children: [
          // Widgets du dashboard
        ],
      ),
    );
  }
}

```

### Gestion d'État avec Riverpod

```dart
// providers/health_provider.dart
final healthDataProvider = StateNotifierProvider<HealthDataNotifier, List<HealthData>>((ref) {
  return HealthDataNotifier();
});

class HealthDataNotifier extends StateNotifier<List<HealthData>> {
  HealthDataNotifier() : super([]);
  
  Future<void> loadHealthData() async {
    // Chargement des données
  }
}

```

---

## Base de Données

### Schéma PostgreSQL

```sql
-- Table des utilisateurs
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table des données de santé
CREATE TABLE health_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    date TIMESTAMP NOT NULL,
    heart_rate INTEGER,
    blood_pressure_systolic INTEGER,
    blood_pressure_diastolic INTEGER,
    weight DECIMAL(5,2),
    height DECIMAL(5,2),
    bmi DECIMAL(4,2),
    source VARCHAR(50) NOT NULL,
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index pour les performances
CREATE INDEX idx_health_data_user_date ON health_data(user_id, date);
CREATE INDEX idx_health_data_source ON health_data(source);

```

### Migrations Alembic

```python
# alembic/versions/001_create_users_table.py
def upgrade():
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

```

---

## Tests et Qualité

### Tests Unitaires

```python
# tests/test_health_connectors.py
import pytest
from health_connectors import SamsungHealthConnector

class TestSamsungHealthConnector:
    @pytest.mark.asyncio
    async def test_connect(self):
        connector = SamsungHealthConnector("api_key", "api_secret")
        result = await connector.connect()
        assert result is True
        assert connector.is_connected is True

```

### Tests d'Intégration

```python
# tests/test_api_integration.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_sync_endpoint():
    response = client.post("/api/health/sync", json={"days_back": 7})
    assert response.status_code == 200
    assert "success" in response.json()

```

### Tests Flutter

```dart
// test/widget_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:arkalia_aria/main.dart';

void main() {
  testWidgets('Dashboard loads correctly', (WidgetTester tester) async {
    await tester.pumpWidget(ARKALIAARIAApp());
    expect(find.text('ARKALIA ARIA'), findsOneWidget);
  });
}

```

### Qualité du Code

#### Ruff (Linting)

```bash
ruff check .
ruff format .

```

#### Black (Formatage)

```bash
black .

```

#### Mypy (Type Checking)

```bash
mypy .

```

#### Coverage

```bash
pytest --cov=health_connectors --cov-report=html

```

---

## Déploiement

### Docker

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/arkalia
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=arkalia
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

```

### GitHub Actions

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest
          ruff check .
          mypy .

```

---

## Contributions

### Processus de Contribution

1. **Fork** le repository
2. **Créer** une branche feature (`git checkout -b feature/amazing-feature`)
3. **Commit** vos changements (`git commit -m 'Add amazing feature'`)
4. **Push** vers la branche (`git push origin feature/amazing-feature`)
5. **Ouvrir** une Pull Request

### Standards de Code

#### Python

- **PEP 8** : Style de code Python
- **Type Hints** : Annotations de type obligatoires
- **Docstrings** : Documentation des fonctions
- **Tests** : Couverture minimale de 80%

#### Dart/Flutter

- **Effective Dart** : Guide de style Dart
- **Widget Tests** : Tests pour tous les widgets
- **Integration Tests** : Tests d'intégration
- **Performance** : Optimisation des performances

#### JavaScript

- **ESLint** : Linting JavaScript
- **Prettier** : Formatage automatique
- **JSDoc** : Documentation des fonctions
- **Unit Tests** : Tests avec Jest

### Guidelines

#### Commits

```text
feat: add new health connector
fix: resolve sync issue
docs: update API documentation
style: format code with black
refactor: improve error handling
test: add unit tests for sync manager

```

#### Pull Requests

- **Titre** : Description claire et concise
- **Description** : Détails des changements
- **Tests** : Preuve que les tests passent
- **Documentation** : Mise à jour si nécessaire

---

## 📚 Ressources

### Documentation Externe

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Flutter Documentation](https://docs.flutter.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)

### Outils de Développement

- [VS Code](https://code.visualstudio.com/)
- [Android Studio](https://developer.android.com/studio)
- [Postman](https://www.postman.com/)
- [DBeaver](https://dbeaver.io/)

### Communauté

- [GitHub Discussions](https://github.com/arkalia-aria/arkalia-aria/discussions)
- [Discord Server](https://discord.gg/arkalia-aria)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/arkalia-aria)

---

## Troubleshooting

### Problèmes Courants

#### Erreur de connexion à la base de données

```bash
# Vérifier les permissions
ls -la aria_pain.db

# Recréer la base si nécessaire
rm aria_pain.db
python -c "from core.database import DatabaseManager; DatabaseManager().init_database()"

```

#### Tests qui échouent

```bash
# Nettoyer le cache
rm -rf .pytest_cache
rm -rf __pycache__

# Relancer les tests
pytest tests/ -v

```

#### Problèmes de performance

```bash
# Vérifier les processus lourds
ps aux | grep python

# Nettoyer les caches
make clean-cache

```

### Logs et Debug

#### Activer les logs détaillés

```python
import logging
logging.basicConfig(level=logging.DEBUG)

```

#### Vérifier les métriques

```bash
curl <http://localhost:8001/metrics>

```

---

## Performance

### Optimisations Implémentées

- **Cache intelligent** : TTL 60s pour les requêtes fréquentes
- **Lazy loading** : Import des modules lourds à la demande
- **Connexion DB unique** : Singleton pattern pour éviter les doublons
- **Compression** : Gzip pour les réponses API

### Monitoring des Performances

```bash
# Métriques système (nécessite ARIA_ENABLE_METRICS=true)
curl <http://localhost:8001/metrics>

# Métriques santé unifiées
curl <http://localhost:8001/health/metrics/unified?days_back=7>

```

### Optimisations Recommandées

- [ ] Cache Redis pour les sessions
- [ ] CDN pour les assets statiques
- [ ] Compression brotli
- [ ] Mise en cache des calculs ML
- [ ] Indexation des requêtes DB fréquentes

---

## Sécurité

### Bonnes Pratiques

- **Secrets** : Toujours utiliser des variables d'environnement
- **HTTPS** : Obligatoire en production
- **Validation** : Toutes les entrées utilisateur
- **Logs** : Ne jamais logger de données sensibles

### Audit de Sécurité

```bash
# Scan de sécurité complet
bandit -r . -f json -o reports/bandit-report.json

# Vérification des dépendances
safety check --json --output reports/safety-report.json

# Audit personnalisé
python -m devops_automation.security.aria_security_validator

```

### Configuration Sécurisée

- [ ] Chiffrement des données au repos
- [ ] Rotation automatique des tokens
- [ ] Limitation des tentatives de connexion
- [ ] Audit des accès aux données sensibles

---

## Monitoring

### Métriques Disponibles

- **Système** : CPU, RAM, disque, réseau
- **Application** : Requêtes, erreurs, temps de réponse
- **Base de données** : Connexions, requêtes, taille
- **Sécurité** : Tentatives d'intrusion, accès suspects

### Alertes Configurées

- [ ] CPU > 80% pendant 5 minutes
- [ ] RAM > 90% pendant 2 minutes
- [ ] Erreurs > 10% des requêtes
- [ ] Temps de réponse > 5 secondes
- [ ] Tentatives de connexion suspectes

### Dashboards

- **Grafana** : Métriques système et application
- **Prometheus** : Collecte des métriques
- **ELK Stack** : Logs et analyses

---

## Référence Technique Complète

### Structure Détaillée du Projet

```text
/Volumes/T7/arkalia-aria/
├── main.py                          # Point d'entrée principal
├── requirements.txt                 # Dépendances Python (versions épinglées)
├── pyproject.toml                   # Configuration projet et outils
├── docker-compose.yml              # Configuration Docker
├── Dockerfile                      # Image Docker
├── mkdocs.yml                      # Configuration documentation
├── env.example                     # Variables d'environnement exemple
├── Makefile                        # Scripts de build
├── .gitignore                      # Fichiers ignorés par Git
├── CODEOWNERS                      # Propriétaires du code
├── CONTRIBUTING.md                 # Guide contribution
├── README.md                       # Documentation principale
├── aria_pain.db                    # Base de données SQLite principale
├── aria_research.db                # Base de données recherche
├── arkalia_aria_venv/              # Environnement virtuel Python
├── config/                         # Configuration centralisée
│   ├── deployment.json             # Configuration déploiement
│   ├── monitoring.json             # Configuration monitoring
│   ├── nginx.conf                  # Configuration Nginx
│   ├── performance.toml            # Configuration performance
│   ├── .bandit                     # Configuration Bandit
│   └── .safety                     # Configuration Safety
├── core/                           # Module centralisé
│   ├── __init__.py
│   ├── api_base.py                 # BaseAPI pour standardisation
│   ├── cache.py                    # CacheManager
│   ├── config.py                   # Configuration centralisée
│   ├── database.py                 # DatabaseManager (Singleton)
│   ├── exceptions.py               # Exceptions personnalisées
│   └── logging.py                  # Système de logging
├── pain_tracking/                  # Module suivi douleur
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   └── __pycache__/
├── pattern_analysis/               # Module analyse patterns
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   ├── emotion_analyzer.py         # Analyseur émotionnel
│   └── __pycache__/
├── prediction_engine/              # Module moteur prédiction
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   ├── ml_analyzer.py              # Analyseur ML
│   └── __pycache__/
├── research_tools/                 # Module outils recherche
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   ├── data_collector.py           # Collecteur de données
│   └── __pycache__/
├── health_connectors/              # Module connecteurs santé
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   ├── base_connector.py           # Connecteur de base
│   ├── config.py                   # Configuration connecteurs
│   ├── data_models.py              # Modèles de données
│   ├── google_fit_connector.py     # Connecteur Google Fit
│   ├── ios_health_connector.py     # Connecteur Apple HealthKit
│   ├── samsung_health_connector.py # Connecteur Samsung Health
│   ├── sync_manager.py             # Gestionnaire synchronisation
│   └── __pycache__/
├── audio_voice/                    # Module audio/voix
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   └── __pycache__/
├── cia_sync/                       # Module synchronisation CIA
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   └── __pycache__/
├── metrics_collector/              # Module collecte métriques
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   ├── cli.py                      # Interface CLI
│   ├── collectors/                 # Collecteurs métriques
│   ├── dashboard/                  # Dashboard web
│   ├── exporters/                  # Exportateurs
│   ├── validators/                 # Validateurs
│   └── __pycache__/
├── devops_automation/              # Module DevOps
│   ├── __init__.py
│   ├── api.py                      # API FastAPI
│   ├── cicd/                       # CI/CD
│   ├── deployment/                 # Déploiement
│   ├── monitoring/                 # Monitoring
│   ├── quality/                    # Qualité code
│   ├── security/                   # Sécurité
│   └── scripts/                    # Scripts
├── mobile_app/                     # Application mobile Flutter
│   ├── android/                    # Configuration Android
│   ├── ios/                        # Configuration iOS
│   ├── lib/                        # Code Dart
│   ├── assets/                     # Assets
│   ├── pubspec.yaml                # Dépendances Flutter
│   └── pubspec.lock                # Lock file Flutter
├── tests/                          # Tests
│   ├── __init__.py
│   ├── integration/                # Tests d'intégration
│   ├── unit/                       # Tests unitaires
│   ├── test_dashboard_web.py       # Tests dashboard
│   ├── test_health_api.py          # Tests API santé
│   ├── test_health_connectors.py   # Tests connecteurs
│   ├── test_integration.py         # Tests intégration
│   ├── test_metrics_collector.py   # Tests métriques
│   └── README.md                   # Documentation tests
├── docs/                           # Documentation
│   ├── index.md                    # Page d'accueil
│   ├── PROFESSIONAL_WORKFLOW.md    # Workflow professionnel
│   ├── PROJECT_STATUS.md           # Statut projet
│   ├── VALIDATION_CHECKLIST.md     # Checklist validation
│   ├── DEVELOPER_GUIDE.md          # Guide développeur
│   ├── API_REFERENCE.md            # Référence API
│   ├── MOBILE_APP.md               # Documentation mobile
│   └── ...                         # Autres docs
├── reports/                        # Rapports générés
│   ├── bandit-report.json          # Rapport Bandit
│   ├── coverage.json               # Rapport couverture
│   ├── safety-report.json          # Rapport Safety
│   └── README.md                    # Documentation rapports
├── .github/                        # GitHub Actions
│   └── workflows/                  # Workflows CI/CD
│       ├── ci-cd.yml               # Workflow principal
│       └── security.yml             # Workflow sécurité
└── dacc/                           # Données de test (à nettoyer)
    └── ...                         # Fichiers de test

```

### Commandes Essentielles

#### Développement Local

```bash
# Activer l'environnement virtuel
source arkalia_aria_venv/bin/activate

# Lancer l'API en mode développement
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
# OU directement
python main.py

# Lancer l'API en mode production
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4

# Vérifier l'état de l'API
curl http://127.0.0.1:8001/health

```

#### Tests

```bash
# Tests rapides (mode fail-fast)
python -m pytest tests/ --tb=short -x

# Tests complets avec couverture
python -m pytest tests/ --cov=. --cov-report=html

# Tests d'intégration uniquement
python -m pytest tests/integration/ -v

# Tests unitaires uniquement
python -m pytest tests/unit/ -v

# Tests avec marqueurs spécifiques
python -m pytest tests/ -m "fast" -v
python -m pytest tests/ -m "not slow" -v

```

#### Qualité du Code

```bash
# Formater le code
black .

# Linter et corrections automatiques
ruff check . --fix

# Vérification des types
mypy .

# Audit de sécurité
bandit -r . -f json -o reports/bandit-report.json
safety check --json --output reports/safety-report.json

# Tous les outils de qualité
black . && ruff check . --fix && mypy . && bandit -r . && safety check

```

#### Git & Déploiement

```bash
# Voir l'état du repository
git status

# Ajouter tous les fichiers modifiés
git add .

# Commit avec message descriptif
git commit -m "feat: ajout fonctionnalité X"

# Push vers le repository distant
git push

# Voir l'historique des commits
git log --oneline -10

```

#### Docker

```bash
# Construire l'image Docker
docker build -t arkalia-aria .

# Lancer avec Docker Compose
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

```

### Endpoints API Principaux

#### Endpoints Standardisés (BaseAPI)

- `GET /health` - Vérification de santé
- `GET /status` - Statut détaillé
- `GET /metrics` - Métriques système

#### Suivi de Douleur (`/api/pain`)

- `GET /api/pain/status` - Statut du module
- `POST /api/pain/quick-entry` - Saisie rapide douleur
- `POST /api/pain/entry` - Saisie détaillée douleur
- `GET /api/pain/entries` - Liste des entrées
- `GET /api/pain/entries/recent` - Entrées récentes
- `GET /api/pain/suggestions` - Suggestions de traitement
- `GET /api/pain/export/csv` - Export CSV
- `GET /api/pain/export/pdf` - Export PDF
- `GET /api/pain/export/excel` - Export Excel
- `GET /api/pain/export/psy-report` - Export rapport psy
- `DELETE /api/pain/entries/{entry_id}` - Supprimer une entrée
- `DELETE /api/pain/entries` - Supprimer toutes les entrées

#### Analyse de Patterns (`/api/patterns`)

- `GET /api/patterns/emotions` - Analyse émotionnelle
- `GET /api/patterns/trends` - Tendances temporelles
- `GET /api/patterns/correlations` - Corrélations
- `GET /api/patterns/reports` - Rapports d'analyse

#### Moteur de Prédiction (`/api/predictions`)

- `POST /api/predictions/analyze` - Analyse ML
- `GET /api/predictions/trends` - Prédictions de tendances
- `GET /api/predictions/crises` - Prédiction de crises
- `GET /api/predictions/recommendations` - Recommandations

#### Outils de Recherche (`/api/research`)

- `POST /api/research/collect` - Collecte de données
- `GET /api/research/experiments` - Expérimentations
- `GET /api/research/analytics` - Analytics avancées
- `GET /api/research/export` - Export recherche

#### Connecteurs Santé (`/health`)

- `GET /health/connectors/status` - Statut de tous les connecteurs
- `POST /health/samsung/sync` - Synchronisation Samsung Health
- `POST /health/google/sync` - Synchronisation Google Fit
- `POST /health/ios/sync` - Synchronisation iOS Health
- `POST /health/sync/all` - Synchronisation de tous les connecteurs
- `GET /health/data/activity` - Données d'activité unifiées
- `GET /health/data/sleep` - Données de sommeil unifiées
- `GET /health/data/stress` - Données de stress unifiées
- `GET /health/data/health` - Données de santé unifiées
- `GET /health/metrics/unified` - Métriques unifiées pour dashboard
- `GET /health/config` - Configuration des connecteurs
- `PUT /health/config` - Mettre à jour la configuration

#### Synchronisation CIA (`/api/sync`)

- `GET /api/sync/status` - Statut de la connexion CIA
- `GET /api/sync/connection` - Détails de la connexion
- `POST /api/sync/selective` - Synchronisation sélective
- `GET /api/sync/psy-mode` - Mode présentation psy
- `POST /api/sync/push-data` - Envoyer des données vers CIA

#### Audio/Voix (`/api/audio`)

- `POST /api/audio/transcribe` - Transcription
- `POST /api/audio/analyze` - Analyse audio
- `GET /api/audio/recordings` - Enregistrements

#### Métriques (`/metrics`) - Optionnel (ARIA_ENABLE_METRICS=true)

- `GET /metrics` - Métriques complètes
- `GET /metrics/health` - Statut de santé
- `GET /metrics/dashboard` - Dashboard HTML
- `GET /metrics/export/{format}` - Export (json, markdown, html, csv)
- `POST /metrics/collect` - Collecte forcée
- `GET /metrics/validate` - Validation des métriques
- `GET /metrics/summary` - Résumé des métriques
- `GET /metrics/alerts` - Alertes et recommandations

#### DevOps (`/api/devops`)

- `GET /api/devops/status` - Statut DevOps
- `POST /api/devops/deploy` - Déploiement
- `GET /api/devops/logs` - Logs système
- `POST /api/devops/backup` - Sauvegarde

### Base de Données Référence

#### Fichiers de Base de Données

- `aria_pain.db` - Base principale (données douleur)
- `aria_research.db` - Base recherche (expérimentations)

#### Tables Principales

```sql
-- Table des entrées de douleur
CREATE TABLE pain_entries (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    pain_level INTEGER NOT NULL,
    location TEXT,
    description TEXT,
    emotions TEXT,
    activities TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table des patterns émotionnels
CREATE TABLE emotion_patterns (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    emotion_type TEXT NOT NULL,
    intensity REAL NOT NULL,
    context TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table des prédictions ML
CREATE TABLE ml_predictions (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    prediction_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    data TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

```

#### Connexion à la Base de Données

```python
from core.database import DatabaseManager

# Obtenir l'instance singleton
db = DatabaseManager()

# Exécuter une requête
result = db.execute_query("SELECT * FROM pain_entries WHERE user_id = ?", (user_id,))

# Exécuter une requête avec retour de données
data = db.fetch_all("SELECT * FROM pain_entries ORDER BY timestamp DESC LIMIT 10")

```

### Configuration Référence

#### Variables d'Environnement

```bash
# Copier le fichier d'exemple
cp env.example .env

# Variables principales
ARIA_DB_PATH=aria_pain.db
ARIA_LOG_LEVEL=INFO
ARIA_MAX_REQUEST_SIZE=10485760
ARIA_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
ARIA_REDIS_URL=redis://localhost:6379
ARIA_SECRET_KEY=your-secret-key-here

```

#### Configuration Centralisée

```python
from core.config import Config

# Obtenir la configuration
config = Config()

# Accéder aux valeurs
db_path = config.get("ARIA_DB_PATH", "aria_pain.db")
log_level = config.get("ARIA_LOG_LEVEL", "INFO")
max_request_size = config.get("ARIA_MAX_REQUEST_SIZE", 10485760)

```

### Application Mobile Flutter

#### Structure Flutter

```text
mobile_app/
├── lib/
│   ├── main.dart                    # Point d'entrée
│   ├── models/                      # Modèles de données
│   ├── services/                    # Services API
│   ├── screens/                     # Écrans
│   ├── widgets/                     # Widgets réutilisables
│   └── utils/                       # Utilitaires
├── android/                         # Configuration Android
├── ios/                            # Configuration iOS
├── assets/                         # Assets (images, etc.)
├── pubspec.yaml                    # Dépendances Flutter
└── pubspec.lock                    # Lock file

```

#### Commandes Flutter

```bash
# Aller dans le dossier mobile
cd mobile_app/

# Installer les dépendances
flutter pub get

# Lancer l'app en mode debug
flutter run

# Lancer l'app sur iOS
flutter run -d ios

# Lancer l'app sur Android
flutter run -d android

# Construire l'app pour production
flutter build apk --release
flutter build ios --release

```

### Docker & Déploiement

#### Docker Compose

```yaml
version: '3.8'
services:
  aria:
    build: .
    ports:
      - "8001:8001"
    environment:
      - ARIA_DB_PATH=/app/aria_pain.db
      - ARIA_LOG_LEVEL=INFO
    volumes:
      - ./aria_pain.db:/app/aria_pain.db
      - ./aria_research.db:/app/aria_research.db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - aria
    restart: unless-stopped

```

#### Déploiement Production

```bash
# Construire l'image
docker build -t arkalia-aria:latest .

# Lancer avec Docker Compose
docker-compose up -d

# Vérifier les logs
docker-compose logs -f aria

# Arrêter les services
docker-compose down

```

### Debugging & Monitoring

#### Logs

```bash
# Voir les logs de l'application
tail -f logs/app.log

# Voir les logs Docker
docker-compose logs -f aria

# Voir les logs système
journalctl -u aria -f

```

#### Monitoring

```bash
# Vérifier l'état de l'API
curl http://127.0.0.1:8001/health

# Vérifier les métriques (nécessite ARIA_ENABLE_METRICS=true)
curl http://127.0.0.1:8001/metrics

# Vérifier les processus
ps aux | grep python

# Vérifier les ports
lsof -i :8001

# Vérifier l'utilisation mémoire
free -h

```

#### Base de Données

```bash
# Ouvrir la base de données SQLite
sqlite3 aria_pain.db

# Voir les tables
.tables

# Voir la structure d'une table
.schema pain_entries

# Exécuter une requête
SELECT * FROM pain_entries LIMIT 5;

# Quitter
.quit

```

### Dépannage Courant

#### L'API ne démarre pas

```bash
# Vérifier le port
lsof -i :8001

# Tuer le processus qui utilise le port
kill -9 $(lsof -t -i:8001)

# Relancer l'API
python main.py

```

#### Tests échouent

```bash
# Vérifier les imports
python -c "import main"

# Vérifier les dépendances
pip list

# Relancer les tests avec plus de détails
python -m pytest tests/ -v --tb=long

```

#### Erreurs de base de données

```bash
# Vérifier que la base existe
ls -la aria_pain.db

# Vérifier les permissions
chmod 664 aria_pain.db

# Recréer la base si nécessaire
rm aria_pain.db
python -c "from core.database import DatabaseManager; db = DatabaseManager(); db.init_database()"

```

#### Problèmes de cache

```bash
# Nettoyer le cache Python
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Nettoyer le cache de tests
rm -rf .pytest_cache
rm -rf .coverage

```

### Ressources Utiles

#### Documentation

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Flutter Docs](https://flutter.dev/docs)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [Docker Docs](https://docs.docker.com/)

#### Outils de Développement

- [Postman](https://www.postman.com/) - Test API
- [Insomnia](https://insomnia.rest/) - Test API alternatif
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Interface graphique SQLite
- [Flutter Inspector](https://flutter.dev/docs/development/tools/devtools/inspector) - Debug Flutter

#### Sécurité & RGPD

- [CNIL](https://www.cnil.fr/) - Commission Nationale Informatique et Libertés
- [RGPD Guide](https://www.cnil.fr/fr/reglement-europeen-protection-donnees)
- [Bandit Docs](https://bandit.readthedocs.io/)
- [Safety Docs](https://pyup.io/safety/)

---

*Dernière mise à jour :* Novembre 2025
*Version du guide :* 1.0.0 (aligné avec version ARIA 1.0.0)
