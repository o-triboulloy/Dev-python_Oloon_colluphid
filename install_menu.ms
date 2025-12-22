-- Script d'installation pour ajouter l'icône au menu de 3ds Max
-- Compatible avec toutes les versions de 3ds Max (2023-2026+)
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

-- Fonction pour créer automatiquement la toolbar
fn createToolbar =
(
    try
    (
        -- Créer une toolbar flottante avec un floater
        local toolbarName = "UNIKALO Tools"

        -- Créer un floater personnalisé qui contient le bouton
        rollout unikaloToolbar "UNIKALO Tools"
        (
            button btnUnikalo "UNIKALO RenderTool" width:150 height:30

            on btnUnikalo pressed do
            (
                -- Exécuter le macroScript
                local scriptPath = (getDir #userScripts + "\\menu_plugin.py")
                if (doesFileExist scriptPath) then
                    python.executeFile scriptPath
                else
                    messageBox "Fichier menu_plugin.py introuvable" title:"Erreur"
            )
        )

        -- Créer le floater
        createDialog unikaloToolbar width:170 style:#(#style_toolwindow, #style_sysmenu, #style_resizing)

        print "Toolbar 'UNIKALO Tools' créée avec succès!"
        return true
    )
    catch
    (
        print "Note: Création automatique de toolbar impossible, voir instructions ci-dessous"
        return false
    )
)

-- Message d'installation réussie
print "======================================================================"
print "=== INSTALLATION RÉUSSIE ==="
print "======================================================================"
print ""
print "Le MacroScript 'UNIKALO RenderTool' a été créé avec succès!"
print ""

-- Tenter de créer la toolbar automatiquement
toolbarCreated = createToolbar()

if toolbarCreated then
(
    print "Une toolbar flottante 'UNIKALO Tools' a été créée automatiquement!"
    print "Vous pouvez la déplacer où vous voulez dans l'interface."
)
else
(
    print "INSTALLATION MANUELLE REQUISE:"
    print ""
    print "Méthode 1 - Créer une toolbar personnalisée :"
    print "  1. Allez dans : Customize > Customize User Interface (ou touche Y)"
    print "  2. Cliquez sur l'onglet 'Toolbars'"
    print "  3. Cliquez sur 'New...' et nommez-la 'UNIKALO'"
    print "  4. Dans 'Category', sélectionnez 'Custom Tools'"
    print "  5. Glissez 'Ouvrir la fenêtre des outils personnalisés' sur la nouvelle toolbar"
    print ""
    print "Méthode 2 - Assigner un raccourci clavier :"
    print "  1. Allez dans : Customize > Customize User Interface (ou touche Y)"
    print "  2. Cliquez sur l'onglet 'Keyboard'"
    print "  3. Dans 'Category', sélectionnez 'Custom Tools'"
    print "  4. Assignez un raccourci (ex: Ctrl+Shift+U)"
)

print ""
print "======================================================================"

if toolbarCreated then
    messageBox "Installation réussie!\n\nUne toolbar 'UNIKALO Tools' a été créée automatiquement.\n\nVous pouvez la déplacer où vous voulez." title:"U-Rtool - Installation"
else
    messageBox "Installation réussie!\n\nLe bouton 'UNIKALO RenderTool' est disponible.\n\nConsultez le Listener pour les instructions d'installation manuelle." title:"U-Rtool - Installation"

