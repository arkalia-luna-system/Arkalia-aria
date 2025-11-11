#!/bin/bash
# ARKALIA ARIA - Script d'urgence pour libérer la RAM
# Arrête tous les processus lourds et nettoie la mémoire

echo "🚨 NETTOYAGE D'URGENCE RAM - ARKALIA ARIA"
echo "=========================================="

# 1. Arrêter tous les processus de développement lourds
echo "🛑 Arrêt des processus lourds..."
pkill -9 -f "pytest" 2>/dev/null || true
pkill -9 -f "bandit" 2>/dev/null || true
pkill -9 -f "mypy.*\. " 2>/dev/null || true
pkill -9 -f "ruff.*check.*\." 2>/dev/null || true
pkill -9 -f "black.*\." 2>/dev/null || true
pkill -9 -f "safety check" 2>/dev/null || true
pkill -9 -f "coverage" 2>/dev/null || true
sleep 2

# 2. Nettoyer les fichiers temporaires
echo "🧹 Nettoyage des fichiers temporaires..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name ".coverage" -delete 2>/dev/null || true
find . -name "bandit-report.json" -delete 2>/dev/null || true
find . -name "safety-report.json" -delete 2>/dev/null || true
find . -name ".mypy_cache" -type d -exec rm -rf {} + 2>/dev/null || true

# 3. Variables d'environnement pour désactiver les processus lourds
export ARIA_ENABLE_METRICS=false
export ARIA_ENABLE_HEAVY_CHECKS=false
export ARIA_QUICK_MODE=true
export ARIA_MAX_PARALLEL_JOBS=1
export ARIA_BANDIT_JOBS=1
export ARIA_PYTEST_JOBS=1
export ARIA_MYPY_JOBS=1
export BANDIT_SKIP_TESTS=true
export SAFETY_SKIP_TESTS=true
export PYTEST_CURRENT_TEST=""
export ARIA_METRICS_FAST=1

echo "✅ Variables d'environnement optimisées"

# 4. Afficher l'état de la mémoire
echo ""
echo "📊 État de la mémoire:"
if command -v python3 &> /dev/null; then
    python3 -c "import psutil; mem = psutil.virtual_memory(); print(f'  RAM utilisée: {mem.percent:.1f}%'); print(f'  RAM disponible: {mem.available / (1024**3):.2f} GB'); print(f'  RAM totale: {mem.total / (1024**3):.2f} GB')" 2>/dev/null || true
fi
vm_stat | head -5

# 5. Processus Python restants
echo ""
echo "🔍 Processus Python actifs:"
ps aux | grep -E "python.*test|python.*bandit|pytest" | grep -v grep | head -5 || echo "  ✅ Aucun processus lourd détecté"

# 6. Forcer le nettoyage de la mémoire compressée (macOS)
echo ""
echo "🔄 Libération de la mémoire compressée..."
# Essayer de libérer la mémoire inactive
sudo purge 2>/dev/null || {
    echo "  ⚠️  Purge nécessite sudo, tentative alternative..."
    # Alternative : forcer le swap
    sync && sync && sync
    # Nettoyer les caches système
    sudo dscacheutil -flushcache 2>/dev/null || true
    sudo killall -HUP mDNSResponder 2>/dev/null || true
}

# 7. Afficher l'état final
echo ""
echo "📊 État FINAL de la mémoire:"
if command -v python3 &> /dev/null; then
    python3 -c "import psutil; mem = psutil.virtual_memory(); print(f'  RAM utilisée: {mem.percent:.1f}%'); print(f'  RAM disponible: {mem.available / (1024**3):.2f} GB'); print(f'  RAM compressée: {mem.used / (1024**3) - mem.available / (1024**3):.2f} GB (estimation)')" 2>/dev/null || true
fi

echo ""
echo "✅ Nettoyage d'urgence terminé !"
echo "💡 La RAM devrait être libérée dans quelques secondes"
echo ""
echo "⚠️  NOTE: Si la RAM reste élevée, c'est probablement à cause de:"
echo "   - Cursor/Comet (applications lourdes)"
echo "   - Fermez des onglets inutilisés"
echo "   - Redémarrez Cursor si nécessaire"

