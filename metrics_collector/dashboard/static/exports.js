/**
 * ARKALIA ARIA - Export Functions
 * ===============================
 * 
 * Fonctions d'export pour le dashboard ARIA.
 * Supporte l'export en PDF, Excel, HTML et JSON.
 */

class ARIAExports {
    constructor() {
        this.exportQueue = [];
        this.isExporting = false;
        this.supportedFormats = ['pdf', 'excel', 'html', 'json'];
    }

    /**
     * Exporte les données en PDF
     */
    async exportToPDF(data, options = {}) {
        const defaultOptions = {
            title: 'Rapport ARKALIA ARIA',
            filename: `aria-report-${new Date().toISOString().split('T')[0]}.pdf`,
            includeCharts: true,
            includeInsights: true,
            includeRecommendations: true,
            includeRawData: false
        };

        const exportOptions = { ...defaultOptions, ...options };

        try {
            this.showExportProgress('Génération du PDF...');

            const response = await fetch('/dashboard/export/pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: data,
                    options: exportOptions
                })
            });

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            const blob = await response.blob();
            this.downloadFile(blob, exportOptions.filename);

            this.hideExportProgress();
            this.showExportSuccess('PDF généré avec succès');

        } catch (error) {
            this.hideExportProgress();
            this.showExportError('Erreur lors de la génération du PDF: ' + error.message);
            console.error('Erreur export PDF:', error);
        }
    }

    /**
     * Exporte les données en Excel
     */
    async exportToExcel(data, options = {}) {
        const defaultOptions = {
            filename: `aria-data-${new Date().toISOString().split('T')[0]}.xlsx`,
            sheets: ['Données', 'Résumé', 'Graphiques'],
            includeCharts: true,
            includeFormulas: true
        };

        const exportOptions = { ...defaultOptions, ...options };

        try {
            this.showExportProgress('Génération du fichier Excel...');

            const response = await fetch('/dashboard/export/excel', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: data,
                    options: exportOptions
                })
            });

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            const blob = await response.blob();
            this.downloadFile(blob, exportOptions.filename);

            this.hideExportProgress();
            this.showExportSuccess('Fichier Excel généré avec succès');

        } catch (error) {
            this.hideExportProgress();
            this.showExportError('Erreur lors de la génération Excel: ' + error.message);
            console.error('Erreur export Excel:', error);
        }
    }

    /**
     * Exporte les données en HTML
     */
    async exportToHTML(data, options = {}) {
        const defaultOptions = {
            filename: `aria-report-${new Date().toISOString().split('T')[0]}.html`,
            includeStyles: true,
            includeScripts: false,
            standalone: true
        };

        const exportOptions = { ...defaultOptions, ...options };

        try {
            this.showExportProgress('Génération du HTML...');

            const response = await fetch('/dashboard/export/html', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: data,
                    options: exportOptions
                })
            });

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            const htmlContent = await response.text();
            const blob = new Blob([htmlContent], { type: 'text/html' });
            this.downloadFile(blob, exportOptions.filename);

            this.hideExportProgress();
            this.showExportSuccess('Fichier HTML généré avec succès');

        } catch (error) {
            this.hideExportProgress();
            this.showExportError('Erreur lors de la génération HTML: ' + error.message);
            console.error('Erreur export HTML:', error);
        }
    }

    /**
     * Exporte les données en JSON
     */
    async exportToJSON(data, options = {}) {
        const defaultOptions = {
            filename: `aria-data-${new Date().toISOString().split('T')[0]}.json`,
            prettyPrint: true,
            includeMetadata: true
        };

        const exportOptions = { ...defaultOptions, ...options };

        try {
            this.showExportProgress('Génération du JSON...');

            let jsonData = data;

            if (exportOptions.includeMetadata) {
                jsonData = {
                    metadata: {
                        exportDate: new Date().toISOString(),
                        version: '1.0.0',
                        source: 'ARKALIA ARIA Dashboard',
                        recordCount: this.countRecords(data)
                    },
                    data: data
                };
            }

            const jsonString = exportOptions.prettyPrint
                ? JSON.stringify(jsonData, null, 2)
                : JSON.stringify(jsonData);

            const blob = new Blob([jsonString], { type: 'application/json' });
            this.downloadFile(blob, exportOptions.filename);

            this.hideExportProgress();
            this.showExportSuccess('Fichier JSON généré avec succès');

        } catch (error) {
            this.hideExportProgress();
            this.showExportError('Erreur lors de la génération JSON: ' + error.message);
            console.error('Erreur export JSON:', error);
        }
    }

    /**
     * Exporte un graphique en image
     */
    exportChartAsImage(chart, format = 'png', filename = null) {
        if (!chart) {
            this.showExportError('Aucun graphique à exporter');
            return;
        }

        try {
            const imageData = chart.toBase64Image();
            const mimeType = `image/${format}`;
            const blob = this.base64ToBlob(imageData, mimeType);

            const defaultFilename = `aria-chart-${new Date().toISOString().split('T')[0]}.${format}`;
            this.downloadFile(blob, filename || defaultFilename);

            this.showExportSuccess(`Graphique exporté en ${format.toUpperCase()}`);

        } catch (error) {
            this.showExportError('Erreur lors de l\'export du graphique: ' + error.message);
            console.error('Erreur export graphique:', error);
        }
    }

    /**
     * Exporte toutes les données du dashboard
     */
    async exportDashboard(options = {}) {
        const defaultOptions = {
            format: 'pdf',
            includeAllPages: true,
            includeCharts: true,
            includeData: true,
            filename: `aria-dashboard-complete-${new Date().toISOString().split('T')[0]}.pdf`
        };

        const exportOptions = { ...defaultOptions, ...options };

        try {
            this.showExportProgress('Collecte des données du dashboard...');

            // Collecter toutes les données nécessaires
            const dashboardData = await this.collectDashboardData();

            this.hideExportProgress();

            // Exporter selon le format demandé
            switch (exportOptions.format.toLowerCase()) {
                case 'pdf':
                    await this.exportToPDF(dashboardData, exportOptions);
                    break;
                case 'excel':
                    await this.exportToExcel(dashboardData, exportOptions);
                    break;
                case 'html':
                    await this.exportToHTML(dashboardData, exportOptions);
                    break;
                case 'json':
                    await this.exportToJSON(dashboardData, exportOptions);
                    break;
                default:
                    throw new Error(`Format non supporté: ${exportOptions.format}`);
            }

        } catch (error) {
            this.hideExportProgress();
            this.showExportError('Erreur lors de l\'export du dashboard: ' + error.message);
            console.error('Erreur export dashboard:', error);
        }
    }

    /**
     * Collecte toutes les données du dashboard
     */
    async collectDashboardData() {
        const data = {
            timestamp: new Date().toISOString(),
            health: {},
            pain: {},
            patterns: {},
            metrics: {}
        };

        try {
            // Collecter les données de santé
            const healthResponse = await fetch('/api/health/metrics/unified?days_back=30');
            if (healthResponse.ok) {
                data.health = await healthResponse.json();
            }

            // Collecter les données de douleur
            const painResponse = await fetch('/api/pain/entries/recent?limit=100');
            if (painResponse.ok) {
                data.pain = await painResponse.json();
            }

            // Collecter les métriques système
            const metricsResponse = await fetch('/api/metrics/system');
            if (metricsResponse.ok) {
                data.metrics = await metricsResponse.json();
            }

            // Collecter les patterns (si disponible)
            try {
                const patternsResponse = await fetch('/api/patterns/analyze');
                if (patternsResponse.ok) {
                    data.patterns = await patternsResponse.json();
                }
            } catch (error) {
                console.warn('Patterns non disponibles:', error);
            }

        } catch (error) {
            console.error('Erreur collecte données:', error);
        }

        return data;
    }

    /**
     * Télécharge un fichier
     */
    downloadFile(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        link.style.display = 'none';

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Nettoyer l'URL après téléchargement
        setTimeout(() => {
            window.URL.revokeObjectURL(url);
        }, 1000);
    }

    /**
     * Convertit une chaîne base64 en Blob
     */
    base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64.split(',')[1]);
        const byteNumbers = new Array(byteCharacters.length);

        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }

    /**
     * Compte le nombre d'enregistrements dans les données
     */
    countRecords(data) {
        if (Array.isArray(data)) {
            return data.length;
        } else if (typeof data === 'object') {
            let count = 0;
            Object.values(data).forEach(value => {
                if (Array.isArray(value)) {
                    count += value.length;
                } else if (typeof value === 'object') {
                    count += this.countRecords(value);
                }
            });
            return count;
        }
        return 0;
    }

    /**
     * Affiche le progrès d'export
     */
    showExportProgress(message) {
        const progressElement = document.getElementById('export-progress');
        if (progressElement) {
            progressElement.style.display = 'block';
            progressElement.querySelector('.progress-message').textContent = message;
        } else {
            // Créer l'élément de progression s'il n'existe pas
            const progressDiv = document.createElement('div');
            progressDiv.id = 'export-progress';
            progressDiv.className = 'export-progress';
            progressDiv.innerHTML = `
                <div class="progress-content">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span class="progress-message">${message}</span>
                </div>
            `;
            document.body.appendChild(progressDiv);
        }
    }

    /**
     * Masque le progrès d'export
     */
    hideExportProgress() {
        const progressElement = document.getElementById('export-progress');
        if (progressElement) {
            progressElement.style.display = 'none';
        }
    }

    /**
     * Affiche un message de succès
     */
    showExportSuccess(message) {
        this.showNotification(message, 'success');
    }

    /**
     * Affiche un message d'erreur
     */
    showExportError(message) {
        this.showNotification(message, 'error');
    }

    /**
     * Affiche une notification
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    /**
     * Valide les options d'export
     */
    validateExportOptions(options) {
        const errors = [];

        if (options.format && !this.supportedFormats.includes(options.format.toLowerCase())) {
            errors.push(`Format non supporté: ${options.format}`);
        }

        if (options.filename && !this.isValidFilename(options.filename)) {
            errors.push('Nom de fichier invalide');
        }

        return errors;
    }

    /**
     * Valide un nom de fichier
     */
    isValidFilename(filename) {
        const invalidChars = /[<>:"/\\|?*]/;
        return !invalidChars.test(filename) && filename.length > 0 && filename.length < 255;
    }

    /**
     * Génère un nom de fichier par défaut
     */
    generateDefaultFilename(format, dataType = 'data') {
        const date = new Date().toISOString().split('T')[0];
        return `aria-${dataType}-${date}.${format}`;
    }
}

// Instance globale
window.ARIAExports = new ARIAExports();

// Fonctions globales pour compatibilité
window.exportData = (format, data, options) => {
    switch (format.toLowerCase()) {
        case 'pdf':
            return window.ARIAExports.exportToPDF(data, options);
        case 'excel':
            return window.ARIAExports.exportToExcel(data, options);
        case 'html':
            return window.ARIAExports.exportToHTML(data, options);
        case 'json':
            return window.ARIAExports.exportToJSON(data, options);
        default:
            console.error(`Format non supporté: ${format}`);
    }
};

window.exportChart = (chart, format, filename) => {
    return window.ARIAExports.exportChartAsImage(chart, format, filename);
};

window.exportDashboard = (options) => {
    return window.ARIAExports.exportDashboard(options);
};

// Export pour utilisation dans d'autres modules
window.ARIAExportUtils = {
    exportToPDF: (data, options) => window.ARIAExports.exportToPDF(data, options),
    exportToExcel: (data, options) => window.ARIAExports.exportToExcel(data, options),
    exportToHTML: (data, options) => window.ARIAExports.exportToHTML(data, options),
    exportToJSON: (data, options) => window.ARIAExports.exportToJSON(data, options),
    exportChart: (chart, format, filename) => window.ARIAExports.exportChartAsImage(chart, format, filename),
    exportDashboard: (options) => window.ARIAExports.exportDashboard(options),
    validateOptions: (options) => window.ARIAExports.validateExportOptions(options),
    generateFilename: (format, dataType) => window.ARIAExports.generateDefaultFilename(format, dataType)
};
