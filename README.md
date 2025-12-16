# U-Rtool - UNIKALO RenderTool pour 3ds Max

Plugin pour 3ds Max permettant l'automatisation des rendus de textures avec Arnold, développé pour Inostudio.

## 🎯 Fonctionnalités

- **Rendu automatisé de textures** : applique automatiquement toutes les textures d'un dossier au matériau MAT_UNIKALO
- **Résolutions personnalisables** : définissez vos propres résolutions pour rendus Standard et HD
- **Multiples types de rendus** :
  - Rendus Standard (JPG)
  - Rendus Détourés (PNG avec alpha, frame 1)
  - Rendus HD (JPG haute résolution)
  - Rendus HD Détourés (PNG HD avec alpha)
- **Interface intuitive** avec progression en temps réel
- **Détection automatique ESC** pour arrêter la série de rendus
- **Organisation automatique** des dossiers de sortie
- **Sauvegarde des paramètres** dans un fichier INI

## 📋 Prérequis

- **3ds Max 2020 ou supérieur**
- **Arnold Renderer** (MAXtoA) installé et configuré
- **Python** intégré à 3ds Max (pymxs)
- **Licence 3ds Max valide** avec Arnold inclus

## 🔧 Installation

### Étape 1 : Copier les fichiers

Copiez **tous les fichiers** dans le dossier des scripts utilisateur de 3ds Max :

```
C:\Users\[VotreNom]\AppData\Local\Autodesk\3dsMax\[Version]\ENU\scripts\
```

**Fichiers à copier :**
- `menu_plugin.py` - Script principal du plugin
- `install_menu.ms` - Script d'installation du menu
- `TITRE_interface.jpg` - Image du titre de l'interface

### Étape 2 : Installer le menu dans 3ds Max

1. Ouvrez **3ds Max**
2. Menu `Scripting` → `Run Script...`
3. Sélectionnez le fichier `install_menu.ms`
4. Le menu **"Inostudio"** apparaît dans la barre de menu

✅ **Installation terminée !** Le menu est maintenant disponible.

### Étape 3 : Première utilisation

1. Cliquez sur **"Inostudio"** → **"UNIKALO RenderTool"** dans la barre de menu
2. La fenêtre U-Rtool s'ouvre
3. Configurez vos dossiers (voir section Configuration ci-dessous)

## 🚀 Configuration initiale

### 1. Configurer les dossiers

**Dossier scènes** :
- Cliquez sur `Dossier scènes`
- Sélectionnez le dossier contenant vos fichiers .max
- Le menu déroulant affiche automatiquement les scènes disponibles

**Dossier textures** :
- Cliquez sur `Dossier textures`
- Sélectionnez le dossier contenant vos textures (JPG, PNG)

**Dossier Rendu** :
- Cliquez sur `Dossier Rendu`
- Sélectionnez le dossier de base où seront créés les sous-dossiers de rendus

💡 **Note** : Ces paramètres sont sauvegardés automatiquement dans un fichier INI.

### 2. Configurer les résolutions

**Rendus Standard** :
- Définissez Largeur et Hauteur (par défaut : 1920×1080)

**Rendus HD** :
- Définissez Largeur et Hauteur (par défaut : 3840×2160)

### 3. Choisir les types de rendus

Cochez les options souhaitées :
- ☑️ **Rendus standard** - JPG à la résolution Standard
- ☑️ **Rendus détourés** - PNG avec alpha, résolution Standard
- ☑️ **Rendu HD** - JPG haute définition
- ☑️ **Rendu HD détourés** - PNG HD avec alpha

## 📖 Utilisation

### Processus de rendu automatisé

1. **Ouvrir une scène** :
   - Sélectionnez une scène dans le menu déroulant
   - Ou ouvrez-la manuellement dans Max

2. **Vérifier la scène** :
   - La scène doit contenir un matériau nommé **"MAT_UNIKALO"** (PhysicalMaterial)
   - Ce matériau doit avoir un slot de texture base_color_map

3. **Configurer les options** :
   - Choisissez vos types de rendus
   - Vérifiez les résolutions

4. **Lancer les rendus** :
   - Cliquez sur `Lancer les rendus`
   - La progression s'affiche en temps réel

### Organisation des fichiers de sortie

Les rendus sont automatiquement organisés :

```
[Dossier Rendu]/
└── [Nom du dossier textures]/
    ├── Rendus_standard/
    │   ├── Rendu_standard_texture1.jpg
    │   └── Rendu_standard_texture2.jpg
    ├── Rendus_detoures/
    │   ├── Rendu_detoure_texture1.png
    │   └── Rendu_detoure_texture2.png
    ├── Rendus_HD/
    └── Rendus_HD_detoures/
```

### Arrêter les rendus

Pour arrêter la série de rendus en cours :
- Appuyez sur **ESC** pendant le rendu
- Le plugin détecte l'annulation et arrête la série complète
- Les rendus déjà effectués sont conservés

### Bouton Reset

Le bouton `Reset` permet de :
- Réinitialiser tous les chemins de dossiers
- Décocher toutes les options de rendu
- Repartir de zéro pour une nouvelle configuration

## ⚙️ Configuration Arnold (IMPORTANT)

Pour des rendus de qualité complète, vérifiez ces paramètres Arnold :

### Paramètres essentiels

**Render Setup (F10) → Arnold Renderer :**

1. **Section Sampling** :
   - `Camera (AA)` : **3 minimum** (5 recommandé pour production)
   - `Adaptive Sampling` : peut rester activé avec threshold bas (0.015)

2. **Section Diagnostics** :
   - ⚠️ **"Abort on Error"** : **DOIT ÊTRE DÉCOCHÉ** ❌
   - ⚠️ **"Preview"** : **DOIT ÊTRE DÉCOCHÉ** ❌

### ⚠️ Problèmes courants

**Si vos rendus s'arrêtent après quelques secondes :**
1. Vérifiez que **"Abort on Error"** est décoché
2. Vérifiez que **"Preview"** est décoché
3. Vérifiez que `Camera (AA)` est positif (3-5), pas négatif

**Si vos rendus sont de mauvaise qualité :**
1. Augmentez `Camera (AA)` à 5 ou plus
2. Désactivez `Adaptive Sampling` ou réduisez le threshold
3. Vérifiez que Preview est décoché

## 🎨 Interface

L'interface U-Rtool contient :

- **Section supérieure** : Image de titre Inostudio
- **Boutons de configuration** : Accès rapide aux dossiers
- **Options Rendus** : Choix des types et résolutions
- **Menu Scènes** : Sélection rapide des fichiers .max
- **Bouton Lancer** : Démarrage des rendus
- **Progression totale** : Affichage en temps réel
  - Nombre de rendus effectués
  - Barre de progression
  - Temps du dernier rendu

## 🔍 Dépannage

### Le menu n'apparaît pas

1. Vérifiez que les fichiers sont dans le bon dossier
2. Relancez `install_menu.ms`
3. Redémarrez 3ds Max

### Erreur "Matériau MAT_UNIKALO non trouvé"

1. Vérifiez le nom exact du matériau (respect de la casse)
2. Le matériau doit être de type **PhysicalMaterial**
3. Ajoutez ou renommez un matériau dans votre scène

### Les textures ne sont pas trouvées

1. Vérifiez que le dossier contient des fichiers JPG ou PNG
2. Les fichiers ne doivent pas être dans des sous-dossiers
3. Vérifiez les permissions d'accès au dossier

### Rendus incomplets ou arrêtés

**SOLUTION :** 99% du temps, c'est **"Abort on Error"** qui est coché !
1. F10 → Arnold → Diagnostics
2. **Décochez "Abort on Error"**
3. **Décochez "Preview"**
4. Relancez les rendus

### Problème de licence Arnold

1. Vérifiez le statut : Menu `Arnold` → `About Arnold`
2. Vérifiez que la licence 3ds Max inclut Arnold
3. Contactez votre administrateur de licences flottantes

## 📝 Notes techniques

### Frames utilisées

- **Frame 0** : Rendus normaux (Standard et HD)
- **Frame 1** : Rendus détourés (avec matte shadow si configuré dans la scène)

### Format de fichiers

- **JPG** : Rendus standard et HD (qualité optimale)
- **PNG** : Rendus détourés (avec canal alpha)

### Fichier de configuration

Les paramètres sont sauvegardés dans :
```
C:\Users\[VotreNom]\AppData\Local\Autodesk\3dsMax\[Version]\ENU\scripts\U-Rtool_settings.ini
```

### Performances

Le temps de rendu dépend de :
- Résolution choisie
- Complexité de la scène
- Paramètres Arnold (Camera AA, GI samples)
- Puissance de votre machine

**Estimation** : 30-60 secondes par rendu 1920×1080 (AA=3)

## 📄 Structure du projet

```
├── menu_plugin.py           # Plugin principal
├── install_menu.ms          # Installation du menu
├── TITRE_interface.jpg      # Image du titre
├── README.md                # Ce guide
└── U-Rtool_settings.ini     # Configuration (créé automatiquement)
```

## 🆘 Support

Pour toute question ou problème :
1. Vérifiez d'abord la section **Dépannage**
2. Vérifiez les paramètres **Arnold** (Abort on Error, Preview)
3. Consultez le Listener MaxScript pour les messages d'erreur

## 🔄 Historique des versions

### Version actuelle (Stable)
- ✅ Résolutions personnalisables
- ✅ Détection ESC optimisée
- ✅ Interface UI complète avec progression
- ✅ Sauvegarde automatique des paramètres
- ✅ Organisation automatique des dossiers
- ✅ Support rendus détourés avec alpha
- ✅ Gestion frame 0/1 automatique

## 👨‍💻 Développement

Plugin développé pour **Inostudio** dans le cadre de l'automatisation des rendus de textures UNIKALO.

**Technologies utilisées :**
- Python (pymxs)
- MaxScript
- Arnold Renderer API

---

**© 2024 Inostudio - UNIKALO RenderTool**
