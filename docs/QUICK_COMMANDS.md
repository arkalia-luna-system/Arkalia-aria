# Commandes Rapides

**ARKALIA ARIA** — Référence rapide des commandes essentielles

**Dernière mise à jour :** 23 janvier 2026

## Démarrage Rapide

### Lancer l'Application

```bash
# Activer l'environnement
source arkalia_aria_venv/bin/activate

# Lancer l'API
python main.py
# OU
uvicorn main:app --host 127.0.0.1 --port 8001 --reload

# Vérifier que ça fonctionne
curl http://127.0.0.1:8001/health

```

### Tests Rapides

```bash
# Tests rapides (mode fail-fast)
python -m pytest tests/ --tb=short -x

# Tests complets
python -m pytest tests/ --cov=. --cov-report=html

# Tests d'intégration
python -m pytest tests/integration/ -v

```

---

## Qualité du Code

### Formatage & Linting

```bash
# Formater le code
black .

# Linter et corrections automatiques
ruff check . --fix

# Vérification des types
mypy .

# Tous les outils de qualité
black . && ruff check . --fix && mypy .

```

### Sécurité

```bash
# Audit de sécurité
bandit -r . -f json -o reports/bandit-report.json
safety check --json --output reports/safety-report.json

# Audit complet
bandit -r . && safety check

```

---

## 🐳 **Docker**

### Docker Compose

```bash
# Lancer avec Docker
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter les services
docker-compose down

# Reconstruire l'image
docker-compose up --build -d

```

### Docker Direct

```bash
# Construire l'image
docker build -t arkalia-aria .

# Lancer le conteneur
docker run -p 8001:8001 arkalia-aria

# Voir les logs
docker logs arkalia-aria

```

---

## Application Mobile

### Flutter

```bash
# Aller dans le dossier mobile
cd mobile_app/

# Installer les dépendances
flutter pub get

# Lancer l'app
flutter run

# Construire pour production
flutter build apk --release
flutter build ios --release

```

---

## Base de Données

### SQLite

```bash
# Ouvrir la base de données
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

### Backup & Restore

```bash
# Backup
cp aria_pain.db aria_pain.db.backup
cp aria_research.db aria_research.db.backup

# Restore
cp aria_pain.db.backup aria_pain.db
cp aria_research.db.backup aria_research.db

```

---

## 🔍 **Debugging**

### Vérifier l'État

```bash
# Vérifier les processus
ps aux | grep python

# Vérifier les ports
lsof -i :8001

# Vérifier l'utilisation mémoire
free -h

# Vérifier l'utilisation disque
df -h

```

### Logs

```bash
# Voir les logs de l'application
tail -f logs/app.log

# Voir les logs Docker
docker-compose logs -f aria

# Voir les logs système
journalctl -u aria -f

```

---

## API & Endpoints

### Tests API

```bash
# Health check
curl http://127.0.0.1:8001/health

# Status détaillé
curl http://127.0.0.1:8001/status

# Métriques
curl http://127.0.0.1:8001/metrics

# Documentation API
open http://127.0.0.1:8001/docs

```

### Endpoints Principaux

```bash
# Suivi de douleur
curl http://127.0.0.1:8001/api/pain/entries
curl http://127.0.0.1:8001/api/pain/quick-entry

# Connecteurs santé
curl http://127.0.0.1:8001/health/connectors/status
curl http://127.0.0.1:8001/health/samsung/sync
curl http://127.0.0.1:8001/health/google/sync
curl http://127.0.0.1:8001/health/ios/sync
curl http://127.0.0.1:8001/health/sync/all

# Exports
curl http://127.0.0.1:8001/api/pain/export/csv
curl http://127.0.0.1:8001/api/pain/export/pdf
curl http://127.0.0.1:8001/api/pain/export/excel

```

---

## 🧹 **Nettoyage**

### Cache & Fichiers Temporaires

```bash
# Nettoyer le cache Python
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Nettoyer le cache de tests
rm -rf .pytest_cache
rm -rf .coverage
rm -rf htmlcov/

# Nettoyer les logs
rm -rf logs/*.log

```

### Fichiers de Build

```bash
# Nettoyer les builds
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Nettoyer Docker
docker system prune -f
docker volume prune -f

```

---

## Monitoring

### Métriques Système

```bash
# CPU et mémoire
top -p $(pgrep -f "python.*main.py")

# Utilisation disque
du -sh aria_pain.db aria_research.db

# Connexions réseau
netstat -tulpn | grep :8001

```

### Métriques Application

```bash
# Métriques système (nécessite ARIA_ENABLE_METRICS=true)
curl http://127.0.0.1:8001/metrics

# Métriques santé unifiées
curl http://127.0.0.1:8001/health/metrics/unified?days_back=7

```

---

## Git & Déploiement

### Git

```bash
# Voir l'état
git status

# Ajouter tous les fichiers
git add .

# Commit
git commit -m "feat: ajout fonctionnalité X"

# Push
git push

# Voir l'historique
git log --oneline -10

```

### Déploiement

```bash
# Construire pour production
docker build -t arkalia-aria:latest .

# Tag pour version
docker tag arkalia-aria:latest arkalia-aria:v1.0.0

# Push vers registry
docker push arkalia-aria:latest

```

---

## 🚨 **Dépannage**

### Problèmes Courants

```bash
# Port 8001 occupé
kill -9 $(lsof -t -i:8001)

# Problème de permissions
chmod 664 aria_pain.db
chmod 664 aria_research.db

# Problème de dépendances
pip install -r requirements.txt

# Problème de cache
rm -rf .pytest_cache __pycache__/

```

### Redémarrage Complet

```bash
# Arrêter tout
docker-compose down
pkill -f "python.*main.py"

# Nettoyer
docker system prune -f

# Relancer
docker-compose up -d
# OU
python main.py

```

---

## 📚 **Documentation**

### Générer la Documentation

```bash
# Documentation MkDocs
mkdocs serve

# Documentation API
open http://127.0.0.1:8001/docs

# Documentation ReDoc
open http://127.0.0.1:8001/redoc

```

### Voir la Documentation

```bash
# Ouvrir la documentation
open docs/index.md

# Voir les guides
ls docs/*.md

# Chercher dans la documentation
grep -r "mot-clé" docs/

```

---

## ⚡ **Commandes Ultra-Rapides**

### Développement Quotidien

```bash
# Workflow complet
source arkalia_aria_venv/bin/activate && python main.py

# Tests rapides
python -m pytest tests/ --tb=short -x

# Qualité code
black . && ruff check . --fix

# Git
git add . && git commit -m "update" && git push

```

### Docker Rapide

```bash
# Lancer
docker-compose up -d

# Logs
docker-compose logs -f

# Arrêter
docker-compose down

```

### API Rapide

```bash
# Health
curl http://127.0.0.1:8001/health

# Docs
open http://127.0.0.1:8001/docs

```

---

**ARKALIA ARIA** - Commandes rapides ! ⚡🚀
