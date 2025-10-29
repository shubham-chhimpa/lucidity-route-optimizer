"""Test configuration and fixtures for the route optimization service."""

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.models import Location, Order
from app.schemas.route import RouteRequest, RouteResponse


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client for the FastAPI application."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


# Test data fixtures
@pytest.fixture
def sample_location() -> Location:
    """Create a sample location for testing."""
    return Location(id="loc1", lat=40.7128, lon=-74.0060)


@pytest.fixture
def sample_restaurant() -> Location:
    """Create a sample restaurant location for testing."""
    return Location(id="rest1", lat=40.7589, lon=-73.9851)


@pytest.fixture
def sample_customer() -> Location:
    """Create a sample customer location for testing."""
    return Location(id="cust1", lat=40.7505, lon=-73.9934)


@pytest.fixture
def sample_order(sample_restaurant: Location, sample_customer: Location) -> Order:
    """Create a sample order for testing."""
    return Order(
        restaurant=sample_restaurant,
        customer=sample_customer,
        prep_time_mins=15.0
    )


@pytest.fixture
def sample_route_request(sample_location: Location, sample_order: Order) -> RouteRequest:
    """Create a sample route request for testing."""
    return RouteRequest(
        source=sample_location,
        orders=[sample_order]
    )


@pytest.fixture
def multiple_orders() -> list[Order]:
    """Create multiple orders for testing complex scenarios."""
    return [
        Order(
            restaurant=Location(id="rest1", lat=40.7589, lon=-73.9851),
            customer=Location(id="cust1", lat=40.7505, lon=-73.9934),
            prep_time_mins=15.0
        ),
        Order(
            restaurant=Location(id="rest2", lat=40.7614, lon=-73.9776),
            customer=Location(id="cust2", lat=40.7489, lon=-73.9857),
            prep_time_mins=20.0
        ),
        Order(
            restaurant=Location(id="rest3", lat=40.7505, lon=-73.9934),
            customer=Location(id="cust3", lat=40.7128, lon=-74.0060),
            prep_time_mins=10.0
        )
    ]


@pytest.fixture
def complex_route_request(sample_location: Location, multiple_orders: list[Order]) -> RouteRequest:
    """Create a complex route request with multiple orders."""
    return RouteRequest(
        source=sample_location,
        orders=multiple_orders
    )


# Edge case fixtures
@pytest.fixture
def empty_route_request(sample_location: Location) -> RouteRequest:
    """Create a route request with no orders."""
    return RouteRequest(
        source=sample_location,
        orders=[]
    )


@pytest.fixture
def same_location_order() -> Order:
    """Create an order where restaurant and customer are at the same location."""
    location = Location(id="same_loc", lat=40.7128, lon=-74.0060)
    return Order(
        restaurant=location,
        customer=location,
        prep_time_mins=5.0
    )


@pytest.fixture
def zero_prep_time_order(sample_restaurant: Location, sample_customer: Location) -> Order:
    """Create an order with zero prep time."""
    return Order(
        restaurant=sample_restaurant,
        customer=sample_customer,
        prep_time_mins=0.0
    )


@pytest.fixture
def long_prep_time_order(sample_restaurant: Location, sample_customer: Location) -> Order:
    """Create an order with very long prep time."""
    return Order(
        restaurant=sample_restaurant,
        customer=sample_customer,
        prep_time_mins=120.0
    )
