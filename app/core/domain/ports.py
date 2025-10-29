from typing import Protocol, Iterable, Dict, Tuple, List
from .entities import Location, Order


class DistanceCalculator(Protocol):
    def distance_km(self, a: Location, b: Location) -> float: ...


class TravelTimeEstimator(Protocol):
    def minutes(self, km: float) -> float: ...


class PathGenerator(Protocol):
    def valid_paths(self, source: Location, orders: Iterable[Order]) -> Iterable[Tuple[str, ...]]: ...


class CostCalculator(Protocol):
    def total_time_mins(
        self,
        source: Location,
        path: Tuple[str, ...],
        travel_times: Dict[str, Dict[str, float]],
        prep_times: Dict[str, float],
    ) -> float: ...


class RouteOptimizer(Protocol):
    def best_route(self, source: Location, orders: Iterable[Order]) -> Tuple[List[str], float]: ...


