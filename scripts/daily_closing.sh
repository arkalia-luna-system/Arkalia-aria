#!/bin/bash
# ARKALIA ARIA - Script de Fin de Journée
# Usage: ./scripts/daily_closing.sh

set -e  # Arrêter en cas d'erreur

# Couleurs pour les logs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de log
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Aller dans le répertoire du projet
cd /Volumes/T7/arkalia-aria

log "🚀 Début du nettoyage quotidien ARKALIA ARIA..."

# 1. Activer l'environnement virtuel
log "🐍 Activation de l'environnement virtuel..."
source arkalia_aria_venv/bin/activate
success "Environnement virtuel activé"

# 2. Tests rapides
log "📋 Exécution des tests..."
if pytest tests/ -q --tb=short; then
    success "Tests passés"
else
    warning "Certains tests ont échoué"
fi

# 3. Linting et formatage
log "🔍 Formatage et linting..."
if black . && ruff check . --fix; then
    success "Code formaté et linté"
else
    warning "Problèmes de formatage détectés"
fi

# 4. Vérification Git
log "📤 Vérification Git..."
git status --porcelain > /tmp/git_status.txt
if [ -s /tmp/git_status.txt ]; then
    log "Changements détectés, commit en cours..."
    git add .
    git commit -m "feat: daily work - $(date '+%d/%m/%Y %H:%M')
- Nettoyage quotidien automatique
- Tests et linting appliqués
- Documentation mise à jour"
    git push origin develop
    success "Changements commités et pushés"
else
    success "Aucun changement à commiter"
fi

# 5. Nettoyage des caches
log "🧹 Nettoyage des caches..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "._*" -type f -delete 2>/dev/null || true
success "Caches nettoyés"

# 6. Nettoyage des logs volumineux
log "📄 Nettoyage des logs volumineux..."
find . -name "*.log" -size +10M -delete 2>/dev/null || true
success "Logs nettoyés"

# 7. Vérification de l'espace disque
log "💾 Vérification de l'espace disque..."
SIZE=$(du -sh . | cut -f1)
log "Taille du projet: $SIZE"

# 8. Mise à jour du log quotidien
log "📝 Mise à jour du log quotidien..."
LOG_FILE="docs/DAILY_LOG.md"
if [ ! -f "$LOG_FILE" ]; then
    echo "# 📅 Log Quotidien ARKALIA ARIA" > "$LOG_FILE"
    echo "" >> "$LOG_FILE"
fi

echo "## $(date '+%d/%m/%Y %H:%M')" >> "$LOG_FILE"
echo "- [x] Nettoyage automatique exécuté" >> "$LOG_FILE"
echo "- [x] Tests: $(pytest tests/ --collect-only -q | wc -l | tr -d ' ') tests" >> "$LOG_FILE"
echo "- [x] Espace disque: $SIZE" >> "$LOG_FILE"
echo "- [x] Git: $(git log --oneline -1)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

success "Log quotidien mis à jour"

# 9. Résumé final
log "📊 Résumé de la session:"
echo "  - Tests: $(pytest tests/ --collect-only -q | wc -l | tr -d ' ') tests"
echo "  - Espace: $SIZE"
echo "  - Git: $(git log --oneline -1)"
echo "  - Heure: $(date '+%H:%M:%S')"

success "🎉 Nettoyage quotidien terminé !"
log "Projet prêt pour demain ! 🚀"
