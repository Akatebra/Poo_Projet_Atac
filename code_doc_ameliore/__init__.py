"""Plugin QGIS « Isochrones Géoplateforme » : point d'entrée lu par QGIS."""
import os
import sys

# On ajoute le dossier du plugin au chemin de recherche de Python,
# pour que "from Point import Point" fonctionne entre nos fichiers.
dossier = os.path.dirname(__file__)
if dossier not in sys.path:
    sys.path.append(dossier)

def classFactory(iface):
    """
    Fonction appelée par QGIS pour créer le plugin.

    Parameters
    ----------
    iface : QgisInterface
        Lien vers l'interface de QGIS.

    Returns
    -------
    IsochronePlugin
        L'objet plugin que QGIS va utiliser.
    """
    from IsochronePlugin import IsochronePlugin
    return IsochronePlugin(iface)