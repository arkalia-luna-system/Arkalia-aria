# Checklist de Fin de Journée

**ARKALIA ARIA** — Routine quotidienne d'excellence

**Dernière mise à jour :** 23 janvier 2026

---

## Checklist Quotidienne

#### Temps estimé : 15 minutes maximum

### 1. Tests & Validation

#### ~5 minutes

```bash
# Activer l'environnement
cd /Volumes/T7/arkalia-aria && source arkalia_aria_venv/bin/activate

# Tests rapides (mode silencieux)
pytest tests/ -q --tb=short

# Linting et formatage
black . && ruff check . --fix

# Vérification de sécurité (optionnel)
bandit -r . -f json -o reports/bandit-report.json
safety check --json --output reports/safety-report.json

```

### 2. Git & Sauvegarde

#### ~3 minutes

```bash
# Status et add
git status
git add .

# Commit avec message structuré
git commit -m "feat: [module] description claire
- Détail 1
- Détail 2
- Fix: correction si applicable"

# Push vers le repository
git push origin develop

```

### 3. Documentation

#### ~3 minutes

```bash
# Mettre à jour le statut
echo "## $(date '+%d/%m/%Y %H:%M')" >> docs/DAILY_LOG.md
echo "- [x] Tâche 1" >> docs/DAILY_LOG.md
echo "- [x] Tâche 2" >> docs/DAILY_LOG.md
echo "" >> docs/DAILY_LOG.md

```

### 4. Nettoyage

#### ~2 minutes

```bash
# Nettoyer les caches Python
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Nettoyer les logs volumineux
find . -name "*.log" -size +10M -delete 2>/dev/null || true

# Vérifier l'espace disque
du -sh .  # Afficher l'espace disque utilisé

```

### 5. Planification

#### ~2 minutes

```bash
# Créer la TODO pour demain
echo "## TODO Demain - $(date -d '+1 day' '+%d/%m/%Y')" >> docs/DAILY_LOG.md
echo "- [ ] Tâche prioritaire 1" >> docs/DAILY_LOG.md
echo "- [ ] Tâche prioritaire 2" >> docs/DAILY_LOG.md
echo "" >> docs/DAILY_LOG.md

```

---

## Script Automatisé

#### Optionnel — Pour automatiser la routine quotidienne

Créer `scripts/daily_closing.sh` :

```bash
#!/bin/bash
cd /Volumes/T7/arkalia-aria
source arkalia_aria_venv/bin/activate

echo "🧹 Nettoyage quotidien ARKALIA ARIA..."

# Tests
echo "📋 Tests..."
pytest tests/ -q --tb=short

# Linting
echo "🔍 Linting..."
black . && ruff check . --fix

# Git
echo "📤 Git..."
git add .
git commit -m "feat: daily work - $(date '+%d/%m/%Y')"
git push origin develop

# Nettoyage
echo "🧹 Nettoyage..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Nettoyage terminé !"

```

---

## Métriques Quotidiennes

### Indicateurs à suivre quotidiennement

- **Lignes de code ajoutées/supprimées** : `git diff --stat`
- **Temps de travail** : Estimation personnelle
- **Tâches accomplies** : Liste des fonctionnalités
- **Problèmes rencontrés** : Bugs ou blocages
- **Espace disque** : `du -sh .`

### Exemple de Log Quotidien

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

## Objectifs de Qualité

### Standards quotidiens

- ✅ **Code** : Black + Ruff = 0 erreur
- ✅ **Tests** : 100% passent
- ✅ **Git** : Commit + Push réussi
- ✅ **Doc** : Mise à jour des changements
- ✅ **Sécurité** : Scan Bandit/Safety (optionnel)

### Standards hebdomadaires

- 📊 **Métriques** : Couverture de code, performance
- 🔍 **Audit** : Review complet du code
- 📚 **Documentation** : Mise à jour des guides
- 🚀 **Déploiement** : Test en préproduction

---

## Recommandations

1. **Tests en priorité** — Vérifier que rien ne casse avant tout
2. **Commits atomiques** — Un commit = une fonctionnalité logique
3. **Messages structurés** — Utiliser `feat:`, `fix:`, `docs:`, `refactor:`
4. **Documentation à jour** — Mise à jour en continu
5. **Nettoyage systématique** — Éviter l'accumulation de déchets
6. **Planification rigoureuse** — Toujours noter les objectifs du lendemain
7. **Métriques suivies** — Mesurer pour progresser

> **Note importante :** Cette checklist doit être exécutée même les jours où l'activité de développement est limitée.
