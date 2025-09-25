# Configuration ARIA

Ce dossier contient tous les fichiers de configuration pour ARIA.

## Fichiers

- `deployment.json` - Configuration de déploiement
- `monitoring.json` - Configuration de monitoring
- `nginx.conf` - Configuration Nginx

## Utilisation

Ces fichiers sont automatiquement générés par le système CI/CD et ne doivent pas être modifiés manuellement.

## Génération

Pour régénérer ces fichiers :

```bash
python -m devops_automation.cicd.aria_cicd_manager
```
