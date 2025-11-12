# ARKALIA ARIA

**Research Intelligence Assistant**  
*Assistant de recherche santé personnelle*

> **Mis à jour régulièrement** — Ce projet est maintenu activement et mis à jour chaque semaine.

---

## Vision

ARKALIA ARIA transforme vos données médicales en insights actionnables, tout en conservant un contrôle total sur vos informations sensibles. Un laboratoire personnel de recherche santé qui travaille exclusivement pour vous, localement, sans jamais partager vos informations sans votre consentement explicite.

---

## Pourquoi ARIA ?

ARKALIA ARIA vous aide à mieux comprendre votre santé en analysant vos données médicales personnelles. Un assistant qui observe vos patterns de douleur, votre sommeil, votre activité physique, et vous fournit des insights utiles pour améliorer votre bien-être.

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

*Optionnel — Pour une utilisation complète avec synchronisation santé*

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

*En développement*

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
├── cia_sync/         # Synchronisation avec CIA si besoin
├── audio_voice/      # Interface vocale
└── docs/             # Documentation complète
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

## Sécurité et confidentialité

- **Local** : Les données sont stockées en local (SQLite). Aucune transmission externe par défaut.
- **Authentification** : Non activée en mode développement local.
- **Partage** : Synchronisation CIA optionnelle, à l'initiative de l'utilisateur.
- **Export** : CSV et rapports possibles ; anonymisation à réaliser côté utilisateur si nécessaire.
- **RGPD** : Conforme RGPD avec endpoints de suppression (droit à l'oubli) implémentés.

---

## Roadmap

- [x] Phase 1 : Structure modulaire
- [x] Phase 2 : Pain tracking (endpoints principaux)
- [x] Phase 3 : Health connectors (Samsung/Google/iOS) ✅ **Terminé**
- [x] Phase 4 : Dashboard web interactif ✅ **Terminé**
- [x] Phase 5 : Application mobile Flutter (architecture) 🚧 **En développement**
- [x] Phase 6 : Tests unitaires complets ✅ **Terminé**
- [x] Phase 7 : Documentation complète ✅ **Terminé**
- [ ] Phase 8 : Pattern analysis (itératif)
- [ ] Phase 9 : Prediction engine (améliorations)
- [ ] Phase 10 : Research tools (laboratoire)

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
<p>
  <a href="https://github.com/arkalia-luna-system/arkalia-aria/actions/workflows/ci-cd.yml">
    <img alt="CI" src="https://github.com/arkalia-luna-system/arkalia-aria/actions/workflows/ci-cd.yml/badge.svg" />
  </a>
  <a href="https://codecov.io/gh/arkalia-luna-system/arkalia-aria">
    <img alt="Codecov" src="https://codecov.io/gh/arkalia-luna-system/arkalia-aria/branch/main/graph/badge.svg" />
  </a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-3776AB" />
  <img alt="Ruff" src="https://img.shields.io/badge/lint-ruff-0A7BBB" />
  <img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000" />
  <a href="https://github.com/arkalia-luna-system/arkalia-aria/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/arkalia-luna-system/arkalia-aria" />
  </a>
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue" />
</p>

---

> **"Vos données médicales sont sacrées. ARIA les protège comme un trésor personnel."** — ARKALIA ARIA
