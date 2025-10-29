from pydantic import BaseModel


class Location(BaseModel):
    id: str
    lat: float
    lon: float


class Order(BaseModel):
    restaurant: Location
    customer: Location
    prep_time_mins: float


