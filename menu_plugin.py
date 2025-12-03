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

            -- Image en haut (ImgTag pour éviter le liseré)
            ImgTag titleImage pos:[12,10] width:182 height:66 bitmap:(openBitMap (getDir #userScripts + "\\TITRE_interface.jpg"))

            -- Boutons
            button btn1 "Dossier scènes" pos:[10,86] width:186 height:30
            button btn2a "Dossier textures" pos:[10,121] width:186 height:30
            button btn2b "Dossier Rendu" pos:[10,156] width:186 height:30

            -- Menu déroulant Scènes
            label lblScenes "Scènes:" pos:[10,196] width:186
            dropdownList ddScenes "" pos:[10,211] width:186 items:#()

            -- Rendus Série 01
            groupBox grpRendu01 "Rendus Série 01" pos:[10,256] width:186 height:75
            checkbox chk01_std "Rendu standard" pos:[20,273] width:160
            checkbox chk01_hd "Rendu HD" pos:[20,290] width:160
            checkbox chk01_det "Détourage" pos:[20,307] width:160

            -- Rendus Série 02
            groupBox grpRendu02 "Rendus Série 02" pos:[10,341] width:186 height:75
            checkbox chk02_std "Rendu standard" pos:[20,358] width:160
            checkbox chk02_hd "Rendu HD" pos:[20,375] width:160
            checkbox chk02_det "Détourage" pos:[20,392] width:160

            -- Rendus Série 03
            groupBox grpRendu03 "Rendus Série 03" pos:[10,426] width:186 height:75
            checkbox chk03_std "Rendu standard" pos:[20,443] width:160
            checkbox chk03_hd "Rendu HD" pos:[20,460] width:160
            checkbox chk03_det "Détourage" pos:[20,477] width:160

            -- Rendus Série 04
            groupBox grpRendu04 "Rendus Série 04" pos:[10,511] width:186 height:75
            checkbox chk04_std "Rendu standard" pos:[20,528] width:160
            checkbox chk04_hd "Rendu HD" pos:[20,545] width:160
            checkbox chk04_det "Détourage" pos:[20,562] width:160

            -- Section Lancer les rendus
            groupBox grpLancer "" pos:[10,596] width:186 height:80
            button btnLogo "" pos:[20,615] width:64 height:64 toolTip:"Lancer les rendus"
            label lblLancerRendus "Lancer\nles rendus" pos:[88,618] width:90 height:40 align:#left

            -- Événement au chargement pour gérer les images
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
                if state == true then chk01_hd.checked = false
            )
            on chk01_hd changed state do
            (
                if state == true then chk01_std.checked = false
            )

            -- Événements checkboxes Série 02 (mutuellement exclusifs)
            on chk02_std changed state do
            (
                if state == true then chk02_hd.checked = false
            )
            on chk02_hd changed state do
            (
                if state == true then chk02_std.checked = false
            )

            -- Événements checkboxes Série 03 (mutuellement exclusifs)
            on chk03_std changed state do
            (
                if state == true then chk03_hd.checked = false
            )
            on chk03_hd changed state do
            (
                if state == true then chk03_std.checked = false
            )

            -- Événements checkboxes Série 04 (mutuellement exclusifs)
            on chk04_std changed state do
            (
                if state == true then chk04_hd.checked = false
            )
            on chk04_hd changed state do
            (
                if state == true then chk04_std.checked = false
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
