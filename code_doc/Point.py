class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toStr(self):
        return f"{self.x},{self.y}"

    def creer_couche(self):
        """Crée une couche QGIS du point."""
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