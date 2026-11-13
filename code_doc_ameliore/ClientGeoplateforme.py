"""Module ClientGeoplateforme : communication avec le service de navigation de la Géoplateforme."""

import requests
from ParametresIsochrone import ParametresIsochrone 
from Point import Point
from ResultatIsochrone import ResultatIsochrone

class ClientGeoplateforme:
    """
    Client du service de navigation de la Géoplateforme (IGN).

    Permet de lire les capacités du service (ressources, paramètres possibles)
    et de lancer un calcul d'isochrone avec la bibliothèque requests.

    Attributes
    ----------
    URL_CAPABILITIES : str
        Adresse du getCapabilities du service.
    URL_ISOCHRONE : str
        Adresse du calcul d'isochrone.
    RESSOURCES_DOCUMENTEES : list of str
        Ressources documentées par l'IGN, les seules proposées par le plugin 
        car ceux etant disponible pour la calcul.
    OPTIONS_PAR_DEFAUT : dict
        Valeurs possibles des paramètres facultatifs, utilisées si getCapabilities
        est inaccessible.
    """
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
        """Crée le client. get_capabilities sera gardé en mémoire après le premier appel."""
        self._capacites= None


    def get_capabilities(self): 
        """
        Récupère les capacités de l'API Géoplateforme.

        La réponse est gardée en mémoire : le service n'est interrogé
        qu'une seule fois par client.

        Returns
        -------
        dict
            La réponse de l'API sous forme de dictionnaire.

        Raises
        ------
        requests.exceptions.RequestException
            Si le service est inaccessible ou renvoie une erreur HTTP.
        """
        if self._capacites is None:
            response = requests.get(self.URL_CAPABILITIES, timeout=10)
            response.raise_for_status()
            self._capacites = response.json()
        return self._capacites

       
    def calcul_isochrone(self, params: ParametresIsochrone):
        """
        Envoie une requête au service pour calculer une isochrone.

        Parameters
        ----------
        params : ParametresIsochrone
            Les paramètres nécessaires au calcul.

        Returns
        -------
        ResultatIsochrone
            Le résultat du calcul.

        Raises
        ------
        ValueError
            Si le service est indisponible (502, 503, 504) ou ne renvoie pas de géométrie.
        requests.exceptions.RequestException
            Pour les autres erreurs de communication ou erreurs HTTP.
        """
        response = requests.get(self.URL_ISOCHRONE, params=params.toDict(), timeout=10)
        if response.status_code in (502, 503, 504):   # 502, 503, 504 : erreurs de passerelle, le service est indisponible
            raise ValueError("Le service de la Géoplateforme ne répond pas pour le moment. Réessayez plus tard.")
        if not response.ok:
            print(response.status_code, response.text)    # affiche le message d'erreur du service
        response.raise_for_status()
        reponse = response.json()
        if "geometry" not in reponse:
            print(reponse)
            raise ValueError("Le service n'a pas renvoyé de géométrie.")
        return ResultatIsochrone(reponse["geometry"], params.crs or "EPSG:4326")
   

    def get_ressources_isochrone(self):
        """
        Renvoie les ressources qui permettent le calcul d'isochrone
        (parmi celles documentées par l'IGN).

        Returns
        -------
        list of str
            Les noms des ressources.
        """
        capacites = self.get_capabilities()
        noms = []
        for r in capacites["resources"]:
            for op in r["availableOperations"]:
                    if op["id"] == "isochrone" and r["id"] in self.RESSOURCES_DOCUMENTEES:
                        noms.append(r["id"])
        return noms


    def get_options_isochrone(self, resource):
        """
        Renvoie les valeurs possibles de chaque paramètre d'isochrone pour une ressource,
        lues dans getCapabilities.

        Parameters
        ----------
        resource : str
            Nom de la ressource, par exemple "bdtopo-valhalla".

        Returns
        -------
        dict
            {nom du paramètre : liste des valeurs possibles}, pour les paramètres
            qui ont une liste de choix (profile, direction, geometryFormat, etc.).
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