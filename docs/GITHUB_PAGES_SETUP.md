# 📚 Configuration GitHub Pages pour ARKALIA ARIA

## ⚠️ Activation Requise

Pour que le déploiement automatique de la documentation fonctionne, **GitHub Pages doit être activé** dans les paramètres du repository.

## 🔧 Étapes d'Activation

### 1. Accéder aux Paramètres
1. Aller sur : https://github.com/arkalia-luna-system/Arkalia-aria/settings/pages
2. Ou : Repository → **Settings** → **Pages** (dans le menu de gauche)

### 2. Configurer la Source
- **Source** : Sélectionner **"GitHub Actions"** (pas "Deploy from a branch")
- **Branch** : Laisser vide (géré par GitHub Actions)
- Cliquer sur **"Save"**

### 3. Vérifier l'Activation
- Un message de confirmation devrait apparaître
- L'URL de la documentation sera : `https://arkalia-luna-system.github.io/Arkalia-aria/`

## 📋 Workflows Disponibles

Le projet contient deux workflows pour la documentation :

1. **`.github/workflows/docs.yml`** - Workflow simple
2. **`.github/workflows/gh-pages.yml`** - Workflow complet avec notifications

Les deux utilisent la méthode moderne `actions/deploy-pages@v4`.

## ✅ Vérification

Une fois activé, le workflow se déclenchera automatiquement à chaque push sur `main` et déploiera la documentation.

Pour vérifier :
- Aller dans l'onglet **Actions** du repository
- Vérifier que le workflow "Build Documentation" ou "Deploy Documentation" s'exécute
- La documentation sera disponible après le premier déploiement réussi

## 🐛 Dépannage

### Erreur : "Not Found" (404)
- **Cause** : GitHub Pages n'est pas activé
- **Solution** : Suivre les étapes ci-dessus

### Erreur : "Permission denied" (403)
- **Cause** : Permissions insuffisantes
- **Solution** : Vérifier que les permissions dans le workflow sont correctes :
  ```yaml
  permissions:
    contents: read
    pages: write
    id-token: write
  ```

### Erreur : "Environment not found"
- **Cause** : L'environment `github-pages` n'existe pas
- **Solution** : GitHub crée automatiquement cet environment lors de l'activation de Pages

## 📚 Documentation

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions for Pages](https://github.com/actions/deploy-pages)

---

**ARKALIA ARIA** - Documentation automatique avec GitHub Pages 📚

