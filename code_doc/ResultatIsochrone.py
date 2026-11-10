
class ResultatIsochrone:
    def __init__(self, geometrie):
        self.geometrie = geometrie

    def nombre_points(self):
        anneau_exterieur = self.geometrie["coordinates"][0]
        return len(anneau_exterieur)
       
    
    def creer_couche(self):
        """
        Crée une couche QGIS à partir de la géométrie de l'isochrone.
        """
        from qgis.core import QgsVectorLayer, QgsFeature, QgsGeometry, QgsPointXY

        anneaux = []
        for anneau in self.geometrie["coordinates"]:
            points = [QgsPointXY(lon, lat) for lon, lat in anneau]
            anneaux.append(points)
        forme = QgsGeometry.fromPolygonXY(anneaux)
        couche = QgsVectorLayer("Polygon?crs=EPSG:4326", "Isochrone", "memory")
        fournisseur = couche.dataProvider()
        entite = QgsFeature()
        entite.setGeometry(forme)
        fournisseur.addFeatures([entite])
        couche.updateExtents()  
        couche.setOpacity(0.5)
        return couche

    

if __name__ == "__main__":
    geometrie_test = {
        "type": "Polygon",
        "coordinates": [[[2.0, 48.0], [2.1, 48.0], [2.1, 48.1], [2.0, 48.0]]]
    }
    resultat = ResultatIsochrone(geometrie_test)
    print(resultat.nombre_points())