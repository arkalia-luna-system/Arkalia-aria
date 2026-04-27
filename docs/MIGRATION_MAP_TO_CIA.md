## Cartographie migration ARIA -> CIA

Date : 27 avril 2026

### Modules prioritaires
- `pain_tracking/api.py` -> backend CIA (endpoints douleur enrichis)
- `pattern_analysis/correlation_analyzer.py` -> backend CIA (corrélations déterministes)
- `cia_compatibility/api.py` -> backend CIA (normalisation contrat API)
- `cia_sync/granularity_config.py` -> backend CIA (partage granulaire privacy-first)

### Modules à traiter avec prudence
- `health_connectors/` -> uniquement après validation d'intégrations réelles (éviter les mocks en production)

### Modules non prioritaires
- `metrics_collector/` (doublon de supervision)
- `devops_automation/` (hors coeur produit final)
- `mobile_app/` (si CIA reste l'app unique)

### Cible finale
- CIA devient l'unique projet actif pour les fonctionnalités utilisateur.
- ARIA reste un dépôt d'archive et d'historique.
