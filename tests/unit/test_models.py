"""Unit tests for Pydantic models."""

import pytest
from pydantic import ValidationError
from app.models import Location, Order, RouteRequest, RouteResponse
from app.schemas.route import Location as SchemaLocation, Order as SchemaOrder, RouteRequest as SchemaRouteRequest, RouteResponse as SchemaRouteResponse


class TestLocationModel:
    """Test cases for Location model."""

    def test_valid_location(self):
        """Test creating a valid location."""
        location = Location(id="test", lat=40.7128, lon=-74.0060)
        assert location.id == "test"
        assert location.lat == 40.7128
        assert location.lon == -74.0060

    def test_invalid_latitude_too_high(self):
        """Test with latitude too high."""
        with pytest.raises(ValidationError):
            Location(id="test", lat=91.0, lon=-74.0060)

    def test_invalid_latitude_too_low(self):
        """Test with latitude too low."""
        with pytest.raises(ValidationError):
            Location(id="test", lat=-91.0, lon=-74.0060)

    def test_invalid_longitude_too_high(self):
        """Test with longitude too high."""
        with pytest.raises(ValidationError):
            Location(id="test", lat=40.7128, lon=181.0)

    def test_invalid_longitude_too_low(self):
        """Test with longitude too low."""
        with pytest.raises(ValidationError):
            Location(id="test", lat=40.7128, lon=-181.0)

    def test_missing_required_fields(self):
        """Test with missing required fields."""
        with pytest.raises(ValidationError):
            Location(id="test", lat=40.7128)  # Missing lon

    def test_invalid_field_types(self):
        """Test with invalid field types."""
        with pytest.raises(ValidationError):
            Location(id="test", lat="invalid", lon=-74.0060)

    def test_edge_case_coordinates(self):
        """Test with edge case coordinates."""
        # Valid edge cases
        Location(id="test1", lat=90.0, lon=180.0)
        Location(id="test2", lat=-90.0, lon=-180.0)
        Location(id="test3", lat=0.0, lon=0.0)

    def test_serialization(self):
        """Test model serialization."""
        location = Location(id="test", lat=40.7128, lon=-74.0060)
        data = location.dict()
        assert data == {"id": "test", "lat": 40.7128, "lon": -74.0060}

    def test_deserialization(self):
        """Test model deserialization."""
        data = {"id": "test", "lat": 40.7128, "lon": -74.0060}
        location = Location(**data)
        assert location.id == "test"
        assert location.lat == 40.7128
        assert location.lon == -74.0060


class TestOrderModel:
    """Test cases for Order model."""

    def test_valid_order(self):
        """Test creating a valid order."""
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        order = Order(restaurant=restaurant, customer=customer, prep_time_mins=15.0)
        
        assert order.restaurant == restaurant
        assert order.customer == customer
        assert order.prep_time_mins == 15.0

    def test_negative_prep_time(self):
        """Test with negative prep time."""
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        
        with pytest.raises(ValidationError):
            Order(restaurant=restaurant, customer=customer, prep_time_mins=-5.0)

    def test_invalid_prep_time_type(self):
        """Test with invalid prep time type."""
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        
        with pytest.raises(ValidationError):
            Order(restaurant=restaurant, customer=customer, prep_time_mins="invalid")

    def test_zero_prep_time(self):
        """Test with zero prep time."""
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        order = Order(restaurant=restaurant, customer=customer, prep_time_mins=0.0)
        
        assert order.prep_time_mins == 0.0

    def test_large_prep_time(self):
        """Test with large prep time."""
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        order = Order(restaurant=restaurant, customer=customer, prep_time_mins=300.0)
        
        assert order.prep_time_mins == 300.0

    def test_missing_required_fields(self):
        """Test with missing required fields."""
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        
        with pytest.raises(ValidationError):
            Order(restaurant=restaurant, prep_time_mins=15.0)  # Missing customer

    def test_serialization(self):
        """Test model serialization."""
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        order = Order(restaurant=restaurant, customer=customer, prep_time_mins=15.0)
        
        data = order.dict()
        expected = {
            "restaurant": {"id": "rest1", "lat": 40.7589, "lon": -73.9851},
            "customer": {"id": "cust1", "lat": 40.7505, "lon": -73.9934},
            "prep_time_mins": 15.0
        }
        assert data == expected


class TestRouteRequestModel:
    """Test cases for RouteRequest model."""

    def test_valid_route_request(self):
        """Test creating a valid route request."""
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        order = Order(restaurant=restaurant, customer=customer, prep_time_mins=15.0)
        
        request = RouteRequest(source=source, orders=[order])
        
        assert request.source == source
        assert request.orders == [order]

    def test_empty_orders(self):
        """Test with empty orders list."""
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        request = RouteRequest(source=source, orders=[])
        
        assert request.orders == []

    def test_multiple_orders(self):
        """Test with multiple orders."""
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        orders = [
            Order(
                restaurant=Location(id=f"rest{i}", lat=40.7589, lon=-73.9851),
                customer=Location(id=f"cust{i}", lat=40.7505, lon=-73.9934),
                prep_time_mins=15.0
            )
            for i in range(3)
        ]
        
        request = RouteRequest(source=source, orders=orders)
        
        assert len(request.orders) == 3

    def test_missing_required_fields(self):
        """Test with missing required fields."""
        with pytest.raises(ValidationError):
            RouteRequest(orders=[])  # Missing source

    def test_invalid_orders_type(self):
        """Test with invalid orders type."""
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        
        with pytest.raises(ValidationError):
            RouteRequest(source=source, orders="invalid")  # Should be list

    def test_serialization(self):
        """Test model serialization."""
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        order = Order(restaurant=restaurant, customer=customer, prep_time_mins=15.0)
        request = RouteRequest(source=source, orders=[order])
        
        data = request.dict()
        assert "source" in data
        assert "orders" in data
        assert len(data["orders"]) == 1


class TestRouteResponseModel:
    """Test cases for RouteResponse model."""

    def test_valid_route_response(self):
        """Test creating a valid route response."""
        response = RouteResponse(
            best_path=["source", "rest1", "cust1"],
            total_time_mins=25.5
        )
        
        assert response.best_path == ["source", "rest1", "cust1"]
        assert response.total_time_mins == 25.5

    def test_empty_path(self):
        """Test with empty path."""
        response = RouteResponse(best_path=[], total_time_mins=0.0)
        
        assert response.best_path == []
        assert response.total_time_mins == 0.0

    def test_negative_time(self):
        """Test with negative time."""
        with pytest.raises(ValidationError):
            RouteResponse(best_path=["source"], total_time_mins=-5.0)

    def test_invalid_time_type(self):
        """Test with invalid time type."""
        with pytest.raises(ValidationError):
            RouteResponse(best_path=["source"], total_time_mins="invalid")

    def test_invalid_path_type(self):
        """Test with invalid path type."""
        with pytest.raises(ValidationError):
            RouteResponse(best_path="invalid", total_time_mins=25.5)

    def test_serialization(self):
        """Test model serialization."""
        response = RouteResponse(
            best_path=["source", "rest1", "cust1"],
            total_time_mins=25.5
        )
        
        data = response.dict()
        assert data == {
            "best_path": ["source", "rest1", "cust1"],
            "total_time_mins": 25.5
        }


class TestSchemaModels:
    """Test cases for schema models (API layer)."""

    def test_schema_location_equivalence(self):
        """Test that schema Location is equivalent to domain Location."""
        domain_loc = Location(id="test", lat=40.7128, lon=-74.0060)
        schema_loc = SchemaLocation(id="test", lat=40.7128, lon=-74.0060)
        
        assert domain_loc.dict() == schema_loc.dict()

    def test_schema_order_equivalence(self):
        """Test that schema Order is equivalent to domain Order."""
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        
        domain_order = Order(restaurant=restaurant, customer=customer, prep_time_mins=15.0)
        schema_order = SchemaOrder(restaurant=restaurant, customer=customer, prep_time_mins=15.0)
        
        assert domain_order.dict() == schema_order.dict()

    def test_schema_route_request_equivalence(self):
        """Test that schema RouteRequest is equivalent to domain RouteRequest."""
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        restaurant = Location(id="rest1", lat=40.7589, lon=-73.9851)
        customer = Location(id="cust1", lat=40.7505, lon=-73.9934)
        order = Order(restaurant=restaurant, customer=customer, prep_time_mins=15.0)
        
        domain_request = RouteRequest(source=source, orders=[order])
        schema_request = SchemaRouteRequest(source=source, orders=[order])
        
        assert domain_request.dict() == schema_request.dict()

    def test_schema_route_response_equivalence(self):
        """Test that schema RouteResponse is equivalent to domain RouteResponse."""
        domain_response = RouteResponse(
            best_path=["source", "rest1", "cust1"],
            total_time_mins=25.5
        )
        schema_response = SchemaRouteResponse(
            best_path=["source", "rest1", "cust1"],
            total_time_mins=25.5
        )
        
        assert domain_response.dict() == schema_response.dict()
