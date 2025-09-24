# 🛠️ Guide Développeur - ARKALIA ARIA

## 🚀 Développement Local

### Installation
```bash
git clone https://github.com/arkalia-luna-system/arkalia-aria.git
cd arkalia-aria
python -m venv arkalia_aria_venv
source arkalia_aria_venv/bin/activate
pip install -r requirements.txt
```

### Tests
```bash
# Tests complets (recommandé pour CI/CD)
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html

# Tests rapides (développement local)
ARIA_FAST_TEST=1 pytest -q

# Tests spécifiques
pytest tests/integration/test_devops_simple.py -v
```

### Qualité du Code
```bash
# Vérifications rapides
ruff check . --exclude arkalia_aria_venv
black . --check --exclude arkalia_aria_venv
mypy .

# Corrections automatiques
ruff check . --fix --exclude arkalia_aria_venv
black . --exclude arkalia_aria_venv

# Sécurité
bandit -r . -x tests -f json -o bandit-report.json
safety check --json -o safety-report.json
```

### Maintenance Workspace
```bash
# Nettoyage caches et rapports
make clean-cache

# Supprimer fichiers macOS cachés (._*, .DS_Store)
make clean-macos

# Vérification santé rapide
make workspace-health
```

### Lancer CIA et ARIA ensemble (développement)
```bash
# Terminal 1
cd ../arkalia-cia && uvicorn app:app --reload --port 8000

# Terminal 2
cd arkalia-aria && python main.py  # port 8001
```

---

## 🔧 Améliorations Récentes

### Corrections CI/CD (Décembre 2024)
- ✅ Workflows GitHub Actions convertis de JSON vers YAML
- ✅ Commande Safety corrigée (suppression du flag `--output` invalide)
- ✅ Suppression des fichiers `._` problématiques pour Black
- ✅ Mode de test rapide `ARIA_FAST_TEST=1` pour développement local
- ✅ Typage mypy complet sur tous les modules (44 fichiers sources)

### Qualité du Code
- ✅ Ruff : 0 erreur de linting
- ✅ Black : formatage cohérent sur 53 fichiers
- ✅ MyPy : typage strict sans erreurs
- ✅ Tests : 60 tests passent (mode rapide et complet)

### Modules Améliorés
- `pattern_analysis/emotion_analyzer.py` : TypedDict pour émotions
- `devops_automation/monitoring/aria_monitoring_system.py` : API complète
- `metrics_collector/cli.py` : dashboard intégré
- `cia_sync/api.py` : import requests robuste
- Tests d'intégration : mode rapide pour développement

---

**ARKALIA ARIA** - Guide développeur ! 🛠️🚀
