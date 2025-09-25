# ✅ Checklist Sécurité & RGPD – ARKALIA ARIA

Dernière mise à jour: 2025-09-25

## Principes Clés
- Licéité, loyauté, transparence
- Limitation des finalités et minimisation des données
- Exactitude, limitation de la conservation, intégrité et confidentialité

## 1) Cartographie et Finalités
- [ ] Registre de traitement à jour pour: santé, douleur, analytics, mobile
- [ ] Finalités documentées dans `docs/` (soins, suivi, recherche, UX)
- [ ] Base légale: consentement explicite pour données santé

## 2) Consentement et Droits
- [ ] Recueil de consentement clair (mobile/web) avec preuve
- [ ] Retrait du consentement simple, sans dégrader l’expérience
- [ ] Droits: accès, rectification, effacement, limitation, portabilité, opposition
- [ ] Procédure de réponse (<30 jours) documentée

## 3) Minimisation des Données
- [ ] Collecte strictement nécessaire (pas de données superflues)
- [ ] Champs optionnels explicitement marqués
- [ ] Pseudonymisation lorsque possible

## 4) Sécurité Technique
- [ ] Données locales chiffrées au repos (SQLite pragma chiffrage si activé)
- [ ] Transport sécurisé (HTTPS en prod)
- [ ] Secrets/API keys en variables d’environnement
- [ ] Politique CORS minimale (`core/config.py`)
- [ ] Limites de taille requêtes (`ARIA_MAX_REQUEST_SIZE`)
- [ ] Journalisation sans PII sensible
- [ ] Sauvegardes chiffrées, test de restauration périodique

## 5) Rétention et Suppression
- [ ] Politique de rétention (ex: 365 jours, configurable)
- [ ] Endpoint/processus de purge + droit à l’oubli
- [ ] Logs: rotation et durée limitée

## 6) Notifications & Compatibilité Système
- [ ] Permissions notifications (iOS/Android) conformes aux guidelines
- [ ] Contenu non sensible dans les notifications
- [ ] Scénarios testés: rappel douleur, sync, rapports

## 7) Connecteurs Santé (Samsung/Google Fit/iOS)
- [ ] Portées minimales, tokens chiffrés, rotation auto
- [ ] Désactivation par connecteur (consentement granulaire)
- [ ] Sync chiffrée, pas d’envoi tiers non autorisé

## 8) Incidents & Conformité
- [ ] Plan de gestion d’incidents (72h notification si applicable)
- [ ] Revue régulière Bandit/Safety, dépendances à jour
- [ ] Revue de code sécurité et pair review obligatoire

## 9) Documentation & Revue
- [ ] Doc harmonisée FastAPI/Flutter (endpoints, cas d’usage santé)
- [ ] Mentions légales et politique privacy accessibles
- [ ] Check de conformité avant release/merge

## 10) Points de Contrôle Rapides
- [ ] `black` + `ruff` OK
- [ ] Tests unitaires critiques OK (pain, analytics)
- [ ] Bandit/Safety OK (hors venv)
- [ ] Lint docs: endpoints à jour (pain: quick-entry, entry, entries, recent, suggestions, exports)
