@echo off
echo ARKALIA ARIA - Demarrage simple (Windows)
echo.

if not exist requirements.txt (
  echo Erreur: requirements.txt introuvable. Lance ce script depuis la racine du projet.
  pause
  goto :eof
)

where python >nul 2>&1
if errorlevel 1 (
  echo Erreur: Python est requis mais introuvable dans le PATH.
  pause
  goto :eof
)

if not exist .venv (
  echo Creation d'un environnement virtuel .venv ...
  python -m venv .venv
)

call .venv\Scripts\activate
echo Installation des dependances (si necessaire)...
python -m pip install -r requirements.txt >nul

echo Lancement d'ARIA sur http://127.0.0.1:8001/app
set ARIA_ENV=development
python -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload

