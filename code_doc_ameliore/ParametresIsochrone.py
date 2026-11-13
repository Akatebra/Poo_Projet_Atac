"""Module ParametresIsochrone : les paramètres d'une requête d'isochrone."""

from Point import Point

class ParametresIsochrone:
    """
    Paramètres d'une requête envoyée au service d'isochrones de la Géoplateforme.

    Les quatre premiers sont obligatoires, les sept autres sont facultatifs :
    laissés à None, ils ne sont pas envoyés et le service utilise sa valeur par défaut.

    Attributes
    ----------
    point : Point
        Point de départ (ou d'arrivée, selon la direction).
    resource : str
        Ressource de calcul, par exemple "bdtopo-valhalla".
    costValue : float
        Valeur du coût : un temps ou une distance selon costType.
    costType : str
        Type de coût : "time" ou "distance".
    profile : str, optional
        Mode de déplacement : "car" ou "pedestrian".
    direction : str, optional
        "departure" (depuis le point) ou "arrival" (vers le point).
    constraints : str, optional
        Contraintes sur le réseau routier (pas encore proposées dans la fenêtre).
    geometryFormat : str, optional
        Format de la géométrie renvoyée : "geojson", "wkt" ou "polyline".
    distanceUnit : str, optional
        Unité de distance : "meter" ou "kilometer".
    timeUnit : str, optional
        Unité de temps : "second", "minute", "hour" ou "standard".
    crs : str, optional
        Système de coordonnées de la géométrie renvoyée, par exemple "EPSG:4326".
    """

    def __init__(self, point: Point, resource: str, costValue: float, costType: str, profile= None, direction= None, constraints= None, geometryFormat= None, distanceUnit= None, timeUnit= None, crs= None):
        """
        Parameters
        ----------
        point : Point
            Point de départ (ou d'arrivée).
        resource : str
            Ressource de calcul.
        costValue : float
            Valeur du coût.
        costType : str
            "time" ou "distance".
        profile, direction, constraints, geometryFormat, distanceUnit, timeUnit, crs : optional
            Paramètres facultatifs, voir la description des attributs de la classe.
        """
        self.point = point
        self.resource = resource
        self.costValue = costValue
        self.costType = costType
        self.profile = profile
        self.direction = direction
        self.constraints = constraints
        self.geometryFormat = geometryFormat
        self.distanceUnit = distanceUnit
        self.timeUnit = timeUnit
        self.crs = crs


    def toDict(self):
        """
        Prépare les paramètres pour la requête HTTP.

        Les paramètres facultatifs sont retirés : ils ne sont pas envoyés.

        Returns
        -------
        dict
            {nom du paramètre : valeur}, avec les noms attendus par le service.
            Le point est converti en texte "lon,lat".
        """
        parameters_dict = {
            "point": self.point.toStr(),
            "resource": self.resource,
            "costValue": self.costValue,
            "costType": self.costType,
            "profile": self.profile,
            "direction": self.direction,
            "constraints": self.constraints,
            "geometryFormat": self.geometryFormat,
            "distanceUnit": self.distanceUnit,
            "timeUnit": self.timeUnit,
            "crs": self.crs
        }
        # On filtre en gardant seulement les paramètres renseignés, les autres options etant facultatifs
        parameters_dictfiltree = {cle: valeur for cle, valeur in parameters_dict.items() if valeur is not None}
        return parameters_dictfiltree


if __name__ == "__main__":
    p = Point(2.337306, 48.849319)
    params = ParametresIsochrone(point=p, resource="bdtopo-valhalla", costValue=30, costType="time", profile= "car", timeUnit="second", crs="EPSG:4326")
    print(params.toDict())
    