from fastapi import Depends
from app.core.services.route_optimizer import RouteOptimizer
from app.core.services.path_generator import PermutationPathGenerator
from app.core.services.cost_calculator import TimeCostCalculator
from app.infrastructure.distance.haversine_calculator import HaversineDistance
from app.infrastructure.distance.speed_config import ConstantSpeedEstimator
from app.infrastructure.settings import get_settings


def get_route_optimizer(settings=Depends(get_settings)) -> RouteOptimizer:
    paths = PermutationPathGenerator()
    cost = TimeCostCalculator()
    dist = HaversineDistance(earth_radius_km=settings.earth_radius_km)
    time = ConstantSpeedEstimator(kmph=settings.average_speed_kmph)
    return RouteOptimizer(paths, cost, dist, time)


