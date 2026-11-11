from Point import Point
class ParametresIsochrone:
    def __init__(self, point: Point, resource: str, costValue: float, costType: str, profile= None, direction= None, constraints= None, geometryFormat= None, distanceUnit= None, timeUnit= None, crs= None):
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
        parameters_dictfiltree = {cle: valeur for cle, valeur in parameters_dict.items() if valeur is not None}
        return parameters_dictfiltree


if __name__ == "__main__":
    p = Point(2.337306, 48.849319)
    params = ParametresIsochrone(point=p, resource="bdtopo-valhalla", costValue=30, costType="time", profile= "car", timeUnit="second", crs="EPSG:4326")
    print(params.toDict())
    