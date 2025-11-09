# 🔧 Référence Technique ARKALIA ARIA

**Dernière mise à jour : 25 Janvier 2025**

## 📁 **Structure du Projet**

```
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
│   ├── ACTION_PLAN.md              # Plan d'action
│   ├── SOLO_WORKFLOW.md            # Workflow solo
│   ├── TODO_SIMPLE.md              # TODO simple
│   ├── PROJECT_STATUS.md           # Statut projet
│   ├── SECURITY_RGPD_CHECKLIST.md  # Checklist RGPD
│   ├── DEVELOPER_GUIDE.md          # Guide développeur
│   ├── API_REFERENCE.md            # Référence API
│   ├── MOBILE_APP.md               # Documentation mobile
│   ├── MODULE_STATUS.md            # Statut modules
│   ├── TECHNICAL_REFERENCE.md      # Cette référence
│   └── ...                         # Autres docs
├── reports/                        # Rapports générés
│   ├── bandit-report.json          # Rapport Bandit
│   ├── coverage.json               # Rapport couverture
│   ├── safety-report.json          # Rapport Safety
│   └── README.md                   # Documentation rapports
├── .github/                        # GitHub Actions
│   └── workflows/                  # Workflows CI/CD
│       ├── ci-cd.yml               # Workflow principal
│       └── security.yml            # Workflow sécurité
└── dacc/                           # Données de test (à nettoyer)
    └── ...                         # Fichiers de test
```

## 🚀 **Commandes Essentielles**

### **Développement Local**
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

### **Tests**
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

### **Qualité du Code**
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

### **Git & Déploiement**
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

### **Docker**
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

## 🔗 **Endpoints API Principaux**

### **Endpoints Standardisés (BaseAPI)**
- `GET /health` - Vérification de santé
- `GET /status` - Statut détaillé
- `GET /metrics` - Métriques système

### **Suivi de Douleur (`/api/pain`)**
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

### **Analyse de Patterns (`/api/patterns`)**
- `GET /api/patterns/emotions` - Analyse émotionnelle
- `GET /api/patterns/trends` - Tendances temporelles
- `GET /api/patterns/correlations` - Corrélations
- `GET /api/patterns/reports` - Rapports d'analyse

### **Moteur de Prédiction (`/api/predictions`)**
- `POST /api/predictions/analyze` - Analyse ML
- `GET /api/predictions/trends` - Prédictions de tendances
- `GET /api/predictions/crises` - Prédiction de crises
- `GET /api/predictions/recommendations` - Recommandations

### **Outils de Recherche (`/api/research`)**
- `POST /api/research/collect` - Collecte de données
- `GET /api/research/experiments` - Expérimentations
- `GET /api/research/analytics` - Analytics avancées
- `GET /api/research/export` - Export recherche

### **Connecteurs Santé (`/health`)**
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

### **Synchronisation CIA (`/api/sync`)**
- `GET /api/sync/status` - Statut de la connexion CIA
- `GET /api/sync/connection` - Détails de la connexion
- `POST /api/sync/selective` - Synchronisation sélective
- `GET /api/sync/psy-mode` - Mode présentation psy
- `POST /api/sync/push-data` - Envoyer des données vers CIA

### **Audio/Voix (`/api/audio`)**
- `POST /api/audio/transcribe` - Transcription
- `POST /api/audio/analyze` - Analyse audio
- `GET /api/audio/recordings` - Enregistrements

### **Métriques (`/metrics`) - Optionnel (ARIA_ENABLE_METRICS=true)**
- `GET /metrics` - Métriques complètes
- `GET /metrics/health` - Statut de santé
- `GET /metrics/dashboard` - Dashboard HTML
- `GET /metrics/export/{format}` - Export (json, markdown, html, csv)
- `POST /metrics/collect` - Collecte forcée
- `GET /metrics/validate` - Validation des métriques
- `GET /metrics/summary` - Résumé des métriques
- `GET /metrics/alerts` - Alertes et recommandations

### **DevOps (`/api/devops`)**
- `GET /api/devops/status` - Statut DevOps
- `POST /api/devops/deploy` - Déploiement
- `GET /api/devops/logs` - Logs système
- `POST /api/devops/backup` - Sauvegarde

## 🗄️ **Base de Données**

### **Fichiers de Base de Données**
- `aria_pain.db` - Base principale (données douleur)
- `aria_research.db` - Base recherche (expérimentations)

### **Tables Principales**
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

### **Connexion à la Base de Données**
```python
from core.database import DatabaseManager

# Obtenir l'instance singleton
db = DatabaseManager()

# Exécuter une requête
result = db.execute_query("SELECT * FROM pain_entries WHERE user_id = ?", (user_id,))

# Exécuter une requête avec retour de données
data = db.fetch_all("SELECT * FROM pain_entries ORDER BY timestamp DESC LIMIT 10")
```

## 🔧 **Configuration**

### **Variables d'Environnement**
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

### **Configuration Centralisée**
```python
from core.config import Config

# Obtenir la configuration
config = Config()

# Accéder aux valeurs
db_path = config.get("ARIA_DB_PATH", "aria_pain.db")
log_level = config.get("ARIA_LOG_LEVEL", "INFO")
max_request_size = config.get("ARIA_MAX_REQUEST_SIZE", 10485760)
```

## 📱 **Application Mobile Flutter**

### **Structure Flutter**
```
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

### **Commandes Flutter**
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

## 🐳 **Docker & Déploiement**

### **Docker Compose**
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

### **Déploiement Production**
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

## 🔍 **Debugging & Monitoring**

### **Logs**
```bash
# Voir les logs de l'application
tail -f logs/app.log

# Voir les logs Docker
docker-compose logs -f aria

# Voir les logs système
journalctl -u aria -f
```

### **Monitoring**
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

### **Base de Données**
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

## 🚨 **Dépannage Courant**

### **Problèmes Fréquents**

#### **L'API ne démarre pas**
```bash
# Vérifier le port
lsof -i :8001

# Tuer le processus qui utilise le port
kill -9 $(lsof -t -i:8001)

# Relancer l'API
python main.py
```

#### **Tests échouent**
```bash
# Vérifier les imports
python -c "import main"

# Vérifier les dépendances
pip list

# Relancer les tests avec plus de détails
python -m pytest tests/ -v --tb=long
```

#### **Erreurs de base de données**
```bash
# Vérifier que la base existe
ls -la aria_pain.db

# Vérifier les permissions
chmod 664 aria_pain.db

# Recréer la base si nécessaire
rm aria_pain.db
python -c "from core.database import DatabaseManager; db = DatabaseManager(); db.init_database()"
```

#### **Problèmes de cache**
```bash
# Nettoyer le cache Python
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Nettoyer le cache de tests
rm -rf .pytest_cache
rm -rf .coverage
```

## 📚 **Ressources Utiles**

### **Documentation**
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Flutter Docs](https://flutter.dev/docs)
- [SQLite Docs](https://www.sqlite.org/docs.html)
- [Docker Docs](https://docs.docker.com/)

### **Outils de Développement**
- [Postman](https://www.postman.com/) - Test API
- [Insomnia](https://insomnia.rest/) - Test API alternatif
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Interface graphique SQLite
- [Flutter Inspector](https://flutter.dev/docs/development/tools/devtools/inspector) - Debug Flutter

### **Sécurité & RGPD**
- [CNIL](https://www.cnil.fr/) - Commission Nationale Informatique et Libertés
- [RGPD Guide](https://www.cnil.fr/fr/reglement-europeen-protection-donnees)
- [Bandit Docs](https://bandit.readthedocs.io/)
- [Safety Docs](https://pyup.io/safety/)

---

**ARKALIA ARIA** - Référence technique complète ! 🔧📚
