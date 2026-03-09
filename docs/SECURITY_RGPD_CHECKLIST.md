## Checklist Sécurité & RGPD

Cette checklist résume les points principaux de conformité et de sécurité d’ARKALIA ARIA.

- **Localisation des données** : données de santé stockées en local (bases SQLite `aria_pain.db` et `aria_research.db`).
- **Droits des utilisateurs** : endpoints de suppression (droit à l’oubli) implémentés et documentés dans `API_REFERENCE.md`.
- **Sécurité applicative** : scans automatisés via Bandit et Safety, workflows GitHub Actions dédiés (`security.yml`).
- **Chiffrement & accès** : accès protégé au serveur, recommandations TLS/HTTPS décrites dans `CONFIGURATION_GUIDE.md`.
- **Journalisation** : logs centralisés via `core/logging.py`, adaptés pour le diagnostic sans sur-exposition de données sensibles.
- **Documentation légale** : voir `LEGAL_MENTIONS.md`, `PRIVACY_POLICY.md`, `TERMS_OF_USE.md` et `COOKIES_POLICY.md`.

Pour les détails complets et la roadmap conformité, se référer à la section RGPD de `PROJECT_STATUS.md`.
