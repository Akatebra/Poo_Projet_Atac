import requests
from ParametresIsochrone import ParametresIsochrone 
from Point import Point
from ResultatIsochrone import ResultatIsochrone

class ClientGeoplateforme:
       URL_CAPABILITIES = "https://data.geopf.fr/navigation/getcapabilities"
       URL_ISOCHRONE = "https://data.geopf.fr/navigation/isochrone"


       def get_capabilities(self):
               """
               Récupère les capacités de l'API Geopf.
       
               Returns:
                   dict: La réponse de l'API sous forme de dictionnaire.
               """
               response = requests.get(self.URL_CAPABILITIES, timeout=10)
               response.raise_for_status()
               return response.json()
       
       def calcul_isochrone(self, params: ParametresIsochrone):
        """
        Envoie une requête à l'API Geopf pour calculer les isochrones en utilisant les paramètres fournis.

        parameters:
            params (ParametresIsochrone): Les paramètres nécessaires pour le calcul des isochrones.
        Returns:
            ResultatIsochrone : le résultat du calcul.
        """

        response = requests.get(self.URL_ISOCHRONE, params=params.toDict(), timeout=10)
        if not response.ok:
            print(response.status_code, response.text)
        reponse = response.json()
        return ResultatIsochrone(reponse["geometry"])

       
       





if __name__ == "__main__":
    client = ClientGeoplateforme()
    p = Point(2.337306, 48.849319)
    params = ParametresIsochrone(point=p, resource="bdtopo-valhalla", costValue=30, costType="time", timeUnit="minute", crs="EPSG:4326")
    resultat = client.calcul_isochrone(params)
    print(resultat.nombre_points())
    capacites = client.get_capabilities()
    ressources = capacites["resources"]
    for r in ressources:
         print(r["id"], r["availableOperations"])
    print(ressources[0].keys())