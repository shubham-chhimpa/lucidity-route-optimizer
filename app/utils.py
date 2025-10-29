import math
from app.models import Location
from app.config import AVERAGE_SPEED_KMPH, EARTH_RADIUS_KM


def haversine_distance(loc1: Location, loc2: Location) -> float:
    """
    Calculate the great-circle distance between two points
    on the earth (specified in decimal degrees) using the
    Haversine formula.
    """
    lat1_rad = math.radians(loc1.lat)
    lon1_rad = math.radians(loc1.lon)
    lat2_rad = math.radians(loc2.lat)
    lon2_rad = math.radians(loc2.lon)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = EARTH_RADIUS_KM * c
    return distance_km


def calculate_travel_time_mins(loc1: Location, loc2: Location) -> float:
    """
    Calculates the travel time in minutes between two locations
    based on Haversine distance and average speed.
    """
    distance_km = haversine_distance(loc1, loc2)
    time_hours = distance_km / AVERAGE_SPEED_KMPH
    time_minutes = time_hours * 60
    return time_minutes
