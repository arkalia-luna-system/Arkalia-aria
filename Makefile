# Makefile pour Arkalia-ARIA
# Basé sur les standards des autres projets Arkalia

.PHONY: help install install-dev test test-cov lint format security clean build run docs clean-cache clean-macos workspace-health

# Variables
PYTHON := python3
PIP := pip
VENV := arkalia_aria_venv
PYTHON_VENV := $(VENV)/bin/python
PIP_VENV := $(VENV)/bin/pip

# Couleurs pour les messages
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Afficher l'aide
	@echo "$(GREEN)Arkalia-ARIA - Commandes disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Installer les dépendances de base
    @echo "$(GREEN)Installation des dépendances de base...$(NC)"
    $(PIP_VENV) install -r requirements.txt
    $(PIP_VENV) install -e .

install-dev: ## Installer les dépendances de développement
    @echo "$(GREEN)Installation des dépendances de développement...$(NC)"
    $(PIP_VENV) install -r requirements.txt
    $(PIP_VENV) install -e ".[dev]"
    $(PIP_VENV) install pre-commit
    pre-commit install

test: ## Lancer les tests
	@echo "$(GREEN)Lancement des tests...$(NC)"
	$(PYTHON) -m pytest tests/ -v

test-cov: ## Lancer les tests avec couverture
	@echo "$(GREEN)Lancement des tests avec couverture...$(NC)"
	$(PYTHON) -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

test-integration: ## Lancer les tests d'intégration CIA/ARIA
	@echo "$(GREEN)Lancement des tests d'intégration...$(NC)"
	$(PYTHON) tests/integration/test_cia_aria_integration.py

lint: ## Lancer le linting
	@echo "$(GREEN)Lancement du linting...$(NC)"
	ruff check .
	mypy . --ignore-missing-imports || true

format: ## Formater le code
    @echo "$(GREEN)Formatage du code...$(NC)"
    ruff check . --fix
    black .

format-check: ## Vérifier le formatage sans modifier
	@echo "$(GREEN)Vérification du formatage...$(NC)"
	black --check --diff .
	isort --check-only --diff .

security: ## Lancer les vérifications de sécurité
	@echo "$(GREEN)Vérifications de sécurité...$(NC)"
	bandit -r . -f json -o bandit-report.json || true
	bandit -r . || true
	safety check --json --output safety-report.json || true
	safety check || true

clean: ## Nettoyer les fichiers temporaires
	@echo "$(GREEN)Nettoyage...$(NC)"
	./devops_automation/scripts/cleanup_heavy_processes.sh

clean-cache: ## Nettoyage caches Python et rapports
	@echo "$(GREEN)Nettoyage des caches Python et rapports...$(NC)"
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "bandit-report.json" -delete
	find . -type f -name "safety-report.json" -delete

clean-macos: ## Supprimer les fichiers cachés macOS (._*, .DS_Store)
	@echo "$(GREEN)Nettoyage fichiers macOS...$(NC)"
	find . -name "._*" -type f -delete || true
	find . -name ".DS_Store" -type f -delete || true

clean-heavy: ## Nettoyer les processus lourds (bandit, safety, pytest)
	@echo "$(GREEN)Nettoyage des processus lourds...$(NC)"
	./devops_automation/scripts/cleanup_heavy_processes.sh

workspace-health: ## Vérification santé rapide du workspace
	@echo "$(GREEN)Vérification santé du workspace...$(NC)"
	@echo "- Espace disque:"
	@df -h . | tail -n+2 || true
	@echo "- Processus Python actifs:"
	@ps aux | grep -i python | grep -v grep | head -n 10 || true
	@echo "- Fichiers macOS cachés restants:"
	@bash -c 'cnt=$(find . -name "._*" -type f | wc -l); echo $$cnt';

build: ## Construire le package
	@echo "$(GREEN)Construction du package...$(NC)"
	$(PYTHON) -m build

run: ## Lancer l'API ARIA
	@echo "$(GREEN)Lancement de l'API ARIA...$(NC)"
	$(PYTHON) main.py

run-dev: ## Lancer l'API en mode développement
	@echo "$(GREEN)Lancement de l'API en mode développement...$(NC)"
	uvicorn main:app --host 0.0.0.0 --port 8001 --reload

run-cia: ## Lancer CIA pour les tests d'intégration
	@echo "$(GREEN)Lancement de CIA pour les tests...$(NC)"
	cd ../arkalia-cia && source arkalia_cia_venv/bin/activate && uvicorn arkalia_cia_python_backend.api:app --host 127.0.0.1 --port 8000 &

docs: ## Construire la documentation
	@echo "$(GREEN)Construction de la documentation...$(NC)"
	mkdocs build --clean

docs-serve: ## Servir la documentation localement
	@echo "$(GREEN)Service de documentation local...$(NC)"
	mkdocs serve

docs-deploy: ## Déployer la documentation
	@echo "$(GREEN)Déploiement de la documentation...$(NC)"
	mkdocs gh-deploy

check: lint test security ## Lancer tous les checks (lint, test, security)

ci: clean install-dev check build ## Pipeline CI complet

# Commandes de développement
dev-setup: install-dev ## Configuration complète pour le développement
	@echo "$(GREEN)Configuration de développement terminée!$(NC)"
	@echo "$(YELLOW)Pour lancer l'API: make run-dev$(NC)"
	@echo "$(YELLOW)Pour lancer les tests: make test$(NC)"
	@echo "$(YELLOW)Pour la documentation: make docs-serve$(NC)"

# Commandes de déploiement
deploy-test: check build ## Déploiement de test
	@echo "$(GREEN)Déploiement de test...$(NC)"
	@echo "$(YELLOW)Prêt pour le déploiement!$(NC)"

deploy-prod: check build ## Déploiement de production
	@echo "$(GREEN)Déploiement de production...$(NC)"
	@echo "$(YELLOW)Prêt pour le déploiement en production!$(NC)"

# Commandes d'intégration CIA/ARIA
integration-test: ## Test complet d'intégration CIA/ARIA
	@echo "$(GREEN)Test d'intégration CIA/ARIA...$(NC)"
	@echo "$(YELLOW)Démarrage de CIA...$(NC)"
	cd ../arkalia-cia && source arkalia_cia_venv/bin/activate && uvicorn arkalia_cia_python_backend.api:app --host 127.0.0.1 --port 8000 &
	@sleep 3
	@echo "$(YELLOW)Démarrage d'ARIA...$(NC)"
	$(PYTHON) main.py &
	@sleep 3
	@echo "$(YELLOW)Lancement des tests d'intégration...$(NC)"
	$(PYTHON) tests/integration/test_cia_aria_integration.py
	@echo "$(GREEN)Test d'intégration terminé!$(NC)"

# Commandes de monitoring
status: ## Vérifier le statut des services
	@echo "$(GREEN)Vérification du statut des services...$(NC)"
	@curl -s http://127.0.0.1:8001/health || echo "$(RED)ARIA non accessible$(NC)"
	@curl -s http://127.0.0.1:8000/health || echo "$(RED)CIA non accessible$(NC)"

logs: ## Afficher les logs récents
	@echo "$(GREEN)Logs récents...$(NC)"
	@tail -f logs/aria.log 2>/dev/null || echo "$(YELLOW)Aucun log trouvé$(NC)"

# Commandes de sauvegarde
backup: ## Sauvegarder les données
	@echo "$(GREEN)Sauvegarde des données...$(NC)"
	@mkdir -p backups/$(shell date +%Y%m%d_%H%M%S)
	@cp *.db backups/$(shell date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "$(YELLOW)Aucune base de données à sauvegarder$(NC)"
	@echo "$(GREEN)Sauvegarde terminée!$(NC)"
