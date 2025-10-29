from app.core.domain.ports import TravelTimeEstimator
from app.infrastructure.settings import get_settings


class ConstantSpeedEstimator(TravelTimeEstimator):
    def __init__(self, kmph: float | None = None) -> None:
        self._kmph = kmph or get_settings().average_speed_kmph

    def minutes(self, km: float) -> float:
        return (km / self._kmph) * 60.0


