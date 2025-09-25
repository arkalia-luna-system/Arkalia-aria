#!/bin/bash
# ARKALIA ARIA - Surveillance des processus lourds
# Surveille et arrête automatiquement les processus qui consomment trop de ressources

echo "🔍 Surveillance des processus lourds ARKALIA ARIA..."

# Fonction pour surveiller et arrêter les processus problématiques
monitor_and_kill() {
    local process_name="$1"
    local max_cpu="$2"
    local max_memory="$3"
    
    # Trouver les processus qui dépassent les limites
    pids=$(ps aux | awk -v proc="$process_name" -v max_cpu="$max_cpu" -v max_mem="$max_memory" '
        $11 ~ proc && ($3 > max_cpu || $4 > max_mem) { print $2 }
    ')
    
    if [ -n "$pids" ]; then
        echo "⚠️  Processus $process_name problématique détecté (PIDs: $pids)"
        echo "$pids" | xargs kill -9 2>/dev/null || true
        echo "✅ Processus $process_name arrêté"
        return 0
    fi
    return 1
}

# Surveillance continue
while true; do
    # Vérifier bandit (CPU > 50% ou RAM > 200MB)
    if monitor_and_kill "bandit" 50 2.0; then
        echo "🛑 Bandit arrêté - $(date)"
    fi
    
    # Vérifier pytest avec couverture (CPU > 30% ou RAM > 100MB)
    if monitor_and_kill "pytest.*--cov" 30 1.0; then
        echo "🛑 Pytest --cov arrêté - $(date)"
    fi
    
    # Vérifier safety (CPU > 30% ou RAM > 100MB)
    if monitor_and_kill "safety" 30 1.0; then
        echo "🛑 Safety arrêté - $(date)"
    fi
    
    # Attendre 10 secondes avant la prochaine vérification
    sleep 10
done
