from pydantic import BaseModel, Field, field_validator
from typing import List
from typing import Any
try:
    # Import domain models for coercion in validators (optional)
    from app.core.domain.entities import Location as DomainLocation, Order as DomainOrder
except Exception:  # pragma: no cover - optional import for runtime
    DomainLocation = Any  # type: ignore
    DomainOrder = Any  # type: ignore


class Location(BaseModel):
    id: str
    lat: float = Field(..., ge=-90.0, le=90.0)
    lon: float = Field(..., ge=-180.0, le=180.0)


class Order(BaseModel):
    restaurant: Location
    customer: Location
    prep_time_mins: float = Field(..., ge=0.0)

    # Allow coercion from domain or other BaseModel types
    @field_validator("restaurant", "customer", mode="before")
    @classmethod
    def _coerce_location(cls, v: Any):
        if isinstance(v, Location):
            return v
        # Pydantic BaseModel from another type
        if hasattr(v, "model_dump"):
            try:
                data = v.model_dump()
                return Location(**data)
            except Exception:
                pass
        # Plain object with attributes
        if hasattr(v, "id") and hasattr(v, "lat") and hasattr(v, "lon"):
            return Location(id=getattr(v, "id"), lat=getattr(v, "lat"), lon=getattr(v, "lon"))
        # Dict input
        if isinstance(v, dict):
            return Location(**v)
        return v


class RouteRequest(BaseModel):
    source: Location
    orders: List[Order]

    @field_validator("source", mode="before")
    @classmethod
    def _coerce_source(cls, v: Any):
        return Order._coerce_location(v)  # reuse logic

    @field_validator("orders", mode="before")
    @classmethod
    def _coerce_orders(cls, v: Any):
        if v is None:
            return v
        result = []
        for item in v:
            if isinstance(item, Order):
                result.append(item)
                continue
            if hasattr(item, "model_dump"):
                try:
                    data = item.model_dump()
                    result.append(Order(**data))
                    continue
                except Exception:
                    pass
            if isinstance(item, dict):
                result.append(Order(**item))
                continue
            # Fallback: try attribute access
            if hasattr(item, "restaurant") and hasattr(item, "customer") and hasattr(item, "prep_time_mins"):
                result.append(
                    Order(
                        restaurant=Order._coerce_location(getattr(item, "restaurant")),
                        customer=Order._coerce_location(getattr(item, "customer")),
                        prep_time_mins=float(getattr(item, "prep_time_mins")),
                    )
                )
                continue
            result.append(item)
        return result


class RouteResponse(BaseModel):
    best_path: List[str]
    total_time_mins: float = Field(..., ge=0.0)


