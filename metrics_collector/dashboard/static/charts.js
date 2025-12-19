/**
 * ARKALIA ARIA - Charts.js Helper Functions
 * =========================================
 * 
 * Fonctions utilitaires pour la création et la gestion des graphiques Chart.js
 * dans le dashboard ARIA.
 */

// Configuration globale des graphiques
Chart.defaults.font.family = "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
Chart.defaults.font.size = 12;
Chart.defaults.color = '#666666';

// Couleurs du thème ARIA
const ARIA_COLORS = {
    primary: '#e74c3c',
    secondary: '#3498db',
    success: '#2ecc71',
    warning: '#f39c12',
    danger: '#e74c3c',
    info: '#17a2b8',
    light: '#f8f9fa',
    dark: '#343a40',
    gradient: {
        primary: ['#e74c3c', '#c0392b'],
        secondary: ['#3498db', '#2980b9'],
        success: ['#2ecc71', '#27ae60'],
        warning: ['#f39c12', '#e67e22']
    }
};

/**
 * Crée un graphique de ligne pour les données temporelles
 */
function createLineChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            }
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Temps'
                }
            },
            y: {
                display: true,
                beginAtZero: true
            }
        },
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
        }
    };

    const chartOptions = { ...defaultOptions, ...options };

    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: chartOptions
    });
}

/**
 * Crée un graphique en barres
 */
function createBarChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    const chartOptions = { ...defaultOptions, ...options };

    return new Chart(ctx, {
        type: 'bar',
        data: data,
        options: chartOptions
    });
}

/**
 * Crée un graphique en secteurs (pie)
 */
function createPieChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
            }
        }
    };

    const chartOptions = { ...defaultOptions, ...options };

    return new Chart(ctx, {
        type: 'pie',
        data: data,
        options: chartOptions
    });
}

/**
 * Crée un graphique en donut
 */
function createDoughnutChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
            }
        }
    };

    const chartOptions = { ...defaultOptions, ...options };

    return new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: chartOptions
    });
}

/**
 * Crée un graphique en aires
 */
function createAreaChart(canvasId, data, options = {}) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            }
        },
        scales: {
            x: {
                display: true
            },
            y: {
                beginAtZero: true
            }
        }
    };

    const chartOptions = { ...defaultOptions, ...options };

    return new Chart(ctx, {
        type: 'line',
        data: {
            ...data,
            datasets: data.datasets.map(dataset => ({
                ...dataset,
                fill: true,
                tension: 0.4
            }))
        },
        options: chartOptions
    });
}

/**
 * Génère des données d'exemple pour les tests
 */
function generateSampleData(type, count = 7) {
    const labels = [];
    const data = [];

    // Générer les labels temporels
    for (let i = count - 1; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('fr-FR'));
    }

    // Générer les données selon le type
    switch (type) {
        case 'pain':
            for (let i = 0; i < count; i++) {
                data.push(Math.floor(Math.random() * 10) + 1);
            }
            break;
        case 'heartRate':
            for (let i = 0; i < count; i++) {
                data.push(Math.floor(Math.random() * 40) + 60);
            }
            break;
        case 'steps':
            for (let i = 0; i < count; i++) {
                data.push(Math.floor(Math.random() * 10000) + 5000);
            }
            break;
        case 'sleep':
            for (let i = 0; i < count; i++) {
                data.push(Math.floor(Math.random() * 3) + 6);
            }
            break;
        default:
            for (let i = 0; i < count; i++) {
                data.push(Math.floor(Math.random() * 100));
            }
    }

    return { labels, data };
}

/**
 * Met à jour un graphique existant avec de nouvelles données
 */
function updateChart(chart, newData) {
    if (chart && newData) {
        chart.data = newData;
        chart.update();
    }
}

/**
 * Détruit un graphique
 */
function destroyChart(chart) {
    if (chart) {
        chart.destroy();
    }
}

/**
 * Crée un graphique de corrélation
 */
function createCorrelationChart(canvasId, correlations) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const data = {
        labels: Object.keys(correlations),
        datasets: [{
            label: 'Corrélation',
            data: Object.values(correlations),
            backgroundColor: Object.values(correlations).map(value =>
                value > 0 ? ARIA_COLORS.success : ARIA_COLORS.danger
            ),
            borderColor: Object.values(correlations).map(value =>
                value > 0 ? ARIA_COLORS.success : ARIA_COLORS.danger
            ),
            borderWidth: 1
        }]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                min: -1,
                max: 1,
                ticks: {
                    callback: function (value) {
                        return value.toFixed(2);
                    }
                }
            }
        }
    };

    return new Chart(ctx, {
        type: 'bar',
        data: data,
        options: options
    });
}

/**
 * Crée un graphique de corrélation sommeil-douleur interactif
 */
function createSleepPainCorrelationChart(canvasId, correlationData) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    // Préparer les données pour un graphique scatter ou line
    const sleepData = correlationData.sleep_data || [];
    const painData = correlationData.pain_data || [];
    const correlation = correlationData.correlation || 0;

    // Créer des labels de dates
    const labels = sleepData.map((_, index) => `Jour ${index + 1}`);

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Sommeil (heures)',
                data: sleepData.map(d => d.duration_hours || 0),
                borderColor: ARIA_COLORS.secondary,
                backgroundColor: ARIA_COLORS.secondary + '20',
                yAxisID: 'y',
                tension: 0.4
            },
            {
                label: 'Douleur (intensité)',
                data: painData.map(d => d.intensity || 0),
                borderColor: ARIA_COLORS.danger,
                backgroundColor: ARIA_COLORS.danger + '20',
                yAxisID: 'y1',
                tension: 0.4
            }
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            tooltip: {
                mode: 'index',
                intersect: false
            },
            title: {
                display: true,
                text: `Corrélation Sommeil-Douleur: ${correlation.toFixed(3)}`
            }
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Temps'
                }
            },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                    display: true,
                    text: 'Sommeil (heures)'
                },
                beginAtZero: true
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                title: {
                    display: true,
                    text: 'Douleur (intensité)'
                },
                beginAtZero: true,
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    };

    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });
}

/**
 * Crée un graphique de corrélation stress-douleur interactif
 */
function createStressPainCorrelationChart(canvasId, correlationData) {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const stressData = correlationData.stress_data || [];
    const painData = correlationData.pain_data || [];
    const correlation = correlationData.correlation || 0;

    const labels = stressData.map((_, index) => `Jour ${index + 1}`);

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'Stress (niveau)',
                data: stressData.map(d => d.stress_level || 0),
                borderColor: ARIA_COLORS.warning,
                backgroundColor: ARIA_COLORS.warning + '20',
                yAxisID: 'y',
                tension: 0.4
            },
            {
                label: 'Douleur (intensité)',
                data: painData.map(d => d.intensity || 0),
                borderColor: ARIA_COLORS.danger,
                backgroundColor: ARIA_COLORS.danger + '20',
                yAxisID: 'y1',
                tension: 0.4
            }
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'index',
            intersect: false
        },
        plugins: {
            legend: {
                display: true,
                position: 'top'
            },
            tooltip: {
                mode: 'index',
                intersect: false
            },
            title: {
                display: true,
                text: `Corrélation Stress-Douleur: ${correlation.toFixed(3)}`
            }
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Temps'
                }
            },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
                title: {
                    display: true,
                    text: 'Stress (niveau)'
                },
                beginAtZero: true
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
                title: {
                    display: true,
                    text: 'Douleur (intensité)'
                },
                beginAtZero: true,
                grid: {
                    drawOnChartArea: false
                }
            }
        }
    };

    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });
}

/**
 * Crée un graphique de tendance temporelle
 */
function createTrendChart(canvasId, data, trendType = 'linear') {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                mode: 'index',
                intersect: false,
            }
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Temps'
                }
            },
            y: {
                display: true,
                beginAtZero: false
            }
        },
        elements: {
            line: {
                tension: trendType === 'smooth' ? 0.4 : 0
            }
        }
    };

    return new Chart(ctx, {
        type: 'line',
        data: data,
        options: options
    });
}

/**
 * Crée un graphique de comparaison multi-séries
 */
function createComparisonChart(canvasId, datasets, chartType = 'line') {
    const ctx = document.getElementById(canvasId).getContext('2d');

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    return new Chart(ctx, {
        type: chartType,
        data: {
            labels: datasets[0]?.labels || [],
            datasets: datasets.map((dataset, index) => ({
                ...dataset,
                backgroundColor: ARIA_COLORS.gradient[Object.keys(ARIA_COLORS.gradient)[index % 4]][0] + '20',
                borderColor: ARIA_COLORS.gradient[Object.keys(ARIA_COLORS.gradient)[index % 4]][0],
                borderWidth: 2
            }))
        },
        options: options
    });
}

/**
 * Exporte un graphique en image
 */
function exportChart(chart, filename = 'chart.png') {
    if (chart) {
        const url = chart.toBase64Image();
        const link = document.createElement('a');
        link.download = filename;
        link.href = url;
        link.click();
    }
}

/**
 * Applique un thème sombre aux graphiques
 */
function applyDarkTheme(chart) {
    if (chart) {
        chart.options.plugins.legend.labels.color = '#ffffff';
        chart.options.scales.x.ticks.color = '#ffffff';
        chart.options.scales.y.ticks.color = '#ffffff';
        chart.options.scales.x.title.color = '#ffffff';
        chart.options.scales.y.title.color = '#ffffff';
        chart.update();
    }
}

/**
 * Applique un thème clair aux graphiques
 */
function applyLightTheme(chart) {
    if (chart) {
        chart.options.plugins.legend.labels.color = '#666666';
        chart.options.scales.x.ticks.color = '#666666';
        chart.options.scales.y.ticks.color = '#666666';
        chart.options.scales.x.title.color = '#666666';
        chart.options.scales.y.title.color = '#666666';
        chart.update();
    }
}

/**
 * Initialise tous les graphiques du dashboard
 */
function initializeDashboardCharts() {
    // Graphique d'activité
    const activityData = generateSampleData('steps', 7);
    window.activityChart = createLineChart('activityChart', {
        labels: activityData.labels,
        datasets: [{
            label: 'Pas quotidiens',
            data: activityData.data,
            borderColor: ARIA_COLORS.primary,
            backgroundColor: ARIA_COLORS.primary + '20',
            tension: 0.4
        }]
    });

    // Graphique sommeil/stress
    const sleepData = generateSampleData('sleep', 7);
    const stressData = generateSampleData('default', 7);
    window.sleepStressChart = createAreaChart('sleepStressChart', {
        labels: sleepData.labels,
        datasets: [{
            label: 'Sommeil (heures)',
            data: sleepData.data,
            borderColor: ARIA_COLORS.secondary,
            backgroundColor: ARIA_COLORS.secondary + '20'
        }, {
            label: 'Stress (%)',
            data: stressData.data,
            borderColor: ARIA_COLORS.warning,
            backgroundColor: ARIA_COLORS.warning + '20'
        }]
    });
}

/**
 * Fonction utilitaire pour formater les données de l'API
 */
function formatApiDataForChart(apiData, xField, yField, label = 'Données') {
    const labels = apiData.map(item => {
        const date = new Date(item[xField]);
        return date.toLocaleDateString('fr-FR');
    });

    const data = apiData.map(item => item[yField]);

    return {
        labels: labels,
        datasets: [{
            label: label,
            data: data,
            borderColor: ARIA_COLORS.primary,
            backgroundColor: ARIA_COLORS.primary + '20',
            tension: 0.4
        }]
    };
}

// Export des fonctions pour utilisation globale
window.ARIACharts = {
    createLineChart,
    createBarChart,
    createPieChart,
    createDoughnutChart,
    createAreaChart,
    createCorrelationChart,
    createTrendChart,
    createComparisonChart,
    generateSampleData,
    updateChart,
    destroyChart,
    exportChart,
    applyDarkTheme,
    applyLightTheme,
    initializeDashboardCharts,
    formatApiDataForChart,
    COLORS: ARIA_COLORS
};
