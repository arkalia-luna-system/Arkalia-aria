# ARKALIA ARIA

**Research Intelligence Assistant**  
**Version :** 1.0.0

## Assistant de recherche santé personnelle

> **Mis à jour régulièrement** — Ce projet est maintenu activement et mis à jour chaque semaine.  
> **Dernière mise à jour majeure** : 12 décembre 2025 — Audit complet ARIA, corrections compatibilité CIA, documentation mise à jour.  
> **Phase 2 & 3 terminées** : Pattern analysis avancé et synchronisation CIA complète (bidirectionnelle + auto-sync).  
> **Audit 12 décembre 2025** : Voir [`docs/AUDIT_ARIA_12_DECEMBRE_2025.md`](docs/AUDIT_ARIA_12_DECEMBRE_2025.md) pour le détail complet.

---

## Vision

ARKALIA ARIA transforme vos données médicales en insights actionnables, tout en conservant un contrôle total sur vos informations sensibles. Un laboratoire personnel de recherche santé qui travaille exclusivement pour vous, localement, sans jamais partager vos informations sans votre consentement explicite.

> **📋 Audit Complet - 12 Décembre 2025** : Un audit complet du projet ARIA a été réalisé le 12 décembre 2025 suite aux corrections importantes apportées à CIA. Voir [`docs/AUDIT_ARIA_12_DECEMBRE_2025.md`](docs/AUDIT_ARIA_12_DECEMBRE_2025.md) pour le détail complet, [`docs/STATUT_IMPLEMENTATION_ARIA.md`](docs/STATUT_IMPLEMENTATION_ARIA.md) pour le statut d'implémentation, et [`docs/CORRECTIONS_NECESSAIRES_ARIA.md`](docs/CORRECTIONS_NECESSAIRES_ARIA.md) pour la liste des corrections nécessaires.

---

## Pourquoi ARIA ?

ARKALIA ARIA est votre **laboratoire personnel de recherche santé** : un journal de douleur intelligent et un analyseur de patterns psychologiques connecté à **CIA** (votre coffre-fort santé familial), avec export professionnel sécurisé pour médecins et psychologues.

**ARIA = microscope sur la douleur + mental**, préparant le contenu qui ira éventuellement dans CIA pour une vue d'ensemble santé.

### Pour qui ?

- **Patients chroniques** : Personnes souffrant de douleurs récurrentes (migraines, fibromyalgie, arthrite, etc.)
- **Personnes en burnout** : Suivi du stress, de l'anxiété et de la dysrégulation émotionnelle
- **Psychologues** : Outil d'accompagnement pour analyser les patterns comportementaux et émotionnels
- **Médecins** : Rapports structurés pour consultations plus efficaces

### Impact sur votre santé

**Pour la douleur chronique :**

- 📊 **Comprendre vos patterns** : Détection automatique des moments et causes d'apparition de vos douleurs
- 🔍 **Identifier les déclencheurs** : Stress, météo, activité physique, sommeil — ARIA trouve les corrélations
- ⚠️ **Anticiper les crises** : L'intelligence artificielle apprend vos patterns et peut vous prévenir avant une crise
- 📈 **Suivre l'efficacité** : Visualiser l'impact réel de vos traitements et actions

**Pour le bien-être mental :**

- 🧘 **Corrélation stress-douleur** : Comprendre comment votre état mental affecte votre douleur physique
- 😴 **Qualité du sommeil** : Observer l'impact du sommeil sur vos douleurs et votre humeur
- 📱 **Données de votre montre** : Synchronisation avec Samsung Health, Google Fit ou Apple Health pour une vue complète
- 🎯 **Objectifs personnalisés** : Recommandations basées sur votre profil unique

---

### Cas d'usage

#### Suivi de douleur chronique

> *"Je souffre de migraines chroniques. ARIA m'aide à identifier que mes crises arrivent souvent deux jours après un manque de sommeil. En faisant plus attention à mon rythme de sommeil, j'ai réduit mes migraines de 40%."*

**Fonctionnement :**

1. Saisie rapide de votre douleur (3 questions, 30 secondes)
2. Synchronisation automatique de vos données de sommeil depuis votre montre
3. Détection des patterns et visualisation des corrélations
4. Alertes préventives lorsque les conditions à risque se présentent

#### Préparation de consultation médicale

> *"Avant ma consultation chez le rhumatologue, j'exporte mes données ARIA en PDF. Mon médecin voit immédiatement l'évolution de ma douleur, les déclencheurs identifiés, et l'efficacité des traitements. Nous gagnons du temps et sommes plus précis."*

**Fonctionnement :**

1. Export d'un rapport complet (PDF, Excel, ou CSV)
2. Rapport contenant vos données de douleur, activité, sommeil, stress
3. Visualisation claire des graphiques et patterns pour votre médecin
4. Prise de décisions basées sur des données réelles

#### Amélioration du bien-être global

> *"ARIA m'a montré que mon niveau de stress (mesuré par ma montre Samsung) était corrélé avec mes douleurs dorsales. En travaillant sur la gestion du stress, j'ai réduit mes douleurs de dos de 60%."*

**Fonctionnement :**

1. Synchronisation de vos données de santé (pulsations, stress, activité)
2. Identification des corrélations entre stress, sommeil, activité et douleur
3. Réception de recommandations personnalisées
4. Suivi de l'impact de vos changements de mode de vie

---

## Douleur & Psy : Ce qu'ARIA suit

ARIA capture et analyse des données structurées pour comprendre vos patterns de douleur et votre état psychologique.

### Données de douleur

**Intensité** : Échelle 0-10 (0 = aucune douleur, 10 = douleur insupportable)

**Localisation** : Zone du corps affectée (tête, dos, genou, etc.)

**Qualité** : Type de douleur via déclencheurs :

- **Déclencheurs physiques** : Activité, posture, mouvement, météo, alimentation
- **Déclencheurs mentaux** : Stress, anxiété, fatigue, émotions

**Contexte temporel** :

- Heure de la journée
- Activité en cours
- État de sommeil (via synchronisation montre)
- Niveau de stress (via synchronisation montre)

**Actions et efficacité** :

- Action prise pour soulager (médicament, repos, étirement, etc.)
- Efficacité perçue (0-10)
- Notes libres pour détails supplémentaires

### Données psychologiques

**Humeur** : Suivi via corrélations avec douleur et activité

**Anxiété** : Détection via patterns de déclencheurs mentaux

**Dysrégulation émotionnelle** : Identification via corrélations stress-douleur

**Patterns comportementaux** : Détection automatique de routines et déclencheurs récurrents

### Utilisation des données

**Visualisation** :

- Graphiques temporels (timeline de douleur)
- Corrélations (stress ↔ douleur, sommeil ↔ douleur)
- Heatmaps (pics horaires, jours de la semaine)

**Détection de patterns** :

- Algorithmes simples au départ (règles déterministes)
- Intelligence artificielle pour corrélations complexes (en développement)

**Préparation de rapports** :

- Synthèses par période
- Export structuré pour professionnels de santé

---

## Export médical

ARIA génère des rapports professionnels pour vos consultations médicales et psychologiques.

### Formats disponibles

**PDF** : Rapport complet avec graphiques et synthèse

**CSV** : Données brutes pour analyse Excel/tableurs

**Excel** : Format tabulaire avec graphiques intégrés

**HTML** : Rapport psychologue prêt à imprimer (mode anonymisé)

### Contenu des rapports

**Synthèse statistique** :

- Nombre d'entrées sur la période
- Intensité moyenne
- Top déclencheurs (physiques et mentaux)
- Actions les plus efficaces
- Pics horaires récurrents

**Historique détaillé** :

- Toutes les entrées avec timestamp
- Intensité, localisation, déclencheurs
- Actions prises et efficacité
- Notes libres

**Graphiques** :

- Évolution temporelle de la douleur
- Corrélations avec sommeil, stress, activité
- Distribution par heure/jour

### Confidentialité et contrôle

**Filtrage** : Vous choisissez ce qui est inclus dans l'export

**Anonymisation** : Mode spécial pour psychologues (données anonymisées)

**Local-first** : Tous les exports sont générés localement, aucune donnée ne quitte votre machine

**Droit à l'oubli** : Suppression complète possible à tout moment (endpoints RGPD)

### Exemple de rapport médecin

Un médecin recevrait un PDF contenant :

1. **Résumé exécutif** : "Patient avec 45 entrées sur 30 jours, intensité moyenne 6.2/10"
2. **Déclencheurs identifiés** : "Manque de sommeil (12 occurrences), stress professionnel (8 occurrences)"
3. **Actions efficaces** : "Repos 20min → efficacité moyenne 7.5/10"
4. **Timeline** : Graphique montrant l'évolution sur la période
5. **Données brutes** : Tableau complet pour analyse approfondie

---

## ARIA vs CIA : Quelle différence ?

ARIA et CIA (Companion Intelligence Assistant) sont complémentaires dans l'écosystème Arkalia Luna, mais servent des objectifs différents.

### Positionnement clair

| Aspect | **CIA** | **ARIA** |
|--------|---------|----------|
| **Rôle principal** | Coffre-fort santé généraliste / Assistant familial | Laboratoire personnel profond / Microscope intime |
| **Public cible** | Seniors, familles, proches aidants | Patients chroniques, personnes en burnout, psy |
| **Type de données** | Documents médicaux, RDV, contacts urgence | Douleur fine-grain, patterns psy, corrélations |
| **Granularité** | Vue d'ensemble, agrégats, synthèses | Détails intimes, chaque entrée, chaque pattern |
| **Fréquence** | Événements ponctuels (RDV, documents) | Suivi continu (journal quotidien) |
| **Stockage** | Documents sécurisés (AES-256) | Base de données locale (SQLite) |
| **Export** | Documents médicaux complets | Rapports spécialisés (douleur, psy) |
| **Mode** | 100% offline, pas de cloud | 100% local, synchronisation optionnelle |

### En pratique

**CIA** = "Mon coffre-fort santé familial"

- Je stocke mes documents médicaux (ordonnances, résultats d'analyses)
- Je gère mes rendez-vous et rappels
- J'ai mes contacts d'urgence (ICE) à portée de main
- Je consulte mes portails santé
- **C'est mon point d'ancrage santé général**

**ARIA** = "Mon laboratoire personnel de recherche"

- Je note ma douleur et mon humeur tous les jours (3 questions, 30 secondes)
- J'analyse les patterns (stress → douleur, sommeil → humeur)
- Je prépare mes consultations avec des rapports structurés
- Je comprends mes déclencheurs et l'efficacité de mes actions
- **C'est mon microscope sur ma santé intime**

### Complémentarité

#### ARIA prépare → CIA consolide

1. **Dans ARIA** : Je note ma douleur quotidienne, j'analyse les patterns
2. **Vers CIA** : Les données agrégées (résumés, synthèses) vont dans CIA
3. **Dans CIA** : J'ai une vue d'ensemble avec mes documents médicaux
4. **Pour consultation** : CIA génère un rapport unifié (documents + données ARIA)

**Exemple concret** :

- **ARIA** : "J'ai noté 45 entrées de douleur sur 30 jours, intensité moyenne 6.2/10, déclencheur principal : manque de sommeil"
- **CIA** : "Rapport médical complet : Documents + Synthèse ARIA (douleur moyenne 6.2/10, déclencheur sommeil) + Historique RDV"

---

## Synchronisation ARIA ↔ CIA

ARIA et **CIA** (Companion Intelligence Assistant) travaillent ensemble dans l'écosystème Arkalia Luna.

### Scénarios de synchronisation

#### Scénario 1 : Journal quotidien dans ARIA → Agrégats dans CIA

> *"Je note ma douleur et mon humeur tous les jours dans ARIA. CIA ne voit que des agrégats pour les documents (ex: 'douleur moyenne cette semaine: 5/10'), pas tous les détails intimes de chaque entrée. Sauf si je choisis de partager plus."*

**Fonctionnalité** :

- ARIA stocke toutes les entrées détaillées localement
- CIA reçoit des résumés périodiques (quotidien, hebdomadaire)
- L'utilisateur contrôle le niveau de détail partagé

#### Scénario 2 : Préparation de consultation → Rapport généré

> *"Avant un RDV médical, CIA récupère les données pertinentes d'ARIA pour générer un rapport résumé. Le médecin voit l'évolution de la douleur, les déclencheurs identifiés, et l'efficacité des traitements, le tout intégré dans le dossier médical CIA."*

**Fonctionnalité** :

- Export ARIA → Import CIA avant consultation
- Rapport unifié (documents CIA + données ARIA)
- Partage sécurisé avec professionnel de santé

#### Scénario 3 : Mode psychologue anonymisé

> *"Pour ma séance avec mon psychologue, j'active le mode 'psy' dans ARIA. Les données sont anonymisées (pas de timestamps précis, pas de notes personnelles), puis exportées vers CIA pour partage sécurisé."*

**Fonctionnalité** :

- Anonymisation automatique (timestamps floutés, notes filtrées)
- Export HTML prêt à imprimer
- Synchronisation optionnelle avec CIA

### État d'implémentation

**✅ Implémenté** :

- Module `cia_sync/` avec API de synchronisation complète
- **Synchronisation automatique périodique** : Activée au démarrage si `ARIA_CIA_SYNC_ENABLED=true` (intervalle configurable)
- **Synchronisation bidirectionnelle** : Push ARIA → CIA et Pull CIA → ARIA (endpoint `/api/sync/pull-from-cia`)
- Endpoints de vérification de connexion CIA
- Synchronisation sélective (douleur, patterns, prédictions)
- **Agrégation intelligente** : Résumés vs détails selon granularité configurée
- Mode présentation psychologue (anonymisation automatique)
- **Intégration BBIA** : Module `bbia_integration/` pour communication avec robot (mode simulation)
- Push de données vers CIA
- Intégration complète avec documents CIA

**⚠️ Incompatibilités identifiées (12 décembre 2025)** :

- **Endpoints** : CIA attend `/api/pain-records` mais ARIA expose `/api/pain/entries` - Voir [`docs/CORRECTIONS_NECESSAIRES_ARIA.md`](docs/CORRECTIONS_NECESSAIRES_ARIA.md) pour les détails
- **Support URLs** : Vérifier compatibilité avec `https://xxx.onrender.com` et `127.0.0.1:8080` (CIA supporte maintenant ces formats)

**🚧 En développement** :

- Interface utilisateur pour contrôle granularité (Phase 4)
- Endpoints de compatibilité CIA (à implémenter)

---

## Écosystème Arkalia Luna

ARIA fait partie de l'écosystème **Arkalia Luna System**, un ensemble de projets interconnectés pour la santé personnelle.

### Projets liés

**CIA (Companion Intelligence Assistant)** : Coffre-fort santé familial

- [GitHub](https://github.com/arkalia-luna-system/arkalia-cia)
- Documents médicaux sécurisés, rappels, urgence
- Point d'ancrage santé de l'écosystème

**BBIA-SIM** : Moteur cognitif robotique pour Reachy Mini

- [GitHub](https://github.com/arkalia-luna-system/bbia-sim)
- 12 émotions robotiques, vision, voix
- Interface incarnée pour l'écosystème (Phase 4)
- **Intégration ARIA** : État émotionnel adaptatif basé sur données douleur/stress

### 📚 Pour aller plus loin

**Documentation détaillée côté CIA** :

- **[ARIA Integration](https://github.com/arkalia-luna-system/arkalia-cia/blob/develop/docs/ARIA_INTEGRATION.md)** — Vision clinique complète de l'intégration CIA ↔ ARIA avec scénarios d'utilisation
- **[Ecosystem Vision](https://github.com/arkalia-luna-system/arkalia-cia/blob/develop/docs/ECOSYSTEM_VISION.md)** — Vision stratégique de l'écosystème Arkalia Luna System
- **[Use Cases](https://github.com/arkalia-luna-system/arkalia-cia/blob/develop/docs/USE_CASES.md)** — Cas d'usage concrets pour différents profils utilisateurs (senior, patient douleur chronique, famille, professionnel santé)

### Vision système

```text
┌─────────────────────────────────────────────────────────────┐
│              ÉCOSYSTÈME ARKALIA LUNA SYSTEM                  │
│         Trois composants interconnectés pour la santé       │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────┐
    │                    ARIA                              │
    │         (Research Intelligence Assistant)            │
    │  • Journal douleur quotidien                        │
    │  • Analyse patterns psychologiques                  │
    │  • Prédictions ML locales                           │
    │  • Base de données locale (SQLite)                   │
    │  • Port: 8001                                        │
    └───────────────┬──────────────────┬───────────────────┘
                    │                  │
        ┌───────────▼──────────┐       │
        │   Synchronisation    │       │
        │   Bidirectionnelle   │       │
        │   • Auto-sync (60min)│       │
        │   • Push agrégats    │       │
        │   • Pull contexte    │       │
        └───────────┬──────────┘       │
                    │                  │
    ┌───────────────▼──────────────────▼───────────────────┐
    │                    CIA                                │
    │    (Companion Intelligence Assistant)                │
    │  • Coffre-fort santé familial                         │
    │  • Documents médicaux sécurisés (AES-256)            │
    │  • Rendez-vous médicaux                              │
    │  • Contacts urgence (ICE)                            │
    │  • Port: 8000                                        │
    └───────────────┬──────────────────────────────────────┘
                    │
        ┌───────────▼──────────┐
        │   État émotionnel   │
        │   • Douleur → Empathie│
        │   • Stress → Calmant │
        │   • Sommeil → Support│
        └───────────┬──────────┘
                    │
    ┌───────────────▼───────────────────────────────────────┐
    │                  BBIA-SIM                              │
    │         (Robot compagnon Reachy Mini)                  │
    │  • 12 émotions robotiques adaptatives                 │
    │  • Vision (YOLO, MediaPipe)                           │
    │  • Voix (Whisper, TTS)                                 │
    │  • Mode simulation disponible                          │
    │  • Port: 8002                                          │
    │  • Robot physique: janvier 2026                        │
    └────────────────────────────────────────────────────────┘
```

**Flux de données (implémentés)** :

- **ARIA** → **CIA** : Données de douleur/psy agrégées pour documents (synchronisation automatique périodique, intervalle configurable)
- **CIA** → **ARIA** : Contexte santé (RDV médicaux, médicaments, documents, historique) via endpoint `/api/sync/pull-from-cia`
- **ARIA** → **BBIA** : État émotionnel adaptatif basé sur douleur/stress/sommeil (mode simulation disponible, 4 endpoints API)

**Flux de données (futurs)** :

- **BBIA** → **ARIA/CIA** : Interactions et observations comportementales (nécessite robot physique)

**Futures intégrations** :

- BBIA adapte son comportement selon l'état ARIA (douleur élevée → empathie renforcée)
- CIA génère des rappels basés sur les patterns ARIA
- Métriques système collectées pour amélioration continue

### Pour aller plus loin

**Documentation détaillée côté CIA** :

- [`docs/ARIA_INTEGRATION.md`](https://github.com/arkalia-luna-system/arkalia-cia/blob/develop/docs/ARIA_INTEGRATION.md) : Vision clinique de l'intégration ARIA ↔ CIA
- [`docs/ECOSYSTEM_VISION.md`](https://github.com/arkalia-luna-system/arkalia-cia/blob/develop/docs/ECOSYSTEM_VISION.md) : Vision complète de l'écosystème Arkalia Luna
- [`docs/USE_CASES.md`](https://github.com/arkalia-luna-system/arkalia-cia/blob/develop/docs/USE_CASES.md) : Cas d'usage par profils utilisateurs

**Documentation ARIA** :

- [`docs/API_REFERENCE.md`](docs/API_REFERENCE.md) : Documentation complète des endpoints
- [`docs/DEVELOPER_GUIDE.md`](docs/DEVELOPER_GUIDE.md) : Guide développeur et contribution
- [`docs/PROFESSIONAL_WORKFLOW.md`](docs/PROFESSIONAL_WORKFLOW.md) : Workflow pour professionnels de santé

**Audits et Statut** :

- [`docs/AUDIT_ARIA_12_DECEMBRE_2025.md`](docs/AUDIT_ARIA_12_DECEMBRE_2025.md) : Audit complet du 12 décembre 2025
- [`docs/STATUT_IMPLEMENTATION_ARIA.md`](docs/STATUT_IMPLEMENTATION_ARIA.md) : Statut d'implémentation détaillé
- [`docs/CORRECTIONS_NECESSAIRES_ARIA.md`](docs/CORRECTIONS_NECESSAIRES_ARIA.md) : Liste des corrections nécessaires priorisées

---

## Confidentialité

**Vos données vous appartiennent :**

- ✅ **100% local** : Tout est stocké sur votre ordinateur, jamais dans le cloud
- ✅ **Contrôle total** : Vous choisissez ce que vous partagez, quand vous le partagez
- ✅ **Conforme RGPD** : Suppression de toutes vos données possible à tout moment
- ✅ **Aucun tracking** : Aucune donnée n'est envoyée sans votre consentement explicite

---

## 💻 **Compatibilité**

### Versions Python Supportées

| Version | Statut | Notes |
|---------|--------|-------|
| Python 3.10 | ✅ Supporté | Version recommandée |
| Python 3.11 | ✅ Supporté | Testé et validé |
| Python 3.12 | ✅ Supporté | Testé et validé |
| Python 3.9 | ❌ Non supporté | Trop ancien |
| Python 3.13+ | ⚠️ Non testé | Peut fonctionner mais non validé |

### Systèmes d'Exploitation

| OS | Statut | Notes |
|----|--------|-------|
| Linux | ✅ Supporté | Testé sur Ubuntu 20.04+ |
| macOS | ✅ Supporté | Testé sur macOS 12+ |
| Windows | ✅ Supporté | Testé sur Windows 10/11 |
| WSL | ✅ Supporté | Windows Subsystem for Linux |

### Navigateurs Web (Dashboard)

| Navigateur | Version minimale | Statut |
|------------|------------------|--------|
| Chrome | 90+ | ✅ Supporté |
| Firefox | 88+ | ✅ Supporté |
| Safari | 14+ | ✅ Supporté |
| Edge | 90+ | ✅ Supporté |

### Connecteurs Santé

| Plateforme | Statut | Versions testées |
|------------|--------|------------------|
| Samsung Health | ✅ Supporté | Galaxy Watch 4+, S24+ |
| Google Fit | ✅ Supporté | Android 8+ |
| Apple Health | ✅ Supporté | iOS 14+, iPadOS 14+ |

---

## Démarrage rapide

### ⚡ **5 minutes pour tester ARIA**

```bash
# 1. Cloner le projet
git clone https://github.com/arkalia-luna-system/arkalia-aria.git
cd arkalia-aria

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer ARIA
python main.py
```

L'application démarre sur `http://localhost:8000`

### Premiers pas

1. **Ouvrir votre navigateur** : `http://localhost:8000`
2. **Noter votre première douleur** : Cliquer sur "Saisie rapide" (3 questions, 30 secondes)
3. **Explorer le dashboard** : Observer vos données s'afficher en temps réel
4. **Activer le mode sombre** : Cliquer sur l'icône lune 🌙 dans l'en-tête

### Installation complète

#### Optionnel — Pour une utilisation complète avec synchronisation santé

Pour une utilisation complète avec synchronisation santé :

1. **Connecter votre montre** : Dans "Connecteurs Santé", choisir Samsung Health, Google Fit ou Apple Health
2. **Configurer les connecteurs** : Suivre le guide dans `docs/USER_GUIDE.md`
3. **Explorer les fonctionnalités** : Dashboard, patterns, exports, etc.

---

## Fonctionnalités

### Suivi de douleur intelligent

- **Saisie ultra-rapide** : 3 questions, 30 secondes maximum
- **Historique complet** : Toutes vos entrées avec filtres par date, intensité, localisation
- **Export professionnel** : PDF, Excel, CSV pour vos médecins
- **Détection de patterns** : L'intelligence artificielle trouve automatiquement les corrélations

### Synchronisation santé

- **Samsung Health** : Montres Samsung (Galaxy Watch)
- **Google Fit** : Téléphones Android
- **Apple Health** : iPhone et iPad
- **Données synchronisées** : Activité, sommeil, pulsations, stress, poids

### Application mobile

#### En développement

- Interface native Flutter
- Synchronisation bidirectionnelle
- Notifications intelligentes
- Mode hors-ligne

### Dashboard interactif

- **Graphiques temps réel** : Visualisation de vos données de santé
- **Analyses avancées** : Patterns, corrélations, tendances
- **Exports multiples** : PDF, Excel, HTML
- **Interface moderne** : Design intuitif et responsive

### Intelligence artificielle

- **Détection de patterns** : Trouve automatiquement les déclencheurs
- **Prédictions** : Anticipe les crises avant qu'elles arrivent
- **Recommandations** : Suggestions personnalisées basées sur votre profil
- **Apprentissage continu** : Plus vous utilisez ARIA, plus il devient précis

---

## Architecture

### Structure du projet

```text
arkalia-aria/
├── core/              # Module centralisé (DatabaseManager, Cache, Logging)
├── pain_tracking/     # Module tracking douleur
├── pattern_analysis/  # IA découverte de patterns
├── prediction_engine/ # Anticiper les crises
├── health_connectors/ # Connecteurs Samsung/Google/iOS Health
├── metrics_collector/ # Dashboard web interactif
├── mobile_app/        # Application Flutter native
├── research_tools/    # Laboratoire personnel
├── cia_sync/         # Synchronisation avec CIA
├── audio_voice/      # Interface vocale
└── docs/             # Documentation complète
```

### Diagramme d'architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    ARKALIA ARIA                              │
│              (FastAPI + SQLite Local)                        │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   UI Layer   │   │  API Layer   │   │  Data Layer  │
│              │   │              │   │              │
│ - Dashboard  │   │ - FastAPI    │   │ - SQLite     │
│   Web        │   │ - REST API   │   │ - Local DB   │
│ - Mobile App │   │ - WebSocket  │   │ - Cache      │
│   (Flutter)  │   │              │   │              │
└──────┬───────┘   └──────┬───────┘   └──────┬───────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Pain Tracking│  │   Pattern    │  │  Prediction  │
│              │  │   Analysis   │  │   Engine     │
│ - Quick Entry│  │              │  │              │
│ - Detailed   │  │ - Corrélations│ │ - ML Models  │
│ - History    │  │ - Patterns   │  │ - Alerts     │
│ - Export     │  │ - Trends     │  │ - Forecasts │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Health     │ │   CIA Sync   │ │   Metrics   │
│  Connectors  │ │              │ │  Collector  │
│              │ │ - Selective  │ │              │
│ - Samsung    │ │ - Bidirectional│ - Dashboard │
│ - Google Fit │ │ - Anonymize  │ │ - Reports   │
│ - iOS Health │ │              │ │ - Analytics │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │   External       │
              │   - CIA API     │
              │   - Health APIs │
              └──────────────────┘
```

---

### Modules

#### Pain Tracking ✅ **Opérationnel**

- Saisie ultra-rapide (3 questions) — API testée et fonctionnelle
- Historique complet avec filtres — Endpoint `/api/pain/entries/recent`
- Export pour professionnels de santé
- Intégration capteurs (optionnel)

#### Health Connectors ✅ **Opérationnel**

- **Samsung Health** : Synchronisation montres Samsung
- **Google Fit** : Intégration Android (S24)
- **iOS Health** : Connexion iPad Apple Health
- **API FastAPI** : 16 endpoints santé complets
- **Sync Manager** : Gestionnaire de synchronisation unifié

#### Pattern Analysis

- Détection automatique de corrélations
- Analyse temporelle des crises
- Identification des déclencheurs
- Rapports visuels interactifs

#### Prediction Engine

- Modèles ML locaux (Ollama)
- Alertes préventives
- Recommandations personnalisées
- Apprentissage continu

---

## CI/CD & Qualité

ARIA suit les mêmes standards de qualité industrielle que CIA et BBIA.

### Pipeline CI/CD

**Workflows GitHub Actions** :

- **CI/CD Principal** (`ci-cd.yml`) :
  - Tests unitaires sur Python 3.10, 3.11, 3.12
  - Formatage (Black), Linting (Ruff), Types (MyPy)
  - Sécurité (Bandit, Safety)
  - Couverture de code (Codecov)
  - Build Docker
  - Déploiement automatique

- **Security Audit** (`security.yml`) :
  - Analyse statique (Bandit)
  - Vulnérabilités (Safety)
  - Scan avancé (Semgrep)
  - Audit des dépendances
  - Vérification de licences

- **Documentation** (`gh-pages.yml`) :
  - Construction MkDocs
  - Déploiement GitHub Pages

### Métriques de qualité

**Tests** :

- 394 tests collectés (100% passent)
- Couverture de code : Suivi via Codecov (badge affiche la branche `main`)
- Tests d'intégration CIA/ARIA

**Code Quality** :

- **Black** : Formatage automatique (ligne 88)
- **Ruff** : Linting rapide (E, F, W, I, B, C4, UP)
- **MyPy** : Vérification de types
- **Bandit** : Analyse de sécurité
- **Safety** : Audit des dépendances

**Standards** :

- Code conforme PEP 8
- Typage strict avec MyPy
- Documentation des fonctions
- Tests pour chaque module

### Badges de statut

Les badges en haut du README affichent :

- Statut CI/CD (passing/failing)
- Couverture de code (Codecov)
- Versions Python supportées
- Linters (Ruff, Black)
- Nombre d'issues ouvertes
- Licence (MIT)

### Workflow de développement

1. **Commit** : Pre-commit hooks (Black, Ruff, MyPy)
2. **Push** : Déclenchement automatique du pipeline CI/CD
3. **Tests** : Exécution sur 3 versions Python
4. **Lint** : Vérification formatage et qualité
5. **Sécurité** : Scan automatique
6. **Merge** : Validation requise avant merge sur `main`

### Documentation

- **API Reference** : `docs/API_REFERENCE.md`
- **Developer Guide** : `docs/DEVELOPER_GUIDE.md`
- **Technical Reference** : `docs/TECHNICAL_REFERENCE.md`
- **GitHub Actions** : `.github/README.md`

---

## Sécurité et confidentialité

### Stockage local

**100% local** : Les données sont stockées en local (SQLite). Aucune transmission externe par défaut.

**Chiffrement** : Stockage local sécurisé (à venir : chiffrement AES-256 pour données sensibles)

**Aucun cloud forcé** : Aucune donnée ne quitte votre machine sans consentement explicite

### Contrôle utilisateur

**Partage granular** : Synchronisation CIA optionnelle, à l'initiative de l'utilisateur

**Filtrage export** : Vous choisissez ce qui est inclus dans les rapports

**Anonymisation** : Mode spécial pour psychologues avec anonymisation automatique

**Droit à l'oubli** : Endpoints RGPD implémentés pour suppression complète des données

### Conformité

**RGPD** : Conforme RGPD avec :

- Droit d'accès (export de toutes vos données)
- Droit de rectification (modification des entrées)
- Droit à l'oubli (suppression complète)
- Portabilité des données (export CSV/JSON)

**Aucun tracking** : Aucune donnée analytique envoyée sans consentement

**Transparence** : Code source ouvert, audit de sécurité possible

---

## Roadmap

Roadmap alignée avec l'écosystème Arkalia Luna (CIA, BBIA).

### Phase 1 : Journal douleur & export basique ✅ **Terminé**

- [x] Structure modulaire
- [x] Pain tracking (endpoints principaux)
- [x] Saisie rapide (3 questions, 30 secondes)
- [x] Export CSV/PDF/Excel pour professionnels
- [x] Base de données locale SQLite

### Phase 2 : Patterns psy & corrélations ✅ **Terminé**

- [x] Health connectors (Samsung/Google/iOS) ✅ **Terminé**
- [x] Dashboard web interactif ✅ **Terminé**
- [x] Tests unitaires complets ✅ **Terminé**
- [x] Pattern analysis avancé (corrélations sommeil, stress) ✅ **Terminé**
- [x] Détection automatique de déclencheurs récurrents ✅ **Terminé**
- [ ] Visualisations interactives (heatmaps, timelines) 🔮 **Planifié (Phase 4)**

### Phase 3 : Synchro CIA + anonymisation ✅ **Terminé**

- [x] Module `cia_sync/` avec API ✅ **Terminé**
- [x] Synchronisation sélective (douleur, patterns, prédictions) ✅ **Terminé**
- [x] Mode présentation psychologue (anonymisation) ✅ **Terminé**
- [x] Synchronisation automatique périodique ✅ **Terminé**
- [x] Agrégation intelligente (résumés vs détails) ✅ **Terminé**
- [x] Système de configuration granularité ✅ **Terminé**
- [x] Intégration complète avec documents CIA ✅ **Terminé**
- [ ] Interface utilisateur pour contrôle granularité 🔮 **Planifié (Phase 4)**

### Phase 4 : Boucle avec BBIA 🔮 **Planifié**

- [ ] Application mobile Flutter native (architecture en place)
- [ ] Prédiction engine amélioré (ML locaux)
- [ ] Intégration BBIA (émotions, coaching adaptatif)
- [ ] BBIA adapte comportement selon état ARIA
- [ ] Research tools (laboratoire personnel avancé)
- [ ] Intelligence artificielle pour patterns complexes

---

## Contribution

Ce projet fait partie de l'écosystème Arkalia Luna System. Les contributions sont les bienvenues.

### Bon point de départ

Vous êtes nouveau dans le projet ? Commencez par ces issues marquées `good first issue` :

- [Voir les "good first issue"](https://github.com/arkalia-luna-system/arkalia-aria/labels/good%20first%20issue)

### Comment contribuer

- 🐛 **Issues** : Signaler des bugs
- 💡 **Feature Requests** : Proposer des améliorations
- 📖 **Documentation** : Améliorer la documentation
- 🧪 **Testing** : Tester et valider
- 🎨 **UI/UX** : Améliorer l'interface (mode sombre, accessibilité)
- 🔒 **Sécurité** : Scanner et corriger les vulnérabilités

---

## Contact et liens

- **GitHub** : [arkalia-luna-system](https://github.com/arkalia-luna-system)
- **Issues** : [Ouvrir une issue](https://github.com/arkalia-luna-system/arkalia-aria/issues)
- **Documentation API** : `docs/API_REFERENCE.md`
- **Guide Utilisateur** : `docs/USER_GUIDE.md`
- **Guide Développeur** : `docs/DEVELOPER_GUIDE.md`

---

<!-- Badges -->
<!-- markdownlint-disable MD033 -->
<p>
  <a href="https://github.com/arkalia-luna-system/arkalia-aria/actions/workflows/ci-cd.yml">
    <img alt="CI" src="https://github.com/arkalia-luna-system/arkalia-aria/actions/workflows/ci-cd.yml/badge.svg" />
  </a>
  <a href="https://codecov.io/gh/arkalia-luna-system/arkalia-aria">
    <img alt="Codecov" src="https://codecov.io/gh/arkalia-luna-system/arkalia-aria/branch/main/graph/badge.svg" />
    <!-- Note: Badge affiche la couverture de la branche main (stable). Pour develop, voir le dashboard Codecov -->
  </a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-3776AB" />
  <img alt="Ruff" src="https://img.shields.io/badge/lint-ruff-0A7BBB" />
  <img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000" />
  <a href="https://github.com/arkalia-luna-system/arkalia-aria/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/arkalia-luna-system/arkalia-aria" />
  </a>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue" />
</p>
<!-- markdownlint-enable MD033 -->

---

> **"Vos données médicales sont sacrées. ARIA les protège comme un trésor personnel."** — ARKALIA ARIA
