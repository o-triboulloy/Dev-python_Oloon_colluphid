-- Script d'installation pour ajouter les icônes au menu de 3ds Max
-- Compatible avec toutes les versions de 3ds Max (2023-2026+)
-- À exécuter une seule fois dans 3ds Max

-- MacroScript pour la version Simple (1 composant)
macroScript OpenCustomToolSimple
category:"inostudio"
buttonText:"UNIKALO RenderTool"
tooltip:"Version simple - 1 composant"
(
    local scriptPath = (getDir #userScripts + "\\menu_plugin_multi.py")
    if (doesFileExist scriptPath) then
    (
        python.executeFile scriptPath
    )
    else
    (
        messageBox ("Fichier non trouvé: " + scriptPath + "\n\nAssurez-vous que menu_plugin_multi.py est dans le dossier des scripts utilisateur.")
    )
)

-- MacroScript pour la version Multi (3 composants)
macroScript OpenCustomToolMulti
category:"inostudio"
buttonText:"UNIKALO Multi-composant"
tooltip:"Version multi-composants - A/B/C"
(
    local scriptPath = (getDir #userScripts + "\\menu_plugin_simple.py")
    if (doesFileExist scriptPath) then
    (
        python.executeFile scriptPath
    )
    else
    (
        messageBox ("Fichier non trouvé: " + scriptPath + "\n\nAssurez-vous que menu_plugin_simple.py est dans le dossier des scripts utilisateur.")
    )
)

-- Fonction pour créer automatiquement la toolbar
fn createToolbar =
(
    try
    (
        -- Créer une toolbar flottante avec un floater
        local toolbarName = "inostudio"

        -- Créer un floater personnalisé qui contient les deux boutons
        rollout unikaloToolbar "inostudio"
        (
            button btnSimple "UNIKALO RenderTool" width:150 height:30
            button btnMulti "UNIKALO Multi-composant" width:150 height:30

            on btnSimple pressed do
            (
                local scriptPath = (getDir #userScripts + "\\menu_plugin_multi.py")
                if (doesFileExist scriptPath) then
                    python.executeFile scriptPath
                else
                    messageBox "Fichier menu_plugin_multi.py introuvable" title:"Erreur"
            )

            on btnMulti pressed do
            (
                local scriptPath = (getDir #userScripts + "\\menu_plugin_simple.py")
                if (doesFileExist scriptPath) then
                    python.executeFile scriptPath
                else
                    messageBox "Fichier menu_plugin_simple.py introuvable" title:"Erreur"
            )
        )

        -- Créer le floater
        createDialog unikaloToolbar width:170 style:#(#style_toolwindow, #style_sysmenu, #style_resizing)

        print "Toolbar 'inostudio' créée avec succès!"
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
print "Deux MacroScripts ont été créés dans la catégorie 'inostudio':"
print "  - UNIKALO RenderTool (1 composant)"
print "  - UNIKALO Multi-composant (3 composants A/B/C)"
print ""

-- Tenter de créer la toolbar automatiquement
toolbarCreated = createToolbar()

if toolbarCreated then
(
    print "Une toolbar flottante 'inostudio' a été créée automatiquement!"
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
    print "  4. Dans 'Category', sélectionnez 'inostudio'"
    print "  5. Glissez 'UNIKALO RenderTool' et 'UNIKALO Multi-composant' sur la toolbar"
    print ""
    print "Méthode 2 - Assigner des raccourcis clavier :"
    print "  1. Allez dans : Customize > Customize User Interface (ou touche Y)"
    print "  2. Cliquez sur l'onglet 'Keyboard'"
    print "  3. Dans 'Category', sélectionnez 'inostudio'"
    print "  4. Assignez des raccourcis (ex: Ctrl+Shift+U et Ctrl+Shift+M)"
)

print ""
print "======================================================================"

if toolbarCreated then
    messageBox "Installation réussie!\n\nUne toolbar 'inostudio' a été créée automatiquement.\n\nElle contient 2 boutons:\n- UNIKALO RenderTool (simple)\n- UNIKALO Multi-composant\n\nVous pouvez la déplacer où vous voulez." title:"U-Rtool - Installation"
else
    messageBox "Installation réussie!\n\nDeux boutons ont été créés dans la catégorie 'inostudio':\n- UNIKALO RenderTool\n- UNIKALO Multi-composant\n\nConsultez le Listener pour les instructions d'installation manuelle." title:"U-Rtool - Installation"

