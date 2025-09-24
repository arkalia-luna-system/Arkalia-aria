/**
 * ARKALIA ARIA - Dashboard JavaScript Moderne
 * Interactions et fonctionnalités avancées
 */

class ARKALIADashboard {
    constructor() {
        this.charts = new Map();
        this.realTimeInterval = null;
        this.theme = localStorage.getItem('aria-theme') || 'light';
        this.init();
    }

    init() {
        this.setupTheme();
        this.setupEventListeners();
        this.initializeCharts();
        this.startRealTimeUpdates();
        console.log('🚀 ARKALIA ARIA Dashboard initialisé');
    }

    setupTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        this.updateThemeIcon();
    }

    setupEventListeners() {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleNavigation(item);
            });
        });

        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleButtonClick(btn, e);
            });
        });
    }

    handleNavigation(navItem) {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        navItem.classList.add('active');
    }

    handleButtonClick(btn, event) {
        if (btn.textContent.includes('Synchroniser')) {
            this.syncAllData();
        } else if (btn.textContent.includes('Thème')) {
            this.toggleTheme();
        }
    }

    async syncAllData() {
        const syncBtn = document.querySelector('[data-action="sync"]');
        if (syncBtn) {
            syncBtn.disabled = true;
            syncBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Synchronisation...';
        }

        try {
            const response = await fetch('/api/health/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ days_back: 7, force_sync: true })
            });

            if (response.ok) {
                this.showNotification('Synchronisation réussie !', 'success');
            } else {
                throw new Error('Erreur de synchronisation');
            }
        } catch (error) {
            this.showNotification(`Erreur: ${error.message}`, 'error');
        } finally {
            if (syncBtn) {
                syncBtn.disabled = false;
                syncBtn.innerHTML = '<i class="fas fa-sync"></i> Synchroniser';
            }
        }
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', this.theme);
        localStorage.setItem('aria-theme', this.theme);
        this.updateThemeIcon();
    }

    updateThemeIcon() {
        const themeBtn = document.querySelector('[data-action="theme"]');
        if (themeBtn) {
            const icon = themeBtn.querySelector('i');
            if (icon) {
                icon.className = this.theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
            }
        }
    }

    initializeCharts() {
        this.initMainChart();
        this.initHealthChart();
    }

    initMainChart() {
        const ctx = document.getElementById('mainChart');
        if (!ctx) return;

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.generateTimeLabels(7),
                datasets: [{
                    label: 'Score de Santé',
                    data: this.generateSampleData(7, 60, 100),
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { min: 0, max: 100 }
                }
            }
        });

        this.charts.set('main', chart);
    }

    initHealthChart() {
        const ctx = document.getElementById('healthChart');
        if (!ctx) return;

        const chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Excellent', 'Bon', 'Moyen', 'Faible'],
                datasets: [{
                    data: [45, 30, 20, 5],
                    backgroundColor: ['#10b981', '#3b82f6', '#f59e0b', '#ef4444'],
                    borderWidth: 0,
                    cutout: '70%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });

        this.charts.set('health', chart);
    }

    startRealTimeUpdates() {
        this.realTimeInterval = setInterval(() => {
            this.updateRealTimeData();
        }, 30000);
    }

    async updateRealTimeData() {
        try {
            const response = await fetch('/api/health/metrics/unified');
            if (response.ok) {
                const data = await response.json();
                this.updateMetricsCards(data);
            }
        } catch (error) {
            console.error('Erreur mise à jour temps réel:', error);
        }
    }

    updateMetricsCards(data) {
        const cards = document.querySelectorAll('.metric-card');
        cards.forEach(card => {
            const valueElement = card.querySelector('.metric-value');
            if (valueElement) {
                valueElement.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    valueElement.style.transform = '';
                }, 200);
            }
        });
    }

    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="margin-left: auto; background: none; border: none; color: inherit; cursor: pointer;">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        document.body.appendChild(notification);
        setTimeout(() => notification.classList.add('show'), 100);
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    generateTimeLabels(days) {
        const labels = [];
        for (let i = days - 1; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString('fr-FR', { month: 'short', day: 'numeric' }));
        }
        return labels;
    }

    generateSampleData(days, min, max) {
        const data = [];
        for (let i = 0; i < days; i++) {
            data.push(Math.floor(Math.random() * (max - min + 1)) + min);
        }
        return data;
    }
}

// Initialisation globale
document.addEventListener('DOMContentLoaded', () => {
    window.ariaDashboard = new ARKALIADashboard();
});

// Fonctions globales
function syncAllData() {
    if (window.ariaDashboard) {
        window.ariaDashboard.syncAllData();
    }
}

function toggleTheme() {
    if (window.ariaDashboard) {
        window.ariaDashboard.toggleTheme();
    }
}