# 📚 Référence API - ARKALIA ARIA

## 🌐 Endpoints Principaux

### Base URL
```
http://127.0.0.1:8001
```

### Documentation Interactive
- **Swagger UI** : http://127.0.0.1:8001/docs
- **ReDoc** : http://127.0.0.1:8001/redoc

## 🔍 Pain Tracking API

### POST `/api/pain/quick-entry`
Saisie ultra-rapide de douleur (3 questions seulement)

**Request Body:**
```json
{
  "intensity": 6,
  "physical_trigger": "stress",
  "action_taken": "respiration"
}
```

**Response:**
```json
{
  "id": 1,
  "intensity": 6,
  "physical_trigger": "stress",
  "mental_trigger": null,
  "activity": null,
  "location": null,
  "action_taken": "respiration",
  "effectiveness": null,
  "notes": null,
  "timestamp": "2025-01-27T21:00:00Z",
  "created_at": "2025-01-27T21:00:00Z"
}
```

### 📐 Schémas JSON

#### QuickEntry (requête)
```json
{
  "intensity": 0,
  "physical_trigger": "string (1-128)",
  "action_taken": "string (1-128)"
}
```
Règles:
- intensity: entier 0..10
- physical_trigger, action_taken: chaînes non vides ≤128 caractères

#### PainEntryOut (réponse)
```json
{
  "id": 1,
  "intensity": 5,
  "physical_trigger": "string|null",
  "mental_trigger": "string|null",
  "activity": "string|null",
  "location": "string|null",
  "action_taken": "string|null",
  "effectiveness": 0,
  "notes": "string|null",
  "timestamp": "ISO-8601",
  "created_at": "YYYY-MM-DD HH:MM:SS"
}
```

### POST `/api/pain/entry`
Saisie détaillée de douleur

**Request Body:**
```json
{
  "intensity": 7,
  "physical_trigger": "marche prolongée",
  "mental_trigger": "stress",
  "activity": "travail",
  "location": "dos",
  "action_taken": "étirement",
  "effectiveness": 6,
  "notes": "Amélioration après étirement"
}
```

### GET `/api/pain/entries/recent`
Récupérer les entrées récentes

**Query Parameters:**
- `limit` (int, optional) : Nombre d'entrées à retourner (défaut: 10)

**Response:**
```json
[
  {
    "id": 1,
    "intensity": 6,
    "physical_trigger": "marche",
    "mental_trigger": "stress",
    "activity": "travail",
    "location": "dos",
    "action_taken": "étirement",
    "effectiveness": 6,
    "notes": "Amélioration",
    "timestamp": "2025-01-27T21:00:00Z"
  }
]
```

### GET `/api/pain/export/csv`
Exporter les données en CSV

**Response:**
```json
{
  "content": "Date,Heure,Intensité,Déclencheur Physique...",
  "filename": "pain_export_20250127_210000.csv",
  "entries_count": 15
}
```

### GET `/api/pain/status`
Statut du module pain tracking

**Response:**
```json
{
  "module": "pain_tracking",
  "status": "healthy",
  "timestamp": "2025-01-27T21:00:00Z",
  "features": ["quick_entry", "detailed_entry", "history", "export"]
}
```

### 🗄️ Schéma Base de Données (SQLite)

Table: `pain_entries`
```sql
CREATE TABLE IF NOT EXISTS pain_entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp TEXT NOT NULL,
  intensity INTEGER NOT NULL,
  physical_trigger TEXT,
  mental_trigger TEXT,
  activity TEXT,
  location TEXT,
  action_taken TEXT,
  effectiveness INTEGER,
  notes TEXT,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_pain_ts ON pain_entries(timestamp);
CREATE INDEX IF NOT EXISTS idx_pain_intensity ON pain_entries(intensity);
```

### GET `/api/pain/export/psy-report`
Exporter un rapport HTML prêt à imprimer pour psychologue

**Response:**
```json
{
  "html": "<!doctype html>...",
  "filename": "psy_report_20250127_210000.html",
  "entries_count": 15
}
```

### GET `/api/pain/suggestions`
Suggestions intelligentes basées sur les données récentes

**Query Parameters:**
- `window` (int, optional) : Nombre de jours à analyser (défaut: 30)

**Response:**
```json
{
  "window_days": 30,
  "summary": { "avg_intensity": 5.2, "entries_count": 15 },
  "suggestions": [
    "Déclencheur fréquent identifié: stress — prévoir stratégies d’évitement/atténuation.",
    "Action efficace à privilégier: respiration (efficacité moyenne 7.0)."
  ],
  "follow_up_questions": [
    "Avez-vous remarqué un déclencheur physique récurrent ces derniers jours ?"
  ],
  "generated_at": "2025-01-27T21:00:00Z"
}
```

## 🧠 Pattern Analysis API

### GET `/api/patterns/status`
Statut du module pattern analysis

**Response:**
```json
{
  "module": "pattern_analysis",
  "status": "healthy",
  "timestamp": "2025-01-27T21:00:00Z",
  "features": ["correlation_detection", "temporal_patterns", "trigger_analysis", "visual_reports"]
}
```

### GET `/api/patterns/recent`
Analyse des patterns récents

**Response:**
```json
{
  "message": "Pattern analysis en développement",
  "patterns": [],
  "confidence": 0.0
}
```

### POST `/api/patterns/analyze`
Lancer une analyse de patterns

**Request Body:**
```json
{
  "data_type": "pain_entries",
  "timeframe": "7_days",
  "parameters": {
    "correlation_threshold": 0.7,
    "min_samples": 10
  }
}
```

## 🔮 Prediction Engine API

### GET `/api/predictions/status`
Statut du module prediction engine

**Response:**
```json
{
  "module": "prediction_engine",
  "status": "healthy",
  "timestamp": "2025-01-27T21:00:00Z",
  "features": ["crisis_prediction", "early_warnings", "personalized_recommendations", "ml_learning"]
}
```

### GET `/api/predictions/current`
Prédictions actuelles

**Response:**
```json
{
  "message": "Prediction engine en développement",
  "risk_level": "low",
  "predictions": [],
  "confidence": 0.0
}
```

### POST `/api/predictions/train`
Entraîner le modèle ML

**Request Body:**
```json
{
  "training_data": "recent_entries",
  "model_type": "pattern_recognition",
  "parameters": {
    "learning_rate": 0.01,
    "epochs": 100
  }
}
```

## 🔬 Research Tools API

### GET `/api/research/status`
Statut du module research tools

**Response:**
```json
{
  "module": "research_tools",
  "status": "healthy",
  "timestamp": "2025-01-27T21:00:00Z",
  "features": ["data_laboratory", "controlled_experiments", "advanced_metrics", "anonymized_export"]
}
```

### GET `/api/research/experiments`
Liste des expérimentations

**Response:**
```json
{
  "message": "Research tools en développement",
  "experiments": [],
  "active_count": 0
}
```

### POST `/api/research/experiment/create`
Créer une expérimentation

**Request Body:**
```json
{
  "name": "Test relaxation",
  "duration": "7_days",
  "parameters": {
    "technique": "respiration",
    "frequency": "daily",
    "metrics": ["pain_intensity", "stress_level"]
  }
}
```

## 🔗 CIA Sync API

### GET `/api/sync/status`
Statut de la synchronisation CIA

En local, si CIA n’est pas lancé, la réponse peut être: `{ "status": "cia_unavailable", "cia_connected": false }`.

**Response (CIA en ligne):**
```json
{
  "message": "CIA sync opérationnel",
  "connected": true,
  "cia_url": "http://127.0.0.1:8000",
  "timestamp": "2025-01-27T21:00:00Z"
}
```

### POST `/api/sync/selective`
Synchronisation sélective avec CIA

**Request Body:**
```json
{
  "sync_pain_entries": true,
  "sync_patterns": true,
  "sync_predictions": false
}
```

**Response:**
```json
{
  "message": "Synchronisation sélective réussie",
  "synced_data": [
    {
      "type": "pain_entries",
      "count": 15,
      "status": "synced"
    }
  ],
  "status": "completed",
  "timestamp": "2025-01-27T21:00:00Z"
}
```

### GET `/api/sync/psy-mode`
Mode présentation pour psychologue

**Response:**
```json
{
  "message": "Données anonymisées pour psychologue",
  "anonymized_data": {
    "total_entries": 15,
    "average_intensity": 5.2,
    "common_triggers": ["stress", "fatigue"],
    "effectiveness_patterns": {
      "respiration": 0.7,
      "étirement": 0.6
    }
  },
  "status": "success",
  "timestamp": "2025-01-27T21:00:00Z"
}
```

### POST `/api/sync/push-data`
Pousser des données vers CIA

Note: CIA doit être lancé pour une synchronisation effective. En local, l’état peut être `cia_unavailable`.

**Request Body:**
```json
{
  "data_type": "pain_entries",
  "data": [
    {
      "intensity": 6,
      "physical_trigger": "stress",
      "action_taken": "respiration",
      "timestamp": "2025-01-27T21:00:00Z"
    }
  ]
}
```

## 🌐 Endpoints Globaux

### GET `/`
Page d'accueil ARIA

**Response:**
```json
{
  "message": "ARKALIA ARIA - Research Intelligence Assistant",
  "version": "1.0.0",
  "status": "running",
  "modules": [
    "pain_tracking",
    "pattern_analysis",
    "prediction_engine",
    "research_tools",
    "cia_sync"
  ]
}
```

### GET `/health`
Vérification de santé globale

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-27T21:00:00Z",
  "modules_status": "all_operational"
}
```

## 📊 Codes de Statut HTTP

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Créé avec succès |
| 400 | Requête invalide |
| 404 | Ressource non trouvée |
| 422 | Erreur de validation |
| 500 | Erreur serveur interne |
| 503 | Service non disponible |

## 🔒 Authentification

Actuellement, ARIA fonctionne sans authentification pour un usage local. Pour un déploiement en production, considérez :

- **API Keys** : Authentification par clé
- **JWT Tokens** : Tokens d'authentification
- **OAuth2** : Authentification tierce

## 📝 Exemples d'Utilisation

### Python
```python
import requests

# Saisie rapide
response = requests.post(
    "http://127.0.0.1:8001/api/pain/quick-entry",
    json={
        "intensity": 6,
        "physical_trigger": "stress",
        "action_taken": "respiration"
    }
)
print(response.json())
```

### JavaScript
```javascript
// Récupérer l'historique
fetch('http://127.0.0.1:8001/api/pain/entries/recent?limit=5')
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL
```bash
# Statut de santé
curl -X GET "http://127.0.0.1:8001/health"

# Export CSV
curl -X GET "http://127.0.0.1:8001/api/pain/export/csv" \
  -H "Accept: application/json"
```

## 🛠️ DevOps API

### 🔒 Sécurité

#### GET `/devops/security/dashboard`
Dashboard HTML de sécurité (événements récents, tentatives bloquées, résumé des risques)

Réponse: `text/html` (page prête à consulter/imprimer)

#### POST `/devops/security/validate-command`
Valider une commande système avant exécution

Body:
```json
{ "command": ["ls", "-la"], "context": "api" }
```

#### POST `/devops/security/execute-command`
Exécuter une commande de manière sécurisée (journalisée)

Body:
```json
{ "command": ["echo", "hello"], "context": "api" }
```

### 📈 Monitoring

#### GET `/devops/monitoring/dashboard`
Dashboard HTML de monitoring (santé, performances, alertes)

Réponse: `text/html`

#### GET `/devops/monitoring/health`
Statut de santé du système

#### GET `/devops/monitoring/performance?hours=24`
Résumé des performances pour la période donnée

#### GET `/devops/monitoring/alerts?hours=24`
Résumé des alertes

## 🎙️ Audio/Voix API

### GET `/api/audio/status`
Statut du module audio/voix

**Response:**
```json
{
  "module": "audio_voice",
  "status": "ready",
  "features": ["tts_simulated", "audio_note_store"],
  "timestamp": "2025-01-27T21:00:00Z"
}
```

### POST `/api/audio/tts`
Synthèse vocale simulée côté serveur (aucune dépendance)

**Request Body:**
```json
{ "text": "Bonjour ARIA", "voice": "amelie" }
```

**Response:**
```json
{
  "status": "ok",
  "voice": "amelie",
  "text": "Bonjour ARIA",
  "message": "TTS simulée côté serveur - aucune dépendance installée"
}
```

### POST `/api/audio/note`
Sauvegarde d’une note audio encodée en base64 dans `dacc/audio_notes/`

**Request Body:**
```json
{ "content_base64": "UklGR...", "filename": "optionnel.wav" }
```

## ⌚ Watch Integration API

### GET `/api/watch/status`
Statut du module montre

**Response:**
```json
{
  "module": "watch_integration",
  "status": "ready",
  "endpoints": ["/heart-rate","/sleep-session","/stress","/steps"],
  "timestamp": "2025-01-27T21:00:00Z"
}
```

### POST `/api/watch/heart-rate`
Ingestion fréquence cardiaque

**Request Body:**
```json
{ "timestamp": "2025-01-27T21:00:00Z", "bpm": 72, "resting": 60 }
```

### POST `/api/watch/sleep-session`
Ingestion session de sommeil

**Request Body:**
```json
{ "start": "2025-01-27T00:00:00Z", "end": "2025-01-27T07:20:00Z", "quality": 0.8 }
```

### POST `/api/watch/stress`
Ingestion niveau de stress (0-100)

**Request Body:**
```json
{ "timestamp": "2025-01-27T10:00:00Z", "level": 62 }
```

### POST `/api/watch/steps`
Ingestion pas quotidiens

**Request Body:**
```json
{ "date": "2025-01-27", "steps": 8650, "active_minutes": 42 }
```

**Response:**
```json
{
  "status": "saved",
  "file_path": "/abs/path/dacc/audio_notes/note.wav",
  "size_bytes": 1234,
  "timestamp": "2025-01-27T21:00:00Z"
}
```

## 🚨 Gestion d'Erreurs

### Erreurs de Validation
```json
{
  "detail": [
    {
      "loc": ["body", "intensity"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge",
      "ctx": {"limit_value": 0}
    }
  ]
}
```

### Erreurs de Service
```json
{
  "detail": "CIA non disponible"
}
```

---

**ARKALIA ARIA API** - Documentation complète pour développeurs ! 🚀📚