import sys
import requests  

try:
    from qgis.core import QgsProject
except ImportError:
    QgsProject = None

try:
    from qgis.PyQt.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                                     QFormLayout, QLineEdit, QMessageBox, QComboBox)
except ImportError:
    from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                                 QFormLayout, QLineEdit, QMessageBox, QComboBox)
    
from Point import Point
from ParametresIsochrone import ParametresIsochrone
from ClientGeoplateforme import ClientGeoplateforme

class FenetrePlugin(QWidget):
    """
    Classe représentant la fenêtre du plugin QGIS-Isochrone. 
    Cette fenêtre permet à l'utilisateur de saisir les paramètres nécessaires pour calculer les isochrones.
    """
    def __init__(self):
        """
        Initialise la fenêtre du plugin et configure l'interface utilisateur.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Configure l'interface utilisateur.
        Crée les champs de saisie pour les paramètres importants.
        Crée les boutons pour sélectionner un point et lancer le calcul.
        """
        self.setWindowTitle("Plugin QGIS-Isochrone")
        self.resize(800,500)
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
            ressources = ClientGeoplateforme().get_ressources_isochrone()
        except (requests.exceptions.RequestException, KeyError, ValueError):
            ressources = ClientGeoplateforme.RESSOURCES_DOCUMENTEES
        self.resourceBox.addItems(ressources)
        self.resourceBox.setCurrentText("bdtopo-valhalla")
       


        
        self.costTypeBox = QComboBox()
        self.costTypeBox.addItems(["time", "distance"])

        self.costValueEdit = QLineEdit()

        form.addRow("Ressource :", self.resourceBox)
        form.addRow("Type de coût :", self.costTypeBox)
        form.addRow("Valeur du coût :", self.costValueEdit)

        self.selectButton = QPushButton("Sélectionner un point")
        self.calculateButton = QPushButton("Lancer le calcul")
        layout.addWidget(self.selectButton)
        layout.addWidget(self.calculateButton)
        self.setLayout(layout)

        self.selectButton.clicked.connect(self.select_point)
        self.calculateButton.clicked.connect(self.lancer_calcul)

        

    def select_point(self):
       
        print("Point sélectionné")


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
        if costValue <= 0:
            QMessageBox.warning(self, "Erreur", "La valeur du coût doit être positive.")
            return

        resource = self.resourceBox.currentText()
        costType = self.costTypeBox.currentText()
        point = Point(lon, lat)
        params = ParametresIsochrone(point=point, resource=resource, costValue=costValue, costType=costType)
        print(params.toDict())

        try:
            client = ClientGeoplateforme()
            resultat = client.calcul_isochrone(params)
        except (requests.exceptions.RequestException, ValueError) as e:
            QMessageBox.warning(self, "Erreur", f"Le calcul a échoué : {e}")
            return

        if QgsProject is not None:
            QgsProject.instance().addMapLayer(resultat.creer_couche())

        QMessageBox.information(self, "Résultat", f"Isochrone calculée : {resultat.nombre_points()} points.")

         


if __name__ == "__main__":
    app = QApplication.instance() 
    if not app: # sinon on crée une instance de QApplication
        app = QApplication(sys.argv)
    fen = FenetrePlugin()
    fen.show()
    app.exec()
