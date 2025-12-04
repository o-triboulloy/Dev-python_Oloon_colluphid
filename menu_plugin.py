"""
Plugin 3ds Max - Interface avec boutons
Crée une icône dans le menu qui ouvre une fenêtre avec 3 boutons
"""

try:
    from pymxs import runtime as rt
except ImportError:
    print("Ce script doit être exécuté dans 3ds Max avec pymxs installé")
    rt = None


class MenuPlugin:
    """Classe principale pour le plugin de menu 3ds Max"""

    def __init__(self):
        self.dialog = None

    def create_ui(self):
        """Crée l'interface utilisateur avec image, 3 boutons et 2 menus déroulants"""
        if rt is None:
            return

        # Création du rollout (fenêtre) avec MaxScript
        rollout_code = """
        rollout CustomToolWindow "U-Rtool" width:206 height:460
        (
            -- Variables globales
            local sceneFolderPath = ""
            local sceneFiles = #()
            local textureFolderPath = ""
            local renderFolderPath = ""
            local iniFile = getDir #userScripts + "\\\\U-Rtool_settings.ini"
            local isLoading = false  -- Flag pour éviter les conflits pendant le chargement

            -- Image en haut (ImgTag pour éviter le liseré)
            ImgTag titleImage pos:[12,10] width:182 height:66 bitmap:(openBitMap (getDir #userScripts + "\\\\TITRE_interface.jpg"))

            -- Boutons
            button btn1 "Dossier scènes" pos:[10,86] width:186 height:30
            button btn2a "Dossier textures" pos:[10,121] width:186 height:30
            button btn2b "Dossier Rendu" pos:[10,156] width:186 height:30

            -- Menu déroulant Scènes
            label lblScenes "Scènes:" pos:[10,196] width:186
            dropdownList ddScenes "" pos:[10,211] width:186 items:#()

            -- Options Rendus
            groupBox grpRendu "Options Rendus" pos:[10,256] width:186 height:95
            checkbox chkRenduStd "Rendus standard" pos:[20,273] width:160
            checkbox chkRenduDet "Rendus détourés" pos:[20,290] width:160
            checkbox chkRenduHD "Rendu HD" pos:[20,307] width:160
            checkbox chkRenduHDDet "Rendu HD détourés" pos:[20,324] width:160

            -- Section Lancer les rendus
            groupBox grpLancer "" pos:[10,366] width:186 height:80
            button btnLancer "Lancer les rendus" pos:[20,377] width:166 height:64

            -- Événement au chargement pour gérer les images et charger les paramètres
            on CustomToolWindow open do
            (
                if titleImage.bitmap == undefined then
                (
                    print "Image TITRE_interface.jpg non trouvée dans le dossier des scripts"
                )

                -- Charger les paramètres sauvegardés directement
                isLoading = true
                print "=== CHARGEMENT ==="

                -- Charger le dossier scènes et remplir le menu
                local loadedPath = getINISetting iniFile "Paths" "SceneFolder"
                if loadedPath != "" then
                (
                    sceneFolderPath = loadedPath
                    print ("Dossier scènes: " + sceneFolderPath)
                    sceneFiles = getFiles (sceneFolderPath + "\\\\*.max")
                    local sceneNames = #()
                    for sceneFile in sceneFiles do
                        append sceneNames (filenameFromPath sceneFile)
                    ddScenes.items = sceneNames
                    print ((sceneNames.count as string) + " scènes chargées")
                )

                -- Charger les autres chemins
                loadedPath = getINISetting iniFile "Paths" "TextureFolder"
                if loadedPath != "" then textureFolderPath = loadedPath

                loadedPath = getINISetting iniFile "Paths" "RenderFolder"
                if loadedPath != "" then renderFolderPath = loadedPath

                -- Charger les options de rendu
                local val = getINISetting iniFile "OptionsRendu" "RenduStandard"
                if val == "true" then chkRenduStd.checked = true
                val = getINISetting iniFile "OptionsRendu" "RenduDetoure"
                if val == "true" then chkRenduDet.checked = true
                val = getINISetting iniFile "OptionsRendu" "RenduHD"
                if val == "true" then chkRenduHD.checked = true
                val = getINISetting iniFile "OptionsRendu" "RenduHDDetoure"
                if val == "true" then chkRenduHDDet.checked = true

                isLoading = false
                print "=== CHARGEMENT TERMINÉ ==="
            )

            -- Événement à la fermeture
            on CustomToolWindow close do
            (
                print "Fermeture de l'interface"
            )

            -- Bouton 1: Choisir le dossier des scènes
            on btn1 pressed do
            (
                local folderPath = getSavePath caption:"Choisir le dossier des scènes" initialDir:sceneFolderPath
                if folderPath != undefined then
                (
                    sceneFolderPath = folderPath
                    print ("Dossier sélectionné: " + sceneFolderPath)

                    -- Lister les fichiers .max dans le dossier
                    sceneFiles = getFiles (sceneFolderPath + "\\\\*.max")

                    -- Extraire juste les noms de fichiers (sans le chemin complet)
                    local sceneNames = #()
                    for sceneFile in sceneFiles do
                    (
                        append sceneNames (filenameFromPath sceneFile)
                    )

                    -- Mettre à jour le menu déroulant
                    ddScenes.items = sceneNames

                    if sceneNames.count > 0 then
                        print (sceneNames.count as string + " scènes trouvées")
                    else
                        print "Aucune scène .max trouvée dans ce dossier"
                )
            )

            -- Bouton 2a: Choisir le dossier des textures
            on btn2a pressed do
            (
                local folderPath = getSavePath caption:"Choisir le dossier des textures" initialDir:textureFolderPath
                if folderPath != undefined then
                (
                    textureFolderPath = folderPath
                    print ("Dossier textures sélectionné: " + textureFolderPath)

                    -- Ajouter le dossier aux External File Paths pour cette session
                    try
                    (
                        pathConfig.appendSessionPath #bitmap textureFolderPath
                        print "Dossier ajouté aux External File Paths (Bitmap) pour cette session"
                    )
                    catch
                    (
                        print "Erreur lors de l'ajout du dossier aux External File Paths"
                    )
                )
            )

            -- Bouton 2b: Choisir le dossier de rendu
            on btn2b pressed do
            (
                local folderPath = getSavePath caption:"Choisir le dossier de rendu" initialDir:renderFolderPath
                if folderPath != undefined then
                (
                    renderFolderPath = folderPath
                    print ("Dossier de rendu sélectionné: " + renderFolderPath)
                )
            )

            -- Bouton: Lancer les rendus
            on btnLancer pressed do
            (
                -- Sauvegarder la configuration avant de lancer les rendus
                print "=== SAUVEGARDE ==="

                -- Sauvegarder les chemins
                setINISetting iniFile "Paths" "SceneFolder" sceneFolderPath
                setINISetting iniFile "Paths" "TextureFolder" textureFolderPath
                setINISetting iniFile "Paths" "RenderFolder" renderFolderPath

                -- Sauvegarder les options de rendu
                setINISetting iniFile "OptionsRendu" "RenduStandard" (if chkRenduStd.checked then "true" else "false")
                setINISetting iniFile "OptionsRendu" "RenduDetoure" (if chkRenduDet.checked then "true" else "false")
                setINISetting iniFile "OptionsRendu" "RenduHD" (if chkRenduHD.checked then "true" else "false")
                setINISetting iniFile "OptionsRendu" "RenduHDDetoure" (if chkRenduHDDet.checked then "true" else "false")

                print "=== Configuration sauvegardée ==="
                print "=== LANCEMENT DES RENDUS ==="

                -- Vérifications préalables
                if textureFolderPath == "" or renderFolderPath == "" then
                (
                    messageBox "Veuillez sélectionner un dossier de textures ET un dossier de rendu avant de lancer les rendus." title:"Erreur"
                    return false
                )

                -- Vérifier qu'au moins une option est cochée
                if not chkRenduStd.checked and not chkRenduDet.checked and not chkRenduHD.checked and not chkRenduHDDet.checked then
                (
                    messageBox "Veuillez cocher au moins une option de rendu." title:"Erreur"
                    return false
                )

                -- Trouver le matériau MAT_UNIKALO
                local targetMat = undefined
                for mat in sceneMaterials do
                (
                    if mat.name == "MAT_UNIKALO" then
                    (
                        targetMat = mat
                        exit
                    )
                )

                if targetMat == undefined then
                (
                    messageBox "Matériau 'MAT_UNIKALO' introuvable dans la scène." title:"Erreur"
                    return false
                )

                print ("Matériau trouvé: " + targetMat.name)
                print ("Type de matériau: " + (classOf targetMat as string))

                -- Afficher toutes les propriétés du matériau pour diagnostic
                print "=== PROPRIÉTÉS DU MATÉRIAU ==="
                showProperties targetMat

                -- Lister les textures du dossier
                local textureFiles = getFiles (textureFolderPath + "\\\\*.jpg") + getFiles (textureFolderPath + "\\\\*.png") + getFiles (textureFolderPath + "\\\\*.tga")

                if textureFiles.count == 0 then
                (
                    messageBox "Aucune texture trouvée dans le dossier sélectionné." title:"Erreur"
                    return false
                )

                print (textureFiles.count as string + " textures trouvées")

                -- Créer la structure de dossiers
                local textureFolderName = filterString textureFolderPath "\\\\"
                textureFolderName = textureFolderName[textureFolderName.count]
                local baseRenderPath = renderFolderPath + "\\\\" + textureFolderName

                -- Créer le dossier principal
                makeDir baseRenderPath all:true

                -- Créer les sous-dossiers selon les options cochées
                local renderJobs = #()

                if chkRenduStd.checked then
                (
                    local folderPath = baseRenderPath + "\\\\Rendus_standard"
                    makeDir folderPath all:true
                    append renderJobs #("standard", folderPath, 1200, 1200, "jpg", false)
                    print ("Dossier créé: " + folderPath)
                )

                if chkRenduDet.checked then
                (
                    local folderPath = baseRenderPath + "\\\\Rendus_detoures"
                    makeDir folderPath all:true
                    append renderJobs #("detoure", folderPath, 1200, 1200, "png", true)
                    print ("Dossier créé: " + folderPath)
                )

                if chkRenduHD.checked then
                (
                    local folderPath = baseRenderPath + "\\\\Rendus_HD"
                    makeDir folderPath all:true
                    append renderJobs #("HD", folderPath, 10000, 10000, "jpg", false)
                    print ("Dossier créé: " + folderPath)
                )

                if chkRenduHDDet.checked then
                (
                    local folderPath = baseRenderPath + "\\\\Rendus_HD_detoures"
                    makeDir folderPath all:true
                    append renderJobs #("HD_detoure", folderPath, 10000, 10000, "png", true)
                    print ("Dossier créé: " + folderPath)
                )

                -- Sauvegarder les paramètres de rendu actuels
                local originalWidth = renderWidth
                local originalHeight = renderHeight

                -- Compter le nombre total de rendus
                local totalRendus = textureFiles.count * renderJobs.count
                local renduCourant = 0

                print ("=== DÉBUT DES RENDUS (" + totalRendus as string + " rendus à effectuer) ===")

                -- Boucle sur chaque texture
                for textureFile in textureFiles do
                (
                    local textureName = filenameFromPath textureFile
                    local textureBaseName = getFilenameFile textureFile

                    print ("\n--- Texture: " + textureName + " ---")

                    -- Charger la texture dans le matériau Arnold
                    try
                    (
                        local newBitmap = Bitmaptexture fileName:textureFile

                        -- Assigner à base_color_shader (Arnold Standard Surface)
                        targetMat.base_color_shader = newBitmap
                        print ("Texture assignée: " + textureName)
                    )
                    catch
                    (
                        print ("ERREUR: Impossible de charger ou assigner la texture " + textureName)
                        continue
                    )

                    -- Boucle sur chaque type de rendu
                    for job in renderJobs do
                    (
                        local jobName = job[1]
                        local jobFolder = job[2]
                        local jobWidth = job[3]
                        local jobHeight = job[4]
                        local jobFormat = job[5]
                        local jobAlpha = job[6]

                        renduCourant += 1
                        print ("  [" + renduCourant as string + "/" + totalRendus as string + "] Rendu " + jobName + "...")

                        -- Configurer les paramètres de rendu
                        renderWidth = jobWidth
                        renderHeight = jobHeight

                        -- Configurer Arnold pour l'alpha si nécessaire
                        if jobAlpha then
                        (
                            -- Activer l'alpha dans Arnold
                            try
                            (
                                renderers.current.beauty_aov_exr_enable_rgba = true
                                print ("    Alpha activé pour rendu détouré")
                            )
                            catch
                            (
                                print ("    ATTENTION: Impossible d'activer l'alpha (vérifier que Arnold est le renderer actif)")
                            )
                        )

                        -- Nom du fichier de sortie
                        local outputFileName = "Rendu_" + jobName + "_" + textureBaseName + "." + jobFormat
                        local outputPath = jobFolder + "\\\\" + outputFileName

                        -- Lancer le rendu
                        try
                        (
                            local renderedImage = render outputfile:outputPath
                            print ("    OK: " + outputFileName)
                        )
                        catch
                        (
                            print ("    ERREUR lors du rendu: " + outputFileName)
                        )
                    )
                )

                -- Restaurer les paramètres originaux
                renderWidth = originalWidth
                renderHeight = originalHeight

                print ("\n=== RENDUS TERMINÉS ===")
                print (renduCourant as string + " rendus effectués")
                messageBox ("Rendus terminés !\n\n" + renduCourant as string + " rendus effectués avec succès.") title:"Succès"
            )

            -- Événement menu déroulant Scènes
            on ddScenes selected sel do
            (
                if sceneFiles.count > 0 and sel > 0 and sel <= sceneFiles.count then
                (
                    local sceneToLoad = sceneFiles[sel]
                    print ("Tentative de chargement: " + sceneToLoad)

                    -- Demander confirmation avant de charger
                    local confirmLoad = yesNoCancelBox ("Charger la scène:\n" + (filenameFromPath sceneToLoad) + "\n\nVoulez-vous sauvegarder la scène actuelle ?") title:"Charger scène"

                    if confirmLoad == #yes then
                    (
                        print "Sauvegarde puis chargement..."
                        -- Sauvegarder puis charger
                        if maxFileName != "" then
                            saveMaxFile (maxFilePath + maxFileName)
                        loadMaxFile sceneToLoad
                        print ("Scène chargée: " + sceneToLoad)
                    )
                    else if confirmLoad == #no then
                    (
                        print "Chargement sans sauvegarde..."
                        -- Charger sans sauvegarder
                        loadMaxFile sceneToLoad
                        print ("Scène chargée: " + sceneToLoad)
                    )
                    else
                    (
                        print "Chargement annulé"
                    )
                )
            )

        )
        """

        # Exécuter le code MaxScript pour créer le rollout
        rt.execute(rollout_code)

        # Créer et afficher le dialog
        self.dialog = rt.createDialog(rt.CustomToolWindow)

    def show_window(self):
        """Affiche la fenêtre de l'interface"""
        if self.dialog is None:
            self.create_ui()
        else:
            # Si le dialog existe déjà, le ramener au premier plan
            try:
                rt.createDialog(rt.CustomToolWindow)
            except:
                self.create_ui()


def open_tool_window():
    """Fonction appelée par l'icône du menu"""
    plugin = MenuPlugin()
    plugin.show_window()


# Si exécuté directement, ouvrir la fenêtre
if __name__ == "__main__":
    open_tool_window()
