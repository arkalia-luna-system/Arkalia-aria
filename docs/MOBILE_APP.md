# 📱 **ARKALIA ARIA - Application Mobile Flutter**

**Application Mobile Native pour la Gestion de Santé Personnelle**

---

## 📋 **Vue d'ensemble**

L'application mobile ARKALIA ARIA est une application Flutter native qui offre une interface intuitive et complète pour la gestion de votre santé personnelle, avec synchronisation bidirectionnelle et mode hors ligne.

### 🎯 **Objectifs**

- **Interface intuitive** : Design moderne et accessible
- **Synchronisation bidirectionnelle** : Données en temps réel
- **Mode hors ligne** : Fonctionnement sans connexion
- **Notifications intelligentes** : Rappels et alertes personnalisées
- **Rapports avancés** : Export PDF/Excel/HTML

---

## 🏗️ **Architecture**

### **Structure des Fichiers**

```
mobile_app/
├── lib/
│   ├── models/                    # Modèles de données
│   │   └── health_data.dart       # Modèle principal de données santé
│   ├── services/                  # Services métier
│   │   ├── health_connector_service.dart
│   │   ├── notification_service.dart
│   │   └── offline_cache_service.dart
│   ├── screens/                   # Écrans (vide - en développement)
│   ├── utils/                     # Utilitaires (vide - en développement)
│   ├── android/                   # Configuration Android
│   ├── ios/                       # Configuration iOS
│   └── pubspec.yaml               # Dépendances Flutter
├── android/                       # Configuration Android
├── ios/                          # Configuration iOS
└── pubspec.yaml                  # Dépendances Flutter
```

### **Diagramme d'Architecture**

```mermaid
graph TB
    subgraph "Flutter App"
        UI[Screens/UI]
        S[Services]
        M[Models]
    end
    
    subgraph "Services"
        HCS[HealthConnectorService]
        NS[NotificationService]
        OCS[OfflineCacheService]
        ES[ExportService]
    end
    
    subgraph "Backend ARIA"
    API[FastAPI Backend (/api/pain,...)]
        DB[(SQLite Database)]
    end
    
    subgraph "External"
        SH[Samsung Health]
        GF[Google Fit]
        IH[iOS Health]
    end
    
    UI --> S
    S --> M
    
    HCS --> API
    HCS --> SH
    HCS --> GF
    HCS --> IH
    
    OCS --> DB
    ES --> API
    
    API --> DB
```

---

## 📱 **Architecture de l'Application**

### **🏗️ Structure Actuelle**

L'application mobile Flutter est actuellement en phase de développement avec une architecture modulaire :

**Composants Implémentés** :
- **Modèles de données** : `HealthData` pour la gestion des données santé
- **Services métier** : Communication API, notifications, cache offline
- **Configuration** : Support Android et iOS

**Fonctionnalités Prévues** :
- Interface utilisateur complète avec écrans spécialisés
- Synchronisation bidirectionnelle avec l'API ARIA
- Mode hors ligne avec cache intelligent
- Notifications push personnalisées
- Export de rapports multiples

### **🔧 Services Disponibles**

**HealthConnectorService** :
- Communication avec l'API ARIA
- Gestion des connecteurs santé (Samsung, Google Fit, iOS Health)
- Synchronisation des données

**NotificationService** :
- Gestion des notifications push
- Configuration des rappels
- Permissions système

**OfflineCacheService** :
- Cache local des données
- Synchronisation hors ligne
- Gestion de la cohérence

---

## 🔧 **Services**

### **HealthConnectorService**

**Fichier** : `lib/services/health_connector_service.dart`

**Responsabilités** :
- Communication avec l'API ARIA
- Gestion des connecteurs santé
- Synchronisation des données
- Gestion des erreurs

**Méthodes principales** :
```dart
// Synchronisation
Future<void> syncAllConnectors()
Future<void> syncConnector(String connectorName)

// Récupération de données
Future<UnifiedHealthMetrics> getUnifiedMetrics(int daysBack)
Future<List<ActivityData>> getUnifiedActivityData(int daysBack)
Future<List<SleepData>> getUnifiedSleepData(int daysBack)
Future<List<StressData>> getUnifiedStressData(int daysBack)
Future<List<HealthData>> getUnifiedHealthData(int daysBack)

// Statut des connecteurs
Future<SyncSummary> getConnectorsStatus()
```

### **NotificationService**

**Fichier** : `lib/services/notification_service.dart`

**Responsabilités** :
- Gestion des notifications push
- Rappels de douleur
- Alertes santé
- Configuration des permissions

**Méthodes principales** :
```dart
// Permissions
Future<bool> requestPermission()
Future<bool> isPermissionGranted()

// Notifications
Future<void> showNotification(String title, String body, {String? payload})
Future<void> schedulePainReminder(int intervalHours)
Future<void> scheduleDailyReport(int hour)

// Configuration
Future<void> configureNotifications(Map<String, dynamic> settings)
```

### **OfflineCacheService**

**Fichier** : `lib/services/offline_cache_service.dart`

**Responsabilités** :
- Cache local des données
- Synchronisation hors ligne
- Gestion de la cohérence des données
- Optimisation des performances

**Méthodes principales** :
```dart
// Cache
Future<void> cacheAllData(Map<String, dynamic> data)
Future<Map<String, dynamic>> getAllCachedData()
Future<void> clearAllCache()

// Synchronisation
Future<bool> isCacheUpToDate()
Future<DateTime?> getLastSyncTimestamp()
Future<void> markCacheAsStale()
```

### **Services en Développement**

**ExportService** (prévu) :
- Génération de rapports
- Export PDF/Excel/HTML
- Partage de fichiers
- Sauvegarde locale

**Écrans Utilisateur** (prévus) :
- Dashboard principal
- Synchronisation santé
- Analyses avancées
- Paramètres
- Notifications
- Rapports

---

## 📊 **Modèles de Données**

### **HealthData**

```dart
class HealthData {
  final String id;
  final DateTime timestamp;
  final String source;
  final double? heartRate;
  final double? bloodPressure;
  final double? bloodGlucose;
  final double? bodyTemperature;
  final double? weight;
  final double? height;
  final double? bmi;
  final Map<String, dynamic>? rawData;
  
  // Constructeur et méthodes
  const HealthData({...});
  factory HealthData.fromJson(Map<String, dynamic> json);
  Map<String, dynamic> toJson();
}
```

### **Modèles en Développement**

**PainEntry** (prévu) :
- Gestion des entrées de douleur
- Intensité, déclencheurs, localisation
- Actions prises et efficacité

**AnalyticsData** (prévu) :
- Données d'analyse avancées
- Corrélations et tendances
- Métriques de performance

**SyncStatus** (prévu) :
- Statut de synchronisation
- Gestion des connecteurs
- Suivi des erreurs

---

## 🚀 **Installation et Configuration**

### **Prérequis**

- Flutter SDK 3.0+
- Dart SDK 3.0+
- Android Studio / Xcode
- Accès à l'API ARIA

### **Installation**

```bash
# Cloner le projet
git clone https://github.com/arkalia-luna-system/arkalia-aria.git
cd arkalia-aria/mobile_app

# Installer les dépendances
flutter pub get

# Configuration Android
flutter build apk --release

# Configuration iOS
flutter build ios --release
```

### **Configuration**

1. **API Backend** :
   ```dart
   // lib/config/api_config.dart
   class ApiConfig {
     static const String baseUrl = 'http://localhost:8001';
     // Endpoints ARIA Pain
     static const String painQuick = '/api/pain/quick-entry';
     static const String painEntry = '/api/pain/entry';
     static const String painEntries = '/api/pain/entries';
     static const String painRecent = '/api/pain/entries/recent';
     static const String painSuggestions = '/api/pain/suggestions';
     static const String painExportCsv = '/api/pain/export/csv';
     static const String painExportPsy = '/api/pain/export/psy-report';
   }
   ```

2. **Notifications** :
   ```yaml
   # android/app/src/main/AndroidManifest.xml
   <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"/>
   <uses-permission android:name="android.permission.VIBRATE"/>
   ```

3. **Permissions iOS** :
   ```xml
   <!-- ios/Runner/Info.plist -->
   <key>NSHealthShareUsageDescription</key>
   <string>ARKALIA ARIA accède à vos données de santé pour la synchronisation</string>
   ```

---

## 🔒 **Sécurité et Confidentialité**

### **Stockage Local**

- Données chiffrées avec SQLite
- Cache sécurisé avec SharedPreferences
- Aucune transmission non autorisée

### **Authentification**

- Tokens JWT pour l'API
- Stockage sécurisé des credentials
- Renouvellement automatique

### **Permissions**

- Contrôle granulaire des permissions
- Consentement explicite requis
- Possibilité de désactiver chaque fonctionnalité

---

## 🧪 **Tests**

### **Tests Unitaires**

```bash
# Tests des services
flutter test test/services/

# Tests des modèles
flutter test test/models/

# Tests des écrans
flutter test test/screens/
```

### **Tests d'Intégration**

```bash
# Tests d'intégration complets
flutter test integration_test/
```

### **Tests de Performance**

```bash
# Profiling des performances
flutter run --profile
```

---

## 📈 **Monitoring et Analytics**

### **Métriques de Performance**

- Temps de chargement des écrans
- Latence des API calls
- Utilisation mémoire
- Taux d'erreur

### **Analytics Utilisateur**

- Fonctionnalités les plus utilisées
- Patterns d'utilisation
- Taux de rétention
- Feedback utilisateur

---

## 🐛 **Dépannage**

### **Problèmes Courants**

1. **Synchronisation échouée** :
   - Vérifier la connectivité réseau
   - Contrôler les permissions
   - Vérifier les credentials API

2. **Notifications non reçues** :
   - Vérifier les permissions de notification
   - Contrôler la configuration système
   - Tester avec une notification de test

3. **Cache corrompu** :
   - Vider le cache dans les paramètres
   - Redémarrer l'application
   - Réinstaller si nécessaire

### **Logs et Debug**

```dart
// Activation des logs détaillés
import 'package:flutter/foundation.dart';

void main() {
  if (kDebugMode) {
    debugPrint('ARKALIA ARIA - Mode Debug');
  }
  runApp(MyApp());
}
```

---

## 🔮 **Évolutions Futures**

### **Fonctionnalités Avancées**

- **IA Intégrée** : Recommandations personnalisées
- **Reconnaissance Vocale** : Saisie vocale de douleur
- **Reality Augmentée** : Visualisation 3D des données
- **Wearables** : Support étendu des montres connectées

### **Améliorations UX**

- **Thèmes Personnalisés** : Personnalisation avancée
- **Gestures** : Navigation par gestes
- **Accessibilité** : Support complet des handicaps
- **Multilingue** : Support de nombreuses langues

---

## 📞 **Support**

- **Documentation** : `docs/MOBILE_APP.md`
- **Issues** : [GitHub Issues](https://github.com/arkalia-luna-system/arkalia-aria/issues)
- **Community** : [Discord ARKALIA](https://discord.gg/arkalia)

---

## 🚧 **Fonctionnalités Manquantes**

### **Interface Utilisateur**
- [ ] Écrans UI complets (screens/)
- [ ] Navigation entre écrans
- [ ] Thème sombre/clair
- [ ] Responsive design
- [ ] Accessibilité (a11y)
- [ ] Internationalisation (i18n)

### **Fonctionnalités Avancées**
- [ ] Notifications push (iOS/Android)
- [ ] Mode hors ligne complet
- [ ] Synchronisation bidirectionnelle
- [ ] Export PDF/Excel depuis mobile
- [ ] Graphiques interactifs
- [ ] Géolocalisation
- [ ] Biométrie (Touch ID/Face ID)

### **Tests & Qualité**
- [ ] Tests unitaires Flutter
- [ ] Tests d'intégration mobile
- [ ] Tests de performance
- [ ] Tests d'accessibilité
- [ ] Tests de compatibilité

### **Déploiement**
- [ ] Configuration App Store
- [ ] Configuration Google Play
- [ ] Certificats de signature
- [ ] Métadonnées d'application
- [ ] Screenshots et descriptions

---

> **"Votre santé dans votre poche. ARIA mobile vous accompagne partout."**
