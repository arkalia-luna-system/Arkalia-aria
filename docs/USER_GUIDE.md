# Guide Utilisateur

**ARKALIA ARIA** — Guide complet pour psychologues, patients et utilisateurs

**Version :** 1.0.0
*Dernière mise à jour :* Novembre 2025

---

## Table des matières

1. [Introduction](#introduction)
2. [Installation et Configuration](#installation-et-configuration)
3. [Interface Utilisateur](#interface-utilisateur)
4. [Gestion des Données de Santé](#gestion-des-données-de-santé)
5. [Suivi de la Douleur](#suivi-de-la-douleur)
6. [Analyses et Rapports](#analyses-et-rapports)
7. [Synchronisation Multi-Plateforme](#synchronisation-multi-plateforme)
8. [Paramètres et Personnalisation](#paramètres-et-personnalisation)
9. [Résolution de Problèmes](#résolution-de-problèmes)
10. [FAQ](#faq)

---

## Introduction

ARKALIA ARIA est une plateforme complète de recherche et d'assistance en intelligence artificielle pour le suivi de la santé mentale et physique. Cette solution intègre des connecteurs de santé multi-plateforme, un dashboard web interactif et une application mobile native.

### Pour qui est ARKALIA ARIA ?

- **Psychologues** : Outils d'analyse avancés et rapports détaillés
- **Patients** : Suivi personnel de la santé et de la douleur
- **Chercheurs** : Données anonymisées et analyses statistiques
- **Médecins** : Intégration avec les systèmes de santé existants

---

## Installation et Configuration

### Prérequis

- **Web Dashboard** : Navigateur moderne (Chrome, Firefox, Safari, Edge)
- **Application Mobile** : iOS 14+ ou Android 8+
- **Connecteurs Santé** : Montre Samsung, Google Fit, ou Apple Health

### Installation Web

1. Clonez le repository : `git clone <https://github.com/arkalia-luna-system/arkalia-aria.git`>
2. Installez les dépendances : `pip install -r requirements.txt`
3. Lancez l'application : `python main.py`
4. Accédez à <http://localhost:8000/dashboard>
5. Configurez vos connecteurs de santé

### Installation Mobile

#### iOS (En Développement)

1. Naviguez vers `arkalia-aria/mobile_app/`
2. Installez Flutter SDK
3. Exécutez `flutter pub get`
4. Lancez `flutter run` (simulateur iOS requis)

#### Android (En Développement)

1. Naviguez vers `arkalia-aria/mobile_app/`
2. Installez Flutter SDK
3. Exécutez `flutter pub get`
4. Lancez `flutter run` (émulateur Android requis)

---

## Interface Utilisateur

### Dashboard Web

#### Navigation Principale

- **Accueil** : Vue d'ensemble des métriques
- **Santé** : Données de santé détaillées
- **Douleur** : Suivi et analyse de la douleur
- **Patterns** : Visualisation des tendances
- **Rapports** : Génération de rapports

#### Fonctionnalités Clés

- **Thème Sombre/Clair** : Basculement en un clic
- **Synchronisation** : Mise à jour automatique des données
- **Exports** : PDF, Excel, HTML
- **Temps Réel** : Mise à jour automatique

### Application Mobile (En Développement)

#### Architecture Actuelle

- **Services** : Communication API, notifications, cache offline
- **Modèles** : Gestion des données de santé
- **Configuration** : Support Android et iOS

#### Fonctionnalités Prévues

- **Interface utilisateur** : Écrans spécialisés (en développement)
- **Synchronisation** : Bidirectionnelle avec l'API ARIA
- **Mode hors ligne** : Cache intelligent local
- **Notifications** : Push personnalisées

---

## Gestion des Données de Santé

### Connecteurs Disponibles

#### Samsung Health (Montres Samsung)

- **Fréquence cardiaque** : Mesures continues
- **Activité physique** : Pas, distance, calories
- **Sommeil** : Durée et qualité
- **Stress** : Niveaux de stress détectés

#### Google Fit (Android)

- **Activité** : Exercices et mouvements
- **Santé** : Poids, taille, IMC
- **Sommeil** : Données de repos
- **Nutrition** : Apport calorique

#### iOS Health (iPad/iPhone)

- **Santé générale** : Métriques complètes
- **Activité** : Exercices et objectifs
- **Sommeil** : Analyse du sommeil
- **Médicaments** : Rappels et suivi

### Synchronisation des Données

#### Configuration Initiale

1. Sélectionnez vos connecteurs
2. Autorisez l'accès aux données
3. Configurez la fréquence de sync
4. Testez la connexion

#### Synchronisation Automatique

- **Fréquence** : Toutes les 6 heures
- **Conditions** : Connexion réseau disponible
- **Batterie** : Niveau suffisant
- **Données** : Nouvelles données disponibles

#### Synchronisation Manuelle

- **Web** : Bouton "Synchroniser" dans l'en-tête
- **Mobile** : Pull-to-refresh ou bouton FAB
- **API** : Endpoints de synchronisation

---

## Suivi de la Douleur

### Saisie des Données

#### Niveaux de Douleur (0-10)

- **0** : Aucune douleur
- **1-3** : Légère
- **4-6** : Modérée
- **7-8** : Intense
- **9-10** : Très intense à insupportable

#### Types de Douleur

- **Musculaire** : Tensions, courbatures
- **Articulaire** : Rhumatismes, arthrose
- **Nerveuse** : Sciatique, névralgie
- **Migraine** : Maux de tête sévères
- **Crampe** : Contractions musculaires
- **Brûlure** : Sensation de brûlure
- **Pression** : Sensation de pression
- **Autre** : Douleur non classée

#### Localisations

- **Tête** : Crâne, visage, mâchoire
- **Cou** : Cervicales, trapèzes
- **Épaules** : Articulations, muscles
- **Dos** : Dorsales, lombaires
- **Poitrine** : Côtes, sternum
- **Abdomen** : Viscères, muscles
- **Membres** : Bras, jambes, mains, pieds

### Facteurs Déclencheurs

#### Saisie Rapide vs Détaillée

- **Rapide**: Intensité, déclencheur physique, action immédiate
- **Détaillée**: Déclencheurs physiques/mentaux, activité, localisation, efficacité, notes

#### Facteurs Physiques

- **Mouvement** : Certains gestes
- **Position** : Assis, debout, couché
- **Temps** : Heures, saisons
- **Météo** : Pression, humidité

#### Facteurs Psychologiques

- **Stress** : Tension, anxiété
- **Fatigue** : Manque de sommeil
- **Émotions** : Tristesse, colère
- **Concentration** : Effort mental

#### Facteurs Environnementaux

- **Alimentation** : Certains aliments
- **Médicaments** : Effets secondaires
- **Sommeil** : Qualité du repos
- **Activité** : Exercice, travail

---

## Analyses et Rapports

### Types d'Analyses

#### Analyses Temporelles

- **Tendances** : Évolution sur le temps
- **Cycles** : Patterns récurrents
- **Corrélations** : Liens entre facteurs
- **Prédictions** : Anticipation des crises

#### Analyses Comparatives

- **Avant/Après** : Efficacité des traitements
- **Périodes** : Comparaison temporelle
- **Groupes** : Comparaison avec d'autres patients
- **Objectifs** : Progression vers les buts

#### Analyses Statistiques

- **Moyennes** : Valeurs centrales
- **Médianes** : Valeurs typiques
- **Écarts-types** : Variabilité
- **Percentiles** : Distribution des données

### Génération de Rapports

#### Formats Disponibles

- **PDF** : Rapports professionnels
- **Excel** : Données tabulaires
- **HTML** : Rapports interactifs
- **CSV** : Données brutes

#### Types de Rapports

- **Rapport Hebdomadaire** : Synthèse de la semaine
- **Rapport Mensuel** : Bilan du mois
- **Rapport de Traitement** : Efficacité thérapeutique
- **Rapport Personnalisé** : Selon vos besoins

#### Personnalisation

- **Période** : Dates de début et fin
- **Métriques** : Données à inclure
- **Format** : Style et présentation
- **Destinataires** : Partage avec professionnels

---

## Synchronisation Multi-Plateforme

### Architecture de Synchronisation

#### Sources de Données

- **Montres Samsung** : Samsung Health
- **Android** : Google Fit
- **iOS** : Apple Health
- **Saisie Manuelle** : Interface utilisateur

#### Processus de Sync

1. **Collecte** : Récupération des données
2. **Validation** : Vérification de la qualité
3. **Normalisation** : Format unifié
4. **Stockage** : Sauvegarde sécurisée
5. **Synchronisation** : Mise à jour des plateformes

### Gestion des Conflits

#### Types de Conflits

- **Données Dupliquées** : Même période, sources différentes
- **Données Incohérentes** : Valeurs contradictoires
- **Données Manquantes** : Périodes non couvertes
- **Données Corrompues** : Erreurs de transmission

#### Résolution Automatique

- **Priorité** : Source la plus fiable
- **Validation** : Vérification de cohérence
- **Fusion** : Combinaison intelligente
- **Notification** : Alerte en cas de problème

---

## Paramètres et Personnalisation

### Paramètres Généraux

#### Interface

- **Thème** : Clair, sombre, automatique
- **Langue** : Français, Anglais, autres
- **Taille de Police** : Petite, normale, grande
- **Animations** : Activées, désactivées

#### Notifications

- **Synchronisation** : Alertes de sync
- **Rappels** : Saisie de données
- **Alertes** : Niveaux critiques
- **Mises à jour** : Nouvelles fonctionnalités

#### Confidentialité

- **Données Anonymes** : Partage anonyme
- **Chiffrement** : Protection des données
- **Rétention** : Durée de conservation
- **Suppression** : Droit à l'oubli

### Paramètres de Santé

#### Connecteurs

- **Activation** : Connecteurs actifs
- **Fréquence** : Intervalle de synchronisation
- **Données** : Types de données collectées
- **Seuils** : Valeurs d'alerte

#### Douleur

- **Échelle** : 0-6, 0-10, visuelle
- **Types** : Types de douleur suivis
- **Fréquence** : Saisie quotidienne, hebdomadaire
- **Rappels** : Notifications de saisie

---

## Résolution de Problèmes

### Problèmes Courants

#### Synchronisation

- **Pas de données** : Vérifiez la connexion
- **Données anciennes** : Forcez la synchronisation
- **Erreurs de connexion** : Redémarrez l'application
- **Permissions** : Vérifiez les autorisations

#### Performance

- **Lenteur** : Vérifiez la connexion réseau
- **Plantages** : Redémarrez l'application
- **Batterie** : Optimisez les paramètres
- **Espace** : Libérez de l'espace de stockage

#### Données

- **Données manquantes** : Vérifiez les connecteurs
- **Données incorrectes** : Vérifiez la saisie
- **Données dupliquées** : Contactez le support
- **Données perdues** : Vérifiez la sauvegarde

### Support Technique

#### Ressources

- **Documentation** : Guides détaillés
- **FAQ** : Questions fréquentes
- **Tutoriels** : Vidéos explicatives
- **Communauté** : Forum utilisateurs

#### Contact

- **Email** : <arkalia.luna.system@gmail.com>
- **Téléphone** : +33 1 23 45 67 89
- **Chat** : Support en ligne
- **Ticket** : Système de tickets

---

## FAQ

### Questions Générales

**Q : ARKALIA ARIA est-il gratuit ?**
R : Oui, la version de base est gratuite. Des fonctionnalités avancées sont disponibles avec un abonnement premium.

**Q : Mes données sont-elles sécurisées ?**
R : Oui, toutes les données sont chiffrées et stockées de manière sécurisée conformément au RGPD.

**Q : Puis-je utiliser ARKALIA ARIA sans connecteur de santé ?**
R : Oui, vous pouvez saisir vos données manuellement via l'interface web ou mobile.

### Questions Techniques

**Q : Quels appareils sont compatibles ?**
R : ARKALIA ARIA fonctionne sur tous les navigateurs modernes, iOS 14+, et Android 8+.

**Q : La synchronisation fonctionne-t-elle hors ligne ?**
R : Les données sont mises en cache localement et synchronisées dès que la connexion est rétablie.

**Q : Puis-je exporter mes données ?**
R : Oui, vous pouvez exporter vos données en PDF, Excel, ou CSV à tout moment.

### Questions Médicales

**Q : ARKALIA ARIA remplace-t-il un médecin ?**
R : Non, ARKALIA ARIA est un outil de suivi qui complète mais ne remplace pas les soins médicaux.

**Q : Les données peuvent-elles être partagées avec mon médecin ?**
R : Oui, vous pouvez générer des rapports à partager avec vos professionnels de santé.

**Q : Que faire en cas d'urgence médicale ?**
R : En cas d'urgence, contactez immédiatement les services d'urgence (15 en France).

---

## Contact et Support

### Support Utilisateur

- **Email** : <arkalia.luna.system@gmail.com>
- **Téléphone** : +33 1 23 45 67 89
- **Horaires** : Lundi-Vendredi 9h-18h

### Support Technique (Détails)

- **Email** : <arkalia.luna.system@gmail.com>
- **Documentation** : <https://docs.arkalia-aria.com>
- **GitHub** : <https://github.com/arkalia-aria>

### Communauté

- **Forum** : <https://community.arkalia-aria.com>
- **Discord** : <https://discord.gg/arkalia-aria>
- **Twitter** : @ARKALIA_ARIA

---

*Dernière mise à jour :* Novembre 2025
*Version du guide :* 1.0.0 (aligné avec version ARIA 1.0.0)
