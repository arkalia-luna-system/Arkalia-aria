# Guide Développeur ARKALIA ARIA
*Documentation technique complète pour les développeurs*

**Dernière mise à jour : 23 Septembre 2025**

## 📋 Table des Matières

1. [Architecture Générale](#architecture-générale)
2. [🆕 Module Core](#module-core)
3. [🆕 BaseAPI](#baseapi)
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

---

## 🆕 Module Core

### Vue d'Ensemble
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

## 🆕 BaseAPI

### Vue d'Ensemble
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

## 🏗️ Architecture Générale

### Vue d'Ensemble

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

## 🚀 Installation et Configuration

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
git clone https://github.com/arkalia-aria/arkalia-aria.git
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

## 📁 Structure du Projet

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

## 🔌 API Documentation

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

## 💊 Connecteurs de Santé

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

## 🖥️ Dashboard Web

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

## 📱 Application Mobile

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

## 🗄️ Base de Données

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

## 🧪 Tests et Qualité

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

## 🚀 Déploiement

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

## 🤝 Contributions

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

*Dernière mise à jour : Septembre 2024*
*Version du guide : 1.0.0*