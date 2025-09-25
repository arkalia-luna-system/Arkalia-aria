#!/bin/bash
# ARKALIA ARIA - Script d'optimisation pour le développement
# Désactive les processus lourds et optimise les performances

echo "🚀 Optimisation ARKALIA ARIA pour le développement..."

# Variables d'environnement pour désactiver les processus lourds
export ARIA_ENABLE_METRICS=false
export ARIA_ENABLE_HEAVY_CHECKS=false
export ARIA_QUICK_MODE=true
export ARIA_MAX_PARALLEL_JOBS=2
export ARIA_BANDIT_JOBS=1
export ARIA_PYTEST_JOBS=2
export ARIA_MYPY_JOBS=1
export BANDIT_SKIP_TESTS=true
export SAFETY_SKIP_TESTS=true

echo "✅ Variables d'environnement configurées pour le développement"

# Arrêter tous les processus lourds existants
echo "🧹 Arrêt des processus lourds..."
pkill -f "bandit -r" 2>/dev/null || true
pkill -f "pytest.*--cov" 2>/dev/null || true
pkill -f "safety check" 2>/dev/null || true

echo "✅ Processus lourds arrêtés"

# Vérifier l'état du système
echo "📊 État du système après optimisation:"
echo "CPU: $(top -l 1 | grep "CPU usage" | awk '{print $3 " " $5 " " $7}')"
echo "Mémoire: $(top -l 1 | grep "PhysMem" | awk '{print $2 " utilisée, " $6 " libre"}')"
echo "Load Average: $(uptime | awk -F'load averages:' '{print $2}')"

echo ""
echo "🎉 Optimisation terminée ! Votre Mac devrait être beaucoup plus réactif."
echo "💡 Pour réactiver les métriques: export ARIA_ENABLE_METRICS=true"
echo "💡 Pour réactiver les vérifications lourdes: export ARIA_ENABLE_HEAVY_CHECKS=true"
