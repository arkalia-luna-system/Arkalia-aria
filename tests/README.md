# 🧪 Tests ARKALIA ARIA

## Structure des Tests

```
tests/
├── __init__.py
├── integration/
│   ├── __init__.py
│   └── test_cia_aria_integration.py
└── README.md
```

## Tests d'Intégration

### Test CIA/ARIA Integration

**Fichier** : `integration/test_cia_aria_integration.py`

**Fonctionnalités testées** :
- ✅ Santé des services CIA et ARIA
- ✅ Statut d'intégration ARIA depuis CIA
- ✅ Statut de synchronisation CIA depuis ARIA
- ✅ Saisie rapide de douleur
- ✅ Récupération de l'historique
- ✅ Export CSV pour professionnels

**Lancement** :
```bash
cd arkalia-aria
source arkalia_aria_venv/bin/activate
python tests/integration/test_cia_aria_integration.py
```

**Prérequis** :
- CIA démarré sur le port 8000
- ARIA démarré sur le port 8001
- Environnements virtuels activés

## Résultats Attendus

```
🚀 Test d'intégration optimisée CIA/ARIA
==================================================
🔍 Test de santé CIA...
✅ CIA est opérationnel
🔍 Test de santé ARIA...
✅ ARIA est opérationnel

==================================================
🔍 Test du statut d'intégration ARIA...
✅ Intégration ARIA: healthy
   - ARIA connecté: True
   - Fonctionnalités: quick_pain_entry, detailed_pain_entry, pain_history, export_to_psy, pattern_analysis, prediction_engine
🔍 Test du statut de synchronisation CIA...
✅ Sync CIA: healthy
   - CIA connecté: True
   - Fonctionnalités: selective_sync, psy_presentation_mode, granular_permissions, data_control, bidirectional_sync

==================================================
🔍 Test de saisie rapide de douleur...
✅ Entrée créée avec ID: X
   - Intensité: 7
   - Déclencheur: stress
🔍 Test de récupération de l'historique...
✅ Historique récupéré: X entrées
   - Dernière entrée: ID X, intensité 7
🔍 Test d'export CSV...
✅ Export CSV généré: pain_export_YYYYMMDD_HHMMSS.csv
   - Entrées: X

==================================================
✅ Tests d'intégration terminés
📊 Résumé:
   - CIA: ✅
   - ARIA: ✅
   - Intégration: ✅
   - Synchronisation: ✅
```

## Développement

Pour ajouter de nouveaux tests :

1. Créez un nouveau fichier dans `integration/`
2. Suivez le pattern des tests existants
3. Documentez les nouvelles fonctionnalités testées
4. Mettez à jour ce README
