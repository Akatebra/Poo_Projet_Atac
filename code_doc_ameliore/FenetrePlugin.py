import sys
import requests  

try:
    from qgis.core import QgsProject, QgsCoordinateReferenceSystem, QgsCoordinateTransform
    from qgis.gui import QgsMapToolEmitPoint, QgsVertexMarker
    from qgis.PyQt.QtGui import QColor
except ImportError:
    QgsProject = None
    QgsCoordinateReferenceSystem = None
    QgsCoordinateTransform = None
    QgsMapToolEmitPoint = None
    QgsVertexMarker = None
    QColor = None

try:
    from qgis.PyQt.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                                     QFormLayout, QLineEdit, QMessageBox, QComboBox)
except ImportError:
    from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                                 QFormLayout, QLineEdit, QMessageBox, QComboBox)
    
from Point import Point
from ParametresIsochrone import ParametresIsochrone
from ClientGeoplateforme import ClientGeoplateforme


DEFAUT = "(par défaut)"
FORMATS_GERES = ["geojson", "wkt"]

class FenetrePlugin(QWidget):
    """
    Classe représentant la fenêtre du plugin QGIS-Isochrone. 
    Cette fenêtre permet à l'utilisateur de saisir les paramètres nécessaires pour calculer les isochrones.
    """
    def __init__(self, iface=None):
        """
        Initialise la fenêtre du plugin et configure l'interface utilisateur.
        """
        super().__init__()
        self.iface = iface
        self.outil = None
        self.marqueur = None
        self.client = ClientGeoplateforme()
        self.capacites_ok = False
        self.options = {}
        self.initUI()

    def initUI(self):
        """
        Configure l'interface utilisateur.
        Crée les champs de saisie pour les paramètres importants.
        Crée les boutons pour sélectionner un point et lancer le calcul.
        """
        self.setWindowTitle("Calcul-Isochrone")
        self.resize(800,600)
        self.move(30,200)

        layout = QVBoxLayout()
        form = QFormLayout() 
        self.lonEdit = QLineEdit()
        self.latEdit = QLineEdit()
        form.addRow("Longitude :", self.lonEdit)
        form.addRow("Latitude :", self.latEdit)
        layout.addLayout(form)

        self.resourceBox = QComboBox()
        try:
            ressources = self.client.get_ressources_isochrone()
            self.capacites_ok = True
        except (requests.exceptions.RequestException, KeyError, ValueError):
            ressources = ClientGeoplateforme.RESSOURCES_DOCUMENTEES
            self.capacites_ok = False
        self.resourceBox.addItems(ressources)
        self.resourceBox.setCurrentText("bdtopo-valhalla")
        
        self.costTypeBox = QComboBox()
        self.costTypeBox.addItems(["time", "distance"])

        self.costValueEdit = QLineEdit()
        self.unitBox = QComboBox()

        self.profileBox = QComboBox()
        self.directionBox = QComboBox()
        self.formatBox = QComboBox()
        self.projectionBox = QComboBox()

        form.addRow("Ressource :", self.resourceBox)
        form.addRow("Type de coût :", self.costTypeBox)
        form.addRow("Valeur du coût :", self.costValueEdit)
        form.addRow("Unité du coût :", self.unitBox)
        form.addRow("Profil :", self.profileBox)
        form.addRow("Direction (departure = depuis le point, arrival = vers le point) :", self.directionBox)
        form.addRow("Format de la géométrie :", self.formatBox)
        form.addRow("Projection de la réponse :", self.projectionBox)

        self.selectButton = QPushButton("Sélectionner un point")
        self.calculateButton = QPushButton("Lancer le calcul")
        layout.addWidget(self.selectButton)
        layout.addWidget(self.calculateButton)
        self.setLayout(layout)

        self.selectButton.clicked.connect(self.select_point)
        self.calculateButton.clicked.connect(self.lancer_calcul)

        self.resourceBox.currentTextChanged.connect(self.maj_options)
        self.costTypeBox.currentTextChanged.connect(self.maj_unites)
        self.maj_options()


    def remplir(self, boite, valeurs):
        """
        Remplit une liste déroulante : "(par défaut)" puis les valeurs données.
 
        Parameters
        ----------
        boite : QComboBox
            La liste à remplir.
        valeurs : list of str
            Les choix à proposer.
        """
        boite.clear()
        boite.addItem(DEFAUT)
        boite.addItems(valeurs)

 
    def maj_options(self, texte=None):
        """
        Remplit les listes d'options selon la ressource choisie.
 
        Les valeurs viennent de getCapabilities, ou de la liste de secours
        si le service n'a pas répondu. Le paramètre `texte` est envoyé par le
        signal de la liste des ressources ; on ne l'utilise pas.
        """
        options = ClientGeoplateforme.OPTIONS_PAR_DEFAUT
        if self.capacites_ok:
            try:
                options = self.client.get_options_isochrone(self.resourceBox.currentText())
            except (KeyError, ValueError):
                pass
        self.options = options
 
        self.remplir(self.profileBox, options.get("profile", []))
        self.remplir(self.directionBox, options.get("direction", []))
        formats = [f for f in options.get("geometryFormat", []) if f in FORMATS_GERES]
        self.remplir(self.formatBox, formats)
        self.remplir(self.projectionBox, options.get("projection", []))
        self.maj_unites()

 
    def maj_unites(self, texte=None):
        """
        Remplit la liste des unités selon le type de coût :
        timeUnit pour un coût en temps, distanceUnit pour un coût en distance.
        """
        cle = "timeUnit" if self.costTypeBox.currentText() == "time" else "distanceUnit"
        valeurs = [v for v in self.options.get(cle, []) if v != "standard"]
        self.remplir(self.unitBox, valeurs)
 
    def valeur_choisie(self, boite):
        """
        Renvoie la valeur choisie dans une liste, ou None si "(par défaut)".
 
        Returns
        -------
        str or None
            None signifie qu'on n'envoie pas le paramètre au service.
        """
        
        if boite.currentIndex() == 0:
            return None
        return boite.currentText()

    def select_point(self):
        """

        """
        if self.iface is None or QgsMapToolEmitPoint is None:
            QMessageBox.information(self, "Info", "La sélection sur la carte n'est possible que dans QGIS.")
            return
        canvas = self.iface.mapCanvas()
        if self.outil is None:
            self.outil = QgsMapToolEmitPoint(canvas)
            self.outil.canvasClicked.connect(self.point_clique)
        canvas.setMapTool(self.outil)
        self.iface.messageBar().pushMessage(
            "Isochrone", "Cliquez sur la carte pour choisir le point de départ.", duration=5)
        self.hide()


    def point_clique(self, point):
        """
         Appelée au clic sur la carte : convertit le point en lon/lat,
        remplit les champs et affiche un marqueur.
 
        Parameters
        ----------
        point : QgsPointXY
            Le point cliqué, dans le système de coordonnées de la carte.
        """

        canvas = self.iface.mapCanvas()
        crs_carte = canvas.mapSettings().destinationCrs()
        crs_service = QgsCoordinateReferenceSystem("EPSG:4326")
        transformation = QgsCoordinateTransform(crs_carte, crs_service, QgsProject.instance())
        point_lonlat = transformation.transform(point)
    
        self.lonEdit.setText(f"{point_lonlat.x():.6f}")
        self.latEdit.setText(f"{point_lonlat.y():.6f}")
    
        canvas.unsetMapTool(self.outil)
        self.afficher_marqueur(point)
        self.show()
        self.raise_()
        self.activateWindow()
    


    def lancer_calcul(self):
        """
        Récupère les paramètres saisis par l'utilisateur, 
        crée un objet Point et un objet ParametresIsochrone, 
        puis lit les champs, vérifie les valeurs, 
        lance le calcul d’isochrone et affiche le résultat.
        """
        lon_text = self.lonEdit.text()
        lat_text = self.latEdit.text()
        costValue_text = self.costValueEdit.text()
        try:
            lon = float(lon_text)
            lat = float(lat_text)
            costValue = float(costValue_text)
 
        except ValueError:
            QMessageBox.warning(self, "Erreur", "La longitude, la latitude et la valeur du coût doivent être des nombres.")
            return
        
        if not (-180 <= lon <= 180):
            QMessageBox.warning(self, "Erreur", "La longitude doit être comprise entre -180 et 180.")
            return
        if not (-90 <= lat <= 90):
            QMessageBox.warning(self, "Erreur", "La latitude doit être comprise entre -90 et 90.")
            return
        if not (0 < costValue <= 50000):
            QMessageBox.warning(self, "Erreur", "La valeur du coût doit être comprise entre 0 et 50000.")
            return

        resource = self.resourceBox.currentText()
        costType = self.costTypeBox.currentText()
        point = Point(lon, lat)

        unite = self.valeur_choisie(self.unitBox)
        timeUnit = unite if costType == "time" else None
        distanceUnit = unite if costType == "distance" else None
 
        params = ParametresIsochrone(
            point=point, resource=resource, costValue=costValue, costType=costType,
            profile=self.valeur_choisie(self.profileBox),
            direction=self.valeur_choisie(self.directionBox),
            geometryFormat=self.valeur_choisie(self.formatBox),
            timeUnit=timeUnit,
            distanceUnit=distanceUnit,
            crs=self.valeur_choisie(self.projectionBox),
        )
        print(params.toDict())


        try:
            resultat = self.client.calcul_isochrone(params)
        except (requests.exceptions.RequestException, ValueError) as e:
            QMessageBox.warning(self, "Erreur", f"Le calcul a échoué : {e}")
            return
 
        if QgsProject is not None:
            QgsProject.instance().addMapLayer(resultat.creer_couche())
            QgsProject.instance().addMapLayer(point.creer_couche())
            self.effacer_marqueur()

        QMessageBox.information(self, "Résultat", f"Isochrone calculée : {resultat.nombre_points()} points.")


    def reinitialiser(self):
        """Remet les champs de la fenêtre à leur état initial."""
        self.lonEdit.clear()
        self.latEdit.clear()
        self.costValueEdit.clear()
        self.costTypeBox.setCurrentIndex(0)
        self.resourceBox.setCurrentText("bdtopo-valhalla")
        for boite in (self.unitBox, self.profileBox, self.directionBox, self.formatBox, self.projectionBox):
            boite.setCurrentIndex(0)
        self.effacer_marqueur()

    def closeEvent(self, event):
        """Appelée quand l'utilisateur ferme la fenêtre : on remet tout à zéro."""
        self.reinitialiser()
        super().closeEvent(event)


    def afficher_marqueur(self, point):
        """Affiche un rond rouge sur la carte à l'endroit du point cliqué."""
        self.effacer_marqueur()
        self.marqueur = QgsVertexMarker(self.iface.mapCanvas())
        self.marqueur.setCenter(point)
        try:
            self.marqueur.setIconType(QgsVertexMarker.IconType.ICON_CIRCLE)
        except AttributeError:      #
            self.marqueur.setIconType(QgsVertexMarker.ICON_CIRCLE)
        self.marqueur.setColor(QColor(255, 0, 0))
        if hasattr(self.marqueur, "setFillColor"):  
            self.marqueur.setFillColor(QColor(255, 0, 0))
        self.marqueur.setIconSize(8)
        self.marqueur.setPenWidth(1)

    def effacer_marqueur(self):
        """Retire la croix de la carte si elle existe."""
        if self.marqueur is not None:
            self.iface.mapCanvas().scene().removeItem(self.marqueur)
            self.marqueur = None


if __name__ == "__main__":
    app = QApplication.instance() 
    if not app: # sinon on crée une instance de QApplication
        app = QApplication(sys.argv)
    fen = FenetrePlugin()
    fen.show()
    app.exec()
