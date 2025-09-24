#!/usr/bin/env python3
"""
ARKALIA ARIA - Dashboard Web Interactif
======================================

Dashboard web interactif pour visualiser les métriques ARIA en temps réel.
Intégration avec FastAPI pour servir le dashboard via l'API.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


class ARIA_MetricsDashboard:
    """
    Dashboard web interactif pour les métriques ARIA.

    Fournit une interface web moderne pour visualiser :
    - Métriques en temps réel
    - Graphiques interactifs
    - Alertes et recommandations
    - Historique des métriques
    """

    def __init__(self, app: FastAPI | None = None) -> None:
        """
        Initialise le dashboard ARIA.

        Args:
            app: Instance FastAPI pour intégration (optionnel)
        """
        self.app = app
        self.templates_dir = Path(__file__).parent / "templates"
        self.static_dir = Path(__file__).parent / "static"

        # Créer les répertoires si nécessaire
        self.templates_dir.mkdir(exist_ok=True)
        self.static_dir.mkdir(exist_ok=True)

        self.templates = Jinja2Templates(directory=str(self.templates_dir))

        if self.app:
            self._setup_routes()

    def _setup_routes(self) -> None:
        """Configure les routes du dashboard."""
        if self.app is None:
            # Protection de type pour mypy: app requis pour l'attachement des routes
            return

        @self.app.get("/dashboard", response_class=HTMLResponse)
        async def dashboard_home(request: Request):
            """Page principale du dashboard."""
            return self.templates.TemplateResponse(
                "dashboard.html",
                {"request": request, "title": "ARKALIA ARIA Dashboard"},
            )

        @self.app.get("/dashboard/metrics", response_class=HTMLResponse)
        async def dashboard_metrics(request: Request):
            """Page des métriques détaillées."""
            return self.templates.TemplateResponse(
                "metrics.html", {"request": request, "title": "Métriques ARIA"}
            )

        @self.app.get("/dashboard/security", response_class=HTMLResponse)
        async def dashboard_security(request: Request):
            """Page de sécurité."""
            return self.templates.TemplateResponse(
                "security.html", {"request": request, "title": "Sécurité ARIA"}
            )

        @self.app.get("/dashboard/performance", response_class=HTMLResponse)
        async def dashboard_performance(request: Request):
            """Page de performance."""
            return self.templates.TemplateResponse(
                "performance.html", {"request": request, "title": "Performance ARIA"}
            )

    def generate_dashboard_html(self, metrics: dict[str, Any]) -> str:  # noqa: W293
        """
        Génère le HTML du dashboard avec les métriques.

        Args:
            metrics: Métriques à afficher

        Returns:
            HTML du dashboard
        """
        timestamp = metrics.get("timestamp", datetime.now().isoformat())

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARKALIA ARIA - Dashboard Interactif</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3em;
            color: #667eea;
            margin-bottom: 10px;
            font-weight: 300;
        }}
        
        .header p {{
            color: #666;
            font-size: 1.2em;
        }}
        
        .dashboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}
        
        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }}
        
        .card h3 {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.4em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .metric-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .metric-row:last-child {{
            border-bottom: none;
        }}
        
        .metric-label {{
            color: #666;
            font-weight: 500;
        }}
        
        .metric-value {{
            font-weight: bold;
            color: #333;
            font-size: 1.1em;
        }}
        
        .status-good {{
            color: #28a745;
        }}
        
        .status-warning {{
            color: #ffc107;
        }}
        
        .status-error {{
            color: #dc3545;
        }}
        
        .chart-container {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .chart-title {{
            color: #667eea;
            margin-bottom: 20px;
            font-size: 1.4em;
            text-align: center;
        }}
        
        .alerts-section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .alert {{
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid;
        }}
        
        .alert-error {{
            background: #f8d7da;
            border-left-color: #dc3545;
            color: #721c24;
        }}
        
        .alert-warning {{
            background: #fff3cd;
            border-left-color: #ffc107;
            color: #856404;
        }}
        
        .alert-info {{
            background: #d1ecf1;
            border-left-color: #17a2b8;
            color: #0c5460;
        }}
        
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 30px;
            padding: 20px;
        }}
        
        .refresh-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: background 0.3s ease;
            margin: 20px auto;
            display: block;
        }}
        
        .refresh-btn:hover {{
            background: #5a6fd8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 ARKALIA ARIA</h1>
            <p>Dashboard Interactif - {timestamp}</p>
            <button class="refresh-btn" onclick="location.reload()">🔄 Actualiser</button>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h3>🐍 Code Python</h3>
                <div class="metric-row">
                    <span class="metric-label">Fichiers Python</span>
                    <span class="metric-value">{metrics.get('python_files', {}).get('count', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Lignes de Code</span>
                    <span class="metric-value">{metrics.get('python_files', {}).get('total_lines', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Fichiers Core</span>
                    <span class="metric-value">{metrics.get('python_files', {}).get('core_files', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Fichiers Tests</span>
                    <span class="metric-value">{metrics.get('python_files', {}).get('test_files', 0)}</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🎯 Suivi Douleur</h3>
                <div class="metric-row">
                    <span class="metric-label">Entrées Douleur</span>
                    <span class="metric-value">{metrics.get('aria_specific', {}).get('pain_tracking', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Patterns Analysés</span>
                    <span class="metric-value">{metrics.get('aria_specific', {}).get('pattern_analysis', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Prédictions</span>
                    <span class="metric-value">{metrics.get('aria_specific', {}).get('predictions', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Intégration CIA</span>
                    <span class="metric-value {'status-good' if metrics.get('aria_specific', {}).get('cia_integration', {}).get('cia_sync_exists', False) else 'status-error'}">
                        {'✅ Actif' if metrics.get('aria_specific', {}).get('cia_integration', {}).get('cia_sync_exists', False) else '❌ Inactif'}
                    </span>
                </div>
            </div>
            
            <div class="card">
                <h3>🤖 Modèles ML</h3>
                <div class="metric-row">
                    <span class="metric-label">Fichiers ML</span>
                    <span class="metric-value">{metrics.get('ml_models', {}).get('ml_files_count', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Fichiers Modèles</span>
                    <span class="metric-value">{metrics.get('ml_models', {}).get('model_files_count', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Moteur Prédiction</span>
                    <span class="metric-value {'status-good' if metrics.get('ml_models', {}).get('prediction_engine_status', False) else 'status-error'}">
                        {'✅ Actif' if metrics.get('ml_models', {}).get('prediction_engine_status', False) else '❌ Inactif'}
                    </span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Analyseur Émotions</span>
                    <span class="metric-value {'status-good' if metrics.get('ml_models', {}).get('emotion_analyzer_status', False) else 'status-error'}">
                        {'✅ Actif' if metrics.get('ml_models', {}).get('emotion_analyzer_status', False) else '❌ Inactif'}
                    </span>
                </div>
            </div>
            
            <div class="card">
                <h3>🧪 Tests</h3>
                <div class="metric-row">
                    <span class="metric-label">Fichiers Tests</span>
                    <span class="metric-value">{metrics.get('tests', {}).get('test_files_count', 0)}</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Couverture</span>
                    <span class="metric-value {'status-good' if metrics.get('tests', {}).get('coverage_percentage', 0) > 70 else 'status-warning'}">
                        {metrics.get('tests', {}).get('coverage_percentage', 0):.1f}%
                    </span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Tests Intégration</span>
                    <span class="metric-value">{metrics.get('tests', {}).get('integration_tests', 0)}</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🔒 Sécurité</h3>
                <div class="metric-row">
                    <span class="metric-label">Issues Bandit</span>
                    <span class="metric-value {'status-good' if metrics.get('security', {}).get('bandit_scan', {}).get('issues_found', 0) == 0 else 'status-error'}">
                        {metrics.get('security', {}).get('bandit_scan', {}).get('issues_found', 0)}
                    </span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Vulnérabilités Safety</span>
                    <span class="metric-value {'status-good' if metrics.get('security', {}).get('safety_scan', {}).get('vulnerabilities_found', 0) == 0 else 'status-error'}">
                        {metrics.get('security', {}).get('safety_scan', {}).get('vulnerabilities_found', 0)}
                    </span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Dépendances</span>
                    <span class="metric-value">{metrics.get('security', {}).get('dependencies_count', 0)}</span>
                </div>
            </div>
            
            <div class="card">
                <h3>⚡ Performance</h3>
                <div class="metric-row">
                    <span class="metric-label">Mémoire (MB)</span>
                    <span class="metric-value {'status-good' if metrics.get('performance', {}).get('memory_usage_mb', 0) < 500 else 'status-warning'}">
                        {metrics.get('performance', {}).get('memory_usage_mb', 0):.1f}
                    </span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">CPU (%)</span>
                    <span class="metric-value {'status-good' if metrics.get('performance', {}).get('cpu_percent', 0) < 50 else 'status-warning'}">
                        {metrics.get('performance', {}).get('cpu_percent', 0):.1f}
                    </span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Disque (%)</span>
                    <span class="metric-value {'status-good' if metrics.get('performance', {}).get('disk_usage_percent', 0) < 80 else 'status-warning'}">
                        {metrics.get('performance', {}).get('disk_usage_percent', 0):.1f}
                    </span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Processus</span>
                    <span class="metric-value">{metrics.get('performance', {}).get('process_count', 0)}</span>
                </div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3 class="chart-title">📊 Graphique des Métriques</h3>
            <canvas id="metricsChart" width="400" height="200"></canvas>
        </div>
        
        <div class="alerts-section">
            <h3>🚨 Alertes et Recommandations</h3>
            <div id="alerts-container">
                <!-- Les alertes seront générées dynamiquement -->
            </div>
        </div>
        
        <div class="footer">
            <p>Dashboard généré automatiquement par ARKALIA ARIA Metrics Collector</p>
            <p>Dernière mise à jour : {timestamp}</p>
        </div>
    </div>
    
    <script>
        // Graphique des métriques
        const ctx = document.getElementById('metricsChart').getContext('2d');
        const chart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: ['Fichiers Python', 'Tests', 'Couverture %', 'Issues Sécurité', 'Mémoire MB'],
                datasets: [{{
                    label: 'Métriques ARIA',
                    data: [
                        {metrics.get('python_files', {}).get('count', 0)},
                        {metrics.get('tests', {}).get('test_files_count', 0)},
                        {metrics.get('tests', {}).get('coverage_percentage', 0)},
                        {metrics.get('security', {}).get('bandit_scan', {}).get('issues_found', 0)},
                        {metrics.get('performance', {}).get('memory_usage_mb', 0)}
                    ],
                    backgroundColor: [
                        'rgba(102, 126, 234, 0.8)',
                        'rgba(118, 75, 162, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(220, 53, 69, 0.8)',
                        'rgba(40, 167, 69, 0.8)'
                    ],
                    borderColor: [
                        'rgba(102, 126, 234, 1)',
                        'rgba(118, 75, 162, 1)',
                        'rgba(255, 193, 7, 1)',
                        'rgba(220, 53, 69, 1)',
                        'rgba(40, 167, 69, 1)'
                    ],
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
        
        // Actualisation automatique toutes les 30 secondes
        setInterval(() => {{
            location.reload();
        }}, 30000);
    </script>
</body>
</html>"""
        return html

    def create_static_files(self) -> None:
        """Crée les fichiers statiques nécessaires."""
        # Créer le fichier CSS principal
        css_file = self.static_dir / "dashboard.css"
        css_content = """
/* Styles pour le dashboard ARIA */
.dashboard-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.metric-card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.metric-value {
    font-size: 2em;
    font-weight: bold;
    color: #667eea;
}

.status-indicator {
    display: inline-block;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-right: 8px;
}

.status-good { background-color: #28a745; }
.status-warning { background-color: #ffc107; }
.status-error { background-color: #dc3545; }
"""

        with open(css_file, "w", encoding="utf-8") as f:
            f.write(css_content)

        # Créer le fichier JavaScript principal
        js_file = self.static_dir / "dashboard.js"
        js_content = """
// JavaScript pour le dashboard ARIA
document.addEventListener('DOMContentLoaded', function() {
    // Initialisation du dashboard
    initializeDashboard();
    
    // Actualisation automatique
    setInterval(refreshMetrics, 30000);
});

function initializeDashboard() {
    console.log('ARKALIA ARIA Dashboard initialisé');
}

function refreshMetrics() {
    // Recharger les métriques
    fetch('/api/metrics')
        .then(response => response.json())
        .then(data => {
            updateMetricsDisplay(data);
        })
        .catch(error => {
            console.error('Erreur lors de la mise à jour des métriques:', error);
        });
}

function updateMetricsDisplay(metrics) {
    // Mettre à jour l'affichage des métriques
    console.log('Métriques mises à jour:', metrics);
}
"""

        with open(js_file, "w", encoding="utf-8") as f:
            f.write(js_content)
