# Plugin Menu 3ds Max

Plugin simple pour 3ds Max qui ajoute une icône dans la barre de menu pour ouvrir une fenêtre d'outils personnalisés.

## Fonctionnalités

- Icône dans la barre de menu de 3ds Max
- Fenêtre de 100x250 pixels
- 3 boutons personnalisables (vides pour le moment)

## Prérequis

- 3ds Max (version 2020 ou supérieure recommandée)
- Python installé dans 3ds Max (pymxs)

## Installation

### Étape 1 : Copier les fichiers

Copiez le fichier `menu_plugin.py` dans le dossier des scripts utilisateur de 3ds Max :

```
C:\Users\[VotreNom]\AppData\Local\Autodesk\3dsMax\[Version]\ENU\scripts\
```

Ou utilisez le dossier des scripts personnalisés de votre choix.

### Étape 2 : Installer le menu

1. Ouvrez 3ds Max
2. Ouvrez l'éditeur de scripts MaxScript (F11)
3. Ouvrez le fichier `install_menu.ms`
4. **Important** : Modifiez le chemin `scriptPath` dans le fichier pour pointer vers l'emplacement de votre fichier `menu_plugin.py`
5. Exécutez le script (Ctrl+E ou bouton "Evaluate All")

### Étape 3 : Utilisation

Après l'installation, vous verrez un nouveau menu "Outils Perso" dans la barre de menu de 3ds Max. Cliquez dessus pour ouvrir la fenêtre avec les 3 boutons.

## Structure des fichiers

```
├── menu_plugin.py      # Script Python principal avec l'interface UI
├── install_menu.ms     # Script MaxScript d'installation du menu
└── README.md          # Ce fichier
```

## Personnalisation

### Modifier les boutons

Éditez le fichier `menu_plugin.py` dans la section `rollout_code` pour :

- Changer les labels des boutons
- Modifier les positions et tailles
- Ajouter la logique des événements dans les sections `on btnX pressed do`

### Modifier la taille de la fenêtre

Dans `menu_plugin.py`, ligne avec `rollout CustomToolWindow`, modifiez les valeurs `width` et `height`.

## Notes

- Les boutons affichent actuellement un message dans le listener MaxScript quand on clique dessus
- Vous pouvez ajouter votre propre logique dans les événements des boutons

## Licence

À définir
