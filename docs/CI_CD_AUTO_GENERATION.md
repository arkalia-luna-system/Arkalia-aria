# 🔄 Génération Automatique des Workflows CI/CD

## IMPORTANT : Ne pas modifier manuellement les fichiers .yml

Les fichiers dans `.github/workflows/` sont **automatiquement générés** par le système CI/CD d'ARKALIA ARIA.

## Comment ça fonctionne

### Génération automatique
- Le script `devops_automation/cicd/aria_cicd_manager.py` génère les workflows
- Les workflows sont créés en YAML à partir de templates Python
- La génération se fait lors des commits ou via commande manuelle

### Fichiers générés automatiquement
- `.github/workflows/ci-cd.yml`
- `.github/workflows/security.yml` 
- `.github/workflows/docs.yml`
- `.github/workflows/gh-pages.yml`

## 🛠️ **Comment modifier les workflows**

### 1. Modifier le code source
Éditer `devops_automation/cicd/aria_cicd_manager.py` :
- Fonction `_generate_github_actions()` pour les workflows
- Fonction `_generate_docker_config()` pour Docker
- Fonction `_generate_deployment_config()` pour le déploiement

### 2. Régénérer les workflows
```bash
# Régénération complète
python -m devops_automation.cicd.aria_cicd_manager

# Ou via le Makefile
make setup-cicd
```

### 3. Vérifier les changements
```bash
git status
git diff .github/workflows/
```

## 🚫 **Ce qu'il ne faut PAS faire**

- ❌ Modifier directement les fichiers `.yml` dans `.github/workflows/`
- ❌ Commiter des modifications manuelles des workflows
- ❌ Désactiver la génération automatique

## Ce qu'il faut faire

- ✅ Modifier uniquement le code Python dans `devops_automation/`
- ✅ Tester les changements avec `make setup-cicd`
- ✅ Commiter les modifications du code Python
- ✅ Laisser le système régénérer les workflows automatiquement

## 🔍 **Dépannage**

### Problème : Les workflows se changent à chaque commit
**Cause** : Le système régénère automatiquement les workflows
**Solution** : C'est normal ! Ne pas s'inquiéter, c'est le comportement attendu

### Problème : Erreur de syntaxe YAML
**Cause** : Bug dans le code de génération
**Solution** : Corriger `aria_cicd_manager.py` et régénérer

### Problème : Workflow ne fonctionne pas
**Cause** : Configuration incorrecte dans le code Python
**Solution** : Vérifier la logique dans `_generate_github_actions()`

## 📚 **Documentation technique**

- Code source : `devops_automation/cicd/aria_cicd_manager.py`
- Tests : `tests/unit/test_aria_cicd_manager.py`
- Configuration : `pyproject.toml` (section `[tool.aria]`)

## Avantages de cette approche

1. **Cohérence** : Tous les workflows suivent le même template
2. **Maintenance** : Un seul endroit pour modifier la logique CI/CD
3. **Évolutivité** : Facile d'ajouter de nouveaux environnements
4. **Sécurité** : Validation automatique des configurations
5. **Documentation** : Code auto-documenté avec commentaires

---

**Note** : Cette approche est utilisée par de nombreuses entreprises pour maintenir des pipelines CI/CD complexes de manière cohérente et évolutive.
