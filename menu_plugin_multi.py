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
        rollout CustomToolWindow "U-Rtool Multi" width:206 height:855
        (
            -- Variables globales
            local sceneFolderPath = ""
            local sceneFiles = #()
            local mapFolderPath = ""
            local mapFolderPathB = ""
            local mapFolderPathC = ""
            local renderFolderPath = ""
            local contrastValueA = 0
            local contrastValueB = 0
            local contrastValueC = 0
            local brightnessValueA = 0
            local brightnessValueB = 0
            local brightnessValueC = 0
            local iniFile = getDir #userScripts + "\\\\U-Rtool_settings.ini"
            local isLoading = false  -- Flag pour éviter les conflits pendant le chargement
            local stopRendering = false  -- Flag pour arrêter les rendus en cours

            -- Fonction générique pour trouver un matériau par nom (dans sceneMaterials ou multi-matériaux)
            fn findMaterialByName matName =
            (
                local foundMat = undefined

                -- Chercher dans sceneMaterials directement
                for mat in sceneMaterials do
                (
                    local trimmedName = trimLeft (trimRight mat.name)
                    if trimmedName == matName then
                    (
                        foundMat = mat
                        exit
                    )
                )

                -- Si pas trouvé, chercher dans les sous-matériaux des multi-matériaux
                if foundMat == undefined then
                (
                    for mat in sceneMaterials do
                    (
                        if classOf mat == multimaterial then
                        (
                            for subMat in mat.materialList do
                            (
                                if subMat != undefined then
                                (
                                    local trimmedName = trimLeft (trimRight subMat.name)
                                    if trimmedName == matName then
                                    (
                                        foundMat = subMat
                                        exit
                                    )
                                )
                            )
                            if foundMat != undefined then exit
                        )
                    )
                )

                return foundMat
            )

            -- Image en haut (ImgTag pour éviter le liseré)
            ImgTag titleImage pos:[12,10] width:182 height:66 bitmap:(openBitMap (getDir #userScripts + "\\\\TITRE_interface_Multi.jpg"))

            -- Boutons
            button btn1 "Dossier scènes" pos:[10,86] width:186 height:30
            button btn2b "Dossier Rendu" pos:[10,121] width:186 height:30
            button btnReset "Reset" pos:[10,156] width:186 height:30

            -- Composant A
            groupBox grpComponentA "COMPOSANT A" pos:[10,196] width:186 height:95
            button btn2a "Dossier maps A" pos:[20,211] width:166 height:30
            label lblContrastA "Contraste A:" pos:[20,246] width:80
            spinner spnContrastA "" pos:[100,246] width:76 height:16 range:[-100,100,0] type:#integer scale:5 fieldWidth:40
            label lblBrightnessA "Luminosité A:" pos:[20,266] width:80
            spinner spnBrightnessA "" pos:[100,266] width:76 height:16 range:[-100,100,0] type:#integer scale:5 fieldWidth:40

            -- Composant B
            groupBox grpComponentB "COMPOSANT B" pos:[10,301] width:186 height:95
            button btn2aB "Dossier maps B" pos:[20,316] width:166 height:30
            label lblContrastB "Contraste B:" pos:[20,351] width:80
            spinner spnContrastB "" pos:[100,351] width:76 height:16 range:[-100,100,0] type:#integer scale:5 fieldWidth:40
            label lblBrightnessB "Luminosité B:" pos:[20,371] width:80
            spinner spnBrightnessB "" pos:[100,371] width:76 height:16 range:[-100,100,0] type:#integer scale:5 fieldWidth:40

            -- Composant C
            groupBox grpComponentC "COMPOSANT C" pos:[10,406] width:186 height:95
            button btn2aC "Dossier maps C" pos:[20,421] width:166 height:30
            label lblContrastC "Contraste C:" pos:[20,456] width:80
            spinner spnContrastC "" pos:[100,456] width:76 height:16 range:[-100,100,0] type:#integer scale:5 fieldWidth:40
            label lblBrightnessC "Luminosité C:" pos:[20,476] width:80
            spinner spnBrightnessC "" pos:[100,476] width:76 height:16 range:[-100,100,0] type:#integer scale:5 fieldWidth:40

            -- Options Rendus
            groupBox grpRendu "Options Rendus" pos:[10,511] width:186 height:145
            checkbox chkRenduStd "Rendus standard" pos:[20,528] width:160
            spinner spnWidthStd "Largeur:" pos:[30,543] width:145 height:16 range:[1,10000,1920] type:#integer fieldWidth:50
            spinner spnHeightStd "Hauteur:" pos:[30,558] width:145 height:16 range:[1,10000,1080] type:#integer fieldWidth:50
            checkbox chkRenduDet "Rendus détourés" pos:[20,578] width:160
            checkbox chkRenduHD "Rendu HD" pos:[20,595] width:160
            spinner spnWidthHD "Largeur:" pos:[30,610] width:145 height:16 range:[1,10000,3840] type:#integer fieldWidth:50
            spinner spnHeightHD "Hauteur:" pos:[30,625] width:145 height:16 range:[1,10000,2160] type:#integer fieldWidth:50
            checkbox chkRenduHDDet "Rendu HD détourés" pos:[20,645] width:160

            -- Menu déroulant Scènes
            label lblScenes "Scènes:" pos:[10,666] width:186
            dropdownList ddScenes "" pos:[10,681] width:186 items:#()

            -- Section Lancer les rendus
            groupBox grpLancer "" pos:[10,706] width:186 height:74
            button btnLancer "Lancer les\nrendus" pos:[20,717] width:166 height:54

            -- Section Progression
            groupBox grpProgress "Progression totale" pos:[10,790] width:186 height:54
            label lblCurrentRender "" pos:[15,805] width:176 height:14 align:#left
            progressBar pbRender "" pos:[15,819] width:176 height:16 color:orange
            label lblRenderTime "" pos:[15,835] width:176 height:14 align:#left

            -- Événement au chargement pour gérer les images et charger les paramètres
            on CustomToolWindow open do
            (
                if titleImage.bitmap == undefined then
                (
                    print "Image TITRE_interface_Multi.jpg non trouvée dans le dossier des scripts"
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

                loadedPath = getINISetting iniFile "Paths" "MapFolderB"
                if loadedPath != "" then mapFolderPathB = loadedPath

                loadedPath = getINISetting iniFile "Paths" "MapFolderC"
                if loadedPath != "" then mapFolderPathC = loadedPath

                loadedPath = getINISetting iniFile "Paths" "RenderFolder"
                if loadedPath != "" then renderFolderPath = loadedPath

                -- Les valeurs de contraste et luminosité sont toujours initialisées à 0
                -- (pas de chargement depuis INI)

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

                -- Appliquer les valeurs de contraste et luminosité aux Color_Correction nodes (toujours 0)
                try
                (
                    -- Composant A
                    local targetMatA = findMaterialByName "MAT_UNIKALO"
                    if targetMatA != undefined and classOf targetMatA.base_color_map == Color_Correction then
                    (
                        targetMatA.base_color_map.contrast = contrastValueA
                        targetMatA.base_color_map.brightness = brightnessValueA
                        print ("Contraste et luminosité A initialisés à 0")
                    )

                    -- Composant B
                    local targetMatB = findMaterialByName "MAT_UNIKALO_B"
                    if targetMatB != undefined and classOf targetMatB.base_color_map == Color_Correction then
                    (
                        targetMatB.base_color_map.contrast = contrastValueB
                        targetMatB.base_color_map.brightness = brightnessValueB
                        print ("Contraste et luminosité B initialisés à 0")
                    )

                    -- Composant C
                    local targetMatC = findMaterialByName "MAT_UNIKALO_C"
                    if targetMatC != undefined and classOf targetMatC.base_color_map == Color_Correction then
                    (
                        targetMatC.base_color_map.contrast = contrastValueC
                        targetMatC.base_color_map.brightness = brightnessValueC
                        print ("Contraste et luminosité C initialisés à 0")
                    )
                )
                catch()

                isLoading = false
                print "=== CHARGEMENT TERMINÉ ==="
            )

            -- Événement à la fermeture
            on CustomToolWindow close do
            (
                -- Sauvegarder tous les paramètres à la fermeture
                print "=== SAUVEGARDE À LA FERMETURE ==="

                -- Sauvegarder les chemins
                setINISetting iniFile "Paths" "SceneFolder" sceneFolderPath
                setINISetting iniFile "Paths" "MapFolder" mapFolderPath
                setINISetting iniFile "Paths" "MapFolderB" mapFolderPathB
                setINISetting iniFile "Paths" "MapFolderC" mapFolderPathC
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

                print "Paramètres sauvegardés"
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

            -- Bouton 2a: Choisir le dossier des maps A
            on btn2a pressed do
            (
                local folderPath = getSavePath caption:"Choisir le dossier des maps A" initialDir:mapFolderPath
                if folderPath != undefined then
                (
                    mapFolderPath = folderPath
                    print ("Dossier maps A sélectionné: " + mapFolderPath)

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

            -- Spinner Contraste A
            on spnContrastA changed val do
            (
                if not isLoading then
                (
                    contrastValueA = val
                    
                    try
                    (
                        local targetMat = findMaterialByName "MAT_UNIKALO"
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.contrast = val
                            completeRedraw()
                            print ("Contraste A mis à jour: " + val as string)
                        )
                    )
                    catch()
                )
            )
            
            -- Spinner Luminosité A
            on spnBrightnessA changed val do
            (
                if not isLoading then
                (
                    brightnessValueA = val
                    
                    try
                    (
                        local targetMat = findMaterialByName "MAT_UNIKALO"
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.brightness = val
                            completeRedraw()
                            print ("Luminosité A mise à jour: " + val as string)
                        )
                    )
                    catch()
                )
            )


            -- Bouton 2aB: Choisir le dossier des maps B
            on btn2aB pressed do
            (
                local folderPath = getSavePath caption:"Choisir le dossier des maps B" initialDir:mapFolderPathB
                if folderPath != undefined then
                (
                    mapFolderPathB = folderPath
                    print ("Dossier maps B sélectionné: " + mapFolderPathB)

                    -- Ajouter le dossier aux External File Paths pour cette session
                    try
                    (
                        pathConfig.appendSessionPath #bitmap mapFolderPathB
                        print "Dossier ajouté aux External File Paths (Bitmap) pour cette session"
                    )
                    catch
                    (
                        print "Erreur lors de l'ajout du dossier aux External File Paths"
                    )
                )
            )

            -- Spinner Contraste B
            on spnContrastB changed val do
            (
                if not isLoading then
                (
                    contrastValueB = val

                    -- Mettre à jour le Color_Correction en temps réel
                    try
                    (
                        local targetMat = findMaterialByName "MAT_UNIKALO_B"
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.contrast = val
                            completeRedraw()
                            print ("Contraste B mis à jour: " + val as string)
                        )
                    )
                    catch()
                )
            )
            
            -- Spinner Luminosité B
            on spnBrightnessB changed val do
            (
                if not isLoading then
                (
                    brightnessValueB = val
                    
                    try
                    (
                        local targetMat = findMaterialByName "MAT_UNIKALO_B"
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.brightness = val
                            completeRedraw()
                            print ("Luminosité B mise à jour: " + val as string)
                        )
                    )
                    catch()
                )
            )

            -- Bouton 2aC: Choisir le dossier des maps C
            on btn2aC pressed do
            (
                local folderPath = getSavePath caption:"Choisir le dossier des maps C" initialDir:mapFolderPathC
                if folderPath != undefined then
                (
                    mapFolderPathC = folderPath
                    print ("Dossier maps C sélectionné: " + mapFolderPathC)

                    -- Ajouter le dossier aux External File Paths pour cette session
                    try
                    (
                        pathConfig.appendSessionPath #bitmap mapFolderPathC
                        print "Dossier ajouté aux External File Paths (Bitmap) pour cette session"
                    )
                    catch
                    (
                        print "Erreur lors de l'ajout du dossier aux External File Paths"
                    )
                )
            )

            -- Spinner Contraste C
            on spnContrastC changed val do
            (
                if not isLoading then
                (
                    contrastValueC = val

                    -- Mettre à jour le Color_Correction en temps réel
                    try
                    (
                        local targetMat = findMaterialByName "MAT_UNIKALO_C"
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.contrast = val
                            completeRedraw()
                            print ("Contraste C mis à jour: " + val as string)
                        )
                    )
                    catch()
                )
            )
            
            -- Spinner Luminosité C
            on spnBrightnessC changed val do
            (
                if not isLoading then
                (
                    brightnessValueC = val
                    
                    try
                    (
                        local targetMat = findMaterialByName "MAT_UNIKALO_C"
                        if targetMat != undefined and classOf targetMat.base_color_map == Color_Correction then
                        (
                            targetMat.base_color_map.brightness = val
                            completeRedraw()
                            print ("Luminosité C mise à jour: " + val as string)
                        )
                    )
                    catch()
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
                setINISetting iniFile "Paths" "MapFolderB" mapFolderPathB
                setINISetting iniFile "Paths" "MapFolderC" mapFolderPathC
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

                -- Trouver les 3 matériaux avec la fonction générique
                local targetMatA = findMaterialByName "MAT_UNIKALO"
                local targetMatB = findMaterialByName "MAT_UNIKALO_B"
                local targetMatC = findMaterialByName "MAT_UNIKALO_C"

                if targetMatA == undefined then
                (
                    btnLancer.enabled = true
                    btnReset.enabled = true
                    messageBox "Matériau 'MAT_UNIKALO' (composant A) introuvable." title:"Erreur"
                    return false
                )

                print ("Matériau A trouvé: " + targetMatA.name)
                if targetMatB != undefined then print ("Matériau B trouvé: " + targetMatB.name)
                if targetMatC != undefined then print ("Matériau C trouvé: " + targetMatC.name)

                -- Sauvegarder les chemins des fichiers originaux (pas les objets)
                local originalFileA = undefined
                local originalFileB = undefined
                local originalFileC = undefined

                if targetMatA != undefined then
                (
                    if classOf targetMatA.base_color_map == Color_Correction then
                    (
                        if classOf targetMatA.base_color_map.Map == Bitmaptexture then
                            originalFileA = targetMatA.base_color_map.Map.fileName
                    )
                    else if classOf targetMatA.base_color_map == Bitmaptexture then
                        originalFileA = targetMatA.base_color_map.fileName
                )

                if targetMatB != undefined then
                (
                    if classOf targetMatB.base_color_map == Color_Correction then
                    (
                        if classOf targetMatB.base_color_map.Map == Bitmaptexture then
                            originalFileB = targetMatB.base_color_map.Map.fileName
                    )
                    else if classOf targetMatB.base_color_map == Bitmaptexture then
                        originalFileB = targetMatB.base_color_map.fileName
                )

                if targetMatC != undefined then
                (
                    if classOf targetMatC.base_color_map == Color_Correction then
                    (
                        if classOf targetMatC.base_color_map.Map == Bitmaptexture then
                            originalFileC = targetMatC.base_color_map.Map.fileName
                    )
                    else if classOf targetMatC.base_color_map == Bitmaptexture then
                        originalFileC = targetMatC.base_color_map.fileName
                )

                print (">>> Fichiers originaux sauvegardés:")

                -- Fonction pour restaurer les maps originales à partir des chemins de fichiers
                fn restoreOriginalMaps matA matB matC origFileA origFileB origFileC =
                (
                    try
                    (
                        if matA != undefined and origFileA != undefined then
                        (
                            if classOf matA.base_color_map == Color_Correction then
                            (
                                -- Réutiliser le Bitmaptexture existant si possible
                                if classOf matA.base_color_map.Map == Bitmaptexture then
                                    matA.base_color_map.Map.fileName = origFileA
                                else
                                    matA.base_color_map.Map = Bitmaptexture fileName:origFileA
                                matA.base_color_map.contrast = 0
                                matA.base_color_map.brightness = 0
                            )
                            else
                                matA.base_color_map = Bitmaptexture fileName:origFileA
                            print (">>> Map originale A restaurée: " + (filenameFromPath origFileA))
                        )
                        if matB != undefined and origFileB != undefined then
                        (
                            if classOf matB.base_color_map == Color_Correction then
                            (
                                -- Réutiliser le Bitmaptexture existant si possible
                                if classOf matB.base_color_map.Map == Bitmaptexture then
                                    matB.base_color_map.Map.fileName = origFileB
                                else
                                    matB.base_color_map.Map = Bitmaptexture fileName:origFileB
                                matB.base_color_map.contrast = 0
                                matB.base_color_map.brightness = 0
                            )
                            else
                                matB.base_color_map = Bitmaptexture fileName:origFileB
                            print (">>> Map originale B restaurée: " + (filenameFromPath origFileB))
                        )
                        if matC != undefined and origFileC != undefined then
                        (
                            if classOf matC.base_color_map == Color_Correction then
                            (
                                -- Réutiliser le Bitmaptexture existant si possible
                                if classOf matC.base_color_map.Map == Bitmaptexture then
                                    matC.base_color_map.Map.fileName = origFileC
                                else
                                    matC.base_color_map.Map = Bitmaptexture fileName:origFileC
                                matC.base_color_map.contrast = 0
                                matC.base_color_map.brightness = 0
                            )
                            else
                                matC.base_color_map = Bitmaptexture fileName:origFileC
                            print (">>> Map originale C restaurée: " + (filenameFromPath origFileC))
                        )
                        completeRedraw()
                        windows.processPostedMessages()
                    )
                    catch
                    (
                        print "Note: Impossible de restaurer toutes les maps originales"
                    )
                )

                -- Lister les maps des 3 dossiers
                local mapFilesA = getFiles (mapFolderPath + "\\\\*.jpg") + getFiles (mapFolderPath + "\\\\*.png") + getFiles (mapFolderPath + "\\\\*.tga")
                local mapFilesB = #()
                local mapFilesC = #()

                if mapFolderPathB != "" then
                    mapFilesB = getFiles (mapFolderPathB + "\\\\*.jpg") + getFiles (mapFolderPathB + "\\\\*.png") + getFiles (mapFolderPathB + "\\\\*.tga")
                if mapFolderPathC != "" then
                    mapFilesC = getFiles (mapFolderPathC + "\\\\*.jpg") + getFiles (mapFolderPathC + "\\\\*.png") + getFiles (mapFolderPathC + "\\\\*.tga")

                if mapFilesA.count == 0 then
                (
                    btnLancer.enabled = true
                    btnReset.enabled = true
                    messageBox "Aucune map trouvée dans le dossier A." title:"Erreur"
                    return false
                )

                -- Trier les listes par ordre alphabétique
                sort mapFilesA
                if mapFilesB.count > 0 then sort mapFilesB
                if mapFilesC.count > 0 then sort mapFilesC

                print (mapFilesA.count as string + " maps dans dossier A")
                if mapFilesB.count > 0 then print (mapFilesB.count as string + " maps dans dossier B")
                if mapFilesC.count > 0 then print (mapFilesC.count as string + " maps dans dossier C")

                -- Déterminer le nombre maximum de maps
                local maxMaps = mapFilesA.count
                if mapFilesB.count > maxMaps then maxMaps = mapFilesB.count
                if mapFilesC.count > maxMaps then maxMaps = mapFilesC.count


                -- Créer la structure de dossiers (basée sur le nom du dossier A)
                local mapFolderName = filterString mapFolderPath "\\\\"
                mapFolderName = mapFolderName[mapFolderName.count]

                local renderFolderParts = filterString renderFolderPath "\\\\"
                local lastRenderFolderName = renderFolderParts[renderFolderParts.count]

                local baseRenderPath = ""
                if lastRenderFolderName == mapFolderName then
                (
                    baseRenderPath = renderFolderPath
                    print ("INFO - Utilisation directe du dossier rendu: " + baseRenderPath)
                )
                else
                (
                    baseRenderPath = renderFolderPath + "\\\\" + mapFolderName
                    print ("INFO - Création sous-dossier: " + baseRenderPath)
                )

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

                -- Sauvegarder les paramètres de rendu
                local originalWidth = renderWidth
                local originalHeight = renderHeight

                -- Compter le nombre total de rendus
                local totalRendus = maxMaps * renderJobs.count
                local renduCourant = 0

                -- Initialiser la barre de progression
                pbRender.value = 0
                lblCurrentRender.text = "Préparation..."
                lblRenderTime.text = ""

                print ("=== DÉBUT DES RENDUS (" + totalRendus as string + " rendus à effectuer) ===")

                -- Désactiver les fenêtres de rendu
                rendShowVFB = false
                try
                (
                    renderers.current.enable_render_view = false
                    renderers.current.progressive_rendering = false
                    print "Fenêtres de rendu désactivées (mode batch automatique)"
                )
                catch
                (
                    print "Note: Configuration Arnold appliquée avec certaines limitations"
                )

                stopRendering = false

                -- Variables pour garder les dernières maps chargées
                local lastMapA = undefined
                local lastMapB = undefined
                local lastMapC = undefined

                -- Créer/récupérer les Color_Correction nodes et Bitmaptexture UNE SEULE FOIS
                local colorCorrectA = undefined
                local bitmapTexA = undefined
                if targetMatA != undefined then
                (
                    if classOf targetMatA.base_color_map == Color_Correction then
                    (
                        colorCorrectA = targetMatA.base_color_map
                        if classOf colorCorrectA.Map == Bitmaptexture then
                            bitmapTexA = colorCorrectA.Map
                        else
                            bitmapTexA = Bitmaptexture()
                    )
                    else
                    (
                        colorCorrectA = Color_Correction()
                        if classOf targetMatA.base_color_map == Bitmaptexture then
                            bitmapTexA = targetMatA.base_color_map  -- Réutiliser l'existant
                        else
                            bitmapTexA = Bitmaptexture()
                    )
                )

                local colorCorrectB = undefined
                local bitmapTexB = undefined
                if targetMatB != undefined then
                (
                    if classOf targetMatB.base_color_map == Color_Correction then
                    (
                        colorCorrectB = targetMatB.base_color_map
                        if classOf colorCorrectB.Map == Bitmaptexture then
                            bitmapTexB = colorCorrectB.Map
                        else
                            bitmapTexB = Bitmaptexture()
                    )
                    else
                    (
                        colorCorrectB = Color_Correction()
                        if classOf targetMatB.base_color_map == Bitmaptexture then
                            bitmapTexB = targetMatB.base_color_map  -- Réutiliser l'existant
                        else
                            bitmapTexB = Bitmaptexture()
                    )
                )

                local colorCorrectC = undefined
                local bitmapTexC = undefined
                if targetMatC != undefined then
                (
                    if classOf targetMatC.base_color_map == Color_Correction then
                    (
                        colorCorrectC = targetMatC.base_color_map
                        if classOf colorCorrectC.Map == Bitmaptexture then
                            bitmapTexC = colorCorrectC.Map
                        else
                            bitmapTexC = Bitmaptexture()
                    )
                    else
                    (
                        colorCorrectC = Color_Correction()
                        if classOf targetMatC.base_color_map == Bitmaptexture then
                            bitmapTexC = targetMatC.base_color_map  -- Réutiliser l'existant
                        else
                            bitmapTexC = Bitmaptexture()
                    )
                )

                print (">>> Color_Correction et Bitmaptexture nodes préparés (réutilisation des nodes existants)")

                -- Boucle sur le nombre maximum de maps
                for i = 1 to maxMaps do
                (
                    if stopRendering then
                    (
                        print "
!!! ARRÊT DES RENDUS DEMANDÉ !!!"
                        restoreOriginalMaps targetMatA targetMatB targetMatC originalFileA originalFileB originalFileC
                        exit
                    )

                    for k = 1 to 3 do windows.processPostedMessages()
                    sleep 0.01

                    -- Déterminer quelle map charger pour chaque composant
                    local currentMapA = if i <= mapFilesA.count then mapFilesA[i] else lastMapA
                    local currentMapB = if i <= mapFilesB.count then mapFilesB[i] else lastMapB
                    local currentMapC = if i <= mapFilesC.count then mapFilesC[i] else lastMapC

                    local mapBaseName = getFilenameFile currentMapA

                    print ("
--- Itération " + i as string + "/" + maxMaps as string + " ---")
                    print ("Map A: " + filenameFromPath currentMapA)
                    if currentMapB != undefined then print ("Map B: " + filenameFromPath currentMapB)
                    if currentMapC != undefined then print ("Map C: " + filenameFromPath currentMapC)

                    -- Charger les maps dans les matériaux (en réutilisant les nodes existants)
                    try
                    (
                        -- Composant A
                        if currentMapA != undefined and colorCorrectA != undefined and bitmapTexA != undefined then
                        (
                            bitmapTexA.fileName = currentMapA
                            colorCorrectA.Map = bitmapTexA
                            colorCorrectA.contrast = contrastValueA
                            colorCorrectA.brightness = brightnessValueA
                            targetMatA.base_color_map = colorCorrectA
                            lastMapA = currentMapA
                            print ("Map A chargée (contraste: " + contrastValueA as string + ", luminosité: " + brightnessValueA as string + ")")
                        )

                        -- Composant B
                        if targetMatB != undefined and currentMapB != undefined and colorCorrectB != undefined and bitmapTexB != undefined then
                        (
                            bitmapTexB.fileName = currentMapB
                            colorCorrectB.Map = bitmapTexB
                            colorCorrectB.contrast = contrastValueB
                            colorCorrectB.brightness = brightnessValueB
                            targetMatB.base_color_map = colorCorrectB
                            lastMapB = currentMapB
                            print ("Map B chargée (contraste: " + contrastValueB as string + ", luminosité: " + brightnessValueB as string + ")")
                        )

                        -- Composant C
                        if targetMatC != undefined and currentMapC != undefined and colorCorrectC != undefined and bitmapTexC != undefined then
                        (
                            bitmapTexC.fileName = currentMapC
                            colorCorrectC.Map = bitmapTexC
                            colorCorrectC.contrast = contrastValueC
                            colorCorrectC.brightness = brightnessValueC
                            targetMatC.base_color_map = colorCorrectC
                            lastMapC = currentMapC
                            print ("Map C chargée (contraste: " + contrastValueC as string + ", luminosité: " + brightnessValueC as string + ")")
                        )

                        completeRedraw()
                        gc()
                        windows.processPostedMessages()
                    )
                    catch
                    (
                        print ("ERREUR: Impossible de charger les maps pour l'itération " + i as string)
                        continue
                    )

                    -- Boucle sur chaque type de rendu
                    for job in renderJobs do
                    (
                        if stopRendering then
                        (
                            print "  >>> Arrêt demandé, sortie de la boucle de rendus"
                            restoreOriginalMaps targetMatA targetMatB targetMatC originalFileA originalFileB originalFileC
                            exit
                        )

                        for k = 1 to 3 do windows.processPostedMessages()

                        local jobName = job[1]
                        local jobFolder = job[2]
                        local jobWidth = job[3]
                        local jobHeight = job[4]
                        local jobFormat = job[5]
                        local jobAlpha = job[6]

                        renduCourant += 1
                        print ("  [" + renduCourant as string + "/" + totalRendus as string + "] Rendu " + jobName + "...")

                        local progressPercent = 100.0 * renduCourant / totalRendus
                        pbRender.value = progressPercent as integer
                        lblCurrentRender.text = mapBaseName + " - " + jobName + " (" + renduCourant as string + "/" + totalRendus as string + ")"

                        for k = 1 to 5 do
                        (
                            windows.processPostedMessages()
                            sleep 0.01
                        )
                        completeRedraw()
                        print (">>> UI actualisée: " + lblCurrentRender.text)

                        renderWidth = jobWidth
                        renderHeight = jobHeight

                        if jobAlpha then
                        (
                            sliderTime = 1f
                            print ("    Frame: 01 (rendu détouré)")
                        )
                        else
                        (
                            sliderTime = 0f
                            print ("    Frame: 00 (rendu normal)")
                        )

                        local outputFileName = "Rendu_" + jobName + "_" + mapBaseName + "." + jobFormat
                        local outputPath = jobFolder + "\\\\" + outputFileName

                        local startTime = timestamp()
                        try
                        (
                            local renderedImage = render outputfile:outputPath vfb:off
                            local endTime = timestamp()
                            local renderDuration = (endTime - startTime) / 1000.0

                            if not (doesFileExist outputPath) then
                            (
                                print "
!!! RENDU ANNULÉ PAR L'UTILISATEUR (ESC) !!!"
                                print "Arrêt de toute la série de rendus..."
                                lblCurrentRender.text = "Annulé par utilisateur"
                                renduCourant -= 1
                                stopRendering = true
                                exit
                            )

                            local fileSize = getFileSize outputPath

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

                            for k = 1 to 3 do windows.processPostedMessages()
                            gc()

                            print ("    OK: " + outputFileName + " (durée: " + timeText + ", taille: " + fileSize as string + " bytes)")
                            print (">>> Rendu " + renduCourant as string + "/" + totalRendus as string + " terminé")
                        )
                        catch
                        (
                            print ("    ERREUR lors du rendu: " + outputFileName)
                            lblRenderTime.text = "Erreur lors du rendu"
                            windows.processPostedMessages()
                        )
                    )

                    -- Nettoyage mémoire après chaque itération
                    try
                    (
                        freeSceneBitmaps()
                        gc()
                        clearUndoBuffer()
                        windows.processPostedMessages()
                        sleep 0.05
                        print (">>> Mémoire libérée après itération " + i as string)
                    )
                    catch
                    (
                        print "Note: Impossible de libérer complètement la mémoire"
                    )
                )

                -- Restaurer les paramètres originaux
                renderWidth = originalWidth
                renderHeight = originalHeight
                rendShowVFB = true  -- Réactiver le VFB pour les prochains rendus manuels

                -- Restaurer les maps originales dans les matériaux
                restoreOriginalMaps targetMatA targetMatB targetMatC originalFileA originalFileB originalFileC

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
                    mapFolderPathB = ""
                    mapFolderPathC = ""
                    renderFolderPath = ""
                    sceneFiles = #()

                    -- Réinitialiser les contrastes et luminosités
                    contrastValueA = 0
                    contrastValueB = 0
                    contrastValueC = 0
                    brightnessValueA = 0
                    brightnessValueB = 0
                    brightnessValueC = 0
                    spnContrastA.value = 0
                    spnContrastB.value = 0
                    spnContrastC.value = 0
                    spnBrightnessA.value = 0
                    spnBrightnessB.value = 0
                    spnBrightnessC.value = 0

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

                    -- Restaurer les maps par défaut et remettre contraste/luminosité à 0
                    try
                    (
                        local matA = findMaterialByName "MAT_UNIKALO"
                        if matA != undefined and classOf matA.base_color_map == Color_Correction then
                        (
                            matA.base_color_map.contrast = 0
                            matA.base_color_map.brightness = 0
                        )

                        local matB = findMaterialByName "MAT_UNIKALO_B"
                        if matB != undefined and classOf matB.base_color_map == Color_Correction then
                        (
                            matB.base_color_map.contrast = 0
                            matB.base_color_map.brightness = 0
                        )

                        local matC = findMaterialByName "MAT_UNIKALO_C"
                        if matC != undefined and classOf matC.base_color_map == Color_Correction then
                        (
                            matC.base_color_map.contrast = 0
                            matC.base_color_map.brightness = 0
                        )

                        completeRedraw()
                        print (">>> Contraste et luminosité réinitialisés dans les matériaux")
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
