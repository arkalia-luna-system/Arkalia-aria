# Guide Testeur - ARKALIA ARIA

**Version**: 1.0.0  
**Date**: 24 novembre 2025  
**Pour**: Testeurs PlayCode Dev

---

## 🎯 Objectif

Ce guide vous accompagne dans le test d'**ARKALIA ARIA**, un laboratoire de recherche santé personnel qui permet de suivre votre douleur, analyser des patterns et prédire des tendances.

ARIA fait partie de l'écosystème **Arkalia Luna System** et communique avec :

- **CIA** (Companion Intelligence Assistant) : Coffre-fort santé familial
- **BBIA-SIM** : Robot compagnon (intégration future)

---

## 📋 Prérequis

### Installation

1. **Python 3.10+** installé
2. **Git** installé
3. **Accès PlayCode Dev** (vous avez acheté l'accès à 25€)

### Cloner le projet

```bash
git clone https://github.com/arkalia-luna-system/arkalia-aria.git
cd arkalia-aria
```

### Configuration

1. **Créer un environnement virtuel** :

```bash
python -m venv arkalia_aria_venv
source arkalia_aria_venv/bin/activate  # Linux/Mac
# ou
arkalia_aria_venv\Scripts\activate  # Windows
```

2. **Installer les dépendances** :

```bash
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement** :

```bash
cp env.example .env
# Éditer .env avec vos paramètres
```

**Variables importantes pour les tests** :

```env
# Activer la synchronisation automatique avec CIA (si CIA est installé)
ARIA_CIA_SYNC_ENABLED=false
ARIA_CIA_SYNC_INTERVAL_MINUTES=60
CIA_API_URL=http://127.0.0.1:8000

# Activer BBIA (si BBIA-SIM est installé)
ARIA_BBIA_ENABLED=false
BBIA_API_URL=http://127.0.0.1:8002
```

---

## 🚀 Démarrage

### Lancer ARIA

```bash
python main.py
```

L'API sera accessible sur : <http://127.0.0.1:8001>

### Vérifier que tout fonctionne

Ouvrez votre navigateur :

- **Documentation API** : <http://127.0.0.1:8001/docs>
- **Health Check** : <http://127.0.0.1:8001/health>

---

## 🧪 Scénarios de Test

### 1. Suivi de Douleur de Base

**Objectif** : Tester la saisie et récupération d'entrées de douleur

**Étapes** :

1. **Créer une entrée de douleur** :

```bash
curl -X POST "http://127.0.0.1:8001/api/pain/entry" \
  -H "Content-Type: application/json" \
  -d '{
    "intensity": 7,
    "location": "Dos",
    "physical_trigger": "Position assise prolongée",
    "mental_trigger": "Stress",
    "notes": "Douleur après 2h de travail"
  }'
```

2. **Récupérer toutes les entrées** :

```bash
curl "http://127.0.0.1:8001/api/pain/entries"
```

3. **Récupérer les statistiques** :

```bash
curl "http://127.0.0.1:8001/api/pain/stats"
```

**Résultats attendus** :

- ✅ Entrée créée avec succès
- ✅ Entrées récupérées avec toutes les données
- ✅ Statistiques calculées (moyenne, max, min)

---

### 2. Analyse de Patterns

**Objectif** : Tester la détection de corrélations

**Étapes** :

1. **Créer plusieurs entrées sur plusieurs jours** (via l'API ou manuellement)

2. **Analyser les patterns** :

```bash
curl "http://127.0.0.1:8001/api/patterns/analysis?days_back=30"
```

**Résultats attendus** :
- ✅ Corrélations détectées (sommeil/douleur, stress/douleur)
- ✅ Patterns temporels identifiés
- ✅ Recommandations générées

---

### 3. Prédictions ML

**Objectif** : Tester le moteur de prédiction

**Étapes** :

1. **Récupérer les prédictions** :

```bash
curl "http://127.0.0.1:8001/api/predictions/current"
```

2. **Analyser les tendances** :

```bash
curl "http://127.0.0.1:8001/api/predictions/trends?days=7"
```

**Résultats attendus** :
- ✅ Prédictions générées (si assez de données)
- ✅ Tendances identifiées
- ✅ Alertes si douleur élevée

---

### 4. Synchronisation avec CIA

**Objectif** : Tester la communication avec CIA (si installé)

**Prérequis** : CIA doit être lancé sur <http://127.0.0.1:8000>

**Étapes** :

1. **Vérifier la connexion** :

```bash
curl "http://127.0.0.1:8001/api/sync/connection"
```

2. **Synchroniser manuellement** :

```bash
curl -X POST "http://127.0.0.1:8001/api/sync/selective" \
  -H "Content-Type: application/json" \
  -d '{
    "sync_pain_entries": true,
    "sync_patterns": true,
    "sync_predictions": true
  }'
```

3. **Activer la synchronisation automatique** :

```bash
curl -X POST "http://127.0.0.1:8001/api/sync/auto-sync/start?interval_minutes=60"
```

**Résultats attendus** :
- ✅ Connexion CIA détectée
- ✅ Données synchronisées
- ✅ Auto-sync démarrée

---

### 5. Intégration BBIA (Simulation)

**Objectif** : Tester l'intégration BBIA (sans robot physique)

**Étapes** :

1. **Vérifier le statut BBIA** :

```bash
curl "http://127.0.0.1:8001/api/bbia/status"
```

2. **Envoyer un état émotionnel** :

```bash
curl -X POST "http://127.0.0.1:8001/api/bbia/emotional-state" \
  -H "Content-Type: application/json" \
  -d '{
    "pain_intensity": 7,
    "stress_level": 6,
    "sleep_quality": 4
  }'
```

3. **Envoyer depuis dernière entrée de douleur** :

```bash
curl -X POST "http://127.0.0.1:8001/api/bbia/emotional-state/from-latest-pain"
```

**Résultats attendus** :
- ✅ État émotionnel préparé (empathique, neutre, etc.)
- ✅ Comportement recommandé pour BBIA
- ✅ Mode simulation si robot non connecté

---

### 6. Connecteurs Santé

**Objectif** : Tester la synchronisation avec les apps santé

**Étapes** :

1. **Vérifier les connecteurs disponibles** :

```bash
curl "http://127.0.0.1:8001/api/health/connectors"
```

2. **Synchroniser avec Samsung Health** (si configuré) :

```bash
curl -X POST "http://127.0.0.1:8001/api/health/samsung/sync"
```

**Résultats attendus** :
- ✅ Connecteurs listés
- ✅ Synchronisation réussie (si configuré)

---

### 7. Export de Données

**Objectif** : Tester l'export pour professionnels

**Étapes** :

1. **Générer un rapport médical** :

```bash
curl "http://127.0.0.1:8001/api/sync/medical-report?period_days=30"
```

2. **Mode psychologue (anonymisé)** :

```bash
curl "http://127.0.0.1:8001/api/sync/psy-mode"
```

**Résultats attendus** :
- ✅ Rapport généré avec statistiques
- ✅ Données anonymisées pour psy
- ✅ Format prêt pour partage

---

### 8. Dashboard Web

**Objectif** : Tester l'interface web interactive

**Étapes** :

1. **Accéder au dashboard** :

Ouvrez votre navigateur : <http://127.0.0.1:8001/dashboard>

2. **Pages disponibles** :

- Dashboard principal : <http://127.0.0.1:8001/dashboard>
- Métriques santé : <http://127.0.0.1:8001/dashboard/health>
- Analyse douleur : <http://127.0.0.1:8001/dashboard/pain>
- Visualisation patterns : <http://127.0.0.1:8001/dashboard/patterns>
- Rapports : <http://127.0.0.1:8001/dashboard/reports>

**Résultats attendus** :
- ✅ Dashboard accessible
- ✅ Graphiques interactifs fonctionnels
- ✅ Export PDF/Excel/HTML disponible
- ✅ Mise à jour temps réel

**Note** : Le dashboard web est entièrement fonctionnel sans PlayCode ni robot.

---

### 9. Application Mobile (Architecture)

**Objectif** : Vérifier l'architecture mobile Flutter

**Étapes** :

1. **Vérifier la structure** :

```bash
cd mobile_app
flutter pub get
flutter doctor
```

2. **Vérifier les services** :

Les services suivants sont implémentés :
- `lib/services/aria_api_service.dart` : Communication API
- `lib/services/health_connector_service.dart` : Connecteurs santé
- `lib/services/notification_service.dart` : Notifications
- `lib/services/offline_cache_service.dart` : Cache offline

**Résultats attendus** :
- ✅ Structure Flutter valide
- ✅ Services compilent sans erreur
- ✅ Configuration Android/iOS présente

**Note** : L'architecture mobile est prête. Les écrans UI sont en développement mais tous les services backend sont fonctionnels.

---

## 🐛 Signaler un Bug

### Informations à fournir

1. **Description du problème** : Que s'est-il passé ?
2. **Étapes pour reproduire** : Comment reproduire le bug ?
3. **Comportement attendu** : Que devrait-il se passer ?
4. **Comportement observé** : Que s'est-il réellement passé ?
5. **Logs** : Copiez les logs d'erreur
6. **Configuration** : Version Python, OS, variables d'environnement

### Où signaler

- **GitHub Issues** : <https://github.com/arkalia-luna-system/arkalia-aria/issues>
- **Email** : arkalia.luna.system@gmail.com

---

## ✅ Checklist de Test

### Fonctionnalités Core

- [ ] Création d'entrée de douleur
- [ ] Récupération d'entrées
- [ ] Statistiques calculées
- [ ] Analyse de patterns
- [ ] Prédictions ML
- [ ] Export de données

### Intégrations

- [ ] Synchronisation CIA (si installé)
- [ ] Auto-sync CIA (si activé)
- [ ] Intégration BBIA (simulation)
- [ ] Connecteurs santé (si configurés)

### Interface

- [ ] Dashboard web accessible
- [ ] Graphiques interactifs fonctionnels
- [ ] Export PDF/Excel/HTML depuis dashboard
- [ ] API documentation complète
- [ ] Health check fonctionne
- [ ] Architecture mobile Flutter vérifiée

### Performance

- [ ] Réponse API < 1 seconde
- [ ] Pas de fuites mémoire
- [ ] Base de données stable

---

## 📚 Documentation Complète

- **API Reference** : `docs/API_REFERENCE.md`
- **Developer Guide** : `docs/DEVELOPER_GUIDE.md`
- **Mobile App** : `docs/MOBILE_APP.md`
- **Project Status** : `docs/PROJECT_STATUS.md`

---

## Support

- **Documentation** : `docs/`
- **Issues GitHub** : <https://github.com/arkalia-luna-system/arkalia-aria/issues>
- **Contact** : arkalia.luna.system@gmail.com

---

Merci de tester ARKALIA ARIA ! 🚀
