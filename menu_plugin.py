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
        rollout CustomToolWindow "U-Rtool" width:206 height:391
        (
            -- Variables globales
            local sceneFolderPath = ""
            local sceneFiles = #()
            local textureFolderPath = ""

            -- Image en haut (ImgTag pour éviter le liseré)
            ImgTag titleImage pos:[12,10] width:182 height:66 bitmap:(openBitMap (getDir #userScripts + "\\TITRE_interface.jpg"))

            -- Boutons
            button btn1 "Dossier scènes" pos:[10,86] width:186 height:30
            button btn2a "Dossier textures" pos:[10,121] width:186 height:30
            button btn2b "Reload textures" pos:[10,156] width:186 height:30
            button btn3 "Bouton 3" pos:[10,191] width:186 height:30

            -- Menu déroulant Scènes
            label lblScenes "Scènes:" pos:[10,231] width:186
            dropdownList ddScenes "" pos:[10,246] width:186 items:#()

            -- Menu déroulant Opérations
            label lblOperations "Opérations:" pos:[10,276] width:186
            dropdownList ddOperations "" pos:[10,291] width:186 items:#("Opération 1", "Opération 2", "Opération 3")

            -- Événement au chargement pour gérer l'image manquante
            on CustomToolWindow open do
            (
                if titleImage.bitmap == undefined then
                (
                    print "Image TITRE_interface.jpg non trouvée dans le dossier des scripts"
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

                    -- Vérifier si le dossier est déjà dans les External File Paths
                    local currentPaths = pathConfig.getCurrentPathList #Bitmap
                    local pathExists = false

                    for p in currentPaths do
                    (
                        if (toLower p) == (toLower textureFolderPath) then
                        (
                            pathExists = true
                            exit
                        )
                    )

                    -- Ajouter le dossier aux External File Paths s'il n'existe pas déjà
                    if not pathExists then
                    (
                        pathConfig.appendSessionPath #Bitmap textureFolderPath
                        print "Dossier ajouté aux External File Paths (Bitmap) pour cette session"
                    )
                    else
                    (
                        print "Ce dossier est déjà dans les External File Paths"
                    )
                )
            )

            -- Bouton 2b: Recharger toutes les textures
            on btn2b pressed do
            (
                print "Rechargement de toutes les textures..."

                -- Parcourir tous les matériaux de la scène
                local reloadCount = 0
                for mat in sceneMaterials do
                (
                    -- Recharger les textures du matériau
                    if (classOf mat) == StandardMaterial or (classOf mat) == VRayMtl or (classOf mat) == PhysicalMaterial then
                    (
                        -- Parcourir les slots de texture
                        for i = 1 to (getNumSubTexmaps mat) do
                        (
                            local tex = getSubTexmap mat i
                            if tex != undefined and (classOf tex) == Bitmaptexture then
                            (
                                tex.reload()
                                reloadCount += 1
                            )
                        )
                    )
                )

                print (reloadCount as string + " texture(s) rechargée(s)")
                messageBox (reloadCount as string + " texture(s) rechargée(s)") title:"Reload Textures"
            )

            on btn3 pressed do
            (
                print "Bouton 3 cliqué"
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

            -- Événement menu déroulant Opérations
            on ddOperations selected sel do
            (
                print ("Opération sélectionnée: " + ddOperations.items[sel])
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
