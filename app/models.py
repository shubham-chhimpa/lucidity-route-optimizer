from pydantic import BaseModel, Field
from typing import List


class Location(BaseModel):
    """Represents a single geo-location[cite: 9]."""
    id: str
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)


class Order(BaseModel):
    """Represents a single order with its locations and prep time."""
    restaurant: Location
    customer: Location
    prep_time_mins: float = Field(..., ge=0.0)  # Corresponds to pt1, pt2, etc. [cite: 12, 13]


class RouteRequest(BaseModel):
    """The request body for the /find-route endpoint."""
    source: Location
    orders: List[Order]


class RouteResponse(BaseModel):
    """The response body for the /find-route endpoint."""
    best_path: List[str]
    total_time_mins: float = Field(..., ge=0.0)
