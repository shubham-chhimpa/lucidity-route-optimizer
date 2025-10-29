from typing import Iterable, Tuple, Dict, List
from app.core.domain.entities import Location, Order
from app.core.domain.ports import PathGenerator, CostCalculator, DistanceCalculator, TravelTimeEstimator, RouteOptimizer as RouteOptimizerPort


class RouteOptimizer(RouteOptimizerPort):
    def __init__(
        self,
        path_generator: PathGenerator,
        cost_calculator: CostCalculator,
        distance_calculator: DistanceCalculator,
        time_estimator: TravelTimeEstimator,
    ) -> None:
        self._paths = path_generator
        self._cost = cost_calculator
        self._dist = distance_calculator
        self._time = time_estimator

    def best_route(self, source: Location, orders: Iterable[Order]) -> Tuple[List[str], float]:
        orders_list = list(orders)
        locations: Dict[str, Location] = {source.id: source}
        prep_times: Dict[str, float] = {}

        for o in orders_list:
            locations[o.restaurant.id] = o.restaurant
            locations[o.customer.id] = o.customer
            prep_times[o.restaurant.id] = o.prep_time_mins

        travel_times = self._precompute_travel_times(locations)

        valid_paths = list(self._paths.valid_paths(source, orders_list))
        if not valid_paths:
            return [source.id], 0.0

        min_time = float("inf")
        best_path: List[str] = []
        for path in valid_paths:
            t = self._cost.total_time_mins(source, path, travel_times, prep_times)
            if t < min_time:
                min_time = t
                best_path = [source.id] + list(path)

        return best_path, min_time

    def _precompute_travel_times(self, locations: Dict[str, Location]) -> Dict[str, Dict[str, float]]:
        times: Dict[str, Dict[str, float]] = {}
        ids = list(locations.keys())
        for a in ids:
            times[a] = {}
            for b in ids:
                if a == b:
                    times[a][b] = 0.0
                else:
                    km = self._dist.distance_km(locations[a], locations[b])
                    times[a][b] = self._time.minutes(km)
        return times


