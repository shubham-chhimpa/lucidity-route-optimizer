from typing import Dict, Tuple
from app.core.domain.entities import Location
from app.core.domain.ports import CostCalculator


class TimeCostCalculator(CostCalculator):
    def total_time_mins(
        self,
        source: Location,
        path: Tuple[str, ...],
        travel_times: Dict[str, Dict[str, float]],
        prep_times: Dict[str, float],
    ) -> float:
        current_time = 0.0
        current_loc_id = source.id

        for next_loc_id in path:
            travel = travel_times[current_loc_id][next_loc_id]
            arrival_time = current_time + travel
            wait_time = 0.0
            if next_loc_id in prep_times:
                prep_time = prep_times[next_loc_id]
                wait_time = max(0.0, prep_time - arrival_time)
            current_time = arrival_time + wait_time
            current_loc_id = next_loc_id

        return current_time


