import itertools
import logging
from typing import List, Dict, Tuple
from app.models import Location, Order, RouteResponse
from app.utils import calculate_travel_time_mins


logger = logging.getLogger(__name__)


def find_best_route(source: Location, orders: List[Order]) -> RouteResponse:
    """
    Finds the optimal route by checking all valid permutations
    of pickups and deliveries.
    """
    logger.info("Computing best route | source=%s | num_orders=%d", source.id, len(orders))
    # 1. Build a map of all unique locations
    locations = {source.id: source}
    prep_times = {}
    order_pairs = []  # List of (restaurant_id, customer_id)

    for order in orders:
        locations[order.restaurant.id] = order.restaurant
        locations[order.customer.id] = order.customer

        # Store prep time keyed by restaurant ID
        prep_times[order.restaurant.id] = order.prep_time_mins

        # Store the (R, C) relationship
        order_pairs.append((order.restaurant.id, order.customer.id))

    # 2. Precompute all travel times between all locations
    travel_times = _precompute_travel_times(locations)

    # 3. Generate all valid permutations
    # A path is valid if R_i is visited before C_i for all orders
    waypoints = [loc_id for loc_id in locations if loc_id != source.id]
    all_permutations = itertools.permutations(waypoints)

    valid_paths = []
    for path in all_permutations:
        if _is_path_valid(path, order_pairs):
            valid_paths.append(path)

    # 4. Calculate total time for each valid path and find the minimum
    min_time = float('inf')
    best_path = []

    if not valid_paths:
        # Handle edge case of 0 orders
        return RouteResponse(best_path=[source.id], total_time_mins=0)

    for path in valid_paths:
        current_time = _calculate_total_time(
            source,
            path,
            travel_times,
            prep_times
        )

        if current_time < min_time:
            min_time = current_time
            best_path = [source.id] + list(path)
    logger.info("Best route computed | path=%s | total_time_mins=%.4f", best_path, min_time)
    return RouteResponse(best_path=best_path, total_time_mins=min_time)


def _precompute_travel_times(locations: Dict[str, Location]) -> Dict[str, Dict[str, float]]:
    """
    Creates a 2D dictionary (adjacency matrix) of travel times
    between all pairs of locations.
    """
    times = {}
    loc_ids = list(locations.keys())
    for id1 in loc_ids:
        times[id1] = {}
        for id2 in loc_ids:
            if id1 == id2:
                times[id1][id2] = 0.0
            else:
                times[id1][id2] = calculate_travel_time_mins(
                    locations[id1], locations[id2]
                )
    return times


def _is_path_valid(path: Tuple[str], order_pairs: List[Tuple[str, str]]) -> bool:
    """
    Checks if a permutation is valid, i.e., all R_i come before C_i.
    """
    path_indices = {loc_id: index for index, loc_id in enumerate(path)}

    for r_id, c_id in order_pairs:
        if path_indices[r_id] > path_indices[c_id]:
            return False
    return True


def _calculate_total_time(
        source: Location,
        path: Tuple[str],
        travel_times: Dict[str, Dict[str, float]],
        prep_times: Dict[str, float]
) -> float:
    """
    Calculates the total time for a single path, including wait times.
    All restaurants start prep at t=0[cite: 16, 17].
    """
    current_time = 0.0
    current_loc_id = source.id

    for next_loc_id in path:
        # 1. Add travel time from current location to the next one
        travel = travel_times[current_loc_id][next_loc_id]
        arrival_time = current_time + travel

        # 2. Check if the next location is a restaurant and if we must wait
        wait_time = 0.0
        if next_loc_id in prep_times:
            prep_time = prep_times[next_loc_id]
            # Wait time is the difference, if prep time is > arrival time
            wait_time = max(0, prep_time - arrival_time)

        # 3. Update current time
        # The new time is when we *leave* this location
        current_time = arrival_time + wait_time

        # 4. Update current location
        current_loc_id = next_loc_id

    # The final `current_time` is the arrival time at the last customer
    return current_time
