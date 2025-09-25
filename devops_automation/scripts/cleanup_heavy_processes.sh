#!/bin/bash
# ARKALIA ARIA - Script de nettoyage des processus lourds
# Arrête les processus qui consomment trop de ressources

echo "🧹 Nettoyage des processus lourds ARKALIA ARIA..."

# Fonction pour tuer les processus par nom
kill_processes() {
    local process_name="$1"
    local max_cpu="$2"
    
    echo "🔍 Recherche de processus $process_name avec CPU > $max_cpu%..."
    
    # Trouver les PIDs des processus qui consomment trop de CPU
    pids=$(ps aux | awk -v proc="$process_name" -v max="$max_cpu" '
        $11 ~ proc && $3 > max { print $2 }
    ')
    
    if [ -n "$pids" ]; then
        echo "⚠️  Arrêt de $process_name (PIDs: $pids)"
        echo "$pids" | xargs kill -9 2>/dev/null || true
        echo "✅ $process_name arrêté"
    else
        echo "✅ Aucun processus $process_name problématique trouvé"
    fi
}

# Fonction pour vérifier l'état du système
check_system_health() {
    echo "📊 État du système:"
    echo "CPU: $(top -l 1 | grep "CPU usage" | awk '{print $3 " " $5 " " $7}')"
    echo "Mémoire: $(top -l 1 | grep "PhysMem" | awk '{print $2 " utilisée, " $6 " libre"}')"
    echo "Load Average: $(uptime | awk -F'load averages:' '{print $2}')"
}

# Vérifier l'état avant nettoyage
echo "📊 État AVANT nettoyage:"
check_system_health
echo ""

# Arrêter les processus problématiques
kill_processes "bandit" 50
kill_processes "safety" 50
kill_processes "pytest" 30
kill_processes "mypy" 30
kill_processes "black" 20
kill_processes "ruff" 20

# Arrêter les processus Python lourds
echo "🔍 Recherche de processus Python lourds..."
python_pids=$(ps aux | awk '$11 ~ /python/ && $3 > 20 { print $2 }')
if [ -n "$python_pids" ]; then
    echo "⚠️  Arrêt de processus Python lourds (PIDs: $python_pids)"
    echo "$python_pids" | xargs kill -9 2>/dev/null || true
    echo "✅ Processus Python lourds arrêtés"
else
    echo "✅ Aucun processus Python lourd trouvé"
fi

# Nettoyer les fichiers temporaires
echo "🧹 Nettoyage des fichiers temporaires..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "htmlcov" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name ".coverage" -delete 2>/dev/null || true
find . -name "bandit-report.json" -delete 2>/dev/null || true
find . -name "safety-report.json" -delete 2>/dev/null || true

echo "✅ Fichiers temporaires nettoyés"

# Vérifier l'état après nettoyage
echo ""
echo "📊 État APRÈS nettoyage:"
check_system_health

echo ""
echo "🎉 Nettoyage terminé ! Votre Mac devrait être plus réactif maintenant."
