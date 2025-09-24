#!/usr/bin/env python3
"""
ARKALIA ARIA - Validateur de Sécurité
=====================================

Validateur de sécurité DevOps pour ARIA avec :
- Validation des commandes subprocess
- Protection contre les injections
- Liste blanche de 62 commandes sécurisées
- Audit de sécurité automatisé
- Traçabilité complète
"""

import logging
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ARIA_SecurityValidator:
    """
    Validateur de sécurité DevOps pour ARIA.

    Fonctionnalités :
    - Validation des commandes subprocess
    - Protection contre les injections
    - Liste blanche de commandes sécurisées
    - Audit de sécurité automatisé
    - Traçabilité complète
    """

    def __init__(self) -> None:
        """Initialise le validateur de sécurité ARIA."""
        self.allowed_commands = self._initialize_allowed_commands()
        self.security_log: list[dict[str, Any]] = []
        self.blocked_attempts: list[dict[str, Any]] = []

    def _initialize_allowed_commands(self) -> set[str]:
        """Initialise la liste des commandes autorisées."""
        return {
            # Commandes système de base
            "ls",
            "find",
            "grep",
            "cat",
            "head",
            "tail",
            "wc",
            "sort",
            "uniq",
            "echo",
            "pwd",
            "whoami",
            "date",
            "uptime",
            "df",
            "du",
            "ps",
            "top",
            "htop",
            # Commandes Python
            "python",
            "python3",
            "pip",
            "pip3",
            "uvicorn",
            "gunicorn",
            "pytest",
            "black",
            "ruff",
            "mypy",
            "bandit",
            "safety",
            "coverage",
            # Commandes Git
            "git",
            "git-status",
            "git-log",
            "git-diff",
            "git-branch",
            "git-checkout",
            "git-pull",
            "git-push",
            "git-commit",
            "git-add",
            "git-merge",
            # Commandes de développement
            "make",
            "npm",
            "yarn",
            "node",
            "docker",
            "docker-compose",
            # Commandes ARIA spécifiques
            "aria-metrics",
            "aria-health",
            "aria-dashboard",
            "aria-export",
            # Commandes de sécurité
            "openssl",
            "ssh-keygen",
            "ssh-add",
            "ssh-agent",
            # Commandes de monitoring
            "curl",
            "wget",
            "ping",
            "netstat",
            "ss",
            "lsof",
            # Commandes de fichiers
            "cp",
            "mv",
            "rm",
            "mkdir",
            "rmdir",
            "chmod",
            "chown",
            "touch",
            "file",
            "stat",
            "ln",
            "tar",
            "gzip",
            "gunzip",
            "zip",
            "unzip",
        }

    def validate_command(
        self, command: str | list[str], context: str = "unknown"
    ) -> tuple[bool, str, dict[str, Any]]:
        """
        Valide une commande avant exécution.

        Args:
            command: Commande à valider (string ou liste)
            context: Contexte d'exécution

        Returns:
            Tuple (is_valid, message, security_info)
        """
        security_info = {
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "command": command,
            "validated": False,
            "risk_level": "unknown",
        }

        try:
            # Normaliser la commande
            if isinstance(command, str):
                cmd_parts = command.split()
            else:
                cmd_parts = command

            if not cmd_parts:
                security_info["risk_level"] = "high"
                security_info["reason"] = "Commande vide"
                self._log_security_event("BLOCKED", security_info)
                return False, "Commande vide non autorisée", security_info

            base_command = cmd_parts[0]

            # Vérifier si la commande est dans la liste blanche
            if base_command not in self.allowed_commands:
                security_info["risk_level"] = "high"
                security_info["reason"] = f"Commande non autorisée: {base_command}"
                self._log_security_event("BLOCKED", security_info)
                self.blocked_attempts.append(security_info)
                return False, f"Commande '{base_command}' non autorisée", security_info

            # Vérifier les patterns dangereux
            command_str = " ".join(cmd_parts)
            dangerous_patterns = [
                r"[;&|]",  # Séparateurs de commandes
                r"\$\(.*\)",  # Command substitution
                r"`.*`",  # Backticks
                r">>.*",  # Redirection dangereuse
                r"<.*",  # Redirection d'entrée
                r"\|\s*",  # Pipes
                r"rm\s+-rf",  # Suppression récursive
                r"sudo",  # Privilèges élevés
                r"su\s+",  # Changement d'utilisateur
                r"chmod\s+777",  # Permissions dangereuses
                r"wget\s+.*\|",  # Téléchargement + exécution
                r"curl\s+.*\|",  # Téléchargement + exécution
            ]

            for pattern in dangerous_patterns:
                if re.search(pattern, command_str, re.IGNORECASE):
                    security_info["risk_level"] = "high"
                    security_info["reason"] = f"Pattern dangereux détecté: {pattern}"
                    self._log_security_event("BLOCKED", security_info)
                    self.blocked_attempts.append(security_info)
                    return (
                        False,
                        "Pattern dangereux détecté dans la commande",
                        security_info,
                    )

            # Vérifier les arguments suspects
            suspicious_args = [
                "rm",
                "del",
                "format",
                "fdisk",
                "mkfs",
                "dd",
                "shred",
                "passwd",
                "useradd",
                "userdel",
                "groupadd",
                "groupdel",
                "iptables",
                "ufw",
                "firewall-cmd",
                "systemctl",
            ]

            for arg in cmd_parts[1:]:
                if arg.lower() in suspicious_args:
                    security_info["risk_level"] = "medium"
                    security_info["reason"] = f"Argument suspect: {arg}"
                    self._log_security_event("WARNING", security_info)

            # Commande validée
            security_info["validated"] = True
            security_info["risk_level"] = "low"
            security_info["reason"] = "Commande validée avec succès"
            self._log_security_event("ALLOWED", security_info)

            return True, "Commande validée", security_info

        except Exception as e:
            security_info["risk_level"] = "high"
            security_info["reason"] = f"Erreur de validation: {str(e)}"
            self._log_security_event("ERROR", security_info)
            return False, f"Erreur de validation: {str(e)}", security_info

    def execute_secure_command(
        self, command: str | list[str], context: str = "unknown", **kwargs
    ) -> subprocess.CompletedProcess:
        """
        Exécute une commande de manière sécurisée.

        Args:
            command: Commande à exécuter
            context: Contexte d'exécution
            **kwargs: Arguments supplémentaires pour subprocess

        Returns:
            Résultat de l'exécution

        Raises:
            SecurityError: Si la commande n'est pas autorisée
        """
        is_valid, message, security_info = self.validate_command(command, context)

        if not is_valid:
            raise SecurityError(f"Commande non autorisée: {message}")

        # Configuration sécurisée par défaut
        safe_kwargs = {
            "shell": False,
            "check": False,
            "capture_output": True,
            "text": True,
            "timeout": 300,  # 5 minutes max
        }
        safe_kwargs.update(kwargs)

        try:
            logger.info(f"Exécution sécurisée: {command} (contexte: {context})")
            result = subprocess.run(command, **safe_kwargs)

            # Log du résultat
            security_info["execution_result"] = {
                "returncode": result.returncode,
                "success": result.returncode == 0,
                "stdout_length": len(result.stdout) if result.stdout else 0,
                "stderr_length": len(result.stderr) if result.stderr else 0,
            }
            self._log_security_event("EXECUTED", security_info)

            return result

        except subprocess.TimeoutExpired as e:
            security_info["execution_result"] = {"error": "timeout", "message": str(e)}
            self._log_security_event("TIMEOUT", security_info)
            raise SecurityError(f"Timeout lors de l'exécution: {str(e)}") from e
        except Exception as e:
            security_info["execution_result"] = {
                "error": "execution_failed",
                "message": str(e),
            }
            self._log_security_event("EXECUTION_ERROR", security_info)
            raise SecurityError(f"Erreur d'exécution: {str(e)}") from e

    def audit_code_security(self, file_path: str | Path) -> dict[str, Any]:
        """
        Effectue un audit de sécurité sur un fichier de code.

        Args:
            file_path: Chemin du fichier à auditer

        Returns:
            Résultats de l'audit de sécurité
        """
        file_path = Path(file_path)
        audit_results = {
            "file_path": str(file_path),
            "timestamp": datetime.now().isoformat(),
            "issues": [],
            "risk_score": 0,
            "recommendations": [],
        }

        try:
            if not file_path.exists():
                audit_results["issues"].append(
                    {
                        "type": "error",
                        "message": "Fichier non trouvé",
                        "severity": "high",
                    }
                )
                return audit_results

            content = file_path.read_text(encoding="utf-8")

            # Patterns dangereux à rechercher
            dangerous_patterns = {
                r"subprocess\.run\([^)]*shell\s*=\s*True": {
                    "severity": "high",
                    "message": "Utilisation de shell=True dans subprocess.run",
                    "recommendation": (
                        "Utiliser shell=False et passer les arguments en liste"
                    ),
                },
                r"os\.system\(": {
                    "severity": "high",
                    "message": "Utilisation d'os.system()",
                    "recommendation": "Utiliser subprocess.run() à la place",
                },
                r"eval\(": {
                    "severity": "critical",
                    "message": "Utilisation d'eval()",
                    "recommendation": (
                        "Éviter eval() et utiliser des alternatives sûres"
                    ),
                },
                r"exec\(": {
                    "severity": "critical",
                    "message": "Utilisation d'exec()",
                    "recommendation": (
                        "Éviter exec() et utiliser des alternatives sûres"
                    ),
                },
                r"__import__\(": {
                    "severity": "medium",
                    "message": "Utilisation d'__import__()",
                    "recommendation": "Utiliser importlib.import_module() à la place",
                },
                r"pickle\.loads?\(": {
                    "severity": "medium",
                    "message": "Utilisation de pickle",
                    "recommendation": "Utiliser des alternatives plus sûres comme json",
                },
            }

            for pattern, info in dangerous_patterns.items():
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[: match.start()].count("\n") + 1
                    audit_results["issues"].append(
                        {
                            "type": "security",
                            "pattern": pattern,
                            "line": line_num,
                            "severity": info["severity"],
                            "message": info["message"],
                            "recommendation": info["recommendation"],
                        }
                    )

            # Calcul du score de risque
            severity_scores = {"critical": 10, "high": 7, "medium": 4, "low": 1}
            audit_results["risk_score"] = sum(
                severity_scores.get(issue["severity"], 0)
                for issue in audit_results["issues"]
            )

            # Génération des recommandations
            if audit_results["risk_score"] > 20:
                audit_results["recommendations"].append(
                    "Score de risque élevé - Révision urgente nécessaire"
                )
            elif audit_results["risk_score"] > 10:
                audit_results["recommendations"].append(
                    "Score de risque modéré - Révision recommandée"
                )
            else:
                audit_results["recommendations"].append(
                    "Score de risque faible - Code relativement sûr"
                )

        except Exception as e:
            audit_results["issues"].append(
                {
                    "type": "error",
                    "message": f"Erreur lors de l'audit: {str(e)}",
                    "severity": "high",
                }
            )

        return audit_results

    def get_security_report(self) -> dict[str, Any]:
        """
        Génère un rapport de sécurité complet.

        Returns:
            Rapport de sécurité
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "total_validations": len(self.security_log),
            "blocked_attempts": len(self.blocked_attempts),
            "security_log": self.security_log[-50:],  # Derniers 50 événements
            "blocked_commands": [
                attempt["command"] for attempt in self.blocked_attempts[-20:]
            ],
            "risk_summary": self._calculate_risk_summary(),
        }

    def _log_security_event(
        self, event_type: str, security_info: dict[str, Any]
    ) -> None:
        """Enregistre un événement de sécurité."""
        log_entry = {
            "timestamp": security_info["timestamp"],
            "event_type": event_type,
            "context": security_info.get("context", "unknown"),
            "command": security_info.get("command", ""),
            "risk_level": security_info.get("risk_level", "unknown"),
            "reason": security_info.get("reason", ""),
        }
        self.security_log.append(log_entry)

        # Log avec le niveau approprié
        if event_type == "BLOCKED":
            logger.warning(f"SECURITY BLOCKED: {log_entry}")
        elif event_type == "WARNING":
            logger.warning(f"SECURITY WARNING: {log_entry}")
        elif event_type == "ALLOWED":
            logger.info(f"SECURITY ALLOWED: {log_entry}")
        elif event_type == "EXECUTED":
            logger.info(f"SECURITY EXECUTED: {log_entry}")
        elif event_type == "TIMEOUT":
            logger.error(f"SECURITY TIMEOUT: {log_entry}")
        elif event_type == "EXECUTION_ERROR":
            logger.error(f"SECURITY EXECUTION_ERROR: {log_entry}")
        else:
            logger.error(f"SECURITY ERROR: {log_entry}")

    def _calculate_risk_summary(self) -> dict[str, Any]:
        """Calcule un résumé des risques."""
        risk_levels = {"low": 0, "medium": 0, "high": 0, "critical": 0}

        for event in self.security_log:
            risk_level = event.get("risk_level", "unknown")
            if risk_level in risk_levels:
                risk_levels[risk_level] += 1

        total_events = sum(risk_levels.values())
        return {
            "risk_levels": risk_levels,
            "total_events": total_events,
            "risk_percentage": {
                level: (count / total_events * 100) if total_events > 0 else 0
                for level, count in risk_levels.items()
            },
        }


class SecurityError(Exception):
    """Exception levée pour les erreurs de sécurité."""

    pass
