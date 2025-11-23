# 🔌 Référence API - ARKALIA ARIA

**Dernière mise à jour :** Novembre 2025

## Base URL

```
<http://localhost:8001>

```

## Endpoints Standardisés (BaseAPI)

Toutes les APIs ARIA héritent automatiquement de ces endpoints :

### Health Check

```http
GET /api/{module}/health

```
**Exemples :**
- `GET /api/pain/health`
- `GET /api/pattern/health`
- `GET /api/prediction/health`

### Status

```http
GET /api/{module}/status

```
**Exemples :**
- `GET /api/pain/status`
- `GET /api/pattern/status`

### Metrics

```http
GET /api/{module}/metrics

```
**Exemples :**
- `GET /api/pain/metrics`
- `GET /api/pattern/metrics`

---

## Endpoints Principaux

### Health Check

```http
GET /health

```
**Réponse :**

```json
{
  "status": "healthy",
  "timestamp": "2024-12-24T18:00:00Z",
  "version": "1.0.0",
  "modules": {
    "pain_tracking": "active",
    "pattern_analysis": "active",
    "prediction_engine": "active",
    "health_connectors": "active",
    "metrics_collector": "active",
    "research_tools": "active",
    "cia_sync": "active",
    "audio_voice": "active"
  }
}

```

---

## 🩺 **Connecteurs Santé**

### 📊 **Statut des Connecteurs**

```http
GET /health/connectors/status

```
**Réponse :**

```json
{
  "samsung": {
    "status": "connected",
    "last_sync": "2024-12-24T17:30:00Z",
    "data_count": 1250
  },
  "google": {
    "status": "connected", 
    "last_sync": "2024-12-24T17:25:00Z",
    "data_count": 890
  },
  "ios": {
    "status": "disconnected",
    "last_sync": null,
    "data_count": 0
  }
}

```

### 🔄 **Synchronisation Samsung Health**

```http
POST /health/samsung/sync

```
**Réponse :**

```json
{
  "success": true,
  "message": "Synchronisation Samsung Health réussie",
  "data_synced": 45,
  "timestamp": "2024-12-24T18:00:00Z"
}

```

### 🔄 **Synchronisation Google Fit**

```http
POST /health/google/sync

```
**Réponse :**

```json
{
  "success": true,
  "message": "Synchronisation Google Fit réussie",
  "data_synced": 32,
  "timestamp": "2024-12-24T18:00:00Z"
}

```

### 🔄 **Synchronisation Apple Health**

```http
POST /health/ios/sync

```
**Réponse :**

```json
{
  "success": true,
  "message": "Synchronisation Apple Health réussie",
  "data_synced": 28,
  "timestamp": "2024-12-24T18:00:00Z"
}

```

### 🔄 **Synchronisation Complète**

```http
POST /health/sync/all

```
**Réponse :**

```json
{
  "success": true,
  "message": "Synchronisation complète réussie",
  "total_data_synced": 105,
  "connectors": {
    "samsung": {"synced": 45, "status": "success"},
    "google": {"synced": 32, "status": "success"},
    "ios": {"synced": 28, "status": "success"}
  },
  "timestamp": "2024-12-24T18:00:00Z"
}

```

### 📈 **Métriques Santé Unifiées**

```http
GET /health/metrics/unified

```
**Réponse :**

```json
{
  "total_metrics": 1250,
  "metrics": [
    {
      "type": "steps",
      "value": 8542,
      "unit": "steps",
      "date": "2024-12-24",
      "source": "samsung_health"
    },
    {
      "type": "heart_rate",
      "value": 72,
      "unit": "bpm",
      "date": "2024-12-24",
      "source": "google_fit"
    },
    {
      "type": "sleep",
      "value": 7.5,
      "unit": "hours",
      "date": "2024-12-24",
      "source": "apple_health"
    }
  ],
  "summary": {
    "daily_steps_avg": 8234,
    "heart_rate_avg": 68,
    "sleep_avg": 7.2,
    "stress_level": 3.2
  }
}

```

### ⚙️ **Configuration Santé**

```http
GET /health/config

```
**Réponse :**

```json
{
  "auto_sync": true,
  "sync_frequency": "daily",
  "notifications": true,
  "data_retention_days": 365,
  "privacy_mode": false,
  "connection_status": "connected"
}

```

```http
PUT /health/config
Content-Type: application/json

{
  "auto_sync": true,
  "sync_frequency": "hourly",
  "notifications": false
}

```

---

## 🩹 **Suivi de Douleur**

### ⚡ **Enregistrement Rapide**

```http
POST /api/pain/quick-entry
Content-Type: application/json

{
  "intensity": 7,
  "physical_trigger": "stress",
  "action_taken": "respiration"
}

```
**Réponse (PainEntryOut)** :

```json
{
  "id": 1,
  "timestamp": "2025-09-25T14:00:00",
  "intensity": 7,
  "physical_trigger": "stress",
  "mental_trigger": null,
  "activity": null,
  "location": null,
  "action_taken": "respiration",
  "effectiveness": null,
  "notes": null,
  "created_at": "2025-09-25T14:00:00"
}

```

### 📝 **Enregistrement Détaillé**

```http
POST /api/pain/entry
Content-Type: application/json

{
  "intensity": 7,
  "physical_trigger": "stress",
  "mental_trigger": "anxiété",
  "activity": "sitting",
  "location": "dos",
  "action_taken": "respiration",
  "effectiveness": 6,
  "notes": "Douleur après travail",
  "timestamp": "2025-09-25T13:59:00"
}

```

### 📋 **Liste des Entrées**

```http
GET /api/pain/entries
GET /api/pain/entries/recent?limit=20

```
**Réponse (liste de PainEntryOut)** : `200 OK` avec tableau d’entrées triées par date (récentes d'abord)

### 🧠 **Suggestions**

```http
GET /api/pain/suggestions?window=30

```
Retourne des recommandations et questions de suivi basées sur les données récentes.

### 📤 **Exports**

```http
GET /api/pain/export/csv
GET /api/pain/export/psy-report

```
CSV: contenu et nom de fichier; Psy-report: HTML imprimable et métadonnées.

> Note: l’endpoint de statistiques dédié n’est pas exposé; utiliser `/api/pain/suggestions` et les exports pour des synthèses.

---

## 🔬 **Analytics et Patterns**

### 🧠 **Patterns Détectés**

```http
GET /api/patterns/patterns/recent?days=30
GET /api/patterns/correlations/sleep-pain?days=30
GET /api/patterns/correlations/stress-pain?days=30
GET /api/patterns/triggers/recurrent?days=30&min_occurrences=3
POST /api/patterns/analyze

```

**Réponse GET /api/patterns/patterns/recent :**

```json
{
  "period_days": 30,
  "analysis_date": "2025-11-23T10:00:00",
  "sleep_pain_correlation": {
    "correlation": -0.65,
    "confidence": 0.87,
    "data_points": 25,
    "patterns": [
      {
        "type": "sleep_duration",
        "description": "Douleur plus élevée les jours avec moins de sommeil",
        "strength": 0.65
      }
    ],
    "recommendations": [
      "Manque de sommeil corrélé avec douleur élevée. Envisager d'améliorer la durée de sommeil."
    ]
  },
  "stress_pain_correlation": {
    "correlation": 0.72,
    "confidence": 0.82,
    "data_points": 28,
    "patterns": [
      {
        "type": "stress_pain",
        "description": "Stress élevé corrélé avec douleur élevée",
        "strength": 0.72
      }
    ],
    "recommendations": [
      "Stress fortement corrélé avec douleur. Envisager des techniques de gestion du stress."
    ]
  },
  "recurrent_triggers": {
    "triggers": {
      "physical": [
        {"trigger": "marche prolongée", "count": 12},
        {"trigger": "position assise", "count": 8}
      ],
      "mental": [
        {"trigger": "stress", "count": 15},
        {"trigger": "fatigue", "count": 9}
      ],
      "activities": [
        {"activity": "travail sur ordinateur", "count": 10}
      ]
    },
    "temporal_patterns": {
      "hours": [
        {"hour": "14", "count": 8},
        {"hour": "18", "count": 6}
      ],
      "days": [
        {"day": "Monday", "count": 12},
        {"day": "Friday", "count": 10}
      ]
    },
    "total_entries": 45
  }
}

```

**Réponse GET /api/patterns/correlations/sleep-pain :**

```json
{
  "correlation": -0.65,
  "confidence": 0.87,
  "data_points": 25,
  "patterns": [
    {
      "type": "sleep_duration",
      "description": "Douleur plus élevée les jours avec moins de sommeil",
      "strength": 0.65
    }
  ],
  "recommendations": [
    "Manque de sommeil corrélé avec douleur élevée. Envisager d'améliorer la durée de sommeil."
  ]
}

```

### 🔮 **Prédictions Actuelles**

```http
GET /api/predictions/predictions/current?include_correlations=true
POST /api/predictions/predict
POST /api/predictions/train
GET /api/predictions/analytics

```

**Réponse GET /api/predictions/predictions/current :**

```json
{
  "risk_level": "medium",
  "predictions": [
    {
      "predicted_intensity": 6,
      "predicted_trigger": "stress",
      "confidence": 0.75,
      "time_horizon": "2-4 heures",
      "recommendations": [
        "Techniques de relaxation préventives",
        "Surveillance accrue",
        "Plan de gestion activé"
      ],
      "context_factors": {
        "time_of_day": 14,
        "day_of_week": 0,
        "stress_factor": 0.8,
        "fatigue_factor": 0.6,
        "activity_factor": 0.4
      },
      "correlation_factors": {
        "sleep_correlation": -0.65,
        "stress_correlation": 0.72,
        "adjustment": 1
      }
    }
  ],
  "confidence": 0.75,
  "timestamp": "2025-11-23T14:00:00"
}

```

**Réponse POST /api/predictions/predict :**

```json
{
  "predicted_intensity": 7,
  "predicted_trigger": "stress",
  "confidence": 0.82,
  "time_horizon": "2-4 heures",
  "recommendations": [
    "Techniques de relaxation préventives",
    "Surveillance accrue",
    "Plan de gestion activé"
  ],
  "context_factors": {
    "time_of_day": 14,
    "day_of_week": 0,
    "stress_factor": 0.8,
    "fatigue_factor": 0.6,
    "activity_factor": 0.4
  }
}

```

**Réponse GET /api/predictions/analytics :**

```json
{
  "total_events": 145,
  "total_patterns": 8,
  "total_predictions": 32,
  "prediction_accuracy": 0.78,
  "pattern_detection_rate": 5.52,
  "system_health": "operational"
}

```

### 📊 **Expérimentations Recherche**

```http
GET /api/research/experiments
POST /api/research/experiment/create

```
**Réponse :**

```json
{
  "total_patterns": 12,
  "total_predictions": 8,
  "confidence": 0.82,
  "recommendations": [
    "Éviter les activités stressantes entre 14h et 16h",
    "Pratiquer la méditation avant le coucher",
    "Surveiller la météo pour anticiper les douleurs"
  ],
  "data_quality": "excellent",
  "last_analysis": "2024-12-24T18:00:00Z"
}

```

### 🔍 **Analyse de Patterns**

```http
POST /api/analytics/analyze
Content-Type: application/json

{
  "data_range": "last_30_days",
  "analysis_type": "correlation",
  "focus_areas": ["pain_intensity", "stress_level", "sleep_quality"]
}

```
**Réponse :**

```json
{
  "success": true,
  "analysis_id": "analysis_789",
  "patterns_found": 3,
  "correlations": [
    {
      "factor1": "stress_level",
      "factor2": "pain_intensity",
      "correlation": 0.73,
      "significance": "high"
    }
  ],
  "processing_time": "2.3s"
}

```

---

## Métriques et Monitoring

### 📈 **Métriques Système**

```http
GET /metrics/system

```
**Réponse :**

```json
{
  "cpu_usage": 23.5,
  "memory_usage": 45.2,
  "disk_usage": 67.8,
  "uptime": "5d 12h 30m",
  "active_connections": 3,
  "database_size": "125MB",
  "last_backup": "2024-12-24T00:00:00Z"
}

```

### 🩺 **Métriques Santé**

```http
GET /metrics/health

```
**Réponse :**

```json
{
  "total_health_data": 1250,
  "sync_frequency": "daily",
  "data_sources": {
    "samsung_health": 650,
    "google_fit": 400,
    "apple_health": 200
  },
  "last_sync": "2024-12-24T17:30:00Z",
  "sync_status": "healthy"
}

```

### 📊 **Dashboard Data**

```http
GET /dashboard/data

```
**Réponse :**

```json
{
  "pain_summary": {
    "today_entries": 3,
    "avg_intensity": 5.2,
    "trend": "stable"
  },
  "health_summary": {
    "steps_today": 8542,
    "heart_rate_avg": 72,
    "sleep_last_night": 7.5
  },
  "patterns_summary": {
    "active_patterns": 5,
    "predictions_today": 2,
    "confidence": 0.82
  },
  "system_summary": {
    "status": "healthy",
    "uptime": "5d 12h 30m",
    "last_backup": "2024-12-24T00:00:00Z"
  }
}

```

---

## 📤 **Export et Partage**

### 📄 **Export CSV**

```http
GET /api/export/csv?format=complete&start_date=2024-12-01&end_date=2024-12-24
Accept: text/csv

```
**Réponse :** Fichier CSV téléchargeable

### 📊 **Export JSON**

```http
GET /api/export/json?format=summary&period=30_days

```
**Réponse :**

```json
{
  "export_id": "export_456",
  "format": "summary",
  "period": "30_days",
  "data": {
    "pain_entries": 45,
    "health_metrics": 1250,
    "patterns": 12,
    "predictions": 8
  },
  "generated_at": "2024-12-24T18:00:00Z",
  "file_size": "2.3MB"
}

```

### 📋 **Rapport Médical**

```http
GET /api/export/medical-report?period=30_days&include_patterns=true

```
**Réponse :**

```json
{
  "report_id": "report_789",
  "period": "30_days",
  "patient_summary": {
    "total_pain_episodes": 45,
    "avg_intensity": 5.2,
    "most_common_location": "dos",
    "trend": "decreasing"
  },
  "patterns": [
    {
      "description": "Douleur dos corrélée avec stress",
      "confidence": 0.87,
      "recommendations": ["Gestion du stress", "Exercices de relaxation"]
    }
  ],
  "recommendations": [
    "Continuer le suivi actuel",
    "Intégrer des techniques de relaxation",
    "Surveiller l'évolution des patterns"
  ],
  "generated_at": "2024-12-24T18:00:00Z"
}

```

---

## Configuration et Administration

### ⚙️ **Configuration Système**

```http
GET /config/system

```
**Réponse :**

```json
{
  "app_name": "ARKALIA ARIA",
  "version": "1.0.0",
  "environment": "development",
  "debug_mode": false,
  "log_level": "INFO",
  "database_path": "./aria_research.db",
  "backup_enabled": true,
  "backup_frequency": "daily"
}

```

### 🔄 **Redémarrage Modules**

```http
POST /admin/restart-modules
Content-Type: application/json

{
  "modules": ["health_connectors", "prediction_engine"]
}

```

### 🗄️ **Nettoyage Base de Données**

```http
POST /admin/cleanup-database
Content-Type: application/json

{
  "older_than_days": 365,
  "backup_before": true
}

```

---

## Codes d'Erreur

### 4xx - Erreurs Client

- `400` : Bad Request - Données invalides
- `401` : Unauthorized - Authentification requise
- `403` : Forbidden - Accès refusé
- `404` : Not Found - Ressource introuvable
- `422` : Unprocessable Entity - Données malformées

### 5xx - Erreurs Serveur

- `500` : Internal Server Error - Erreur interne
- `502` : Bad Gateway - Problème de connecteur externe
- `503` : Service Unavailable - Service temporairement indisponible

### Exemple d'Erreur

```json
{
  "error": "validation_error",
  "message": "Intensité de douleur doit être entre 1 et 10",
  "details": {
    "field": "intensity",
    "value": 15,
    "constraint": "min:1, max:10"
  },
  "timestamp": "2024-12-24T18:00:00Z"
}

```

---

## Authentification

### Headers Requis

```http
Content-Type: application/json
Accept: application/json
User-Agent: ARIA-Client/1.0

```

### Rate Limiting

- **Limite** : 100 requêtes/minute par IP
- **Headers** : `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

**ARKALIA ARIA** - API Reference ! 🔌📊
