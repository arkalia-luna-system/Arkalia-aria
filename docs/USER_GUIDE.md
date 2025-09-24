# 📖 Guide Utilisateur - ARKALIA ARIA

## 🚀 Démarrage Rapide

### Installation et Configuration

1. **Cloner le projet**
   ```bash
   git clone https://github.com/arkalia-luna-system/arkalia-aria.git
   cd arkalia-aria
   ```

2. **Créer l'environnement virtuel**
   ```bash
   python -m venv arkalia_aria_venv
   source arkalia_aria_venv/bin/activate  # Linux/Mac
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer ARIA**
   ```bash
   python main.py
   ```

### Accès à l'Interface

- **API Documentation** : http://127.0.0.1:8001/docs
- **Interface Alternative** : http://127.0.0.1:8001/redoc
- **Statut de santé** : http://127.0.0.1:8001/health

### Raccourcis Makefile
```bash
# Vérifier l'aide
make help

# Lancer l'API en dev
make run-dev

# Lancer les tests
make test

# Lint + format
make lint && make format
```

## 📊 Utilisation des Modules

### 🔍 Suivi de Douleur

#### Saisie Rapide
```bash
curl -X POST "http://127.0.0.1:8001/api/pain/quick-entry" \
  -H "Content-Type: application/json" \
  -d '{
    "intensity": 6,
    "physical_trigger": "stress",
    "action_taken": "respiration"
  }'
```

#### Saisie Détaillée
```bash
curl -X POST "http://127.0.0.1:8001/api/pain/entry" \
  -H "Content-Type: application/json" \
  -d '{
    "intensity": 7,
    "physical_trigger": "marche prolongée",
    "mental_trigger": "stress",
    "activity": "travail",
    "location": "dos",
    "action_taken": "étirement",
    "effectiveness": 6,
    "notes": "Amélioration après étirement"
  }'
```

### 🧠 Analyse de Patterns

#### Obtenir les Patterns Récents
```bash
curl -X GET "http://127.0.0.1:8001/api/patterns/recent"
```

#### Analyser des Données
```bash
curl -X POST "http://127.0.0.1:8001/api/patterns/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "data_type": "pain_entries",
    "timeframe": "7_days"
  }'
```

### 🔮 Moteur de Prédiction

#### Prédictions Actuelles
```bash
curl -X GET "http://127.0.0.1:8001/api/predictions/current"
```

#### Entraîner le Modèle
```bash
curl -X POST "http://127.0.0.1:8001/api/predictions/train" \
  -H "Content-Type: application/json" \
  -d '{
    "training_data": "recent_entries",
    "model_type": "pattern_recognition"
  }'
```

### 🔬 Outils de Recherche

#### Lister les Expérimentations
```bash
curl -X GET "http://127.0.0.1:8001/api/research/experiments"
```

#### Créer une Expérimentation
```bash
curl -X POST "http://127.0.0.1:8001/api/research/experiment/create" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test relaxation",
    "duration": "7_days",
    "parameters": {
      "technique": "respiration",
      "frequency": "daily"
    }
  }'
```

### 🔗 Intégration CIA

#### Statut de Synchronisation
```bash
curl -X GET "http://127.0.0.1:8001/api/sync/status"
```

#### Synchronisation Sélective
```bash
curl -X POST "http://127.0.0.1:8001/api/sync/selective" \
  -H "Content-Type: application/json" \
  -d '{
    "sync_pain_entries": true,
    "sync_patterns": true,
    "sync_predictions": false
  }'
```

#### Mode Psychologue
```bash
curl -X GET "http://127.0.0.1:8001/api/sync/psy-mode"
```

## 📈 Export et Rapports

### Export CSV
```bash
curl -X GET "http://127.0.0.1:8001/api/pain/export/csv"
```

### Rapport Psychologue (HTML prêt à imprimer)
```bash
curl -X GET "http://127.0.0.1:8001/api/pain/export/psy-report"
```

### Suggestions Intelligentes
```bash
curl -X GET "http://127.0.0.1:8001/api/pain/suggestions?window=30"
```

### Audio/Voix

#### Statut module
```bash
curl -X GET "http://127.0.0.1:8001/api/audio/status"
```

#### Synthèse vocale simulée
```bash
curl -X POST "http://127.0.0.1:8001/api/audio/tts" \
  -H "Content-Type: application/json" \
  -d '{"text":"Bonjour ARIA","voice":"amelie"}'
```

#### Sauvegarder une note audio (base64)
```bash
curl -X POST "http://127.0.0.1:8001/api/audio/note" \
  -H "Content-Type: application/json" \
  -d '{"content_base64":"UklGR..."}'
```

### Montre / Health Connect (ingestion)

#### Statut
```bash
curl -X GET "http://127.0.0.1:8001/api/watch/status"
```

#### Fréquence cardiaque
```bash
curl -X POST "http://127.0.0.1:8001/api/watch/heart-rate" \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2025-01-27T21:00:00Z","bpm":72,"resting":60}'
```

#### Session de sommeil
```bash
curl -X POST "http://127.0.0.1:8001/api/watch/sleep-session" \
  -H "Content-Type: application/json" \
  -d '{"start":"2025-01-27T00:00:00Z","end":"2025-01-27T07:20:00Z","quality":0.8}'
```

#### Stress
```bash
curl -X POST "http://127.0.0.1:8001/api/watch/stress" \
  -H "Content-Type: application/json" \
  -d '{"timestamp":"2025-01-27T10:00:00Z","level":62}'
```

#### Pas quotidiens
```bash
curl -X POST "http://127.0.0.1:8001/api/watch/steps" \
  -H "Content-Type: application/json" \
  -d '{"date":"2025-01-27","steps":8650,"active_minutes":42}'
```

### Dashboards DevOps

#### Sécurité (HTML)
```bash
curl -X GET "http://127.0.0.1:8001/devops/security/dashboard"
```

#### Monitoring (HTML)
```bash
curl -X GET "http://127.0.0.1:8001/devops/monitoring/dashboard"
```

### Historique des Entrées
```bash
curl -X GET "http://127.0.0.1:8001/api/pain/entries/recent?limit=10"
```

## 🔧 Configuration Avancée

### Variables d'Environnement

```bash
# Port personnalisé
export ARIA_PORT=8001

# Base de données personnalisée
export ARIA_DB_PATH=/path/to/custom.db

# Logs détaillés
export ARIA_LOG_LEVEL=debug
```

Valeurs par défaut (si non définies):
- ARIA_PORT=8001
- ARIA_DB_PATH=aria_pain.db (dans le répertoire du module pain_tracking)
- ARIA_LOG_LEVEL=info

### Configuration CIA

```bash
# URL CIA personnalisée
export CIA_BASE_URL=http://localhost:8000

# Timeout de connexion
export CIA_TIMEOUT=10
```

Valeurs par défaut:
- CIA_BASE_URL=http://127.0.0.1:8000
- CIA_TIMEOUT=10

## 🚨 Dépannage

### Problèmes Courants

#### Port déjà utilisé
```bash
# Vérifier les processus sur le port 8001
lsof -i :8001

# Tuer le processus si nécessaire
kill -9 <PID>
```

#### Erreur de base de données
```bash
# Vérifier les permissions
ls -la *.db

# Recréer la base si nécessaire
rm *.db
python main.py
```

#### Problème de connexion CIA
```bash
# Vérifier que CIA est accessible
curl http://127.0.0.1:8000/health

# Vérifier la configuration
curl http://127.0.0.1:8001/api/sync/status
```

### Logs et Debug

#### Activer les logs détaillés
```bash
python main.py --log-level debug
```

#### Consulter les logs
```bash
tail -f logs/aria.log
```

## 📱 Intégration Mobile

### Configuration pour l'App Flutter

```dart
// Configuration de base
const String ariaBaseUrl = 'http://127.0.0.1:8001';
const String ciaBaseUrl = 'http://127.0.0.1:8000';

// Exemple d'utilisation
Future<void> addPainEntry() async {
  final response = await http.post(
    Uri.parse('$ariaBaseUrl/api/pain/quick-entry'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'intensity': 6,
      'trigger': 'stress',
      'action': 'respiration',
    }),
  );
}
```

## 🔒 Sécurité et Confidentialité

### Bonnes Pratiques

1. **Données locales uniquement** : ARIA ne transmet aucune donnée personnelle
2. **Chiffrement** : Base de données SQLite sécurisée
3. **Anonymisation** : Export pour professionnels sans données personnelles
4. **Contrôle d'accès** : Limitation des connexions réseau

### Sauvegarde

```bash
# Sauvegarde automatique
cp *.db backups/aria_backup_$(date +%Y%m%d_%H%M%S).db

# Restauration
cp backups/aria_backup_20240127_120000.db aria.db
```

## 📊 Métriques et Performance

### Surveillance

```bash
# Statut des services
curl http://127.0.0.1:8001/health

# Métriques de performance
curl http://127.0.0.1:8001/api/research/metrics
```

### Optimisation

- **Base de données** : Nettoyage régulier des anciennes entrées
- **Mémoire** : Redémarrage périodique en cas d'utilisation intensive
- **Réseau** : Configuration des timeouts appropriés

---

**ARKALIA ARIA** - Votre laboratoire de recherche santé personnel ! 🧠✨