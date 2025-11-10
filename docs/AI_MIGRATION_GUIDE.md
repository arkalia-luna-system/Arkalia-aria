# 🤖 Guide de Migration pour IA ARKALIA ARIA

**Dernière mise à jour : Novembre 2025**

## 🎯 **Objectif**

Ce guide permet à une nouvelle IA de comprendre rapidement l'état du projet ARKALIA ARIA et de continuer le développement sans perdre de temps.

---

## 📋 **État Actuel du Projet**

### **Architecture**
- **Type** : Application FastAPI + Flutter
- **Base de données** : SQLite (aria_pain.db, aria_research.db)
- **Architecture** : Centralisée avec module `core/`
- **État** : 85% terminé, architecture centralisée complète, 4 modules BaseAPI, 4 modules logging/DB centralisé, prêt pour validation RGPD et tests mobile

### **Modules Principaux**
1. **`core/`** - Module centralisé (DatabaseManager, CacheManager, BaseAPI)
2. **`pain_tracking/`** - Suivi de douleur (migré vers BaseAPI)
3. **`pattern_analysis/`** - Analyse de patterns (migré vers core)
4. **`prediction_engine/`** - Moteur ML (migré vers DatabaseManager)
5. **`research_tools/`** - Outils recherche (migré vers DatabaseManager)
6. **`health_connectors/`** - Connecteurs santé (migré vers BaseAPI)
7. **`audio_voice/`** - Audio/voix (migré vers BaseAPI)
8. **`cia_sync/`** - Sync CIA (migré vers BaseAPI)
9. **`metrics_collector/`** - Métriques (optimisé)
10. **`devops_automation/`** - DevOps (CI/CD automatisé)

---

## 🚀 **Démarrage Rapide**

### **1. Environnement de Développement**
```bash
# Aller dans le projet
cd /Volumes/T7/arkalia-aria

# Activer l'environnement virtuel
source arkalia_aria_venv/bin/activate

# Vérifier l'installation
python --version  # Python 3.10
pip list | grep fastapi  # FastAPI installé
```

### **2. Lancer l'Application**
```bash
# Mode développement
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
# OU directement
python main.py

# Vérifier que ça fonctionne
curl http://127.0.0.1:8001/health
```

### **3. Tests**
```bash
# Tests rapides
python -m pytest tests/ --tb=short -x

# Tests complets
python -m pytest tests/ --cov=. --cov-report=html
```

---

## 📚 **Documentation Essentielle**

### **Documents à Lire en Priorité**
1. **`docs/TECHNICAL_REFERENCE.md`** - Guide technique complet
2. **`docs/SOLO_WORKFLOW.md`** - Workflow de développement
3. **`docs/TODO_SIMPLE.md`** - Tâches à faire
4. **`docs/ACTION_PLAN.md`** - Plan d'action détaillé
5. **`docs/VALIDATION_CHECKLIST.md`** - Checklist de validation

### **Documents de Référence**
- **`docs/API_REFERENCE.md`** - Documentation API
- **`docs/DEVELOPER_GUIDE.md`** - Guide développeur
- **`docs/SECURITY_RGPD_CHECKLIST.md`** - Checklist RGPD
- **`docs/PROJECT_STATUS.md`** - Statut du projet

---

## 🔧 **Architecture Technique**

### **Structure Principale**
```
main.py                    # Point d'entrée FastAPI
├── core/                  # Module centralisé
│   ├── database.py        # DatabaseManager (Singleton)
│   ├── cache.py          # CacheManager
│   ├── config.py         # Configuration
│   ├── api_base.py       # BaseAPI (standardisation)
│   ├── logging.py        # Logging
│   └── exceptions.py     # Exceptions
├── pain_tracking/         # Suivi douleur
├── pattern_analysis/      # Analyse patterns
├── prediction_engine/     # ML
├── research_tools/        # Recherche
├── health_connectors/     # Connecteurs santé
├── audio_voice/          # Audio
├── cia_sync/             # Sync CIA
├── metrics_collector/     # Métriques
└── devops_automation/     # DevOps
```

### **Base de Données**
- **`aria_pain.db`** - Données principales (douleur, patterns, prédictions)
- **`aria_research.db`** - Données de recherche
- **Connexion** : Via `DatabaseManager` (Singleton)

### **API Endpoints**
- **Base** : `http://127.0.0.1:8001`
- **Docs** : `http://127.0.0.1:8001/docs`
- **Health** : `http://127.0.0.1:8001/health`
- **APIs** : `/api/pain`, `/api/patterns`, `/api/predictions`, etc.

---

## 🎯 **Prochaines Étapes Prioritaires**

### **Phase 1 : Validation RGPD (1-2 semaines)**
1. **Créer instance démo** - Environnement de test
2. **Tester checklist RGPD** - Tous les points
3. **Tests mobile réels** - iPhone/Android
4. **Documentation légale** - Mentions, CGU, privacy

### **Phase 2 : Déploiement (2-3 semaines)**
1. **Configuration production** - Serveur, HTTPS, monitoring
2. **Tests de charge** - Performance, scalabilité
3. **Déploiement mobile** - App Store, Google Play

### **Phase 3 : Améliorations (1-2 mois)**
1. **Performance** - Cache Redis, CDN, optimisations
2. **Fonctionnalités** - IA avancée, intégrations tierces
3. **Analytics** - Dashboard avancé, rapports

---

## 🔍 **Points d'Attention**

### **Problèmes Connus**
- **RGPD** : Pas encore testé sur instance réelle
- **Mobile** : Pas testé sur device réel
- **Production** : Pas encore déployé
- **Performance** : Peut être optimisée avec Redis

### **Optimisations Récentes**
- **Architecture centralisée** : Module `core/` créé
- **Performance** : 3x plus rapide (1 connexion DB vs 5)
- **CI/CD** : Workflows automatisés et optimisés
- **Sécurité** : Scans automatisés avec timeouts

---

## 🛠️ **Outils de Développement**

### **Commandes Essentielles**
```bash
# Qualité du code
black . && ruff check . --fix && mypy .

# Tests
python -m pytest tests/ --tb=short -x

# Sécurité
bandit -r . && safety check

# Git
git add . && git commit -m "message" && git push
```

### **Outils de Debug**
```bash
# Vérifier l'API
curl http://127.0.0.1:8001/health

# Vérifier les processus
ps aux | grep python

# Vérifier les ports
lsof -i :8001

# Base de données
sqlite3 aria_pain.db
```

---

## 📱 **Application Mobile**

### **Structure Flutter**
```
mobile_app/
├── lib/                   # Code Dart
├── android/              # Configuration Android
├── ios/                  # Configuration iOS
├── assets/               # Assets
└── pubspec.yaml          # Dépendances
```

### **Commandes Flutter**
```bash
cd mobile_app/
flutter pub get
flutter run
flutter build apk --release
```

---

## 🐳 **Docker & Déploiement**

### **Docker Compose**
```bash
# Lancer avec Docker
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### **Configuration Production**
- **Serveur** : VPS/Cloud avec Docker
- **HTTPS** : Certificats SSL
- **Monitoring** : Prometheus + Grafana
- **Base de données** : PostgreSQL/MySQL

---

## 🚨 **Dépannage Courant**

### **Problèmes Fréquents**
1. **Port 8001 occupé** → `kill -9 $(lsof -t -i:8001)`
2. **Tests échouent** → Vérifier imports et dépendances
3. **Base de données** → Vérifier permissions et existence
4. **Cache** → Nettoyer `.pytest_cache`, `__pycache__`

### **Logs & Debug**
- **API** : Logs dans la console
- **Base de données** : `sqlite3 aria_pain.db`
- **Docker** : `docker-compose logs -f`

---

## 📊 **Métriques Actuelles**

### **Code**
- **Fichiers Python** : 53 fichiers
- **Lignes de code** : ~10 248 lignes
- **Tests** : 394 tests collectés (100% passent)
- **Couverture** : Variable selon les modules

### **Performance**
- **Temps de réponse** : < 2 secondes
- **Connexions DB** : 1 partagée (vs 5 séparées)
- **Mémoire** : < 2GB en utilisation normale
- **CPU** : < 50% en utilisation normale

---

## 🎯 **Objectifs à Court Terme**

### **Cette Semaine**
1. **RGPD** - Tester sur instance démo
2. **Mobile** - Tester sur device réel
3. **Exports** - Tester CSV/PDF/Excel
4. **Documentation** - Rédiger mentions légales

### **Ce Mois**
1. **Tests complets** - Validation end-to-end
2. **Production** - Déploiement et monitoring
3. **Mobile** - Finalisation et stores
4. **Performance** - Optimisations avancées

---

## 📞 **Support & Ressources**

### **Documentation**
- **GitHub** : https://github.com/arkalia-luna-system/arkalia-aria
- **Docs** : https://arkalia-luna-system.github.io/arkalia-aria/
- **Issues** : https://github.com/arkalia-luna-system/arkalia-aria/issues

### **Outils Externes**
- **FastAPI** : https://fastapi.tiangolo.com/
- **Flutter** : https://flutter.dev/docs
- **SQLite** : https://www.sqlite.org/docs.html
- **Docker** : https://docs.docker.com/

---

## ✅ **Checklist de Prise en Main**

### **Première Session (30 min)**
- [ ] Lire `TECHNICAL_REFERENCE.md`
- [ ] Lancer l'application (`python main.py`)
- [ ] Tester l'API (`curl http://127.0.0.1:8001/health`)
- [ ] Lancer les tests (`python -m pytest tests/ --tb=short -x`)

### **Deuxième Session (1h)**
- [ ] Lire `SOLO_WORKFLOW.md`
- [ ] Explorer la structure du code
- [ ] Tester les endpoints principaux
- [ ] Comprendre l'architecture centralisée

### **Troisième Session (2h)**
- [ ] Lire `ACTION_PLAN.md`
- [ ] Identifier les prochaines tâches
- [ ] Commencer la validation RGPD
- [ ] Planifier les tests mobile

---

**ARKALIA ARIA** - Guide de migration pour IA ! 🤖🚀
