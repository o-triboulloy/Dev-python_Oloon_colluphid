-- Script d'installation pour ajouter l'icône au menu de 3ds Max
-- À exécuter une seule fois dans 3ds Max

macroScript OpenCustomTool
category:"Custom Tools"
buttonText:"Mes Outils"
tooltip:"Ouvrir la fenêtre des outils personnalisés"
(
    -- Chemin vers le script Python
    -- IMPORTANT: Modifier ce chemin selon l'emplacement de votre fichier
    local scriptPath = (getDir #userScripts + "\\menu_plugin.py")

    -- Vérifier si le fichier existe
    if (doesFileExist scriptPath) then
    (
        python.executeFile scriptPath
    )
    else
    (
        messageBox ("Fichier non trouvé: " + scriptPath + "\n\nAssurez-vous que menu_plugin.py est dans le dossier des scripts utilisateur.")
    )
)

-- Ajouter le menu à la barre de menu principale
fn addCustomMenu =
(
    local mainMenuBar = menuMan.getMainMenuBar()
    local customMenu = menuMan.createMenu "Outils Perso"

    local customAction = menuMan.createActionItem "OpenCustomTool" "Custom Tools"
    customMenu.addItem customAction 0

    local customSubMenu = menuMan.createSubMenuItem "Outils Perso" customMenu
    mainMenuBar.addItem customSubMenu -1

    menuMan.updateMenuBar()

    print "Menu 'Outils Perso' ajouté avec succès!"
)

-- Exécuter l'installation
addCustomMenu()
