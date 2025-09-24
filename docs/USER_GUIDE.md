# 👤 Guide Utilisateur - ARKALIA ARIA

## 🎯 **Qu'est-ce qu'ARKALIA ARIA ?**

ARKALIA ARIA (Arkalia Research Intelligence Assistant) est votre assistant personnel de recherche santé qui transforme vos données médicales en insights actionables, tout en gardant un contrôle total sur vos informations sensibles.

**Philosophie** : Vos données médicales vous appartiennent. ARIA travaille exclusivement pour vous, localement, sans jamais partager vos informations sans votre consentement explicite.

---

## 🚀 **Démarrage Rapide**

### 1. Installation
```bash
# Cloner le repository
git clone https://github.com/arkalia-luna-system/arkalia-aria.git
cd arkalia-aria

# Créer l'environnement virtuel
python -m venv arkalia_aria_venv
source arkalia_aria_venv/bin/activate  # Linux/Mac
# ou
arkalia_aria_venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancement
```bash
# Démarrer l'API
python main.py

# L'API sera disponible sur http://localhost:8001
# Dashboard web : http://localhost:8001/dashboard
# Documentation API : http://localhost:8001/docs
```

---

## 📱 **Utilisation**

### 🌐 **Dashboard Web**

Accédez au dashboard via `http://localhost:8001/dashboard` pour :

- **Vue d'ensemble** : Résumé de vos données de santé
- **Graphiques temps réel** : Visualisation des tendances
- **Métriques santé** : Données Samsung Health, Google Fit, Apple Health
- **Analytics** : Patterns détectés et prédictions
- **Export** : Téléchargement CSV pour professionnels

### 📱 **App Mobile Flutter**

#### Installation
```bash
cd mobile_app
flutter pub get
flutter run -d ios    # iOS
flutter run -d android # Android
```

#### Écrans Disponibles

1. **Synchronisation Santé** (`/health-sync`)
   - Statut des connecteurs (Samsung Health, Google Fit, Apple Health)
   - Synchronisation manuelle ou automatique
   - Visualisation des données de santé

2. **Dashboard** (`/dashboard`)
   - Résumé général de vos données
   - Métriques de santé récentes
   - Dernières entrées de douleur
   - Statut des modules système

3. **Analytics** (`/analytics`)
   - Patterns détectés par l'IA
   - Prédictions d'épisodes de douleur
   - Recommandations personnalisées
   - Analyse de corrélations

4. **Paramètres** (`/settings`)
   - Configuration des notifications
   - Fréquence de synchronisation
   - Mode sombre/clair
   - Export des données
   - Configuration santé

---

## 🏥 **Connecteurs Santé**

### Samsung Health
- **Authentification** : OAuth 2.0 sécurisé
- **Données** : Pas, fréquence cardiaque, sommeil, stress, calories
- **Synchronisation** : Automatique ou manuelle
- **Privacité** : Données stockées localement uniquement

### Google Fit
- **Authentification** : Google OAuth
- **Données** : Activité physique, métriques de santé
- **Intégration** : Compatible avec tous les appareils Android
- **API** : Google Fit REST API

### Apple HealthKit
- **Support iOS** : Natif iOS/macOS
- **Données** : Santé complète iOS
- **Synchronisation** : Via HealthKit framework
- **Sécurité** : Chiffrement end-to-end Apple

---

## 📊 **Suivi de Douleur**

### Enregistrement Rapide
```bash
# Via API
curl -X POST "http://localhost:8001/api/pain/quick" \
  -H "Content-Type: application/json" \
  -d '{"intensity": 7, "location": "dos", "trigger": "stress"}'
```

### Enregistrement Détaillé
```bash
# Via API
curl -X POST "http://localhost:8001/api/pain/detailed" \
  -H "Content-Type: application/json" \
  -d '{
    "intensity": 7,
    "location": "dos",
    "trigger": "stress",
    "duration": 30,
    "medication": "paracetamol",
    "notes": "Douleur après travail"
  }'
```

### Via Interface Web
1. Allez sur `http://localhost:8001/dashboard`
2. Cliquez sur "Nouvelle entrée douleur"
3. Remplissez le formulaire
4. Sauvegardez

---

## 🔬 **Analytics et Prédictions**

### Patterns Détectés
ARIA analyse automatiquement vos données pour détecter :
- **Corrélations** : Entre douleur et facteurs externes
- **Tendances** : Évolution dans le temps
- **Déclencheurs** : Facteurs qui précipitent la douleur
- **Cycles** : Patterns récurrents

### Prédictions
- **Épisodes futurs** : Probabilité d'épisodes de douleur
- **Intensité** : Estimation de l'intensité
- **Timing** : Quand l'épisode pourrait survenir
- **Confiance** : Niveau de confiance de la prédiction

### Recommandations
Basées sur vos données, ARIA suggère :
- **Modifications comportementales**
- **Moments optimaux** pour certaines activités
- **Alertes préventives**
- **Stratégies de gestion**

---

## 📈 **Export et Partage**

### Export CSV
```bash
# Via API
curl -X GET "http://localhost:8001/api/export/csv" \
  -H "Accept: text/csv" \
  -o "aria_data.csv"
```

### Données Incluses
- Historique complet de douleur
- Métriques de santé synchronisées
- Patterns détectés
- Prédictions générées
- Corrélations identifiées

### Partage avec Professionnels
- **Format CSV** : Compatible Excel, Google Sheets
- **Anonymisation** : Option de masquage des identifiants
- **Filtres** : Par période, type de données
- **Résumé** : Rapport automatique généré

---

## 🔒 **Sécurité et Confidentialité**

### Stockage Local
- **Base de données SQLite** : Stockage local uniquement
- **Chiffrement** : Données sensibles chiffrées
- **Accès** : Contrôle total sur vos données
- **Pas de cloud** : Aucune transmission externe

### Authentification
- **OAuth 2.0** : Pour connecteurs santé
- **Tokens sécurisés** : Renouvellement automatique
- **Permissions minimales** : Accès limité aux données nécessaires
- **Révocation** : Possibilité de retirer l'accès

### Conformité
- **RGPD** : Respect des réglementations européennes
- **Consentement** : Contrôle explicite des données
- **Transparence** : Accès complet à vos données
- **Suppression** : Possibilité de supprimer toutes les données

---

## 🛠️ **Dépannage**

### Problèmes Courants

#### API ne démarre pas
```bash
# Vérifier les dépendances
pip install -r requirements.txt

# Vérifier le port
netstat -an | grep 8001
```

#### Connecteurs santé ne fonctionnent pas
```bash
# Vérifier les credentials
cat health_connectors/config.json

# Tester la connexion
curl http://localhost:8001/health/connectors/status
```

#### App mobile ne se connecte pas
```bash
# Vérifier l'URL dans le service
cat mobile_app/lib/services/aria_api_service.dart | grep baseUrl

# Tester l'API
curl http://localhost:8001/health
```

### Logs et Debug
```bash
# Logs API
tail -f logs/aria.log

# Logs connecteurs
tail -f logs/health_connectors.log

# Mode debug
export ARIA_DEBUG=1
python main.py
```

---

## 📞 **Support**

### Documentation
- **Guide Développeur** : `docs/DEVELOPER_GUIDE.md`
- **API Reference** : `docs/API_REFERENCE.md`
- **Statut Projet** : `docs/PROJECT_STATUS.md`

### Issues GitHub
- **Bugs** : [GitHub Issues](https://github.com/arkalia-luna-system/arkalia-aria/issues)
- **Feature Requests** : [GitHub Discussions](https://github.com/arkalia-luna-system/arkalia-aria/discussions)
- **Documentation** : [GitHub Wiki](https://github.com/arkalia-luna-system/arkalia-aria/wiki)

---

**ARKALIA ARIA** - Votre assistant santé personnel ! 🧠❤️🔬