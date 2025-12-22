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

-- Message d'installation réussie
print "======================================================================"
print "=== INSTALLATION RÉUSSIE ==="
print "======================================================================"
print ""
print "Le MacroScript 'UNIKALO RenderTool' a été créé avec succès!"
print ""
print "COMMENT L'UTILISER :"
print ""
print "Méthode 1 - Ajouter à une barre d'outils :"
print "  1. Allez dans : Customize > Customize User Interface (ou touche Y)"
print "  2. Cliquez sur l'onglet 'Toolbars'"
print "  3. Dans 'Category', sélectionnez 'Custom Tools'"
print "  4. Trouvez 'UNIKALO RenderTool' dans la liste"
print "  5. Glissez-déposez le sur votre barre d'outils principale"
print ""
print "Méthode 2 - Assigner un raccourci clavier :"
print "  1. Allez dans : Customize > Customize User Interface (ou touche Y)"
print "  2. Cliquez sur l'onglet 'Keyboard'"
print "  3. Dans 'Category', sélectionnez 'Custom Tools'"
print "  4. Trouvez 'UNIKALO RenderTool' et assignez un raccourci (ex: Ctrl+Shift+U)"
print ""
print "======================================================================"
messageBox "Installation réussie!\n\nLe bouton 'UNIKALO RenderTool' est maintenant disponible.\n\nConsultez le Listener pour savoir comment l'ajouter à votre interface." title:"U-Rtool - Installation"

