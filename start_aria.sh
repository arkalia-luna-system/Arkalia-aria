#!/usr/bin/env bash
set -e

echo "🚀 ARKALIA ARIA - Démarrage simple"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "Erreur: python3 est requis mais introuvable dans le PATH."
  exit 1
fi

if [ ! -f "requirements.txt" ]; then
  echo "Erreur: requirements.txt introuvable. Lance ce script depuis la racine du projet."
  exit 1
fi

echo "▶ Installation des dépendances (si nécessaire)…"
python3 -m pip install -r requirements.txt >/dev/null

echo "▶ Lancement d'ARIA sur http://127.0.0.1:8001/app"
export ARIA_ENV=development
python3 -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload

