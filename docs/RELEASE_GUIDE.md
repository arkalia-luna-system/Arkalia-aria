# Guide de Release - ARKALIA ARIA

**Version actuelle :** 1.0.0

## Préparation d'une Release

### 1. Vérifier l'état actuel

```bash
# Vérifier que tout est propre
git status

# Vérifier que tous les tests passent
pytest

# Vérifier le linting
ruff check .
black --check .

# Vérifier la sécurité
bandit -r . -f json -o bandit-report.json
```

### 2. Mettre à jour la version

La version est définie dans :
- `main.py` : `version="1.0.0"`
- `pyproject.toml` : `version = "1.0.0"`

Pour une nouvelle version (ex: 1.1.0) :
1. Mettre à jour ces deux fichiers
2. Mettre à jour tous les fichiers `.md` qui mentionnent la version
3. Commit avec message : `chore: bump version to 1.1.0`

### 3. Créer un tag

```bash
# Créer un tag annoté
git tag -a v1.0.0 -m "Release 1.0.0 - Phase 2 & 3 terminées"

# Push le tag
git push origin v1.0.0
```

### 4. Merger develop → main

```bash
# Se placer sur main
git checkout main

# Mettre à jour main
git pull origin main

# Merger develop dans main
git merge develop

# Push sur main
git push origin main
```

### 5. Créer une Release GitHub

1. Aller sur GitHub : https://github.com/arkalia-luna-system/arkalia-aria/releases
2. Cliquer sur "Draft a new release"
3. Choisir le tag `v1.0.0`
4. Titre : `v1.0.0 - Phase 2 & 3 terminées`
5. Description :

```markdown
## 🎉 Release 1.0.0

### ✨ Nouvelles fonctionnalités

#### Phase 2 : Pattern Analysis avancé ✅
- Analyse de corrélations sommeil ↔ douleur
- Analyse de corrélations stress ↔ douleur
- Détection automatique de déclencheurs récurrents
- Patterns temporels (heures, jours de la semaine)
- Recommandations basées sur corrélations

#### Phase 3 : Synchronisation CIA complète ✅
- Synchronisation automatique périodique
- Système de configuration granularité
- Intégration complète avec documents CIA
- Génération de rapports médicaux
- Rapports pour consultation

### 🔧 Améliorations
- 15+ nouveaux endpoints API
- Documentation complète mise à jour
- Code propre (Black, Ruff, MyPy OK)

### 📚 Documentation
- API_REFERENCE.md : sections complètes
- DEVELOPER_GUIDE.md : guides techniques
- README.md : roadmap mise à jour

### 🚀 Prochaines étapes
- Phase 4 : Intégration BBIA (2026+, nécessite robot Reachy Mini)
```

6. Publier la release

## Notes importantes

### Version actuelle : 1.0.0

Cette version inclut :
- ✅ Phase 1 : Journal douleur & export basique
- ✅ Phase 2 : Patterns psy & corrélations
- ✅ Phase 3 : Synchro CIA + anonymisation

### Phase 4 : Planifiée (2026+)

La Phase 4 (intégration BBIA) est planifiée pour 2026+ car :
- Nécessite l'acquisition de robots Reachy Mini (Pollen Robotics)
- Robot personnel prévu : janvier 2026
- Robot pour maman : prévu ultérieurement
- L'architecture est prête pour l'intégration future

### Workflow Git recommandé

```bash
# Développement normal
git checkout develop
# ... faire des modifications ...
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin develop

# Pour une release
git checkout main
git merge develop
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin main
git push origin v1.0.0
```

## Checklist avant release

- [ ] Tous les tests passent
- [ ] Linting OK (Ruff, Black)
- [ ] Sécurité OK (Bandit, Safety)
- [ ] Documentation à jour
- [ ] Versions cohérentes partout
- [ ] README.md à jour
- [ ] CHANGELOG.md à jour (si existe)
- [ ] Tag créé et pushé
- [ ] Release GitHub créée

