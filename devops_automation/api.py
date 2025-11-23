#!/usr/bin/env python3
# ruff: noqa: B904
"""
ARKALIA ARIA - API DevOps
=========================

API FastAPI pour le système DevOps automatisé d'ARIA avec :
- Endpoints de sécurité
- Endpoints CI/CD
- Endpoints d'assurance qualité
- Endpoints de déploiement
- Endpoints de monitoring
"""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

from .cicd.aria_cicd_manager import ARIA_CICDManager
from .deployment.aria_deployment_manager import ARIA_DeploymentManager
from .monitoring.aria_monitoring_system import ARIA_MonitoringSystem
from .quality.aria_quality_assurance import ARIA_QualityAssurance
from .security.aria_security_validator import ARIA_SecurityValidator


class ARIA_DevOpsAPI:
    """
    API REST pour le système DevOps ARIA.

    Endpoints disponibles :
    - /devops/security/* : Sécurité et validation
    - /devops/cicd/* : CI/CD et workflows
    - /devops/quality/* : Assurance qualité
    - /devops/deployment/* : Déploiement
    - /devops/monitoring/* : Monitoring
    """

    def __init__(self, project_root: str = ".") -> None:
        """
        Initialise l'API DevOps ARIA.

        Args:
            project_root: Racine du projet ARIA
        """
        self.project_root = project_root
        self.security_validator = ARIA_SecurityValidator()
        self.cicd_manager = ARIA_CICDManager(project_root)
        self.quality_assurance = ARIA_QualityAssurance(project_root)
        self.deployment_manager = ARIA_DeploymentManager(project_root)
        self.monitoring_system = ARIA_MonitoringSystem(project_root)

        self.router = APIRouter(prefix="/devops", tags=["devops"])
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Configure les routes de l'API DevOps."""

        # Routes de sécurité
        @self.router.post("/security/validate-command")
        async def validate_command(request: Request):
            """Valide une commande avant exécution."""
            try:
                data = await request.json()
                command = data.get("command")
                context = data.get("context", "api")

                if not command:
                    raise HTTPException(status_code=400, detail="Commande requise")

                is_valid, message, security_info = (
                    self.security_validator.validate_command(command, context)
                )

                return {
                    "valid": is_valid,
                    "message": message,
                    "security_info": security_info,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur validation: {str(e)}"
                )

        @self.router.post("/security/execute-command")
        async def execute_command(request: Request):
            """Exécute une commande de manière sécurisée."""
            try:
                data = await request.json()
                command = data.get("command")
                context = data.get("context", "api")

                if not command:
                    raise HTTPException(status_code=400, detail="Commande requise")

                result = self.security_validator.execute_secure_command(
                    command, context
                )

                return {
                    "success": result.returncode == 0,
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur exécution: {str(e)}"
                )

        @self.router.get("/security/audit/{file_path:path}")
        async def audit_file(file_path: str):
            """Effectue un audit de sécurité sur un fichier."""
            try:
                audit_result = self.security_validator.audit_code_security(file_path)
                return {
                    "audit_result": audit_result,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur audit: {str(e)}")

        @self.router.get("/security/report")
        async def get_security_report():
            """Retourne le rapport de sécurité complet."""
            try:
                report = self.security_validator.get_security_report()
                return {
                    "security_report": report,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur rapport: {str(e)}")

        @self.router.get("/security/dashboard", response_class=HTMLResponse)
        async def get_security_dashboard():
            """Retourne un dashboard HTML synthétique de sécurité."""
            try:
                report = self.security_validator.get_security_report()
                html = self.generate_security_dashboard_html(report)
                return HTMLResponse(content=html)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur dashboard: {str(e)}"
                )

        # Routes CI/CD
        @self.router.post("/cicd/setup")
        async def setup_cicd(request: Request):
            """Configure le système CI/CD."""
            try:
                data = await request.json()
                config = data.get("config", {})

                results = self.cicd_manager.setup_cicd(config)

                return {
                    "status": "success",
                    "message": "Configuration CI/CD terminée",
                    "results": results,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur CI/CD: {str(e)}")

        @self.router.get("/cicd/status")
        async def get_cicd_status():
            """Retourne le statut du système CI/CD."""
            try:
                status = self.cicd_manager.get_deployment_status()
                return {
                    "cicd_status": status,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur statut CI/CD: {str(e)}"
                )

        # Routes d'assurance qualité
        @self.router.post("/quality/check")
        async def run_quality_check(request: Request):
            """Exécute une vérification complète de qualité."""
            try:
                data = await request.json()
                fix_issues = data.get("fix_issues", False)

                report = self.quality_assurance.run_full_quality_check(fix_issues)

                return {
                    "quality_report": report,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur qualité: {str(e)}")

        @self.router.get("/quality/history")
        async def get_quality_history():
            """Retourne l'historique des rapports de qualité."""
            try:
                history = self.quality_assurance.get_quality_history()
                return {
                    "quality_history": history,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur historique: {str(e)}"
                )

        @self.router.get("/quality/dashboard", response_class=HTMLResponse)
        async def get_quality_dashboard():
            """Retourne le dashboard HTML de qualité."""
            try:
                # Obtenir le dernier rapport
                history = self.quality_assurance.get_quality_history()
                if not history:
                    return HTMLResponse("<h1>Aucun rapport de qualité disponible</h1>")

                latest_report = history[-1]
                dashboard_html = self.quality_assurance.generate_quality_report_html(
                    latest_report
                )

                return HTMLResponse(content=dashboard_html)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur dashboard: {str(e)}"
                )

        # Routes de déploiement
        @self.router.post("/deployment/deploy")
        async def deploy(request: Request):
            """Déploie ARIA dans un environnement."""
            try:
                data = await request.json()
                environment = data.get("environment", "staging")
                version = data.get("version")

                if environment not in ["staging", "production"]:
                    raise HTTPException(
                        status_code=400, detail="Environnement non supporté"
                    )

                deployment_result = self.deployment_manager.deploy(environment, version)

                return {
                    "deployment_result": deployment_result,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur déploiement: {str(e)}"
                )

        @self.router.post("/deployment/rollback")
        async def rollback(request: Request):
            """Effectue un rollback."""
            try:
                data = await request.json()
                environment = data.get("environment", "staging")
                deployment_id = data.get("deployment_id")

                rollback_result = self.deployment_manager.rollback(
                    environment, deployment_id
                )

                return {
                    "rollback_result": rollback_result,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur rollback: {str(e)}"
                )

        @self.router.get("/deployment/status/{environment}")
        async def get_deployment_status(environment: str):
            """Retourne le statut du déploiement pour un environnement."""
            try:
                status = self.deployment_manager.get_deployment_status(environment)
                return {
                    "deployment_status": status,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur statut: {str(e)}")

        # Routes de monitoring
        @self.router.get("/monitoring/health")
        async def get_health_status():
            """Retourne le statut de santé du système."""
            try:
                health_status = self.monitoring_system.get_health_status()
                return {
                    "health_status": health_status,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur santé: {str(e)}")

        @self.router.get("/monitoring/performance")
        async def get_performance_summary(hours: int = 24):
            """Retourne un résumé des performances."""
            try:
                performance_summary = self.monitoring_system.get_performance_summary(
                    hours
                )
                return {
                    "performance_summary": performance_summary,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur performance: {str(e)}"
                )

        @self.router.get("/monitoring/alerts")
        async def get_alerts_summary(hours: int = 24):
            """Retourne un résumé des alertes."""
            try:
                alerts_summary = self.monitoring_system.get_alerts_summary(hours)
                return {
                    "alerts_summary": alerts_summary,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur alertes: {str(e)}")

        @self.router.get("/monitoring/dashboard", response_class=HTMLResponse)
        async def get_monitoring_dashboard():
            """Retourne le dashboard HTML de monitoring."""
            try:
                dashboard_html = (
                    self.monitoring_system.generate_monitoring_dashboard_html()
                )
                return HTMLResponse(content=dashboard_html)
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur dashboard: {str(e)}"
                )

        @self.router.post("/monitoring/export")
        async def export_monitoring_data(request: Request):
            """Exporte les données de monitoring."""
            try:
                data = await request.json()
                format_type = data.get("format", "json")
                hours = data.get("hours", 24)

                file_path = self.monitoring_system.export_monitoring_data(
                    format_type, hours
                )

                return {
                    "status": "success",
                    "message": f"Données exportées en {format_type.upper()}",
                    "file_path": str(file_path),
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur export: {str(e)}"
                ) from e

        # Routes générales DevOps
        @self.router.get("/status")
        async def get_devops_status():
            """Retourne le statut global du système DevOps."""
            try:
                return {
                    "devops_status": {
                        "security": {
                            "validator_active": True,
                            "blocked_attempts": len(
                                self.security_validator.blocked_attempts
                            ),
                        },
                        "cicd": {
                            "manager_active": True,
                            "deployments": len(self.cicd_manager.deployment_history),
                        },
                        "quality": {
                            "assurance_active": True,
                            "reports": len(self.quality_assurance.quality_reports),
                        },
                        "deployment": {
                            "manager_active": True,
                            "deployments": len(
                                self.deployment_manager.deployment_history
                            ),
                        },
                        "monitoring": {
                            "system_active": self.monitoring_system.is_monitoring,
                            "data_points": len(self.monitoring_system.monitoring_data),
                            "alerts": len(self.monitoring_system.alerts),
                        },
                    },
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Erreur statut: {str(e)}"
                ) from e

    def get_router(self) -> APIRouter:
        """Retourne le router FastAPI configuré."""
        return self.router

    def integrate_with_app(self, app) -> None:
        """Intègre l'API DevOps avec une application FastAPI."""
        app.include_router(self.router)

    # ==== Helpers Dashboards ====
    def generate_security_dashboard_html(self, report: dict[str, Any]) -> str:
        """Génère un HTML simple pour visualiser l'état de sécurité."""

        def esc(s: str) -> str:
            return (
                s.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;")
            )

        ts = esc(datetime.now().strftime("%Y-%m-%d %H:%M"))
        # Compatibilité souple selon la structure du rapport
        risk = report.get("risk_summary", {})

        # Journal complet des événements
        security_log = report.get("security_log", [])
        if not isinstance(security_log, list):
            security_log = []
        recent = security_log[-10:]

        # Commandes bloquées (liste de chaînes ou d'objets)
        blocked_raw = report.get("blocked_commands", [])
        if isinstance(blocked_raw, list):
            # Normaliser en objets avec timestamp inconnu
            blocked = [
                (
                    {"timestamp": "n/a", "command": str(cmd), "reason": "blocked"}
                    if not isinstance(cmd, dict)
                    else cmd
                )
                for cmd in blocked_raw
            ][-10:]
        else:
            blocked = []

        blocked_rows = "".join(
            f"<tr><td>{esc(str(a.get('timestamp','')))}</td><td>{esc(str(a.get('command','')))}</td><td>{esc(str(a.get('reason','')))}</td></tr>"
            for a in blocked
        )
        recent_rows = ""
        for a in recent:
            if isinstance(a, dict):
                ts = esc(str(a.get("timestamp", "")))
                cmd = esc(str(a.get("command", "")))
                risk_level = esc(str(a.get("risk_level", "")))
                etype = esc(str(a.get("event_type", "")))
            else:
                ts = ""
                cmd = esc(str(a))
                risk_level = ""
                etype = ""
            recent_rows += (
                f"<tr><td>{ts}</td><td>{cmd}</td>"
                f"<td>{risk_level}</td><td>{etype}</td></tr>"
            )

        html = f"""
<!doctype html>
<html lang=fr>
<head>
  <meta charset=utf-8>
  <title>Dashboard Sécurité - ARIA</title>
  <meta name=viewport content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 24px; }}
    h1, h2 {{ margin: 0 0 8px 0; }}
    .muted {{ color: #666 }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ border: 1px solid #ddd; padding: 6px 8px; font-size: 13px; }}
    th {{ background: #fafafa; text-align: left; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
    .badge {{ display: inline-block; padding: 2px 8px;
              border-radius: 12px; font-size: 12px; }}
    .b-low {{ background:#e7f7ee; color:#1e7f53 }}
    .b-med {{ background:#fff4cc; color:#a66b00 }}
    .b-hi {{ background:#fde2e1; color:#b42318 }}
  </style>
</head>
<body>
  <h1>🔒 Sécurité ARIA</h1>
  <div class=muted>Généré {ts}</div>

  <h2>1. Résumé des risques</h2>
  <ul>
    <li>Faible: <span class="badge b-low">{esc(str(risk.get('low',0)))}</span></li>
    <li>Moyen: <span class="badge b-med">{esc(str(risk.get('medium',0)))}</span></li>
    <li>Élevé: <span class="badge b-hi">{esc(str(risk.get('high',0)))}</span></li>
  </ul>

  <div class=grid>
    <div>
      <h2>2. Tentatives bloquées (10 dernières)</h2>
      <table>
        <thead><tr><th>Horodatage</th><th>Commande</th><th>Raison</th></tr></thead>
        <tbody>{blocked_rows or '<tr><td colspan=3>Aucune</td></tr>'}</tbody>
      </table>
    </div>
    <div>
      <h2>3. Événements récents</h2>
      <table>
        <thead><tr><th>Horodatage</th><th>Commande</th><th>Risque</th><th>Type</th></tr></thead>
        <tbody>{recent_rows or '<tr><td colspan=4>Aucun</td></tr>'}</tbody>
      </table>
    </div>
  </div>
</body>
</html>
"""
        return html
