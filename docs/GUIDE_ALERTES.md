# 🔔 Guide : Configuration et Utilisation des Alertes

**Date** : 23 janvier 2026  
**Version** : 1.0.0

---

## 🎯 Introduction

ARIA dispose d'un système d'alertes intelligent qui vous prévient automatiquement des patterns détectés, des prédictions de crises, et des corrélations importantes.

---

## 📋 Types d'Alertes

### 1. **Alertes Patterns Détectés**

ARIA détecte automatiquement les déclencheurs récurrents et vous alerte.

**Exemples** :
- "⚠️ Déclencheur récurrent détecté : Manque de sommeil → Douleur moyenne 7/10"
- "⚠️ Pattern temporel : Pics de douleur fréquents le mardi matin"

**Quand** : Dès qu'un pattern est détecté (minimum 3 occurrences).

---

### 2. **Alertes Prédictions**

ARIA prédit les crises potentielles basées sur vos données historiques.

**Exemples** :
- "🔮 Prédiction : Risque élevé de crise dans les 24-48h (probabilité 75%)"
- "🔮 Alerte préventive : Conditions similaires à vos crises précédentes détectées"

**Quand** : Lorsque les conditions d'une crise précédente se reproduisent.

---

### 3. **Alertes Corrélations**

ARIA vous informe des corrélations importantes découvertes.

**Exemples** :
- "📊 Corrélation forte : Sommeil < 6h → Douleur +2 points en moyenne"
- "📊 Corrélation détectée : Stress élevé → Douleur moyenne 8/10"

**Quand** : Lorsqu'une corrélation significative est identifiée.

---

### 4. **Alertes Données Santé**

Alertes basées sur les données synchronisées depuis votre montre/téléphone.

**Exemples** :
- "💤 Sommeil insuffisant : 4h30 la nuit dernière (recommandé : 7-9h)"
- "📈 Stress élevé détecté : Niveau moyen de 8/10 cette semaine"
- "🏃 Activité faible : Seulement 2000 pas aujourd'hui"

**Quand** : Après chaque synchronisation santé automatique.

---

### 5. **Alertes RDV Médicaux**

Rappels pour vos rendez-vous médicaux synchronisés depuis CIA.

**Exemples** :
- "📅 Rappel : RDV médical dans 24h (Dr. Martin, 10h00)"
- "📅 Rappel : RDV médical dans 48h (Dr. Martin, 10h00)"

**Quand** : 24h et 48h avant chaque RDV médical.

---

## 💻 Utilisation via l'API

### Récupérer toutes les alertes

```bash
GET /api/alerts
```

**Réponse** :
```json
{
  "alerts": [
    {
      "id": 1,
      "type": "pattern",
      "severity": "medium",
      "title": "Déclencheur récurrent détecté",
      "message": "Manque de sommeil → Douleur moyenne 7/10",
      "read": false,
      "created_at": "2026-01-23T10:00:00Z"
    }
  ],
  "total": 1,
  "unread_count": 1
}
```

### Récupérer les alertes non lues

```bash
GET /api/alerts?read=false
```

### Marquer une alerte comme lue

```bash
POST /api/alerts/{alert_id}/read
```

### Marquer toutes les alertes comme lues

```bash
POST /api/alerts/read-all
```

### Vérifier les alertes automatiquement

```bash
POST /api/alerts/check
```

Cette commande déclenche une vérification manuelle de tous les types d'alertes.

---

## 🌐 Utilisation via le Dashboard Web

### Visualisation des alertes

1. Accédez au dashboard : `http://localhost:8001/dashboard`
2. La section "Alertes" apparaît en haut de la page
3. Cliquez sur une alerte pour voir les détails
4. Les alertes non lues sont marquées en surbrillance

### Configuration (à venir)

Une interface de configuration des alertes est prévue pour :
- Activer/désactiver certains types d'alertes
- Configurer les seuils (ex: sommeil minimum)
- Personnaliser les notifications

---

## ⚙️ Configuration Automatique

### Synchronisation Santé

Les alertes santé sont créées automatiquement après chaque synchronisation :

```bash
# Synchronisation manuelle
POST /api/health/sync/all

# Les alertes sont créées automatiquement après la sync
```

### Synchronisation CIA

Les alertes RDV médicaux sont créées automatiquement lors de la synchronisation avec CIA :

```bash
# Synchronisation CIA
POST /api/sync/pull-from-cia?data_type=appointments

# Les alertes RDV sont créées automatiquement
```

---

## 🔍 Détails des Types d'Alertes

### Alertes Patterns

**Déclencheurs récurrents** :
- Minimum 3 occurrences nécessaires
- Analyse sur les 30 derniers jours
- Seuil de corrélation : 60%+

**Patterns temporels** :
- Analyse par jour de la semaine
- Analyse par heure de la journée
- Détection de pics récurrents

### Alertes Prédictions

**Méthode** :
- Analyse des conditions précédant les crises
- Comparaison avec les données actuelles
- Probabilité calculée (0-100%)

**Seuils** :
- Faible : 40-60%
- Moyen : 60-80%
- Élevé : 80%+

### Alertes Corrélations

**Types de corrélations** :
- Sommeil ↔ Douleur
- Stress ↔ Douleur
- Activité ↔ Douleur
- Émotions ↔ Douleur

**Seuils** :
- Corrélation faible : 0.3-0.5
- Corrélation moyenne : 0.5-0.7
- Corrélation forte : 0.7+

---

## 📊 Statistiques des Alertes

### Récupérer les statistiques

```bash
GET /api/alerts/stats
```

**Réponse** :
```json
{
  "total": 25,
  "unread": 5,
  "by_type": {
    "pattern": 10,
    "prediction": 5,
    "correlation": 7,
    "health": 2,
    "appointment": 1
  },
  "by_severity": {
    "low": 5,
    "medium": 15,
    "high": 5
  }
}
```

---

## 💡 Conseils d'Utilisation

### 1. **Vérifiez régulièrement**

Consultez vos alertes quotidiennement pour ne rien manquer.

### 2. **Agissez sur les alertes**

Les alertes ne sont utiles que si vous agissez dessus :
- Pattern détecté → Évitez le déclencheur
- Prédiction de crise → Prenez des mesures préventives
- Corrélation → Adaptez votre comportement

### 3. **Marquez comme lues**

Marquez les alertes lues pour garder une vue claire des nouvelles alertes.

### 4. **Analysez les tendances**

Utilisez les statistiques pour comprendre quels types d'alertes sont les plus fréquents.

---

## 🔧 Dépannage

### Les alertes ne s'affichent pas

1. Vérifiez que la synchronisation santé est activée
2. Vérifiez qu'il y a assez de données (minimum 3 entrées)
3. Déclenchez manuellement : `POST /api/alerts/check`

### Trop d'alertes

1. Marquez les anciennes comme lues
2. Les alertes anciennes (> 7 jours) sont automatiquement archivées
3. (À venir) Configurez les seuils pour réduire les alertes

### Alertes incorrectes

1. Vérifiez vos données (entrées de douleur, sync santé)
2. Plus de données = prédictions plus précises
3. Signalez les problèmes via les issues GitHub

---

## 📚 Ressources

- **API Reference** : `docs/API_REFERENCE.md`
- **Dashboard** : `http://localhost:8001/dashboard`
- **Guide Utilisateur** : `docs/USER_GUIDE.md`

---

**Date** : 23 janvier 2026  
**Dernière mise à jour** : 23 janvier 2026
