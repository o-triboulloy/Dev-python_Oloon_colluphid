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
        rollout CustomToolWindow "U-Rtool V1" width:206 height:637
        (
            -- Variables globales
            local sceneFolderPath = ""
            local sceneFiles = #()
            local mapFolderPath = ""
            local renderFolderPath = ""
            local contrastValue = 0
            local brightnessValue = 0
            local iniFile = getDir #userScripts + "\\\\U-Rtool_settings.ini"
            local isLoading = false  -- Flag pour éviter les conflits pendant le chargement
            local stopRendering = false  -- Flag pour arrêter les rendus en cours

            -- Image en haut (ImgTag pour éviter le liseré)
            ImgTag titleImage pos:[12,10] width:182 height:66 bitmap:(openBitMap (getDir #userScripts + "\\\\TITRE_interface.jpg"))

            -- Boutons
            button btn1 "Dossier scènes" pos:[10,86] width:186 height:30
            button btn2a "Dossier maps" pos:[10,121] width:186 height:30
            button btn2b "Dossier Rendu" pos:[10,156] width:186 height:30
            button btnReset "Reset" pos:[10,191] width:186 height:30

            -- Contrôle Color Correction
            groupBox grpColorCorrect "Color Correction" pos:[10,226] width:186 height:65
            label lblContrast "Contraste:" pos:[20,246] width:80
            spinner spnContrast "" pos:[100,246] width:76 height:16 range:[-100,100,0] type:#integer scale:5 fieldWidth:40
            label lblBrightness "Luminosité:" pos:[20,266] width:80
            spinner spnBrightness "" pos:[100,266] width:76 height:16 range:[-100,100,0] type:#integer scale:5 fieldWidth:40

            -- Options Rendus
            groupBox grpRendu "Options Rendus" pos:[10,296] width:186 height:145
            checkbox chkRenduStd "Rendus standard" pos:[20,313] width:160
            spinner spnWidthStd "Largeur:" pos:[30,328] width:145 height:16 range:[1,10000,1920] type:#integer fieldWidth:50
            spinner spnHeightStd "Hauteur:" pos:[30,343] width:145 height:16 range:[1,10000,1080] type:#integer fieldWidth:50
            checkbox chkRenduDet "Rendus détourés" pos:[20,363] width:160
            checkbox chkRenduHD "Rendu HD" pos:[20,380] width:160
            spinner spnWidthHD "Largeur:" pos:[30,395] width:145 height:16 range:[1,10000,3840] type:#integer fieldWidth:50
            spinner spnHeightHD "Hauteur:" pos:[30,410] width:145 height:16 range:[1,10000,2160] type:#integer fieldWidth:50
            checkbox chkRenduHDDet "Rendu HD détourés" pos:[20,430] width:160

            -- Menu déroulant Scènes
            label lblScenes "Scènes:" pos:[10,451] width:186
            dropdownList ddScenes "" pos:[10,466] width:186 items:#()

            -- Section Lancer les rendus
            groupBox grpLancer "" pos:[10,491] width:186 height:74
            button btnLancer "Lancer les\nrendus" pos:[20,502] width:166 height:54

            -- Section Progression
            groupBox grpProgress "Progression totale" pos:[10,575] width:186 height:54
            label lblCurrentRender "" pos:[15,590] width:176 height:14 align:#left
            progressBar pbRender "" pos:[15,604] width:176 height:16 color:orange
            label lblRenderTime "" pos:[15,620] width:176 height:14 align:#left

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
                loadedPath = getINISetting iniFile "Paths" "MapFolder"
                if loadedPath != "" then mapFolderPath = loadedPath

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

                -- Charger les résolutions
                val = getINISetting iniFile "Resolution" "WidthStd"
                if val != "" then spnWidthStd.value = val as integer else spnWidthStd.value = 1920
                val = getINISetting iniFile "Resolution" "HeightStd"
                if val != "" then spnHeightStd.value = val as integer else spnHeightStd.value = 1080
                val = getINISetting iniFile "Resolution" "WidthHD"
                if val != "" then spnWidthHD.value = val as integer else spnWidthHD.value = 3840
                val = getINISetting iniFile "Resolution" "HeightHD"
                if val != "" then spnHeightHD.value = val as integer else spnHeightHD.value = 2160

                -- Initialiser contraste et luminosité à 0 (pas de chargement depuis INI)
                contrastValue = 0
                brightnessValue = 0
                spnContrast.value = 0
                spnBrightness.value = 0

                isLoading = false
                print "=== CHARGEMENT TERMINÉ ==="
            )

            -- Événement à la fermeture
            on CustomToolWindow close do
            (
                print "Fermeture de l'interface"
            )

            -- Handler Spinner Contraste
            on spnContrast changed val do
            (
                if not isLoading then
                (
                    contrastValue = val
                    try
                    (
                        local targetMat = sceneMaterials["MAT_UNIKALO"]
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.contrast = val
                            completeRedraw()
                            print ("Contraste mis à jour: " + val as string)
                        )
                    )
                    catch()
                )
            )

            -- Handler Spinner Luminosité
            on spnBrightness changed val do
            (
                if not isLoading then
                (
                    brightnessValue = val
                    try
                    (
                        local targetMat = sceneMaterials["MAT_UNIKALO"]
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.brightness = val
                            completeRedraw()
                            print ("Luminosité mise à jour: " + val as string)
                        )
                    )
                    catch()
                )
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

            -- Bouton 2a: Choisir le dossier des maps
            on btn2a pressed do
            (
                local folderPath = getSavePath caption:"Choisir le dossier des maps" initialDir:mapFolderPath
                if folderPath != undefined then
                (
                    mapFolderPath = folderPath
                    print ("Dossier maps sélectionné: " + mapFolderPath)

                    -- Ajouter le dossier aux External File Paths pour cette session
                    try
                    (
                        pathConfig.appendSessionPath #bitmap mapFolderPath
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
                setINISetting iniFile "Paths" "MapFolder" mapFolderPath
                setINISetting iniFile "Paths" "RenderFolder" renderFolderPath

                -- Sauvegarder les options de rendu
                setINISetting iniFile "OptionsRendu" "RenduStandard" (if chkRenduStd.checked then "true" else "false")
                setINISetting iniFile "OptionsRendu" "RenduDetoure" (if chkRenduDet.checked then "true" else "false")
                setINISetting iniFile "OptionsRendu" "RenduHD" (if chkRenduHD.checked then "true" else "false")
                setINISetting iniFile "OptionsRendu" "RenduHDDetoure" (if chkRenduHDDet.checked then "true" else "false")

                -- Sauvegarder les résolutions
                setINISetting iniFile "Resolution" "WidthStd" (spnWidthStd.value as string)
                setINISetting iniFile "Resolution" "HeightStd" (spnHeightStd.value as string)
                setINISetting iniFile "Resolution" "WidthHD" (spnWidthHD.value as string)
                setINISetting iniFile "Resolution" "HeightHD" (spnHeightHD.value as string)

                print "=== Configuration sauvegardée ==="
                print "=== LANCEMENT DES RENDUS ==="

                -- Désactiver les boutons pendant l'exécution
                btnLancer.enabled = false
                btnReset.enabled = false

                -- Forcer plusieurs rafraîchissements pour être sûr que l'UI se met à jour
                for i = 1 to 5 do
                (
                    windows.processPostedMessages()
                    sleep 0.01
                )
                completeRedraw()
                print ">>> Interface mise à jour, bouton désactivé"

                -- Vérifications préalables
                if mapFolderPath == "" or renderFolderPath == "" then
                (
                    btnLancer.enabled = true
                    btnReset.enabled = true
                    messageBox "Veuillez sélectionner un dossier de maps ET un dossier de rendu avant de lancer les rendus." title:"Erreur"
                    return false
                )

                -- Vérifier qu'au moins une option est cochée
                if not chkRenduStd.checked and not chkRenduDet.checked and not chkRenduHD.checked and not chkRenduHDDet.checked then
                (
                    btnLancer.enabled = true
                    btnReset.enabled = true
                    messageBox "Veuillez cocher au moins une option de rendu." title:"Erreur"
                    return false
                )

                -- Afficher tous les matériaux de la scène pour diagnostic
                print "=== MATÉRIAUX DANS LA SCÈNE ==="
                for mat in sceneMaterials do
                (
                    print ("  - " + mat.name + " (" + (classOf mat as string) + ")")
                )

                -- Trouver le matériau MAT_UNIKALO (avec trim pour ignorer les espaces)
                local targetMat = undefined
                for mat in sceneMaterials do
                (
                    local trimmedName = trimLeft (trimRight mat.name)
                    if trimmedName == "MAT_UNIKALO" then
                    (
                        targetMat = mat
                        print ("  >> Matériau cible trouvé: '" + mat.name + "'")
                        exit
                    )
                )

                if targetMat == undefined then
                (
                    btnLancer.enabled = true
                    btnReset.enabled = true
                    local errorMsg = "Matériau 'MAT_UNIKALO' introuvable dans la scène.\n\n"
                    errorMsg += "Matériaux disponibles:\n"
                    for mat in sceneMaterials do
                        errorMsg += "  - " + mat.name + "\n"
                    messageBox errorMsg title:"Erreur"
                    return false
                )

                print ("Matériau trouvé: " + targetMat.name)
                print ("Type de matériau: " + (classOf targetMat as string))

                -- Afficher toutes les propriétés du matériau pour diagnostic
                print "=== PROPRIÉTÉS DU MATÉRIAU ==="
                showProperties targetMat

                -- Lister les maps du dossier
                local mapFiles = getFiles (mapFolderPath + "\\\\*.jpg") + getFiles (mapFolderPath + "\\\\*.png") + getFiles (mapFolderPath + "\\\\*.tga")

                if mapFiles.count == 0 then
                (
                    btnLancer.enabled = true
                    btnReset.enabled = true
                    messageBox "Aucune map trouvée dans le dossier sélectionné." title:"Erreur"
                    return false
                )

                print (mapFiles.count as string + " maps trouvées")

                -- Créer la structure de dossiers
                local mapFolderName = filterString mapFolderPath "\\\\"
                mapFolderName = mapFolderName[mapFolderName.count]

                -- Vérifier si le chemin de rendu ne se termine pas déjà par le nom du dossier maps
                local renderFolderParts = filterString renderFolderPath "\\\\"
                local lastRenderFolderName = renderFolderParts[renderFolderParts.count]

                local baseRenderPath = ""
                if lastRenderFolderName == mapFolderName then
                (
                    -- Le dossier rendu se termine déjà par le nom du dossier maps, ne pas dupliquer
                    baseRenderPath = renderFolderPath
                    print ("INFO - Utilisation directe du dossier rendu: " + baseRenderPath)
                )
                else
                (
                    -- Ajouter le nom du dossier maps au chemin de rendu
                    baseRenderPath = renderFolderPath + "\\\\" + mapFolderName
                    print ("INFO - Création sous-dossier: " + baseRenderPath)
                )

                -- Créer le dossier principal
                makeDir baseRenderPath all:true

                -- Créer les sous-dossiers selon les options cochées
                local renderJobs = #()

                if chkRenduStd.checked then
                (
                    local folderPath = baseRenderPath + "\\\\Rendus_standard"
                    makeDir folderPath all:true
                    append renderJobs #("standard", folderPath, spnWidthStd.value, spnHeightStd.value, "jpg", false)
                    print ("Dossier créé: " + folderPath + " (Résolution: " + spnWidthStd.value as string + "x" + spnHeightStd.value as string + ")")
                )

                if chkRenduDet.checked then
                (
                    local folderPath = baseRenderPath + "\\\\Rendus_detoures"
                    makeDir folderPath all:true
                    append renderJobs #("detoure", folderPath, spnWidthStd.value, spnHeightStd.value, "png", true)
                    print ("Dossier créé: " + folderPath + " (Résolution: " + spnWidthStd.value as string + "x" + spnHeightStd.value as string + ")")
                )

                if chkRenduHD.checked then
                (
                    local folderPath = baseRenderPath + "\\\\Rendus_HD"
                    makeDir folderPath all:true
                    append renderJobs #("HD", folderPath, spnWidthHD.value, spnHeightHD.value, "jpg", false)
                    print ("Dossier créé: " + folderPath + " (Résolution: " + spnWidthHD.value as string + "x" + spnHeightHD.value as string + ")")
                )

                if chkRenduHDDet.checked then
                (
                    local folderPath = baseRenderPath + "\\\\Rendus_HD_detoures"
                    makeDir folderPath all:true
                    append renderJobs #("HD_detoure", folderPath, spnWidthHD.value, spnHeightHD.value, "png", true)
                    print ("Dossier créé: " + folderPath + " (Résolution: " + spnWidthHD.value as string + "x" + spnHeightHD.value as string + ")")
                )

                -- Sauvegarder les paramètres de rendu actuels
                local originalWidth = renderWidth
                local originalHeight = renderHeight

                -- Compter le nombre total de rendus
                local totalRendus = mapFiles.count * renderJobs.count
                local renduCourant = 0

                -- Initialiser la barre de progression
                pbRender.value = 0
                lblCurrentRender.text = "Préparation..."
                lblRenderTime.text = ""

                print ("=== DÉBUT DES RENDUS (" + totalRendus as string + " rendus à effectuer) ===")

                -- Désactiver toutes les fenêtres de rendu pour batch automatique
                rendShowVFB = false  -- Désactiver le VFB 3ds Max
                try
                (
                    renderers.current.enable_render_view = false  -- Désactiver Arnold Render View
                    renderers.current.progressive_rendering = false  -- Désactiver le rendu progressif
                    print "Fenêtres de rendu désactivées (mode batch automatique)"
                )
                catch
                (
                    print "Note: Configuration Arnold appliquée avec certaines limitations"
                )

                -- Réinitialiser le flag stop au début
                stopRendering = false

                -- Sauvegarder le CHEMIN du fichier original
                local originalFile = undefined
                if targetMat.base_color_map != undefined then
                (
                    if classOf targetMat.base_color_map == Color_Correction then
                    (
                        if classOf targetMat.base_color_map.Map == Bitmaptexture then
                            originalFile = targetMat.base_color_map.Map.fileName
                    )
                    else if classOf targetMat.base_color_map == Bitmaptexture then
                        originalFile = targetMat.base_color_map.fileName
                    print (">>> Fichier original sauvegardé: " + (filenameFromPath originalFile))
                )

                -- Créer/récupérer le Color_Correction node et le Bitmaptexture UNE SEULE FOIS
                local colorCorrect = undefined
                local bitmapTex = undefined

                if classOf targetMat.base_color_map == Color_Correction then
                    colorCorrect = targetMat.base_color_map
                else
                    colorCorrect = Color_Correction()

                if classOf colorCorrect.Map == Bitmaptexture then
                    bitmapTex = colorCorrect.Map
                else
                    bitmapTex = Bitmaptexture()

                print (">>> Color_Correction et Bitmaptexture nodes préparés")

                -- Boucle sur chaque map
                for mapFile in mapFiles do
                (
                    -- Vérifier si l'arrêt a été demandé
                    if stopRendering then
                    (
                        print "\n!!! ARRÊT DES RENDUS DEMANDÉ !!!"
                        -- Restaurer la map originale (garder le Color_Correction)
                        if originalFile != undefined and targetMat != undefined then
                        (
                            try
                            (
                                if classOf targetMat.base_color_map == Color_Correction then
                                (
                                    if classOf targetMat.base_color_map.Map == Bitmaptexture then
                                        targetMat.base_color_map.Map.fileName = originalFile
                                    else
                                        targetMat.base_color_map.Map = Bitmaptexture fileName:originalFile
                                    targetMat.base_color_map.contrast = 0
                                    targetMat.base_color_map.brightness = 0
                                )
                                completeRedraw()
                                print (">>> Map originale restaurée (Color_Correction conservé)")
                            )
                            catch()
                        )
                        exit
                    )

                    -- Mettre à jour l'interface pour la rendre responsive
                    for i = 1 to 3 do windows.processPostedMessages()
                    sleep 0.01

                    local mapName = filenameFromPath mapFile
                    local mapBaseName = getFilenameFile mapFile

                    print ("\n--- Map: " + mapName + " ---")
                    print ">>> UI refresh avant chargement map"

                    -- Charger la map dans le matériau avec Color_Correction
                    try
                    (
                        -- Réutiliser le Bitmaptexture existant en changeant juste son fileName
                        bitmapTex.fileName = mapFile
                        colorCorrect.Map = bitmapTex
                        colorCorrect.contrast = contrastValue
                        colorCorrect.brightness = brightnessValue
                        targetMat.base_color_map = colorCorrect

                        print ("Map chargée avec Color_Correction: " + mapName)
                        print ("  Contraste: " + contrastValue as string + ", Luminosité: " + brightnessValue as string)

                        -- Forcer le rafraîchissement de la scène
                        completeRedraw()
                        gc()
                        windows.processPostedMessages()
                    )
                    catch
                    (
                        print ("ERREUR: Impossible de charger la map " + mapName)
                        continue
                    )

                    -- Boucle sur chaque type de rendu
                    for job in renderJobs do
                    (
                        -- Vérifier si l'arrêt a été demandé
                        if stopRendering then
                        (
                            print "  >>> Arrêt demandé, sortie de la boucle de rendus"
                            -- Restaurer la map originale (garder le Color_Correction)
                            if originalFile != undefined and targetMat != undefined then
                            (
                                try
                                (
                                    if classOf targetMat.base_color_map == Color_Correction then
                                    (
                                        if classOf targetMat.base_color_map.Map == Bitmaptexture then
                                            targetMat.base_color_map.Map.fileName = originalFile
                                        else
                                            targetMat.base_color_map.Map = Bitmaptexture fileName:originalFile
                                        targetMat.base_color_map.contrast = 0
                                        targetMat.base_color_map.brightness = 0
                                    )
                                    completeRedraw()
                                    print (">>> Map originale restaurée (Color_Correction conservé)")
                                )
                                catch()
                            )
                            exit
                        )

                        -- Mettre à jour l'interface
                        for i = 1 to 3 do windows.processPostedMessages()

                        local jobName = job[1]
                        local jobFolder = job[2]
                        local jobWidth = job[3]
                        local jobHeight = job[4]
                        local jobFormat = job[5]
                        local jobAlpha = job[6]

                        renduCourant += 1
                        print ("  [" + renduCourant as string + "/" + totalRendus as string + "] Rendu " + jobName + "...")

                        -- Mettre à jour la barre de progression et les labels
                        local progressPercent = 100.0 * renduCourant / totalRendus
                        pbRender.value = progressPercent as integer
                        lblCurrentRender.text = mapBaseName + " - " + jobName + " (" + renduCourant as string + "/" + totalRendus as string + ")"

                        -- Forcer plusieurs rafraîchissements UI avant le rendu
                        for i = 1 to 5 do
                        (
                            windows.processPostedMessages()
                            sleep 0.01
                        )
                        completeRedraw()
                        print (">>> UI actualisée: " + lblCurrentRender.text)

                        -- Configurer les paramètres de rendu
                        renderWidth = jobWidth
                        renderHeight = jobHeight

                        -- Configurer la frame selon le type de rendu
                        if jobAlpha then
                        (
                            -- Rendus détourés : frame 01 (avec matte shadow)
                            sliderTime = 1f
                            print ("    Frame: 01 (rendu détouré avec matte shadow)")
                        )
                        else
                        (
                            -- Rendus normaux : frame 00
                            sliderTime = 0f
                            print ("    Frame: 00 (rendu normal)")
                        )

                        -- Nom du fichier de sortie
                        local outputFileName = "Rendu_" + jobName + "_" + mapBaseName + "." + jobFormat
                        local outputPath = jobFolder + "\\\\" + outputFileName

                        -- Lancer le rendu (vfb:off force le rendu sans fenêtre)
                        local startTime = timestamp()
                        try
                        (
                            local renderedImage = render outputfile:outputPath vfb:off
                            local endTime = timestamp()
                            local renderDuration = (endTime - startTime) / 1000.0  -- Convertir en secondes

                            -- Vérifier si le rendu a été annulé (fichier absent ou invalide)
                            if not (doesFileExist outputPath) then
                            (
                                print "\n!!! RENDU ANNULÉ PAR L'UTILISATEUR (ESC) - Fichier absent !!!"
                                print "Arrêt de toute la série de rendus..."
                                lblCurrentRender.text = "Annulé par utilisateur"
                                renduCourant -= 1  -- Ne pas compter ce rendu annulé
                                stopRendering = true
                                exit
                            )

                            -- Calculer le seuil minimum dynamique basé sur la résolution
                            local minFileSize = (jobWidth * jobHeight) / 30  -- Seuil adaptatif selon résolution
                            local fileSize = getFileSize outputPath
                            if fileSize < minFileSize then
                            (
                                print "\n!!! RENDU ANNULÉ PAR L'UTILISATEUR (ESC) - Fichier invalide !!!"
                                print ("Taille du fichier: " + fileSize as string + " bytes (trop petit, minimum " + minFileSize as string + " pour " + jobWidth as string + "x" + jobHeight as string + ")")
                                print "Arrêt de toute la série de rendus..."
                                lblCurrentRender.text = "Annulé par utilisateur"
                                renduCourant -= 1  -- Ne pas compter ce rendu annulé
                                stopRendering = true
                                exit
                            )

                            -- Afficher le temps de rendu
                            local timeText = ""
                            if renderDuration >= 60 then
                            (
                                local minutes = (renderDuration / 60) as integer
                                local seconds = (mod renderDuration 60) as integer
                                timeText = "Dernier rendu: " + minutes as string + "m " + seconds as string + "s"
                            )
                            else
                            (
                                timeText = "Dernier rendu: " + (renderDuration as integer) as string + "s"
                            )
                            lblRenderTime.text = timeText

                            -- Rafraîchir l'UI après chaque rendu
                            for i = 1 to 3 do windows.processPostedMessages()

                            print ("    OK: " + outputFileName + " (durée: " + timeText + ", taille: " + fileSize as string + " bytes)")
                            print (">>> Rendu " + renduCourant as string + "/" + totalRendus as string + " terminé, UI rafraîchie")
                        )
                        catch
                        (
                            print ("    ERREUR lors du rendu: " + outputFileName)
                            lblRenderTime.text = "Erreur lors du rendu"
                            windows.processPostedMessages()
                        )
                    )

                    -- Libérer la mémoire de la map après tous ses rendus
                    try
                    (
                        -- Ne pas supprimer le Color_Correction, juste libérer les bitmaps en cache
                        freeSceneBitmaps()
                        gc light:true
                        windows.processPostedMessages()
                        print (">>> Mémoire bitmap libérée: " + mapBaseName)
                    )
                    catch
                    (
                        print "Note: Impossible de libérer la mémoire bitmap"
                    )
                )

                -- Restaurer la map originale du matériau (garder le Color_Correction)
                if originalFile != undefined then
                (
                    try
                    (
                        if classOf targetMat.base_color_map == Color_Correction then
                        (
                            -- Restaurer le fileName dans le Color_Correction existant
                            if classOf targetMat.base_color_map.Map == Bitmaptexture then
                                targetMat.base_color_map.Map.fileName = originalFile
                            else
                                targetMat.base_color_map.Map = Bitmaptexture fileName:originalFile
                            targetMat.base_color_map.contrast = 0
                            targetMat.base_color_map.brightness = 0
                            print (">>> Map originale restaurée (Color_Correction conservé): " + (filenameFromPath originalFile))
                        )
                        else
                        (
                            -- Pas de Color_Correction, en créer un avec la map originale
                            local newBitmapTex = Bitmaptexture fileName:originalFile
                            local newColorCorrect = Color_Correction()
                            newColorCorrect.Map = newBitmapTex
                            newColorCorrect.contrast = 0
                            newColorCorrect.brightness = 0
                            targetMat.base_color_map = newColorCorrect
                            print (">>> Map originale restaurée avec Color_Correction: " + (filenameFromPath originalFile))
                        )

                        completeRedraw()
                        windows.processPostedMessages()
                    )
                    catch
                    (
                        print "Note: Impossible de restaurer la map originale"
                    )
                )
                else
                (
                    print ">>> Aucune map à restaurer"
                )

                -- Restaurer les paramètres originaux
                renderWidth = originalWidth
                renderHeight = originalHeight
                rendShowVFB = true  -- Réactiver le VFB pour les prochains rendus manuels

                print ("\n=== RENDUS TERMINÉS ===")
                print (renduCourant as string + " rendus effectués")

                -- Mettre à jour l'affichage de progression
                if renduCourant > 0 then
                (
                    pbRender.value = 100
                    lblCurrentRender.text = "Terminé ! " + renduCourant as string + " rendus effectués"
                )
                else
                (
                    pbRender.value = 0
                    lblCurrentRender.text = "Aucun rendu effectué"
                )

                -- Réinitialiser le flag stop
                stopRendering = false

                -- Réactiver les boutons
                btnLancer.enabled = true
                btnReset.enabled = true
                for i = 1 to 5 do
                (
                    windows.processPostedMessages()
                    sleep 0.01
                )
                print ">>> Rendus terminés, interface réactivée"

                if renduCourant > 0 then
                    messageBox ("Rendus terminés !\n\n" + renduCourant as string + " rendus effectués avec succès.") title:"Succès"
                else
                    messageBox "Aucun rendu effectué." title:"Information"
            )

            -- Bouton Reset : Remettre à zéro tous les chemins et checkboxes
            on btnReset pressed do
            (
                local result = queryBox "Êtes-vous sûr de vouloir réinitialiser tous les chemins et options ?" title:"Confirmation Reset"

                if result then
                (
                    -- Réinitialiser les chemins
                    sceneFolderPath = ""
                    mapFolderPath = ""
                    renderFolderPath = ""
                    sceneFiles = #()

                    -- Vider le menu déroulant
                    ddScenes.items = #()

                    -- Décocher toutes les checkboxes
                    chkRenduStd.checked = false
                    chkRenduDet.checked = false
                    chkRenduHD.checked = false
                    chkRenduHDDet.checked = false

                    -- Réinitialiser la barre de progression
                    pbRender.value = 0
                    lblCurrentRender.text = ""
                    lblRenderTime.text = ""

                    -- Réinitialiser contraste et luminosité
                    contrastValue = 0
                    brightnessValue = 0
                    spnContrast.value = 0
                    spnBrightness.value = 0

                    -- Appliquer aux matériaux
                    try
                    (
                        local targetMat = sceneMaterials["MAT_UNIKALO"]
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.contrast = 0
                            targetMat.base_color_map.brightness = 0
                            completeRedraw()
                            print (">>> Contraste et luminosité réinitialisés dans le matériau")
                        )
                    )
                    catch()

                    -- Supprimer le fichier INI
                    try
                    (
                        deleteFile iniFile
                        print "Fichier de configuration supprimé"
                    )
                    catch
                    (
                        print "Aucun fichier de configuration à supprimer"
                    )

                    print "=== RÉINITIALISATION COMPLÈTE ==="
                    messageBox "Tous les chemins et options ont été réinitialisés." title:"Reset effectué"
                )
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
