# 💡 Exemples d'Utilisation - ARKALIA ARIA

## 🚀 Cas d'Usage Courants

### Saisie Rapide de Douleur

```bash
curl -X POST "http://127.0.0.1:8001/api/pain/quick-entry" \
  -H "Content-Type: application/json" \
  -d '{
    "intensity": 6,
    "trigger": "stress",
    "action": "respiration"
  }'

```

### Export des Données

```bash
curl -X GET "http://127.0.0.1:8001/api/pain/export/csv"

```

---

**ARKALIA ARIA** - Exemples pratiques ! 💡🚀
