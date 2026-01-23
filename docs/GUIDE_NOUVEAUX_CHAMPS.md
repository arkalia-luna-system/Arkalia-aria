# 📝 Guide : Utilisation des Nouveaux Champs Journal

**Date** : 23 janvier 2026  
**Version** : 1.0.0

---

## 🎯 Introduction

ARIA propose maintenant 5 nouveaux champs pour enrichir votre journal de douleur et mieux comprendre les patterns émotionnels et contextuels.

---

## 📋 Les Nouveaux Champs

### 1. **Qui présent** (`who_present`)

**Description** : Personnes présentes lors de l'épisode de douleur.

**Exemples** :
- "Seul"
- "Famille"
- "Ami"
- "Collègue"
- "Médecin"

**Pourquoi c'est important** : Comprendre si la présence de certaines personnes influence votre douleur.

---

### 2. **Interactions** (`interactions`)

**Description** : Qui dit/fait quoi - interactions observées.

**Exemples** :
- "Conflit avec proche"
- "Discussion stressante au travail"
- "Soutien émotionnel reçu"
- "Aucune interaction"
- "Échange positif avec ami"

**Pourquoi c'est important** : Identifier les interactions qui déclenchent ou apaisent la douleur.

---

### 3. **Émotions** (`emotions`)

**Description** : Ce que je ressens - émotions et sensations.

**Exemples** :
- "Anxiété, frustration"
- "Joie, sérénité"
- "Colère, tristesse"
- "Calme, détente"
- "Stress, peur"

**Pourquoi c'est important** : Corréler vos émotions avec l'intensité de la douleur.

---

### 4. **Pensées** (`thoughts`)

**Description** : Ce que je pense - pensées et réflexions.

**Exemples** :
- "Je me sens dépassé par la situation"
- "Tout va bien se passer"
- "Je ne peux plus supporter ça"
- "Je vais y arriver"
- "Pourquoi moi ?"

**Pourquoi c'est important** : Comprendre comment vos pensées influencent votre douleur.

---

### 5. **Symptômes Physiques** (`physical_symptoms`)

**Description** : Symptômes physiques détaillés.

**Exemples** :
- "Tension musculaire, maux de tête"
- "Nausées, vertiges"
- "Raideur articulaire"
- "Fatigue intense"
- "Palpitations"

**Pourquoi c'est important** : Documenter tous les symptômes associés à la douleur.

---

## 💻 Utilisation via l'API

### Créer une entrée avec tous les nouveaux champs

```bash
curl -X POST "http://localhost:8001/api/pain/entry" \
  -H "Content-Type: application/json" \
  -d '{
    "intensity": 7,
    "location": "dos",
    "physical_trigger": "stress",
    "mental_trigger": "anxiété",
    "who_present": "Famille",
    "interactions": "Conflit avec proche",
    "emotions": "Anxiété, frustration",
    "thoughts": "Je me sens dépassé par la situation",
    "physical_symptoms": "Tension musculaire, maux de tête"
  }'
```

### Réponse

```json
{
  "id": 123,
  "intensity": 7,
  "location": "dos",
  "who_present": "Famille",
  "interactions": "Conflit avec proche",
  "emotions": "Anxiété, frustration",
  "thoughts": "Je me sens dépassé par la situation",
  "physical_symptoms": "Tension musculaire, maux de tête",
  "timestamp": "2026-01-23T10:30:00Z",
  "created_at": "2026-01-23T10:30:00Z"
}
```

---

## 🌐 Utilisation via le Dashboard Web

### Saisie rapide

1. Accédez au dashboard : `http://localhost:8001/dashboard/pain`
2. Cliquez sur "Ajouter une entrée"
3. Remplissez les champs obligatoires (intensité, localisation)
4. **Optionnel** : Remplissez les nouveaux champs dans la section "Contexte détaillé"
5. Cliquez sur "Enregistrer"

### Visualisation

Les nouveaux champs apparaissent dans :
- Le tableau des entrées récentes
- Les détails de chaque entrée (modal)
- Les exports (CSV, PDF, Excel)

---

## 📊 Analyse et Patterns

### Corrélations automatiques

ARIA analyse automatiquement :
- **Émotions ↔ Douleur** : Quelles émotions sont associées à une douleur plus intense ?
- **Interactions ↔ Douleur** : Certaines interactions déclenchent-elles plus de douleur ?
- **Qui présent ↔ Douleur** : La présence de certaines personnes influence-t-elle la douleur ?

### Accès aux analyses

```bash
# Corrélations émotions-douleur
GET /api/patterns/correlations/emotions-pain

# Déclencheurs récurrents (inclut interactions)
GET /api/patterns/triggers/recurrent

# Analyse complète
GET /api/patterns/analysis/comprehensive
```

---

## 📤 Exports

### Export CSV

Tous les nouveaux champs sont inclus dans l'export CSV :

```bash
GET /api/pain/export/csv
```

**Colonnes** :
- Date, Heure, Intensité, ...
- **Qui présent**
- **Interactions**
- **Émotions**
- **Pensées**
- **Symptômes physiques**

### Export PDF

Les nouveaux champs apparaissent dans le rapport PDF pour vos professionnels de santé.

### Export Excel

Tous les champs sont disponibles dans l'export Excel avec graphiques.

---

## 💡 Conseils d'Utilisation

### 1. **Soyez régulier**

Remplissez les nouveaux champs à chaque entrée pour avoir des données cohérentes.

### 2. **Soyez précis**

Utilisez des termes spécifiques :
- ❌ "Mal"
- ✅ "Anxiété, frustration, colère"

### 3. **Notez tout**

Même les détails qui semblent insignifiants peuvent révéler des patterns importants.

### 4. **Analysez régulièrement**

Consultez les corrélations dans le dashboard pour identifier les patterns.

---

## 🔍 Exemples de Patterns Détectés

### Exemple 1 : Interactions et Douleur

**Pattern détecté** : "Les conflits avec la famille sont associés à une douleur moyenne de 8/10"

**Action** : Travailler sur la communication familiale ou éviter les situations conflictuelles.

### Exemple 2 : Émotions et Douleur

**Pattern détecté** : "L'anxiété est corrélée avec une augmentation de 2 points d'intensité"

**Action** : Techniques de gestion de l'anxiété (respiration, méditation).

### Exemple 3 : Qui présent

**Pattern détecté** : "La douleur est moins intense quand je suis seul"

**Action** : Prévoir des moments de solitude pour récupérer.

---

## ❓ Questions Fréquentes

### Puis-je utiliser seulement certains champs ?

**Oui** ! Tous les nouveaux champs sont optionnels. Remplissez seulement ceux qui sont pertinents pour vous.

### Les anciennes entrées ont-elles ces champs ?

**Non**, seules les nouvelles entrées créées après l'ajout de ces champs les auront. Les anciennes entrées auront `null` pour ces champs.

### Puis-je modifier une entrée existante ?

**Actuellement non**, mais cette fonctionnalité est prévue. Pour l'instant, créez une nouvelle entrée avec les bonnes informations.

### Les données sont-elles privées ?

**Oui**, toutes les données sont stockées localement sur votre machine. Aucune donnée n'est envoyée sans votre consentement explicite.

---

## 📚 Ressources

- **API Reference** : `docs/API_REFERENCE.md`
- **Dashboard** : `http://localhost:8001/dashboard/pain`
- **Guide Utilisateur** : `docs/USER_GUIDE.md`

---

**Date** : 23 janvier 2026  
**Dernière mise à jour** : 23 janvier 2026
