import requests
from ParametresIsochrone import ParametresIsochrone 
from Point import Point
from ResultatIsochrone import ResultatIsochrone

class ClientGeoplateforme:
    URL_CAPABILITIES = "https://data.geopf.fr/navigation/getcapabilities"
    URL_ISOCHRONE = "https://data.geopf.fr/navigation/isochrone"
    RESSOURCES_DOCUMENTEES = ["bdtopo-valhalla", "bdtopo-pgr"]
    OPTIONS_PAR_DEFAUT = {
        "profile": ["car", "pedestrian"],
        "direction": ["departure", "arrival"],
        "geometryFormat": ["geojson", "polyline", "wkt"],
        "timeUnit": ["second", "minute", "hour"],
        "distanceUnit": ["meter", "kilometer"],
        "projection": ["EPSG:4326", "EPSG:2154", "EPSG:3857"],
    }


    def __init__(self):
        self._capacites= None


    def get_capabilities(self): 
        """
              Récupère les capacités de l'API Geopf.
                     
                Returns:
               dict: La réponse de l'API sous forme de dictionnaire.       
              """
        if self._capacites is None:
            response = requests.get(self.URL_CAPABILITIES, timeout=10)
            response.raise_for_status()
            self._capacites = response.json()
        return self._capacites
       
    def calcul_isochrone(self, params: ParametresIsochrone):
        """
        Envoie une requête à l'API Geopf pour calculer les isochrones en utilisant les paramètres fournis.

        parameters:
            params (ParametresIsochrone): Les paramètres nécessaires pour le calcul des isochrones.
        Returns:
            ResultatIsochrone : le résultat du calcul.
        """

        response = requests.get(self.URL_ISOCHRONE, params=params.toDict(), timeout=10)
        if response.status_code in (502, 503, 504):
            raise ValueError("Le service de la Géoplateforme ne répond pas pour le moment. Réessayez plus tard.")
        if not response.ok:
            print(response.status_code, response.text)
        response.raise_for_status()

        reponse = response.json()
        if "geometry" not in reponse:
            print(reponse)
            raise ValueError("Le service n'a pas renvoyé de géométrie.")
        return ResultatIsochrone(reponse["geometry"], params.crs or "EPSG:4326")
   

    def get_ressources_isochrone(self):
        """Renvoie la liste des noms de ressources qui permettent le calcul d'isochrone."""
        capacites = self.get_capabilities()
        noms = []
        for r in capacites["resources"]:
            for op in r["availableOperations"]:
                    if op["id"] == "isochrone" and r["id"] in self.RESSOURCES_DOCUMENTEES:
                        noms.append(r["id"])
        return noms


    def get_options_isochrone(self, resource):
        """
        Renvoie les valeurs possibles de chaque paramètre pour une ressource,
        lues dans getCapabilities. Renvoie un dictionnaire : {nom du paramètre: [valeurs]}.
        """
        options = {}
        capacites = self.get_capabilities()
        for r in capacites["resources"]:
            if r["id"] == resource:
                for op in r["availableOperations"]:
                    if op["id"] == "isochrone":
                        for p in op["availableParameters"]:
                            if isinstance(p["values"], list):   # on garde seulement les listes de choix
                                options[p["id"]] = p["values"]
        return options
        





if __name__ == "__main__":
    """
    Tests du client Geopf pour le calcul d'isochrone afin de verifier son fonctionnement.  
    """
    client = ClientGeoplateforme()
    p = Point(2.337306, 48.849319)
    params = ParametresIsochrone(point=p, resource="bdtopo-valhalla", costValue=300, costType="time")
    resultat = client.calcul_isochrone(params)
    print(resultat.nombre_points())
    print(client.get_ressources_isochrone())
    print(client.get_options_isochrone("bdtopo-valhalla"))