# Checklist Archivage GitHub - ARKALIA ARIA

Date de référence : 27 avril 2026

## 1) Préparation

- [ ] Vérifier que `README.md` indique clairement le statut archive
- [ ] Vérifier présence des docs : `NOTICE_FUSION_CIA.md`, `DEPRECATION.md`, `docs/ARCHIVE_SCOPE.md`, `docs/MIGRATION_MAP_TO_CIA.md`
- [ ] Vérifier que les nouvelles évolutions sont redirigées vers `arkalia-cia`

## 2) Communication publique (repo)

- [ ] Créer une release/tag final de référence (ex: `aria-final-before-archive`)
- [ ] Publier une annonce GitHub (Discussion ou issue épinglée) avec lien vers CIA
- [ ] Mettre à jour la description du repo avec mention "Archived / migrated to CIA"
- [ ] Épingler le message de migration dans le repo

## 3) Gestion des issues et PR

- [ ] Fermer les issues non critiques avec message de migration vers CIA
- [ ] Laisser ouvertes uniquement les issues documentaires indispensables (si besoin)
- [ ] Désactiver l'ouverture de nouvelles features côté ARIA (renvoi vers CIA)
- [ ] Clore ou rediriger les PR de nouvelles fonctionnalités vers CIA

## 4) Hygiène technique avant archive

- [ ] Vérifier que les workflows CI restants ne lancent pas de déploiement inutile
- [ ] Conserver les workflows utiles uniquement pour lisibilité historique
- [ ] Vérifier absence de secrets actifs inutiles dans les settings GitHub

## 5) Action d'archivage

- [ ] Archiver le dépôt dans GitHub settings
- [ ] Vérifier que le dépôt est bien en lecture seule
- [ ] Vérifier que le lien vers CIA est visible immédiatement sur la page principale

## 6) Vérification post-archive

- [ ] Vérifier que les utilisateurs arrivent bien vers CIA depuis ARIA
- [ ] Vérifier que la documentation d'archive reste accessible
- [ ] Noter la date d'archivage effective dans `NOTICE_FUSION_CIA.md`
