"""Factory classes for creating test data using factory_boy."""

import factory
from factory.fuzzy import FuzzyFloat, FuzzyChoice
from app.core.domain.entities import Location, Order
from app.schemas.route import RouteRequest, RouteResponse


class LocationFactory(factory.Factory):
    """Factory for creating Location entities."""
    
    class Meta:
        model = Location
    
    id = factory.Sequence(lambda n: f"loc_{n}")
    lat = FuzzyFloat(-90.0, 90.0)
    lon = FuzzyFloat(-180.0, 180.0)


class OrderFactory(factory.Factory):
    """Factory for creating Order entities."""
    
    class Meta:
        model = Order
    
    restaurant = factory.SubFactory(LocationFactory)
    customer = factory.SubFactory(LocationFactory)
    prep_time_mins = FuzzyFloat(0.0, 60.0)


class RouteRequestFactory(factory.Factory):
    """Factory for creating RouteRequest objects."""
    
    class Meta:
        model = RouteRequest
    
    source = factory.SubFactory(LocationFactory)
    orders = factory.List([factory.SubFactory(OrderFactory) for _ in range(3)])


class RouteResponseFactory(factory.Factory):
    """Factory for creating RouteResponse objects."""
    
    class Meta:
        model = RouteResponse
    
    best_path = factory.List([factory.Sequence(lambda n: f"loc_{n}") for _ in range(5)])
    total_time_mins = FuzzyFloat(0.0, 300.0)


# Specialized factories for specific test scenarios
class ManhattanLocationFactory(LocationFactory):
    """Factory for locations in Manhattan, NYC."""
    
    lat = FuzzyFloat(40.7, 40.8)
    lon = FuzzyFloat(-74.0, -73.9)


class BrooklynLocationFactory(LocationFactory):
    """Factory for locations in Brooklyn, NYC."""
    
    lat = FuzzyFloat(40.6, 40.7)
    lon = FuzzyFloat(-74.0, -73.9)


class QuickPrepOrderFactory(OrderFactory):
    """Factory for orders with quick prep times."""
    
    prep_time_mins = FuzzyFloat(0.0, 10.0)


class SlowPrepOrderFactory(OrderFactory):
    """Factory for orders with slow prep times."""
    
    prep_time_mins = FuzzyFloat(30.0, 120.0)


class SingleOrderRequestFactory(factory.Factory):
    """Factory for route requests with single order."""
    
    class Meta:
        model = RouteRequest
    
    source = factory.SubFactory(LocationFactory)
    orders = factory.List([factory.SubFactory(OrderFactory)])


class EmptyOrderRequestFactory(factory.Factory):
    """Factory for route requests with no orders."""
    
    class Meta:
        model = RouteRequest
    
    source = factory.SubFactory(LocationFactory)
    orders = factory.List([])


class LargeOrderRequestFactory(factory.Factory):
    """Factory for route requests with many orders."""
    
    class Meta:
        model = RouteRequest
    
    source = factory.SubFactory(LocationFactory)
    orders = factory.List([factory.SubFactory(OrderFactory) for _ in range(10)])


# Geographic test data
class NYCGeographicFactory:
    """Factory for NYC-specific geographic test data."""
    
    @staticmethod
    def manhattan_restaurant():
        """Create a restaurant in Manhattan."""
        return LocationFactory(
            id="manhattan_rest",
            lat=40.7589,
            lon=-73.9851
        )
    
    @staticmethod
    def brooklyn_customer():
        """Create a customer in Brooklyn."""
        return LocationFactory(
            id="brooklyn_cust",
            lat=40.6782,
            lon=-73.9442
        )
    
    @staticmethod
    def queens_restaurant():
        """Create a restaurant in Queens."""
        return LocationFactory(
            id="queens_rest",
            lat=40.7282,
            lon=-73.7949
        )
    
    @staticmethod
    def bronx_customer():
        """Create a customer in the Bronx."""
        return LocationFactory(
            id="bronx_cust",
            lat=40.8448,
            lon=-73.8648
        )
    
    @staticmethod
    def staten_island_source():
        """Create a source location in Staten Island."""
        return LocationFactory(
            id="staten_source",
            lat=40.5795,
            lon=-74.1502
        )


class EdgeCaseFactory:
    """Factory for edge case test data."""
    
    @staticmethod
    def same_location_order():
        """Create an order where restaurant and customer are at the same location."""
        location = LocationFactory()
        return OrderFactory(
            restaurant=location,
            customer=location,
            prep_time_mins=5.0
        )
    
    @staticmethod
    def zero_prep_time_order():
        """Create an order with zero prep time."""
        return OrderFactory(prep_time_mins=0.0)
    
    @staticmethod
    def very_long_prep_time_order():
        """Create an order with very long prep time."""
        return OrderFactory(prep_time_mins=300.0)
    
    @staticmethod
    def antipodal_locations():
        """Create locations at antipodal points."""
        return (
            LocationFactory(id="north_pole", lat=90.0, lon=0.0),
            LocationFactory(id="south_pole", lat=-90.0, lon=0.0)
        )
    
    @staticmethod
    def equator_locations():
        """Create locations on the equator."""
        return (
            LocationFactory(id="equator_1", lat=0.0, lon=0.0),
            LocationFactory(id="equator_2", lat=0.0, lon=180.0)
        )
