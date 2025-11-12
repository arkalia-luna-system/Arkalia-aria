# 📚 Configuration GitHub Pages pour ARKALIA ARIA

## ⚠️ URGENT - Activation Requise

**L'erreur 404 que vous voyez signifie que GitHub Pages n'est PAS encore activé.**

Pour que le déploiement automatique de la documentation fonctionne, **GitHub Pages DOIT être activé manuellement** dans les paramètres du repository. Cette action ne peut pas être faite via le code - elle doit être faite dans l'interface web de GitHub.

## 🔧 Étapes d'Activation (À FAIRE MAINTENANT)

### ⚡ Action Immédiate Requise

**Vous devez activer GitHub Pages MAINTENANT pour que le workflow fonctionne.**

### 1. Accéder aux Paramètres

1. **Ouvrir ce lien** : <https://github.com/arkalia-luna-system/Arkalia-aria/settings/pages>
2. Ou manuellement :
   - Aller sur le repository GitHub
   - Cliquer sur **"Settings"** (en haut à droite)
   - Dans le menu de gauche, cliquer sur **"Pages"**

### 2. Configurer la Source (IMPORTANT)
Dans la section **"Source"** :
- **Sélectionner** : `GitHub Actions` (dans le menu déroulant)
  - ⚠️ **NE PAS** sélectionner "Deploy from a branch"
  - ⚠️ **NE PAS** sélectionner "None"
- **Branch** : Laisser vide (géré automatiquement par GitHub Actions)
- Cliquer sur **"Save"** (bouton vert)

### 3. Vérifier l'Activation
Après avoir cliqué sur "Save" :
- ✅ Un message de confirmation devrait apparaître : "Your site is ready to be published"
- ✅ L'environment `github-pages` sera créé automatiquement
- ✅ L'URL de la documentation sera : `https://arkalia-luna-system.github.io/Arkalia-aria/`

### 4. Relancer le Workflow
Une fois GitHub Pages activé :
- Le prochain push sur `main` déclenchera automatiquement le workflow
- Ou vous pouvez relancer manuellement le workflow dans l'onglet "Actions"

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

### ❌ Erreur : "Not Found" (404) - VOUS ÊTES ICI

- **Cause** : GitHub Pages n'est **PAS activé** dans les paramètres
- **Symptôme** : `HttpError: Not Found` dans les logs du workflow
- **Solution IMMÉDIATE** :
  1. Aller sur : <https://github.com/arkalia-luna-system/Arkalia-aria/settings/pages>
  2. Sélectionner **"GitHub Actions"** dans "Source"
  3. Cliquer sur **"Save"**
  4. Attendre quelques secondes
  5. Relancer le workflow ou faire un nouveau push sur `main`
- **Vérification** : Après activation, l'erreur 404 disparaîtra

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

