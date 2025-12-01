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
        rollout CustomToolWindow "U-Rtool" width:206 height:356
        (
            -- Variable globale pour stocker le chemin du dossier scènes
            local sceneFolderPath = ""
            local sceneFiles = #()

            -- Image en haut (ImgTag pour éviter le liseré)
            ImgTag titleImage pos:[12,10] width:182 height:66 bitmap:(openBitMap (getDir #userScripts + "\\TITRE_interface.jpg"))

            -- Trois boutons
            button btn1 "Dossier scène" pos:[10,86] width:186 height:30
            button btn2 "Bouton 2" pos:[10,121] width:186 height:30
            button btn3 "Bouton 3" pos:[10,156] width:186 height:30

            -- Menu déroulant Scènes
            label lblScenes "Scènes:" pos:[10,196] width:186
            dropdownList ddScenes "" pos:[10,211] width:186 items:#()

            -- Menu déroulant Opérations
            label lblOperations "Opérations:" pos:[10,241] width:186
            dropdownList ddOperations "" pos:[10,256] width:186 items:#("Opération 1", "Opération 2", "Opération 3")

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
                        print (sceneNames.count as string + " scène(s) trouvée(s)")
                    else
                        print "Aucune scène .max trouvée dans ce dossier"
                )
            )

            on btn2 pressed do
            (
                print "Bouton 2 cliqué"
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
                    print ("Chargement de la scène: " + sceneToLoad)

                    -- Demander confirmation avant de charger
                    local confirmLoad = queryBox ("Charger la scène:\n" + (filenameFromPath sceneToLoad) + "\n\nVoulez-vous sauvegarder la scène actuelle ?") title:"Charger scène"

                    if confirmLoad == #yes then
                    (
                        -- Sauvegarder puis charger
                        if saveMaxFile (maxFilePath + maxFileName) then
                            loadMaxFile sceneToLoad
                    )
                    else if confirmLoad == #no then
                    (
                        -- Charger sans sauvegarder
                        loadMaxFile sceneToLoad
                    )
                    -- Si #cancel, ne rien faire
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
