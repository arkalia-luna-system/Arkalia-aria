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
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

### Qualité du Code
```bash
ruff check . --fix
black .
bandit -r .
mypy .
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

**ARKALIA ARIA** - Guide développeur ! 🛠️🚀
