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
        rollout CustomToolWindow "U-Rtool" width:206 height:690
        (
            -- Variables globales
            local sceneFolderPath = ""
            local sceneFiles = #()
            local textureFolderPath = ""
            local renderFolderPath = ""
            local iniFile = getDir #userScripts + "\\U-Rtool_settings.ini"
            local isLoading = false  -- Flag pour éviter les conflits pendant le chargement

            -- Fonction pour sauvegarder les paramètres
            fn saveSettings =
            (
                print "=== SAUVEGARDE ==="

                -- Sauvegarder les chemins
                setINISetting iniFile "Paths" "SceneFolder" sceneFolderPath
                setINISetting iniFile "Paths" "TextureFolder" textureFolderPath
                setINISetting iniFile "Paths" "RenderFolder" renderFolderPath

                -- Sauvegarder Config01
                try
                (
                    local val_std = if chk01_std.checked then "true" else "false"
                    local val_hd = if chk01_hd.checked then "true" else "false"
                    local val_det = if chk01_det.checked then "true" else "false"
                    setINISetting iniFile "Config01" "Standard" val_std
                    setINISetting iniFile "Config01" "HD" val_hd
                    setINISetting iniFile "Config01" "Detourage" val_det
                    print "Config01 sauvegardé"
                )
                catch (print "ERREUR Config01")

                -- Sauvegarder Config02
                try
                (
                    local val_std = if chk02_std.checked then "true" else "false"
                    local val_hd = if chk02_hd.checked then "true" else "false"
                    local val_det = if chk02_det.checked then "true" else "false"
                    setINISetting iniFile "Config02" "Standard" val_std
                    setINISetting iniFile "Config02" "HD" val_hd
                    setINISetting iniFile "Config02" "Detourage" val_det
                    print "Config02 sauvegardé"
                )
                catch (print "ERREUR Config02")

                -- Sauvegarder Config03
                try
                (
                    local val_std = if chk03_std.checked then "true" else "false"
                    local val_hd = if chk03_hd.checked then "true" else "false"
                    local val_det = if chk03_det.checked then "true" else "false"
                    setINISetting iniFile "Config03" "Standard" val_std
                    setINISetting iniFile "Config03" "HD" val_hd
                    setINISetting iniFile "Config03" "Detourage" val_det
                    print "Config03 sauvegardé"
                )
                catch (print "ERREUR Config03")

                -- Sauvegarder Config04
                try
                (
                    local val_std = if chk04_std.checked then "true" else "false"
                    local val_hd = if chk04_hd.checked then "true" else "false"
                    local val_det = if chk04_det.checked then "true" else "false"
                    setINISetting iniFile "Config04" "Standard" val_std
                    setINISetting iniFile "Config04" "HD" val_hd
                    setINISetting iniFile "Config04" "Detourage" val_det
                    print "Config04 sauvegardé"
                )
                catch (print "ERREUR Config04")

                print "=== Sauvegarde terminée ==="
            )

            -- Fonction pour charger les paramètres
            fn loadSettings =
            (
                isLoading = true  -- Désactiver les événements pendant le chargement
                print "=== CHARGEMENT ==="

                -- Charger les chemins
                local loadedPath = getINISetting iniFile "Paths" "SceneFolder"
                if loadedPath != "" then
                (
                    sceneFolderPath = loadedPath
                    print ("Dossier scènes chargé: " + sceneFolderPath)

                    -- Remplir le menu déroulant avec les scènes
                    sceneFiles = getFiles (sceneFolderPath + "\\*.max")
                    local sceneNames = #()
                    for sceneFile in sceneFiles do
                        append sceneNames (filenameFromPath sceneFile)

                    -- Vérifier que ddScenes existe avant de l'utiliser
                    if ddScenes != undefined then
                    (
                        ddScenes.items = sceneNames
                        print ((sceneNames.count as string) + " scènes trouvées")
                    )
                    else
                        print "ddScenes non initialisé, scènes chargées en mémoire uniquement"
                )

                loadedPath = getINISetting iniFile "Paths" "TextureFolder"
                if loadedPath != "" then textureFolderPath = loadedPath

                loadedPath = getINISetting iniFile "Paths" "RenderFolder"
                if loadedPath != "" then renderFolderPath = loadedPath

                -- Charger les checkboxes avec protection et debug
                try
                (
                    print "Chargement checkboxes..."

                    -- Config 01
                    local val = getINISetting iniFile "Config01" "Standard"
                    print ("Config01 Standard=" + val)
                    if val != "" and chk01_std != undefined then
                    (
                        chk01_std.checked = (val == "true")
                        print ("  -> chk01_std défini à " + (chk01_std.checked as string))
                    )

                    val = getINISetting iniFile "Config01" "HD"
                    if val != "" and chk01_hd != undefined then chk01_hd.checked = (val == "true")

                    val = getINISetting iniFile "Config01" "Detourage"
                    if val != "" and chk01_det != undefined then chk01_det.checked = (val == "true")

                    -- Config 02
                    val = getINISetting iniFile "Config02" "Standard"
                    if val != "" and chk02_std != undefined then chk02_std.checked = (val == "true")
                    val = getINISetting iniFile "Config02" "HD"
                    if val != "" and chk02_hd != undefined then chk02_hd.checked = (val == "true")
                    val = getINISetting iniFile "Config02" "Detourage"
                    if val != "" and chk02_det != undefined then chk02_det.checked = (val == "true")

                    -- Config 03
                    val = getINISetting iniFile "Config03" "Standard"
                    if val != "" and chk03_std != undefined then chk03_std.checked = (val == "true")
                    val = getINISetting iniFile "Config03" "HD"
                    if val != "" and chk03_hd != undefined then chk03_hd.checked = (val == "true")
                    val = getINISetting iniFile "Config03" "Detourage"
                    if val != "" and chk03_det != undefined then chk03_det.checked = (val == "true")

                    -- Config 04
                    val = getINISetting iniFile "Config04" "Standard"
                    if val != "" and chk04_std != undefined then chk04_std.checked = (val == "true")
                    val = getINISetting iniFile "Config04" "HD"
                    if val != "" and chk04_hd != undefined then chk04_hd.checked = (val == "true")
                    val = getINISetting iniFile "Config04" "Detourage"
                    if val != "" and chk04_det != undefined then chk04_det.checked = (val == "true")

                    print "Checkboxes chargées"
                )
                catch e
                (
                    print ("Erreur lors du chargement des checkboxes: " + (e as string))
                )

                isLoading = false  -- Réactiver les événements
                print "=== CHARGEMENT TERMINÉ ==="
            )

            -- Image en haut (ImgTag pour éviter le liseré)
            ImgTag titleImage pos:[12,10] width:182 height:66 bitmap:(openBitMap (getDir #userScripts + "\\TITRE_interface.jpg"))

            -- Boutons
            button btn1 "Dossier scènes" pos:[10,86] width:186 height:30
            button btn2a "Dossier textures" pos:[10,121] width:186 height:30
            button btn2b "Dossier Rendu" pos:[10,156] width:186 height:30

            -- Menu déroulant Scènes
            label lblScenes "Scènes:" pos:[10,196] width:186
            dropdownList ddScenes "" pos:[10,211] width:186 items:#()

            -- Rendus_Config01
            groupBox grpRendu01 "Rendus_Config01" pos:[10,256] width:186 height:75
            checkbox chk01_std "Rendu standard" pos:[20,273] width:160
            checkbox chk01_hd "Rendu HD" pos:[20,290] width:160
            checkbox chk01_det "Détourage" pos:[20,307] width:160

            -- Rendus_Config02
            groupBox grpRendu02 "Rendus_Config02" pos:[10,341] width:186 height:75
            checkbox chk02_std "Rendu standard" pos:[20,358] width:160
            checkbox chk02_hd "Rendu HD" pos:[20,375] width:160
            checkbox chk02_det "Détourage" pos:[20,392] width:160

            -- Rendus_Config03
            groupBox grpRendu03 "Rendus_Config03" pos:[10,426] width:186 height:75
            checkbox chk03_std "Rendu standard" pos:[20,443] width:160
            checkbox chk03_hd "Rendu HD" pos:[20,460] width:160
            checkbox chk03_det "Détourage" pos:[20,477] width:160

            -- Rendus_Config04
            groupBox grpRendu04 "Rendus_Config04" pos:[10,511] width:186 height:75
            checkbox chk04_std "Rendu standard" pos:[20,528] width:160
            checkbox chk04_hd "Rendu HD" pos:[20,545] width:160
            checkbox chk04_det "Détourage" pos:[20,562] width:160

            -- Section Lancer les rendus
            groupBox grpLancer "" pos:[10,596] width:186 height:80
            button btnLogo "" pos:[20,607] width:64 height:64 toolTip:"Lancer les rendus"
            label lblLancerRendus "          Lancer\n       les rendus" pos:[95,625] width:90 height:40 align:#center

            -- Événement au chargement pour gérer les images et charger les paramètres
            on CustomToolWindow open do
            (
                if titleImage.bitmap == undefined then
                (
                    print "Image TITRE_interface.jpg non trouvée dans le dossier des scripts"
                )

                -- Charger l'image du logo dans le bouton
                local logoPath = getDir #userScripts + "\\Logo-Urt.jpg"
                local logoBitmap = openBitMap logoPath
                if logoBitmap != undefined then
                (
                    btnLogo.images = #(logoBitmap, undefined, 1, 1, 1, 1, 1)
                )
                else
                (
                    print "Image Logo-Urt.jpg non trouvée dans le dossier des scripts"
                )

                -- Charger les paramètres sauvegardés
                loadSettings()
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
                    sceneFiles = getFiles (sceneFolderPath + "\\*.max")

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

            -- Bouton Logo: Lancer les rendus
            on btnLogo pressed do
            (
                -- Sauvegarder la configuration avant de lancer les rendus
                saveSettings()

                print "Lancement des rendus..."
                -- Logique de rendu à implémenter
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

            -- Événements checkboxes Série 01 (mutuellement exclusifs)
            on chk01_std changed state do
            (
                if not isLoading and state == true then chk01_hd.checked = false
            )
            on chk01_hd changed state do
            (
                if not isLoading and state == true then chk01_std.checked = false
            )

            -- Événements checkboxes Série 02 (mutuellement exclusifs)
            on chk02_std changed state do
            (
                if not isLoading and state == true then chk02_hd.checked = false
            )
            on chk02_hd changed state do
            (
                if not isLoading and state == true then chk02_std.checked = false
            )

            -- Événements checkboxes Série 03 (mutuellement exclusifs)
            on chk03_std changed state do
            (
                if not isLoading and state == true then chk03_hd.checked = false
            )
            on chk03_hd changed state do
            (
                if not isLoading and state == true then chk03_std.checked = false
            )

            -- Événements checkboxes Série 04 (mutuellement exclusifs)
            on chk04_std changed state do
            (
                if not isLoading and state == true then chk04_hd.checked = false
            )
            on chk04_hd changed state do
            (
                if not isLoading and state == true then chk04_std.checked = false
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
