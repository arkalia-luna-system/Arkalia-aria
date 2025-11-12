# Contribuer à ARKALIA ARIA

**Dernière mise à jour :** Novembre 2025

Merci de contribuer à ARKALIA ARIA. Voici les règles simples pour garder un dépôt propre, performant et sans erreurs.

---

## Conventions Git

### Workflow des Branches

```
main (production)
  ↑
develop (développement)
  ↑
feature/xxx (nouvelles fonctionnalités)
  ↑
hotfix/xxx (corrections urgentes)
```

**Règles :**
- **`main`** : Branche de production, toujours stable et testée
- **`develop`** : Branche de développement principale
- **`feature/xxx`** : Nouvelles fonctionnalités (ex: `feature/pain-export-pdf`)
- **`hotfix/xxx`** : Corrections urgentes pour production (ex: `hotfix/security-fix`)
- **`fix/xxx`** : Corrections de bugs (ex: `fix/api-error-handling`)

**Workflow :**
1. Créer une branche depuis `develop` : `git checkout -b feature/ma-fonctionnalite`
2. Développer et committer régulièrement
3. Pousser vers `origin` : `git push origin feature/ma-fonctionnalite`
4. Créer une Pull Request vers `develop`
5. Après validation, merger `develop` dans `main` pour la production

### Conventions de Commit

**Format :**
```
<type>(<scope>): <description courte>

<description détaillée optionnelle>

<footer optionnel>
```

**Types de commit :**
- `feat:` : Nouvelle fonctionnalité
- `fix:` : Correction de bug
- `docs:` : Documentation uniquement
- `style:` : Formatage, pas de changement de logique
- `refactor:` : Refactoring sans changement de fonctionnalité
- `perf:` : Amélioration de performance
- `test:` : Ajout ou modification de tests
- `chore:` : Maintenance, dépendances, configuration
- `ci:` : Changements CI/CD
- `build:` : Changements du système de build

**Scopes (optionnels mais recommandés) :**
- `pain` : Module pain_tracking
- `health` : Module health_connectors
- `core` : Module core
- `ci` : CI/CD
- `docs` : Documentation
- `mobile` : Application mobile
- `api` : API FastAPI
- `security` : Sécurité

**Exemples de commits :**
```bash
# Bon
git commit -m "feat(pain): add PDF export endpoint
- Add /api/pain/export/pdf endpoint
- Generate text-based PDF content
- Include pain entries in export
- Closes #123"

# Bon
git commit -m "fix(ci): corriger bandit - exclure fichiers macOS cachés"

# Bon
git commit -m "docs(api): mettre à jour endpoints dans API_REFERENCE.md"

# Mauvais
git commit -m "fix stuff"
git commit -m "update"
git commit -m "WIP"
```

**Règles :**
- Messages en français ou anglais (cohérent dans le projet)
- Description courte : max 72 caractères
- Utiliser l'impératif : "add" pas "added" ou "adds"
- Référencer les issues : `Closes #123`, `Fixes #456`
- Un commit = une modification logique

## Architecture Centralisée

ARKALIA ARIA utilise maintenant une architecture centralisée avec le module `core/` :

- **DatabaseManager** : Gestion centralisée de la base de données
- **CacheManager** : Cache intelligent avec TTL
- **BaseAPI** : Standardisation de toutes les APIs
- **Logging** : Système de logging unifié

**Règle importante** : Toujours utiliser les composants `core/` au lieu de créer des connexions DB ou du logging personnalisé.

## Branches
- Travail au quotidien sur `develop`
- Publication/production sur `main`
- Ouvrir des PRs de `feature/...` vers `develop`, puis `develop` vers `main`

## Qualité de code
- Lancer localement avant commit:
  - `ruff check . --fix`
  - `black .`
  - `pytest -q` (tests légers)
- Zéro warning toléré. Corriger au passage les petites dettes (typages, whitespace, exceptions chainées).

## Commits et PRs
- Messages de commit clairs (français ou anglais), au présent, concis
- Titres de PR: `type(scope): description`
  - Exemples: `feat(audio): tts simulée`, `fix(devops): raise from e`, `docs(mkdocs): nav` 
- Checklist PR:
  - CI verte (tests, lint, sécurité)
  - Docs MkDocs build OK
  - Lint Ruff/Black OK
  - Tests d’intégration légers OK
  - Pas de secrets dans le code

## Documentation
- Mettre à jour `docs/` et `mkdocs.yml` si endpoints ou modules changent
- Garder `README.md`, `DEVELOPER_GUIDE.md`, `API_REFERENCE.md` en phase
- **🆕 Mettre à jour `docs/MODULE_STATUS.md`** si statut des modules change
- Documenter les migrations vers `core/` dans les PRs

## Sécurité
- Pas de commandes dangereuses dans les scripts
- Utiliser les API du module `devops_automation.security` pour exécuter des commandes contrôlées

## Contact
Ouvrez une issue GitHub ou une discussion pour proposer des améliorations.


