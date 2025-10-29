import math
from app.core.domain.entities import Location
from app.core.domain.ports import DistanceCalculator
from app.infrastructure.settings import get_settings


class HaversineDistance(DistanceCalculator):
    def __init__(self, earth_radius_km: float | None = None) -> None:
        self._earth_radius_km = earth_radius_km or get_settings().earth_radius_km

    def distance_km(self, a: Location, b: Location) -> float:
        lat1 = math.radians(a.lat)
        lon1 = math.radians(a.lon)
        lat2 = math.radians(b.lat)
        lon2 = math.radians(b.lon)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(h), math.sqrt(1 - h))
        return self._earth_radius_km * c


