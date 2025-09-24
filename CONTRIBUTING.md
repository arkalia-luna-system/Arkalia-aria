# Contribuer à ARKALIA ARIA

Merci de contribuer à ARKALIA ARIA. Voici les règles simples pour garder un dépôt propre, performant et sans erreurs.

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

## Sécurité
- Pas de commandes dangereuses dans les scripts
- Utiliser les API du module `devops_automation.security` pour exécuter des commandes contrôlées

## Contact
Ouvrez une issue GitHub ou une discussion pour proposer des améliorations.


