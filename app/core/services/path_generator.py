import itertools
from typing import Iterable, Tuple, List
from app.core.domain.entities import Location, Order
from app.core.domain.ports import PathGenerator


class PermutationPathGenerator(PathGenerator):
    def valid_paths(self, source: Location, orders: Iterable[Order]) -> Iterable[Tuple[str, ...]]:
        locations = {source.id: source}
        order_pairs: List[Tuple[str, str]] = []
        for o in orders:
            locations[o.restaurant.id] = o.restaurant
            locations[o.customer.id] = o.customer
            order_pairs.append((o.restaurant.id, o.customer.id))

        waypoints = [loc_id for loc_id in locations if loc_id != source.id]
        for path in itertools.permutations(waypoints):
            if self._is_valid(path, order_pairs):
                yield path

    @staticmethod
    def _is_valid(path: Tuple[str, ...], order_pairs: List[Tuple[str, str]]) -> bool:
        index_of = {lid: i for i, lid in enumerate(path)}
        for r_id, c_id in order_pairs:
            if index_of[r_id] > index_of[c_id]:
                return False
        return True


