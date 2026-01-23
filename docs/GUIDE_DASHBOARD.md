# 📊 Guide : Dashboard Interactif ARIA

**Date** : 23 janvier 2026  
**Version** : 1.0.0

---

## 🎯 Introduction

Le dashboard ARIA est votre interface principale pour visualiser et analyser vos données de santé. Il offre des graphiques interactifs, des filtres avancés, et des exports en un clic.

---

## 🌐 Accès au Dashboard

### URL Locale

```
http://localhost:8001/dashboard
```

### Pages Disponibles

- **Dashboard principal** : `/dashboard`
- **Santé** : `/dashboard/health`
- **Douleur** : `/dashboard/pain`
- **Analytics** : `/dashboard/analytics`
- **Patterns** : `/dashboard/patterns`
- **Rapports** : `/dashboard/reports`

---

## 📊 Fonctionnalités Principales

### 1. **Visualisation des Données**

#### Graphiques Temporels

- **Timeline de douleur** : Évolution de l'intensité dans le temps
- **Graphiques corrélations** : Sommeil ↔ Douleur, Stress ↔ Douleur
- **Heatmaps** : Pics horaires et jours de la semaine

#### Tableaux Interactifs

- **Entrées récentes** : Tableau avec tous les champs (nouveaux champs inclus)
- **Filtres en temps réel** : Filtrez par date, intensité, localisation, etc.
- **Tri** : Cliquez sur les en-têtes pour trier

---

### 2. **Filtres Avancés**

#### Filtres Disponibles

- **Date** : Sélectionnez une plage de dates
- **Intensité** : Filtrez par niveau de douleur (0-10)
- **Localisation** : Filtrez par zone du corps
- **Personnes présentes** : Filtrez par qui était présent
- **Émotions** : Filtrez par type d'émotion
- **Déclencheurs** : Filtrez par déclencheur physique/mental

#### Utilisation

1. Cliquez sur "Filtres" dans la barre latérale
2. Sélectionnez vos critères
3. Les graphiques et tableaux se mettent à jour automatiquement
4. Cliquez sur "Réinitialiser" pour effacer les filtres

---

### 3. **Exports en Un Clic**

#### Formats Disponibles

- **PDF** : Rapport complet avec graphiques
- **Excel** : Données tabulaires avec graphiques intégrés
- **CSV** : Données brutes pour analyse
- **HTML** : Rapport prêt à imprimer

#### Utilisation

1. Appliquez vos filtres (optionnel)
2. Cliquez sur le bouton d'export souhaité
3. Le fichier se télécharge automatiquement
4. Les filtres sont appliqués à l'export

---

### 4. **Alertes Visuelles**

#### Section Alertes

- **Alertes non lues** : Affichées en surbrillance
- **Types d'alertes** : Patterns, prédictions, corrélations, santé, RDV
- **Actions rapides** : Marquer comme lue, voir détails

#### Visualisation

Les alertes apparaissent :
- En haut du dashboard principal
- Dans la barre latérale
- Avec des icônes colorées selon le type

---

## 📈 Graphiques Disponibles

### 1. **Timeline de Douleur**

- **Axe X** : Date/Heure
- **Axe Y** : Intensité (0-10)
- **Interactivité** : Hover pour voir les détails, zoom

### 2. **Graphiques de Corrélations**

#### Sommeil ↔ Douleur

- **Axe X** : Heures de sommeil
- **Axe Y** : Intensité moyenne de douleur
- **Points** : Chaque point = une journée

#### Stress ↔ Douleur

- **Axe X** : Niveau de stress (0-10)
- **Axe Y** : Intensité moyenne de douleur
- **Tendance** : Ligne de régression

### 3. **Heatmaps**

#### Heatmap Temporelle

- **Axe X** : Heures de la journée (0-23)
- **Axe Y** : Jours de la semaine
- **Couleurs** : Intensité de douleur (vert = faible, rouge = élevé)

#### Heatmap de Corrélations

- **Matrice** : Toutes les corrélations possibles
- **Couleurs** : Force de la corrélation
- **Interactivité** : Cliquez pour voir les détails

---

## 🎨 Personnalisation

### Mode Sombre/Clair

1. Cliquez sur l'icône 🌙/☀️ dans l'en-tête
2. Le thème change instantanément
3. Votre préférence est sauvegardée

### Affichage des Colonnes

1. Dans les tableaux, cliquez sur "Colonnes"
2. Cochez/décochez les colonnes à afficher
3. Réorganisez par glisser-déposer

---

## 🔍 Recherche et Navigation

### Recherche Globale

1. Utilisez la barre de recherche en haut
2. Recherchez par :
   - Localisation
   - Notes
   - Émotions
   - Personnes présentes

### Navigation Rapide

- **Raccourcis clavier** :
  - `Ctrl+K` : Recherche rapide
  - `Ctrl+F` : Recherche dans la page
  - `Esc` : Fermer les modals

---

## 📱 Responsive Design

### Mobile

Le dashboard s'adapte automatiquement aux petits écrans :
- Menu hamburger
- Graphiques redimensionnés
- Tableaux scrollables horizontalement

### Tablette

Interface optimisée pour les tablettes avec :
- Navigation latérale
- Graphiques en pleine largeur
- Exports simplifiés

---

## 💡 Conseils d'Utilisation

### 1. **Explorez les Corrélations**

Utilisez les graphiques de corrélations pour identifier les patterns :
- Sommeil insuffisant → Douleur plus intense ?
- Stress élevé → Crises plus fréquentes ?

### 2. **Utilisez les Filtres**

Les filtres vous permettent de :
- Analyser des périodes spécifiques
- Comparer différents contextes
- Identifier des patterns précis

### 3. **Exportez Régulièrement**

Exportez vos données :
- Avant les consultations médicales
- Pour partager avec votre psychologue
- Pour garder une trace

### 4. **Surveillez les Alertes**

Consultez les alertes quotidiennement pour :
- Anticiper les crises
- Adapter votre comportement
- Suivre les recommandations

---

## 🔧 Dépannage

### Les graphiques ne s'affichent pas

1. Vérifiez que JavaScript est activé
2. Videz le cache du navigateur
3. Vérifiez la console pour les erreurs

### Les filtres ne fonctionnent pas

1. Vérifiez que vous avez des données
2. Réinitialisez les filtres
3. Rechargez la page

### Les exports échouent

1. Vérifiez que vous avez des données à exporter
2. Vérifiez les permissions d'écriture
3. Essayez un autre format

---

## 📚 Ressources

- **API Reference** : `docs/API_REFERENCE.md`
- **Guide Nouveaux Champs** : `docs/GUIDE_NOUVEAUX_CHAMPS.md`
- **Guide Alertes** : `docs/GUIDE_ALERTES.md`
- **Guide Utilisateur** : `docs/USER_GUIDE.md`

---

## 🆕 Fonctionnalités Récentes (23 janvier 2026)

- ✅ **Nouveaux champs visibles** : who_present, interactions, emotions, thoughts, physical_symptoms
- ✅ **Filtres avancés** : Filtrage par tous les nouveaux champs
- ✅ **Exports multi-formats** : PDF, Excel, HTML, JSON avec filtres appliqués
- ✅ **Graphiques interactifs** : Timeline avec zoom, hover, tooltips
- ✅ **Heatmaps** : Visualisation des corrélations et patterns temporels

---

**Date** : 23 janvier 2026  
**Dernière mise à jour** : 23 janvier 2026
