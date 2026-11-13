"""Module ResultatIsochrone : le résultat d'un calcul d'isochrone."""

class ResultatIsochrone:
    """
    Résultat d'un calcul d'isochrone renvoyé par le service.

    Attributes
    ----------
    geometrie : dict or str
        La zone atteignable : un dictionnaire GeoJSON (Polygon ou MultiPolygon),
        ou un texte WKT si le format "wkt" a été demandé.
    crs : str
        Système de coordonnées de la géométrie, par exemple "EPSG:4326".
    """

    def __init__(self, geometrie, crs="EPSG:4326"):
        """
        Parameters
        ----------
        geometrie : dict or str
            La géométrie renvoyée par le service (clé "geometry" de la réponse).
        crs : str, optional
            Système de coordonnées de la géométrie (EPSG:4326 par défaut).
        """
        self.geometrie = geometrie
        self.crs = crs


    def nombre_points(self):
        """
        Compte les points du contour de l'isochrone.

        Returns
        -------
        int
            Nombre de points du contour extérieur (additionnés si la zone
            est composée de plusieurs polygones).
        """
        if isinstance(self.geometrie, str):  # format WKT
            from qgis.core import QgsGeometry
            return QgsGeometry.fromWkt(self.geometrie).constGet().nCoordinates()
        if self.geometrie["type"] == "MultiPolygon":
            return sum(len(polygone[0]) for polygone in self.geometrie["coordinates"])
        return len(self.geometrie["coordinates"][0])
       
    
    def creer_couche(self):
        """
        Crée une couche QGIS à partir de la géométrie de l'isochrone.

        Returns
        -------
        QgsVectorLayer
            Couche temporaire (en mémoire), dans le système
            de coordonnées de la réponse.
        """
        # L' import fait en sorte que la classe reste utilisable en dehors de QGIS
        from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY

        # 1. Construire la forme selon le format de la géométrie
        if isinstance(self.geometrie, str):  # format WKT
            forme = QgsGeometry.fromWkt(self.geometrie)
        elif self.geometrie["type"] == "MultiPolygon":
            polygones = []
            for polygone in self.geometrie["coordinates"]:
                anneaux = []
                for anneau in polygone:
                    anneaux.append([QgsPointXY(x, y) for x, y in anneau])
                polygones.append(anneaux)
            forme = QgsGeometry.fromMultiPolygonXY(polygones)
        else:  # Polygon
            anneaux = []
            for anneau in self.geometrie["coordinates"]:
                anneaux.append([QgsPointXY(x, y) for x, y in anneau])
            forme = QgsGeometry.fromPolygonXY(anneaux)
        forme.convertToMultiType()      # Convertir en polygone en multipolygone

        # 2. Créer la couche temporaire et y mettre la forme
        couche = QgsVectorLayer(f"MultiPolygon?crs={self.crs}", "Isochrone", "memory")
        fournisseur = couche.dataProvider()
        entite = QgsFeature()
        entite.setGeometry(forme)
        fournisseur.addFeatures([entite])
        couche.updateExtents()
        couche.setOpacity(0.5)
        return couche
       

        

    

if __name__ == "__main__":
    polygone = {
        "type": "Polygon",
        "coordinates": [[[2.0, 48.0], [2.1, 48.0], [2.1, 48.1], [2.0, 48.0]]]
    }
    print(ResultatIsochrone(polygone).nombre_points())     
 
    multipolygone = {
        "type": "MultiPolygon",
        "coordinates": [
            [[[2.0, 48.0], [2.1, 48.0], [2.1, 48.1], [2.0, 48.0]]],
            [[[3.0, 48.0], [3.1, 48.0], [3.1, 48.1], [3.0, 48.1], [3.0, 48.0]]],
        ]
    }
    print(ResultatIsochrone(multipolygone).nombre_points())

    