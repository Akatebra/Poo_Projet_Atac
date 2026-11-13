"""Module Point : creation de point geographique en longitude et latitude"""

class Point:
    def __init__(self, x, y):
        """
        Initialise nos parametres 
        
        Parameters
        ----------
        x : float
        Longitude, en degrés.
        y : float
        Latitude, en degrés.
        """
        self.x = x
        self.y = y


    def toStr(self):
        """
        Met le point en chaine de caractere pour la requête envoyée au service.

        Returns
        -------
        str
            Le point au format "lon,lat", sans espace ni parenthèses.
        """
        return f"{self.x},{self.y}"


    def creer_couche(self):
        """
        Crée une couche QGIS contenant un point.

        Returns
        -------
        QgsVectorLayer
            Couche temporaire (en mémoire) en EPSG:4326, nommée "Point de départ".
        """

        # Cet import ici fait que la classe Point reste utilisable en dehors de QGIS
        from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY

        couche = QgsVectorLayer("Point?crs=EPSG:4326", "Point de départ", "memory")
        entite = QgsFeature()
        entite.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(self.x, self.y)))
        couche.dataProvider().addFeatures([entite])
        couche.updateExtents()
        return couche


if __name__ == "__main__":
    p = Point(2.337306, 48.849319)
    print(p.toStr())