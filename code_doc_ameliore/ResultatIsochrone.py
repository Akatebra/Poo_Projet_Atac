
class ResultatIsochrone:
    def __init__(self, geometrie, crs="EPSG:4326"):
        self.geometrie = geometrie
        self.crs = crs

    def nombre_points(self):
        if isinstance(self.geometrie, str):  # format WKT
            from qgis.core import QgsGeometry
            return QgsGeometry.fromWkt(self.geometrie).constGet().nCoordinates()
        if self.geometrie["type"] == "MultiPolygon":
            return sum(len(polygone[0]) for polygone in self.geometrie["coordinates"])
        return len(self.geometrie["coordinates"][0])
       
    
    def creer_couche(self):
        """
        Crée une couche QGIS à partir de la géométrie de l'isochrone.
        """

        from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY
 
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
 
        forme.convertToMultiType()
 
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
    print(ResultatIsochrone(polygone).nombre_points())      # 4
 
    multipolygone = {
        "type": "MultiPolygon",
        "coordinates": [
            [[[2.0, 48.0], [2.1, 48.0], [2.1, 48.1], [2.0, 48.0]]],
            [[[3.0, 48.0], [3.1, 48.0], [3.1, 48.1], [3.0, 48.1], [3.0, 48.0]]],
        ]
    }
    print(ResultatIsochrone(multipolygone).nombre_points())

    