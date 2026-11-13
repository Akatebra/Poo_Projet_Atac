"""Module IsochronePlugin : l'intégration du plugin dans QGIS (menu et ouverture de la fenêtre)."""

import sys
try:
    from qgis.PyQt.QtGui import QAction     # QGIS 4 (Qt6)
except ImportError:
    from qgis.PyQt.QtWidgets import QAction       # QGIS 3 (Qt5)

from FenetrePlugin import FenetrePlugin

class IsochronePlugin:
    """
    Classe principale du plugin, appelée par QGIS.

    Elle ajoute une entrée au menu Extensions et ouvre la fenêtre du plugin.

    Attributes
    ----------
    iface : QgisInterface
        Lien vers l'interface de QGIS.
    fenetre : FenetrePlugin or None
        La fenêtre du plugin (créée à la première ouverture).
    action : QAction or None
        L'entrée de menu du plugin.
    """
    def __init__(self, iface):
        """
        Parameters
        ----------
        iface : QgisInterface
            Lien vers l'interface de QGIS, donné par QGIS au chargement du plugin.
        """
        self.iface = iface        
        self.fenetre = None
        self.action = None

    def initGui(self):
        """Appelée par QGIS à l'activation du plugin : 
        ajoute l'entrée dans le menu Extensions."""
        self.action = QAction("Calculer Isochrone", self.iface.mainWindow())
        self.action.triggered.connect(self.ouvrir_fenetre)
        self.iface.addPluginToMenu("Calculer Isochrone", self.action)

    def unload(self):
        """Appelée par QGIS à la désactivation du plugin : 
        retire le menu et ferme la fenêtre."""
        self.iface.removePluginMenu("Calculer Isochrone", self.action)
        if self.fenetre is not None:
            self.fenetre.close()


    def ouvrir_fenetre(self):
        """Ouvre la fenêtre du plugin (la crée la première fois) et la place au premier plan."""
        if self.fenetre is None:
            self.fenetre = FenetrePlugin(self.iface)
        self.fenetre.show()
        self.fenetre.raise_()
        self.fenetre.activateWindow()

        
