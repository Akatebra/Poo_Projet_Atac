import sys
try:
    from qgis.PyQt.QtGui import QAction
except ImportError:
    from qgis.PyQt.QtWidgets import QAction

from FenetrePlugin import FenetrePlugin

class IsochronePlugin:
    def __init__(self, iface):
        self.iface = iface        # iface : le lien vers l'interface de QGIS
        self.fenetre = None
        self.action = None

    def initGui(self):
        self.action = QAction("Calculer Isochrone", self.iface.mainWindow())
        self.action.triggered.connect(self.ouvrir_fenetre)
        self.iface.addPluginToMenu("Calculer Isochrone", self.action)

    def unload(self):
        self.iface.removePluginMenu("Calculer Isochrone", self.action)
        if self.fenetre is not None:
            self.fenetre.close()


    def ouvrir_fenetre(self):
        if self.fenetre is None:
            self.fenetre = FenetrePlugin(self.iface)
        self.fenetre.show()
        self.fenetre.raise_()
        self.fenetre.activateWindow()
        
