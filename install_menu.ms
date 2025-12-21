-- Script d'installation pour ajouter l'icône au menu de 3ds Max
-- À exécuter une seule fois dans 3ds Max

macroScript OpenCustomTool
category:"Custom Tools"
buttonText:"UNIKALO RenderTool"
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
    global menuMan  -- Déclarer menuMan comme global

    -- Compatibilité multi-versions (2023, 2024, 2025, 2026+)
    local mainMenuBar = undefined
    try
    (
        -- Essayer la nouvelle API (2024+)
        mainMenuBar = menuMan.mainMenuBar
    )
    catch
    (
        -- Utiliser l'ancienne API (2023 et antérieurs)
        mainMenuBar = menuMan.getMainMenuBar()
    )

    local customMenu = menuMan.createMenu "Inostudio"

    local customAction = menuMan.createActionItem "OpenCustomTool" "Custom Tools"
    customMenu.addItem customAction 0

    local customSubMenu = menuMan.createSubMenuItem "Inostudio" customMenu
    mainMenuBar.addItem customSubMenu -1

    menuMan.updateMenuBar()

    print "Menu 'Inostudio' ajouté avec succès!"
)

-- Exécuter l'installation
addCustomMenu()
