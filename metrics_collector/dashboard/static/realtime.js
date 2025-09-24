/**
 * ARKALIA ARIA - Real-time Updates
 * ================================
 * 
 * Gestion des mises à jour en temps réel pour le dashboard ARIA.
 * Utilise WebSocket ou polling pour maintenir les données à jour.
 */

class ARIARealTime {
    constructor() {
        this.isConnected = false;
        this.updateInterval = null;
        this.charts = new Map();
        this.callbacks = new Map();
        this.updateFrequency = 30000; // 30 secondes par défaut
        this.retryAttempts = 0;
        this.maxRetries = 5;
        this.retryDelay = 5000; // 5 secondes
    }

    /**
     * Initialise les mises à jour en temps réel
     */
    initialize() {
        this.setupEventListeners();
        this.startRealTimeUpdates();
        this.initializeCharts();
    }

    /**
     * Configure les écouteurs d'événements
     */
    setupEventListeners() {
        // Écouter les changements de visibilité de la page
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.pauseUpdates();
            } else {
                this.resumeUpdates();
            }
        });

        // Écouter les changements de thème
        document.addEventListener('themeChanged', (event) => {
            this.updateTheme(event.detail.theme);
        });

        // Écouter les erreurs de réseau
        window.addEventListener('online', () => {
            this.handleConnectionRestored();
        });

        window.addEventListener('offline', () => {
            this.handleConnectionLost();
        });
    }

    /**
     * Démarre les mises à jour en temps réel
     */
    startRealTimeUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        this.updateInterval = setInterval(() => {
            this.performUpdate();
        }, this.updateFrequency);

        this.isConnected = true;
        this.updateConnectionStatus(true);
    }

    /**
     * Met en pause les mises à jour
     */
    pauseUpdates() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        this.isConnected = false;
        this.updateConnectionStatus(false);
    }

    /**
     * Reprend les mises à jour
     */
    resumeUpdates() {
        if (!this.updateInterval) {
            this.startRealTimeUpdates();
        }
    }

    /**
     * Effectue une mise à jour des données
     */
    async performUpdate() {
        try {
            const updatePromises = [];

            // Mettre à jour les métriques système
            updatePromises.push(this.updateSystemMetrics());

            // Mettre à jour les données de santé
            updatePromises.push(this.updateHealthData());

            // Mettre à jour les données de douleur
            updatePromises.push(this.updatePainData());

            // Mettre à jour le statut des connecteurs
            updatePromises.push(this.updateConnectorsStatus());

            // Attendre que toutes les mises à jour soient terminées
            await Promise.allSettled(updatePromises);

            // Mettre à jour l'horodatage de la dernière mise à jour
            this.updateLastUpdateTime();

            // Réinitialiser le compteur de tentatives
            this.retryAttempts = 0;

        } catch (error) {
            console.error('Erreur lors de la mise à jour:', error);
            this.handleUpdateError(error);
        }
    }

    /**
     * Met à jour les métriques système
     */
    async updateSystemMetrics() {
        try {
            const response = await fetch('/api/metrics/system');
            if (response.ok) {
                const data = await response.json();
                this.updateMetricDisplay('cpu-usage', data.cpu_usage + '%');
                this.updateMetricDisplay('memory-usage', data.memory_usage + '%');
                this.updateMetricDisplay('db-size', data.db_size + ' MB');
                this.updateMetricDisplay('uptime', data.uptime + 'h');
            }
        } catch (error) {
            console.error('Erreur mise à jour métriques système:', error);
        }
    }

    /**
     * Met à jour les données de santé
     */
    async updateHealthData() {
        try {
            const response = await fetch('/api/health/metrics/unified?days_back=1');
            if (response.ok) {
                const data = await response.json();

                // Mettre à jour les métriques d'activité
                if (data.activity) {
                    this.updateMetricDisplay('daily-steps', data.activity.total_steps);
                    this.updateMetricDisplay('calories-burned', data.activity.total_calories);
                    this.updateMetricDisplay('avg-heart-rate', data.activity.avg_heart_rate);
                }

                // Mettre à jour les métriques de sommeil
                if (data.sleep) {
                    this.updateMetricDisplay('sleep-duration',
                        Math.floor(data.sleep.avg_duration_minutes / 60) + 'h' +
                        (data.sleep.avg_duration_minutes % 60) + 'm');
                    this.updateMetricDisplay('sleep-quality',
                        Math.round(data.sleep.avg_quality_score * 100) + '%');
                }

                // Mettre à jour les métriques de stress
                if (data.stress) {
                    this.updateMetricDisplay('stress-level', data.stress.avg_stress_level);
                }

                // Mettre à jour les graphiques si disponibles
                this.updateHealthCharts(data);
            }
        } catch (error) {
            console.error('Erreur mise à jour données santé:', error);
        }
    }

    /**
     * Met à jour les données de douleur
     */
    async updatePainData() {
        try {
            const response = await fetch('/api/pain/entries/recent?limit=10');
            if (response.ok) {
                const data = await response.json();

                if (data.length > 0) {
                    const avgIntensity = data.reduce((sum, entry) => sum + entry.intensity, 0) / data.length;
                    const frequency = data.length / 7; // Entrées par jour sur 7 jours

                    this.updateMetricDisplay('pain-level', avgIntensity.toFixed(1));
                    this.updateMetricDisplay('pain-frequency', frequency.toFixed(1));
                }

                // Mettre à jour les graphiques de douleur
                this.updatePainCharts(data);
            }
        } catch (error) {
            console.error('Erreur mise à jour données douleur:', error);
        }
    }

    /**
     * Met à jour le statut des connecteurs
     */
    async updateConnectorsStatus() {
        try {
            const response = await fetch('/api/health/connectors/status');
            if (response.ok) {
                const data = await response.json();

                Object.keys(data).forEach(connector => {
                    const statusElement = document.getElementById(`${connector.replace('_', '-')}-status`);
                    if (statusElement) {
                        const connectorData = data[connector];
                        statusElement.textContent = connectorData.status === 'connected' ? 'Connecté' : 'Déconnecté';
                        statusElement.className = `connector-status ${connectorData.status}`;
                    }
                });
            }
        } catch (error) {
            console.error('Erreur mise à jour statut connecteurs:', error);
        }
    }

    /**
     * Met à jour l'affichage d'une métrique
     */
    updateMetricDisplay(elementId, value) {
        const element = document.getElementById(elementId);
        if (element) {
            // Animation de transition
            element.style.transition = 'all 0.3s ease';
            element.textContent = value;

            // Effet de pulsation pour indiquer la mise à jour
            element.classList.add('updated');
            setTimeout(() => {
                element.classList.remove('updated');
            }, 1000);
        }
    }

    /**
     * Met à jour les graphiques de santé
     */
    updateHealthCharts(data) {
        // Mettre à jour le graphique d'activité si disponible
        if (window.activityChart && data.activity) {
            const newData = {
                labels: [new Date().toLocaleDateString('fr-FR')],
                datasets: [{
                    label: 'Pas aujourd\'hui',
                    data: [data.activity.total_steps],
                    borderColor: ARIACharts.COLORS.primary,
                    backgroundColor: ARIACharts.COLORS.primary + '20'
                }]
            };
            ARIACharts.updateChart(window.activityChart, newData);
        }
    }

    /**
     * Met à jour les graphiques de douleur
     */
    updatePainCharts(data) {
        // Mettre à jour le graphique d'évolution de la douleur si disponible
        if (window.painEvolutionChart && data.length > 0) {
            const labels = data.map(entry => new Date(entry.timestamp).toLocaleDateString('fr-FR'));
            const intensities = data.map(entry => entry.intensity);

            const newData = {
                labels: labels,
                datasets: [{
                    label: 'Intensité de la Douleur',
                    data: intensities,
                    borderColor: ARIACharts.COLORS.danger,
                    backgroundColor: ARIACharts.COLORS.danger + '20'
                }]
            };
            ARIACharts.updateChart(window.painEvolutionChart, newData);
        }
    }

    /**
     * Met à jour l'horodatage de la dernière mise à jour
     */
    updateLastUpdateTime() {
        const lastUpdateElement = document.getElementById('last-update');
        if (lastUpdateElement) {
            const now = new Date();
            lastUpdateElement.textContent = now.toLocaleTimeString('fr-FR');
        }
    }

    /**
     * Met à jour le statut de connexion
     */
    updateConnectionStatus(isConnected) {
        const statusIndicator = document.querySelector('.connection-status');
        if (statusIndicator) {
            statusIndicator.className = `connection-status ${isConnected ? 'connected' : 'disconnected'}`;
            statusIndicator.textContent = isConnected ? 'Connecté' : 'Déconnecté';
        }
    }

    /**
     * Gère les erreurs de mise à jour
     */
    handleUpdateError(error) {
        this.retryAttempts++;

        if (this.retryAttempts >= this.maxRetries) {
            this.pauseUpdates();
            this.showConnectionError();
        } else {
            // Attendre avant de réessayer
            setTimeout(() => {
                this.performUpdate();
            }, this.retryDelay * this.retryAttempts);
        }
    }

    /**
     * Gère la perte de connexion
     */
    handleConnectionLost() {
        this.pauseUpdates();
        this.showConnectionError();
    }

    /**
     * Gère la restauration de connexion
     */
    handleConnectionRestored() {
        this.retryAttempts = 0;
        this.resumeUpdates();
        this.hideConnectionError();
    }

    /**
     * Affiche une erreur de connexion
     */
    showConnectionError() {
        const errorElement = document.getElementById('connection-error');
        if (errorElement) {
            errorElement.style.display = 'block';
        } else {
            // Créer l'élément d'erreur s'il n'existe pas
            const errorDiv = document.createElement('div');
            errorDiv.id = 'connection-error';
            errorDiv.className = 'connection-error';
            errorDiv.innerHTML = `
                <i class="fas fa-exclamation-triangle"></i>
                <span>Connexion perdue - Tentative de reconnexion...</span>
            `;
            document.body.appendChild(errorDiv);
        }
    }

    /**
     * Masque l'erreur de connexion
     */
    hideConnectionError() {
        const errorElement = document.getElementById('connection-error');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
    }

    /**
     * Met à jour le thème des graphiques
     */
    updateTheme(theme) {
        this.charts.forEach(chart => {
            if (theme === 'dark') {
                ARIACharts.applyDarkTheme(chart);
            } else {
                ARIACharts.applyLightTheme(chart);
            }
        });
    }

    /**
     * Initialise les graphiques pour les mises à jour
     */
    initializeCharts() {
        // Enregistrer les graphiques existants
        if (window.activityChart) {
            this.charts.set('activity', window.activityChart);
        }
        if (window.sleepStressChart) {
            this.charts.set('sleepStress', window.sleepStressChart);
        }
        if (window.painEvolutionChart) {
            this.charts.set('painEvolution', window.painEvolutionChart);
        }
    }

    /**
     * Enregistre un callback pour les mises à jour
     */
    registerCallback(name, callback) {
        this.callbacks.set(name, callback);
    }

    /**
     * Supprime un callback
     */
    unregisterCallback(name) {
        this.callbacks.delete(name);
    }

    /**
     * Exécute tous les callbacks enregistrés
     */
    executeCallbacks(data) {
        this.callbacks.forEach((callback, name) => {
            try {
                callback(data);
            } catch (error) {
                console.error(`Erreur dans le callback ${name}:`, error);
            }
        });
    }

    /**
     * Change la fréquence des mises à jour
     */
    setUpdateFrequency(frequency) {
        this.updateFrequency = frequency;
        if (this.isConnected) {
            this.pauseUpdates();
            this.startRealTimeUpdates();
        }
    }

    /**
     * Arrête complètement les mises à jour en temps réel
     */
    stop() {
        this.pauseUpdates();
        this.charts.clear();
        this.callbacks.clear();
    }
}

// Instance globale
window.ARIARealTime = new ARIARealTime();

// Initialisation automatique
document.addEventListener('DOMContentLoaded', () => {
    window.ARIARealTime.initialize();
});

// Export pour utilisation dans d'autres modules
window.ARIARealTimeUtils = {
    startRealTimeUpdates: () => window.ARIARealTime.startRealTimeUpdates(),
    pauseUpdates: () => window.ARIARealTime.pauseUpdates(),
    resumeUpdates: () => window.ARIARealTime.resumeUpdates(),
    setUpdateFrequency: (freq) => window.ARIARealTime.setUpdateFrequency(freq),
    registerCallback: (name, callback) => window.ARIARealTime.registerCallback(name, callback),
    unregisterCallback: (name) => window.ARIARealTime.unregisterCallback(name)
};
