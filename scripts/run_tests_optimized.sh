#!/bin/bash
# ARKALIA ARIA - Script pour lancer les tests de manière optimisée
# Évite la surcharge système en limitant les processus lourds

echo "🧪 Lancement des tests ARIA en mode optimisé..."

# Variables d'environnement pour éviter les processus lourds
export ARIA_FAST_TEST=1
export ARIA_ENABLE_METRICS=false
export ARIA_ENABLE_HEAVY_CHECKS=false
export ARIA_QUICK_MODE=true
export BANDIT_SKIP_TESTS=true
export SAFETY_SKIP_TESTS=true

echo "✅ Mode rapide activé (ARIA_FAST_TEST=1)"

# Vérifier l'état du système avant
echo "📊 État du système AVANT les tests:"
echo "RAM libre: $(vm_stat | grep 'Pages free' | awk '{print $3 * 16 / 1024 " MB"}')"
echo "Load Average: $(uptime | awk -F'load averages:' '{print $2}')"

# Lancer les tests avec limitation de parallélisme
echo "🚀 Lancement des tests..."
pytest tests/ \
    -n 2 \
    --tb=short \
    --maxfail=5 \
    --durations=10 \
    -v

echo "✅ Tests terminés !"

# Vérifier l'état du système après
echo "📊 État du système APRÈS les tests:"
echo "RAM libre: $(vm_stat | grep 'Pages free' | awk '{print $3 * 16 / 1024 " MB"}')"
echo "Load Average: $(uptime | awk -F'load averages:' '{print $2}')"
