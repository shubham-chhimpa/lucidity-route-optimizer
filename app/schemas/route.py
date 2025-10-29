from pydantic import BaseModel
from typing import List


class Location(BaseModel):
    id: str
    lat: float
    lon: float


class Order(BaseModel):
    restaurant: Location
    customer: Location
    prep_time_mins: float


class RouteRequest(BaseModel):
    source: Location
    orders: List[Order]


class RouteResponse(BaseModel):
    best_path: List[str]
    total_time_mins: float


