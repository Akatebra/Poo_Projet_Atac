import os
import sys

dossier = os.path.dirname(__file__)
if dossier not in sys.path:
    sys.path.append(dossier)

def classFactory(iface):
    from IsochronePlugin import IsochronePlugin
    return IsochronePlugin(iface)