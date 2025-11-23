# Guide Développeur

**ARKALIA ARIA** — Documentation technique complète

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

```
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

### Vue d'ensemble
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

### Vue d'ensemble

ARKALIA ARIA suit une architecture microservices modulaire avec les composants suivants :

```
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

```
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

### Vue d'ensemble

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

### Vue d'ensemble

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

### Vue d'ensemble

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

```
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

*Dernière mise à jour :* Novembre 2025  
*Version du guide :* 2.0.0
