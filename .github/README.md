# 🚀 GitHub Actions - ARKALIA ARIA

Ce répertoire contient les workflows GitHub Actions pour le projet ARKALIA ARIA.

## 📋 Workflows Disponibles

### 🔍 CI/CD Pipeline (`ci-cd.yml`)

#### Pipeline principal de qualité et déploiement

- **Déclencheurs** : Push sur `main`/`develop`, Pull Requests, Déclenchement manuel
- **Jobs** :
  - 🧪 **Test** : Tests unitaires avec couverture sur Python 3.10/3.11/3.12
  - 🔍 **Lint** : Formatage (Black), Linting (Ruff), Types (MyPy), Sécurité (Bandit, Safety)
  - 🔒 **Security** : Scan de sécurité avec ARIA_SecurityValidator
  - 🏗️ **Build** : Construction de l'image Docker
  - 🚀 **Deploy** : Déploiement automatique (uniquement sur `main`)

### 🔒 Security Audit (`security.yml`)

#### Audit de sécurité automatisé

- **Déclencheurs** : Planification quotidienne (2h00 UTC), Déclenchement manuel
- **Jobs** :
  - 🔒 **Security Audit** : Audit de sécurité complet avec ARIA_SecurityValidator (scan de code, validation des commandes, détection de patterns dangereux)

### 📚 GitHub Pages (`deploy-docs.yml`)

#### Déploiement de documentation

- **Déclencheurs** : Push sur `main`/`develop`, PR, Déclenchement manuel
- **Jobs** :
  - 📚 **Build Docs** : Construction avec MkDocs
  - 🚀 **Deploy Docs** : Déploiement automatique sur GitHub Pages
  - 📢 **Notify Deployment** : Notifications de déploiement

## 🎯 Permissions et Sécurité

### Permissions par Workflow

| Workflow | contents | pages | id-token | security-events |
|----------|----------|-------|----------|-----------------|
| CI/CD | ✅ read | ❌ | ❌ | ❌ |
| Security | ✅ read | ❌ | ❌ | ✅ write |
| GitHub Pages | ✅ read | ✅ write | ✅ write | ❌ |

### Sécurité

- **Principe du moindre privilège** : Chaque workflow n'a que les permissions nécessaires
- **Pas de conflit de permissions** entre workflows
- **Audit de sécurité quotidien** automatique
- **Scan des dépendances** pour détecter les vulnérabilités

## 🚀 Utilisation

### Développement Normal

```bash
# Tests locaux
make test
make lint
make security

# Tests d'intégration
make integration-test

# Documentation locale
make docs-serve
```

### Déploiement

- **Automatique** : Push sur `main` → Déploiement automatique
- **Manuel** : Via l'interface GitHub Actions avec choix d'environnement
- **Documentation** : Déploiement automatique sur GitHub Pages

### Monitoring

```bash
# Statut des services
make status

# Logs
make logs

# Sauvegarde
make backup
```

## 📊 Métriques et Rapports

### Rapports Générés

- **Couverture de code** : HTML et XML
- **Sécurité** : Bandit, Safety, Semgrep
- **Qualité** : Ruff, MyPy, Black
- **Tests** : Pytest avec couverture
- **Documentation** : MkDocs

### Artefacts

- **Sécurité** : 90 jours de rétention
- **Couverture** : 30 jours de rétention
- **Documentation** : 1 jour de rétention
- **Packages** : 30 jours de rétention

## 🔧 Configuration

### Variables d'Environnement

- `PYTHON_VERSION` : Version Python (3.10)
- `PROJECT_NAME` : Nom du projet (arkalia-aria)
- `VENV_NAME` : Nom du venv (arkalia_aria_venv)

### Matrices de Test

- **Python** : 3.10, 3.11, 3.12
- **Services** : CIA mock pour tests d'intégration

## 🎨 Personnalisation

### Ajout de Jobs

1. Créer un nouveau fichier `.yml` dans `.github/workflows/`
2. Définir les permissions nécessaires
3. Ajouter les étapes de test/validation
4. Configurer les artefacts et notifications

### Modification des Seuils

- **Couverture** : Modifiable dans `pyproject.toml`
- **Sécurité** : Configurable dans les outils (Bandit, Safety)
- **Qualité** : Ajustable dans Ruff/Black

## 🚨 Dépannage

### Erreurs Communes

- **Permissions insuffisantes** : Vérifier les permissions du workflow
- **Tests d'intégration échoués** : Vérifier que CIA est accessible
- **Déploiement échoué** : Vérifier les secrets GitHub

### Logs et Debug

- **Logs GitHub Actions** : Interface GitHub → Actions → Détails
- **Logs locaux** : `make logs`
- **Statut services** : `make status`

---

**Objectif : Pipeline CI/CD robuste et sécurisé pour ARKALIA ARIA !** 🎯
