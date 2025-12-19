# 📚 Guide de Configuration GitHub Pages

Ce guide explique comment activer GitHub Pages pour déployer automatiquement la documentation du projet ARKALIA ARIA.

## ❌ Erreur Rencontrée

Si vous voyez cette erreur dans les workflows GitHub Actions :

```
Error: HttpError: Not Found
Error: Creating Pages deployment failed
Error: Failed to create deployment (status: 404)
```

Cela signifie que **GitHub Pages n'est pas activé** pour ce repository.

## 🔧 Solution : Activer GitHub Pages

### Étape 1 : Accéder aux Paramètres

1. Allez sur votre repository GitHub :
   ```
   https://github.com/arkalia-luna-system/Arkalia-aria
   ```

2. Cliquez sur l'onglet **Settings** (Paramètres) en haut du repository

3. Dans le menu de gauche, cliquez sur **Pages** (sous "Code and automation")

### Étape 2 : Configurer la Source

1. Dans la section **"Source"**, vous verrez un menu déroulant

2. Sélectionnez **"GitHub Actions"** comme source de déploiement

3. Cliquez sur **"Save"** (Enregistrer)

### Étape 3 : Vérifier l'Activation

Après avoir sauvegardé, vous devriez voir :
- ✅ Un message de confirmation
- ✅ L'URL de votre site GitHub Pages (généralement : `https://arkalia-luna-system.github.io/Arkalia-aria/`)

### Étape 4 : Relancer le Workflow

1. Allez dans l'onglet **Actions** de votre repository

2. Trouvez le workflow **"📚 Deploy Documentation - GitHub Pages"**

3. Cliquez sur **"Run workflow"** (Exécuter le workflow) pour relancer le déploiement

## 📋 Prérequis

Avant d'activer GitHub Pages, assurez-vous que :

- ✅ Vous avez les permissions d'**administrateur** sur le repository
- ✅ Le workflow `.github/workflows/deploy-docs.yml` existe et est valide
- ✅ La documentation MkDocs est correctement configurée (`mkdocs.yml`)

## 🔍 Vérification du Workflow

Le workflow de déploiement est configuré pour :

- **Déclenchement** : Sur push vers `main` ou `develop`
- **Build** : Construction de la documentation avec MkDocs
- **Déploiement** : Déploiement automatique vers GitHub Pages (uniquement sur `main`)

### Permissions Requises

Le workflow nécessite les permissions suivantes :
- `contents: read` - Lire le contenu du repository
- `pages: write` - Écrire sur GitHub Pages
- `id-token: write` - Authentification OIDC

Ces permissions sont déjà configurées dans le workflow.

## 🚀 Après l'Activation

Une fois GitHub Pages activé :

1. **Premier déploiement** : Le workflow se déclenchera automatiquement au prochain push sur `main`
2. **URL de la documentation** : Accessible à `https://arkalia-luna-system.github.io/Arkalia-aria/`
3. **Mises à jour automatiques** : Chaque push sur `main` déclenchera un nouveau déploiement

## 🐛 Dépannage

### Le déploiement échoue toujours après activation

1. Vérifiez que vous avez bien sélectionné **"GitHub Actions"** et non **"Deploy from a branch"**
2. Attendez quelques minutes après l'activation (GitHub peut prendre du temps)
3. Vérifiez les logs du workflow dans l'onglet **Actions**

### L'URL GitHub Pages ne fonctionne pas

1. Attendez 5-10 minutes après le premier déploiement
2. Vérifiez que le workflow s'est terminé avec succès
3. L'URL peut être : `https://arkalia-luna-system.github.io/Arkalia-aria/` ou `https://arkalia-luna-system.github.io/arkalia-aria/` (selon la casse)

### Erreur de permissions

Si vous voyez des erreurs de permissions :
1. Vérifiez que vous êtes administrateur du repository
2. Vérifiez que les permissions du workflow sont correctement configurées
3. Pour les repositories d'organisation, vérifiez les paramètres d'organisation

## 📖 Ressources

- [Documentation officielle GitHub Pages](https://docs.github.com/en/pages)
- [GitHub Actions pour Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#publishing-with-a-custom-github-actions-workflow)
- [Workflow de déploiement](../.github/workflows/deploy-docs.yml)

## ✅ Checklist de Vérification

- [ ] GitHub Pages activé dans les paramètres
- [ ] Source configurée sur "GitHub Actions"
- [ ] Workflow exécuté avec succès
- [ ] Documentation accessible via l'URL GitHub Pages
- [ ] Déploiements automatiques fonctionnels

---

**Note** : Ce guide est spécifique au repository `arkalia-luna-system/Arkalia-aria`. Pour d'autres repositories, adaptez les URLs et noms de repository en conséquence.

