
class ResultatIsochrone:
    def __init__(self, geometrie):
        self.geometrie = geometrie

    def nombre_points(self):
        anneau_exterieur = self.geometrie["coordinates"][0]
        return len(anneau_exterieur)
       
    
    def creer_couche(self):
        pass



if __name__ == "__main__":
    geometrie_test = {
        "type": "Polygon",
        "coordinates": [[[2.0, 48.0], [2.1, 48.0], [2.1, 48.1], [2.0, 48.0]]]
    }
    resultat = ResultatIsochrone(geometrie_test)
    print(resultat.nombre_points())