# Configuration ARKALIA ARIA

Ce dossier contient tous les fichiers de configuration pour optimiser les performances et éviter la surcharge du système.

## 📁 Structure

```
config/
├── .bandit              # Configuration Bandit optimisée
├── .safety              # Configuration Safety optimisée  
├── deployment.json      # Configuration de déploiement
├── monitoring.json      # Configuration de monitoring
├── nginx.conf          # Configuration Nginx
├── performance.toml     # Configuration de performance
└── README.md           # Ce fichier
```

## ⚙️ Fichiers de configuration

### `.bandit`
Configuration optimisée pour Bandit (analyse de sécurité Python) :
- **Timeouts** : 5 minutes maximum
- **Exclusions** : Tests, cache, venv, etc.
- **Tests ignorés** : Faux positifs courants
- **Limites** : Taille de fichier et nombre de lignes

### `.safety`
Configuration optimisée pour Safety (vérification de vulnérabilités) :
- **Timeout** : 3 minutes maximum
- **Cache** : Activé pour éviter les scans répétés
- **Sévérité** : Seulement les vulnérabilités hautes
- **Exclusions** : Versions expirées ignorées

### `performance.toml`
Configuration de performance pour :
- **Développement** : Workers, timeouts, cache
- **CI/CD** : Jobs parallèles, cache, timeouts
- **Optimisation** : Compression, mémoire, base de données

## 🚀 Utilisation

### Via Makefile
```bash
# Nettoyer les processus lourds
make clean-heavy

# Nettoyage complet
make clean
```

### Via script direct
```bash
# Nettoyer les processus lourds
./devops_automation/scripts/cleanup_heavy_processes.sh
```

## 🔧 Optimisations appliquées

1. **Timeouts** : Tous les outils ont des limites de temps
2. **Exclusions** : Répertoires non pertinents exclus
3. **Cache** : Mise en cache des dépendances
4. **Limites** : Taille de fichier et mémoire limitées
5. **Monitoring** : Surveillance des ressources

## 📊 Résultats attendus

- **CPU** : Réduction de 50-80% de la charge
- **RAM** : Économie de 1-2GB
- **Temps** : Scans 3-5x plus rapides
- **Stabilité** : Plus de surcharge système