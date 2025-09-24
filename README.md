# 🧠❤️🔬 **ARKALIA ARIA** - Research Intelligence Assistant

**Assistant de Recherche Santé Personnelle - Laboratoire de données médicales 100% local**

---

<!-- Badges (sobres et factuels) -->
<p>
  <a href="https://github.com/arkalia-luna-system/arkalia-aria/actions/workflows/ci-cd.yml">
    <img alt="CI" src="https://github.com/arkalia-luna-system/arkalia-aria/actions/workflows/ci-cd.yml/badge.svg" />
  </a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-3776AB" />
  <img alt="Ruff" src="https://img.shields.io/badge/lint-ruff-0A7BBB" />
  <img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000" />
  <a href="https://github.com/arkalia-luna-system/arkalia-aria/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/arkalia-luna-system/arkalia-aria" />
  </a>
</p>

---

## Liens utiles

- Documentation API: `docs/API_REFERENCE.md`
- Guide Utilisateur: `docs/USER_GUIDE.md`
- Guide Développeur: `docs/DEVELOPER_GUIDE.md`
- Statut Projet: `docs/PROJECT_STATUS.md`
- Makefile: `Makefile`

---

## 🎯 **Vision**

ARKALIA ARIA (Arkalia Research Intelligence Assistant) est un laboratoire personnel de recherche santé qui transforme tes données médicales en insights actionables, tout en gardant un contrôle total sur tes informations sensibles.

**Philosophie** : Tes données médicales te appartiennent. ARIA travaille exclusivement pour toi, localement, sans jamais partager tes informations sans ton consentement explicite.

---

## 🏗️ **Architecture Modulaire**

```
arkalia-aria/
├── pain_tracking/     # Module tracking douleur avancé
├── pattern_analysis/   # IA découverte de patterns
├── prediction_engine/ # Anticiper les crises
├── health_connectors/ # Connecteurs Samsung/Google/Apple
├── metrics_collector/ # Dashboard web et métriques
├── mobile_app/        # Application Flutter native
├── research_tools/    # Laboratoire personnel
├── cia_sync/         # Sync avec CIA si besoin
└── docs/             # Documentation complète
```

Diagramme d’architecture (simplifié)

```mermaid
flowchart LR
  subgraph ARIA
    A[API FastAPI] --> P[pain_tracking]
    A --> AN[pattern_analysis]
    A --> PR[prediction_engine]
    A --> R[research_tools]
    A --> S[cia_sync]
  end
  S <--> CIA[(Arkalia CIA API 8000)]
```

---

## 🔬 **Modules**

### 📊 **Pain Tracking** ✅ **OPÉRATIONNEL**
- Saisie ultra-rapide (3 questions) - API testée et fonctionnelle
- Historique complet avec filtres - Endpoint `/api/pain/entries/recent`
- Export pour professionnels de santé
- Intégration capteurs (optionnel)
- **Modèles corrigés** : `physical_trigger` et `action_taken`

### 🧠 **Pattern Analysis** 
- Détection automatique de corrélations
- Analyse temporelle des crises
- Identification des déclencheurs
- Rapports visuels interactifs

### 🔮 **Prediction Engine**
- Modèles ML locaux (Ollama)
- Alertes préventives
- Recommandations personnalisées
- Apprentissage continu

### 🧪 **Research Tools**
- Laboratoire de données
- Expérimentations contrôlées
- Métriques de santé avancées
- Export anonymisé (optionnel)

### 🔗 **CIA Sync**
- Synchronisation optionnelle avec CIA
- Partage sélectif de données
- Mode "Psy Presentation"
- Contrôle granulaire des permissions

---

## 🚀 **Getting Started**

```bash
# Installation
git clone https://github.com/arkalia-luna-system/arkalia-aria.git
cd arkalia-aria
pip install -r requirements.txt

# Lancement
python main.py
```

### 🧹 Maintenance rapide

```bash
# Nettoyer caches Python et rapports
make clean-cache

# Supprimer fichiers cachés macOS (._*, .DS_Store)
make clean-macos

# Vérification santé du workspace (disque, processus, fichiers cachés)
make workspace-health
```

---

## 🔒 **Sécurité & Confidentialité**

- Local: les données sont stockées en local (SQLite). Pas de transmission externe par défaut.
- Authentification: non activée en mode développement local.
- Partage: synchronisation CIA optionnelle, à l’initiative de l’utilisateur.
- Export: CSV et rapports possibles; anonymisation à réaliser côté utilisateur si nécessaire.
- Variables d’environnement: voir `docs/USER_GUIDE.md` (valeurs par défaut incluses).

---

## 🌐 **Écosystème Arkalia Luna System**

| Projet | Relation | Description |
|--------|----------|-------------|
| **Arkalia CIA** | Complémentaire | Santé quotidienne basique |
| **Arkalia Quest** | Gamification | Système de récompenses |
| **BBIA Reachy Sim** | IA Émotionnelle | Analyse émotionnelle |
| **Arkalia Metrics** | Monitoring | Métriques système |

---

## 📈 **Roadmap**

- [x] Phase 1: Structure modulaire
- [x] Phase 2: Pain tracking (endpoints principaux)
- [ ] Phase 3: Pattern analysis (itératif)
- [ ] Phase 4: Prediction engine (améliorations)
- [ ] Phase 5: Research tools (laboratoire)
- [ ] Phase 6: Intégrations écosystème

---

## 🤝 **Contribution**

Ce projet fait partie de l'écosystème Arkalia Luna System. Les contributions sont les bienvenues !

- 🐛 **Issues** : Signaler des bugs
- 💡 **Feature Requests** : Proposer des améliorations  
- 📖 **Documentation** : Améliorer la doc
- 🧪 **Testing** : Tester et valider

---

## 📞 **Contact**

- **GitHub** : [arkalia-luna-system](https://github.com/arkalia-luna-system)
- **Issues** : [Ouvrir une issue](https://github.com/arkalia-luna-system/arkalia-aria/issues)

---

> **"Tes données médicales sont sacrées. ARIA les protège comme un trésor personnel."**
