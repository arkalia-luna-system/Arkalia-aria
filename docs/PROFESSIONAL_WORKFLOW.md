# Guide des Bonnes Pratiques

**ARKALIA ARIA** — Standards et routines d'excellence

**Dernière mise à jour :** 23 janvier 2026

---

## Évaluation

### Score actuel : 9/10

#### Points forts

- **Architecture** : Migration vers `core/` parfaite
- **Documentation** : 97 fichiers MD, exhaustive
- **Git** : Commits détaillés et structurés
- **Nettoyage** : Gain de 1.5 GB, optimisation
- **Tests** : Vérification que tout fonctionne
- **Standards** : Black + Ruff systématiquement

#### Points à améliorer (6-7/10)

- **Tests automatisés** : Suite complète pas lancée
- **Sécurité** : Scans Bandit/Safety manquants
- **Monitoring** : Pas de métriques de performance
- **Planification** : Pas de TODO structuré pour demain

---

## Habitudes

### Routine de fin de journée

*Temps estimé : 15 minutes*

#### Tests & Validation (5 min)

```bash
# Tests complets
pytest tests/ -v --tb=short

# Linting et formatage
black . && ruff check . --fix

# Sécurité (optionnel mais recommandé)
bandit -r . -f json -o reports/bandit-report.json
safety check --json --output reports/safety-report.json

```

#### Git & Sauvegarde (3 min)

```bash
# Status et add
git status
git add .

# Commit structuré
git commit -m "feat: [module] description claire
- Détail 1
- Détail 2
- Fix: correction si applicable"

# Push
git push origin develop

```

#### Documentation (3 min)

```bash
# Mettre à jour le statut dans PROJECT_STATUS.md si nécessaire
# Les logs quotidiens sont maintenant dans les commits Git

```

#### Nettoyage (2 min)

```bash
# Caches Python
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Fichiers macOS
find . -name "._*" -type f -delete 2>/dev/null || true

# Logs volumineux
find . -name "*.log" -size +10M -delete 2>/dev/null || true

```

#### Planification (2 min)

```bash
# TODO pour demain - créer une issue GitHub ou noter dans PROJECT_STATUS.md
# Les tâches sont maintenant trackées dans les issues GitHub et PROJECT_STATUS.md

```

---

### Routine de début de journée

*Temps estimé : 10 minutes*

#### Vérification de l'état (3 min)

```bash
# Status Git
git status
git log --oneline -5

# Tests rapides
pytest tests/ -q --tb=short

```

#### Planification (3 min)

```bash
# Lire le TODO
cat docs/PROJECT_STATUS.md | grep -A 20 "Prochaines Étapes"

# Vérifier les issues GitHub pour les priorités
# Les tâches sont maintenant trackées dans PROJECT_STATUS.md et les issues GitHub

```

#### Environnement (2 min)

```bash
# Activer l'environnement
source arkalia_aria_venv/bin/activate

# Vérifier les dépendances
pip list | grep -E "(fastapi|pytest|black|ruff)"

```

#### Nettoyage (Début de journée) (2 min)

```bash
# Nettoyer les caches
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "._*" -type f -delete 2>/dev/null || true

```

---

## Standards

### Messages de Commit

#### Format

```text
<type>(<scope>): <description>

<body>

<footer>

```

#### Types

- `feat:` : Nouvelle fonctionnalité
- `fix:` : Correction de bug
- `docs:` : Documentation
- `style:` : Formatage, pas de changement de code
- `refactor:` : Refactoring
- `test:` : Tests
- `chore:` : Maintenance

#### Exemples

```bash
# Bon
git commit -m "feat(pain): add PDF export endpoint
- Add /api/pain/export/pdf endpoint
- Generate text-based PDF content
- Include 917 pain entries in export

Closes #123"

# Mauvais
git commit -m "fix stuff"

```

### Code Review

*Auto-review avant chaque commit*

#### Avant chaque commit

1. **Lire le code** : Est-ce que c'est clair ?
2. **Tester** : Est-ce que ça fonctionne ?
3. **Documenter** : Est-ce que c'est documenté ?
4. **Optimiser** : Est-ce que c'est efficace ?

#### Questions à se poser

- Est-ce que le code est lisible ?
- Est-ce que les noms de variables sont clairs ?
- Est-ce que les fonctions font une seule chose ?
- Est-ce que les erreurs sont gérées ?
- Est-ce que c'est testé ?

---

### Métriques Quotidiennes

#### À noter chaque jour

```bash
# Lignes de code
git diff --stat

# Couverture de tests
pytest --cov=. --cov-report=html

# Espace disque
du -sh .

# Performance
time python main.py

```

#### Exemple de log quotidien

```markdown
## 25/09/2025 18:30
- [x] Migration architecture centralisée
- [x] Nettoyage doublons (gain 1.5 GB)
- [x] Tests RGPD endpoints
- [x] Documentation mise à jour
- [x] Git push réussi

**Métriques :**
- Lignes : +150, -200
- Espace : 4.6 GB
- Tests : 100% passent
- Temps : 4h

**Demain :**
- [ ] Tests mobile device réel
- [ ] Validation RGPD expert
- [ ] Déploiement production

```

---

## Outils

### Scripts Automatiques

#### 1. Script de fin de journée

```bash
./scripts/daily_closing.sh

```

#### 2. Script de début de journée

```bash
./scripts/daily_start.sh

```

#### 3. Script de nettoyage

```bash
./scripts/cleanup.sh

```

### Configuration IDE

#### VSCode (Recommandé)

```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}

```

#### Extensions utiles

- Python
- GitLens
- Git Graph
- Markdown All in One
- REST Client

---

## Évolution

### Objectifs à court terme

*1 mois*

- [ ] Automatiser 100% des tests
- [ ] Implémenter les scans de sécurité
- [ ] Créer des métriques de performance
- [ ] Standardiser la documentation

### Objectifs à moyen terme

*3 mois*

- [ ] CI/CD complètement automatisé
- [ ] Monitoring en temps réel
- [ ] Tests de performance
- [ ] Documentation interactive

### Objectifs à long terme

*6 mois*

- [ ] Architecture microservices
- [ ] Déploiement automatique
- [ ] Monitoring avancé
- [ ] Formation d'autres développeurs

---

## Recommandations

### 1. Commence toujours par les tests

- Écris les tests avant le code (TDD)
- Vérifie que les tests passent
- Ajoute des tests pour les cas limites

### 2. Commits atomiques

- Un commit = une fonctionnalité
- Messages clairs et descriptifs
- Commits fréquents (plusieurs par jour)

### 3. Documentation vivante

- Mise à jour en continu
- Exemples concrets
- Guides pour les nouveaux

### 4. Nettoyage régulier

- Supprime le code mort
- Optimise les performances
- Garde la structure claire

### 5. Planification

- TODO quotidien
- Objectifs hebdomadaires
- Vision à long terme

### 6. Mesure et améliore

- Métriques de code
- Métriques de performance
- Métriques de qualité

---

## Conclusion

### Évaluation

Les habitudes de développement sont excellentes :

- ✅ Architecture solide
- ✅ Documentation exhaustive
- ✅ Git bien utilisé
- ✅ Standards respectés
- ✅ Nettoyage proactif

### Recommandations pour progresser

- 🔧 Automatiser les tests
- 🔍 Ajouter les scans de sécurité
- 📊 Mesurer les performances
- 📋 Planifier les journées de travail

### Conclusion

Les pratiques actuelles sont de très bon niveau et respectent les standards d'excellence.
