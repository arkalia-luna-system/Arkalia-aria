#!/usr/bin/env python3
"""
ARKALIA ARIA - Exporteur de Métriques
====================================

Exporteur de métriques ARIA en différents formats :
- JSON (pour APIs et intégrations)
- Markdown (pour documentation)
- HTML (pour dashboards)
- CSV (pour analyse)
"""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


class ARIA_MetricsExporter:
    """
    Exporteur de métriques ARIA en différents formats.

    Supporte l'export en :
    - JSON (pour APIs et intégrations)
    - Markdown (pour documentation)
    - HTML (pour dashboards)
    - CSV (pour analyse)
    """

    def __init__(self, output_dir: str = "metrics_reports") -> None:
        """
        Initialise l'exporteur de métriques.

        Args:
            output_dir: Répertoire de sortie pour les rapports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def export_json(self, metrics: dict[str, Any], filename: str | None = None) -> Path:
        """
        Exporte les métriques en format JSON.

        Args:
            metrics: Données des métriques à exporter
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aria_metrics_{timestamp}.json"

        file_path = self.output_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)

        return file_path

    def export_markdown(
        self, metrics: dict[str, Any], filename: str | None = None
    ) -> Path:
        """
        Exporte les métriques en format Markdown.

        Args:
            metrics: Données des métriques à exporter
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aria_metrics_{timestamp}.md"

        file_path = self.output_dir / filename

        markdown_content = self._generate_markdown_report(metrics)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return file_path

    def export_html(self, metrics: dict[str, Any], filename: str | None = None) -> Path:
        """
        Exporte les métriques en format HTML avec dashboard.

        Args:
            metrics: Données des métriques à exporter
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aria_metrics_{timestamp}.html"

        file_path = self.output_dir / filename

        html_content = self._generate_html_dashboard(metrics)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return file_path

    def export_csv(self, metrics: dict[str, Any], filename: str | None = None) -> Path:
        """
        Exporte les métriques en format CSV.

        Args:
            metrics: Données des métriques à exporter
            filename: Nom du fichier (optionnel)

        Returns:
            Chemin du fichier créé
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aria_metrics_{timestamp}.csv"

        file_path = self.output_dir / filename

        csv_data = self._flatten_metrics_for_csv(metrics)

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
            writer.writeheader()
            writer.writerows(csv_data)

        return file_path

    def export_all_formats(
        self, metrics: dict[str, Any], base_filename: str | None = None
    ) -> dict[str, Path]:
        """
        Exporte les métriques dans tous les formats disponibles.

        Args:
            metrics: Données des métriques à exporter
            base_filename: Nom de base pour les fichiers (optionnel)

        Returns:
            Dict avec les chemins des fichiers créés
        """
        if base_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_filename = f"aria_metrics_{timestamp}"

        files = {}
        files["json"] = self.export_json(metrics, f"{base_filename}.json")
        files["markdown"] = self.export_markdown(metrics, f"{base_filename}.md")
        files["html"] = self.export_html(metrics, f"{base_filename}.html")
        files["csv"] = self.export_csv(metrics, f"{base_filename}.csv")

        return files

    def _generate_markdown_report(self, metrics: dict[str, Any]) -> str:
        """Génère un rapport Markdown à partir des métriques."""
        timestamp = metrics.get("timestamp", datetime.now().isoformat())

        report = f"""# 📊 ARKALIA ARIA - Rapport de Métriques

**Généré le :** {timestamp}

## 📈 Métriques Générales

| Métrique | Valeur | Statut |
|----------|--------|--------|
| **🐍 Fichiers Python** | {metrics.get('python_files', {}).get('count', 0)} | ✅ |
| **📝 Lignes de Code** | {metrics.get('python_files', {}).get('total_lines', 0)} | ✅ |
| **🧪 Tests** | {metrics.get('tests', {}).get('test_files_count', 0)} | ✅ |
| **📊 Couverture** | {metrics.get('tests', {}).get('coverage_percentage', 0):.1f}% | ✅ |

## 🎯 Métriques Spécifiques ARIA

### Suivi de la Douleur
- **Entrées de douleur** : {metrics.get('aria_specific', {}).get('pain_tracking', 0)}
- **Patterns analysés** : {metrics.get('aria_specific', {}).get('pattern_analysis', 0)}
- **Prédictions générées** : {metrics.get('aria_specific', {}).get('predictions', 0)}

### Intégration CIA
- **État de l'intégration** : {'✅ Actif' if metrics.get('aria_specific', {}).get('cia_integration', {}).get('cia_sync_exists', False) else '❌ Inactif'}
- **Endpoints disponibles** : {metrics.get('aria_specific', {}).get('cia_integration', {}).get('integration_endpoints', 0)}

## 🤖 Modèles ML

| Composant | Statut |
|-----------|--------|
| **Moteur de Prédiction** | {'✅ Actif' if metrics.get('ml_models', {}).get('prediction_engine_status', False) else '❌ Inactif'} |
| **Analyseur d'Émotions** | {'✅ Actif' if metrics.get('ml_models', {}).get('emotion_analyzer_status', False) else '❌ Inactif'} |
| **Fichiers ML** | {metrics.get('ml_models', {}).get('ml_files_count', 0)} |

## 🔒 Sécurité

| Scan | Statut | Vulnérabilités |
|------|--------|----------------|
| **Bandit** | {metrics.get('security', {}).get('bandit_scan', {}).get('status', 'Non exécuté')} | {metrics.get('security', {}).get('bandit_scan', {}).get('issues_found', 0)} |
| **Safety** | {metrics.get('security', {}).get('safety_scan', {}).get('status', 'Non exécuté')} | {metrics.get('security', {}).get('safety_scan', {}).get('vulnerabilities_found', 0)} |

## 📚 Documentation

- **Fichiers Markdown** : {metrics.get('documentation', {}).get('markdown_files', 0)}
- **MkDocs configuré** : {'✅ Oui' if metrics.get('documentation', {}).get('mkdocs_status', False) else '❌ Non'}

## ⚡ Performance

| Métrique | Valeur |
|----------|--------|
| **Mémoire utilisée** | {metrics.get('performance', {}).get('memory_usage_mb', 0):.1f} MB |
| **CPU** | {metrics.get('performance', {}).get('cpu_percent', 0):.1f}% |
| **Disque** | {metrics.get('performance', {}).get('disk_usage_percent', 0):.1f}% |

---

*Rapport généré automatiquement par ARKALIA ARIA Metrics Collector*
"""
        return report

    def _generate_html_dashboard(self, metrics: dict[str, Any]) -> str:  # noqa: W293
        """Génère un dashboard HTML à partir des métriques."""
        timestamp = metrics.get("timestamp", datetime.now().isoformat())

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARKALIA ARIA - Dashboard Métriques</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .metric-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #667eea;
            transition: transform 0.3s ease;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .metric-card h3 {{
            margin: 0 0 15px 0;
            color: #667eea;
            font-size: 1.2em;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
            margin: 10px 0;
        }}
        .metric-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .status-active {{
            color: #28a745;
        }}
        .status-inactive {{
            color: #dc3545;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 ARKALIA ARIA</h1>
            <p>Dashboard de Métriques - {timestamp}</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>🐍 Code Python</h3>
                <div class="metric-value">{metrics.get('python_files', {}).get('count', 0)}</div>
                <div class="metric-label">Fichiers Python</div>
                <div class="metric-value">{metrics.get('python_files', {}).get('total_lines', 0)}</div>
                <div class="metric-label">Lignes de Code</div>
            </div>
            
            <div class="metric-card">
                <h3>🧪 Tests</h3>
                <div class="metric-value">{metrics.get('tests', {}).get('test_files_count', 0)}</div>
                <div class="metric-label">Fichiers de Tests</div>
                <div class="metric-value">{metrics.get('tests', {}).get('coverage_percentage', 0):.1f}%</div>
                <div class="metric-label">Couverture</div>
            </div>
            
            <div class="metric-card">
                <h3>🎯 Suivi Douleur</h3>
                <div class="metric-value">{metrics.get('aria_specific', {}).get('pain_tracking', 0)}</div>
                <div class="metric-label">Entrées de Douleur</div>
                <div class="metric-value">{metrics.get('aria_specific', {}).get('pattern_analysis', 0)}</div>
                <div class="metric-label">Patterns Analysés</div>
            </div>
            
            <div class="metric-card">
                <h3>🤖 Modèles ML</h3>
                <div class="metric-value">{metrics.get('ml_models', {}).get('ml_files_count', 0)}</div>
                <div class="metric-label">Fichiers ML</div>
                <div class="metric-value">{'✅' if metrics.get('ml_models', {}).get('prediction_engine_status', False) else '❌'}</div>
                <div class="metric-label">Moteur Prédiction</div>
            </div>
            
            <div class="metric-card">
                <h3>🔒 Sécurité</h3>
                <div class="metric-value">{metrics.get('security', {}).get('bandit_scan', {}).get('issues_found', 0)}</div>
                <div class="metric-label">Issues Bandit</div>
                <div class="metric-value">{metrics.get('security', {}).get('safety_scan', {}).get('vulnerabilities_found', 0)}</div>
                <div class="metric-label">Vulnérabilités Safety</div>
            </div>
            
            <div class="metric-card">
                <h3>⚡ Performance</h3>
                <div class="metric-value">{metrics.get('performance', {}).get('memory_usage_mb', 0):.1f} MB</div>
                <div class="metric-label">Mémoire Utilisée</div>
                <div class="metric-value">{metrics.get('performance', {}).get('cpu_percent', 0):.1f}%</div>
                <div class="metric-label">CPU</div>
            </div>
        </div>
        
        <div class="footer">
            <p>Dashboard généré automatiquement par ARKALIA ARIA Metrics Collector</p>
        </div>
    </div>
</body>
</html>"""
        return html

    def _flatten_metrics_for_csv(self, metrics: dict[str, Any]) -> list[dict[str, Any]]:
        """Aplatit les métriques pour l'export CSV."""
        csv_data = []

        # Métriques générales
        csv_data.append(
            {
                "category": "general",
                "metric": "python_files_count",
                "value": metrics.get("python_files", {}).get("count", 0),
                "timestamp": metrics.get("timestamp", ""),
            }
        )

        csv_data.append(
            {
                "category": "general",
                "metric": "total_lines",
                "value": metrics.get("python_files", {}).get("total_lines", 0),
                "timestamp": metrics.get("timestamp", ""),
            }
        )

        # Métriques ARIA spécifiques
        csv_data.append(
            {
                "category": "aria_specific",
                "metric": "pain_tracking",
                "value": metrics.get("aria_specific", {}).get("pain_tracking", 0),
                "timestamp": metrics.get("timestamp", ""),
            }
        )

        csv_data.append(
            {
                "category": "aria_specific",
                "metric": "pattern_analysis",
                "value": metrics.get("aria_specific", {}).get("pattern_analysis", 0),
                "timestamp": metrics.get("timestamp", ""),
            }
        )

        # Métriques de sécurité
        csv_data.append(
            {
                "category": "security",
                "metric": "bandit_issues",
                "value": (
                    metrics.get("security", {})
                    .get("bandit_scan", {})
                    .get("issues_found", 0)
                ),
                "timestamp": metrics.get("timestamp", ""),
            }
        )

        csv_data.append(
            {
                "category": "security",
                "metric": "safety_vulnerabilities",
                "value": (
                    metrics.get("security", {})
                    .get("safety_scan", {})
                    .get("vulnerabilities_found", 0)
                ),
                "timestamp": metrics.get("timestamp", ""),
            }
        )

        return csv_data
