## Périmètre d'archivage ARIA

Date : 27 avril 2026

Ce document décrit ce qui est figé dans ARIA et ce qui sert de source de migration vers CIA.

### Répertoires figés (archive)
- `mobile_app/`
- `metrics_collector/`
- `devops_automation/`
- `research_tools/`

### Répertoires source de migration (lecture/extraction)
- `pain_tracking/`
- `pattern_analysis/`
- `cia_compatibility/`
- `cia_sync/` (sélectivement, surtout logique de granularité)

### Règle de décision
- migrer dans CIA ce qui apporte une valeur clinique claire,
- ne pas migrer les composants simulés ou redondants sans besoin produit explicite.
