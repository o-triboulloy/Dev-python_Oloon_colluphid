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
        rollout CustomToolWindow "U-Rtool" width:206 height:350
        (
            -- Image en haut
            bitmap titleBitmap pos:[10,10] width:186 height:60 fileName:(getDir #userScripts + "\\TITRE_interface.jpg")

            -- Trois boutons
            button btn1 "Bouton 1" pos:[10,80] width:186 height:30
            button btn2 "Bouton 2" pos:[10,115] width:186 height:30
            button btn3 "Bouton 3" pos:[10,150] width:186 height:30

            -- Menu déroulant Scènes
            label lblScenes "Scènes:" pos:[10,190] width:186
            dropdownList ddScenes "" pos:[10,205] width:186 items:#("Scène 1", "Scène 2", "Scène 3")

            -- Menu déroulant Opérations
            label lblOperations "Opérations:" pos:[10,235] width:186
            dropdownList ddOperations "" pos:[10,250] width:186 items:#("Opération 1", "Opération 2", "Opération 3")

            -- Événement au chargement pour gérer l'image manquante
            on CustomToolWindow open do
            (
                if titleBitmap.bitmap == undefined then
                (
                    print "Image TITRE_interface.jpg non trouvée dans le dossier des scripts"
                )
            )

            -- Événements des boutons (vides pour le moment)
            on btn1 pressed do
            (
                print "Bouton 1 cliqué"
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
                print ("Scène sélectionnée: " + ddScenes.items[sel])
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
