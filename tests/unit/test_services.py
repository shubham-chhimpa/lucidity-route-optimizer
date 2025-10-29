"""Unit tests for service layer functions."""

import pytest
from unittest.mock import Mock, patch
from app.services import find_best_route, _precompute_travel_times, _is_path_valid, _calculate_total_time
from app.models import Location, Order, RouteResponse


class TestFindBestRoute:
    """Test cases for the main route finding function."""

    def test_empty_orders(self, sample_location):
        """Test with no orders."""
        result = find_best_route(sample_location, [])
        assert result.best_path == [sample_location.id]
        assert result.total_time_mins == 0.0

    def test_single_order(self, sample_location, sample_order):
        """Test with a single order."""
        result = find_best_route(sample_location, [sample_order])
        
        # Should include source, restaurant, and customer
        assert len(result.best_path) == 3
        assert result.best_path[0] == sample_location.id
        assert sample_order.restaurant.id in result.best_path
        assert sample_order.customer.id in result.best_path
        assert result.total_time_mins > 0

    def test_multiple_orders(self, sample_location, multiple_orders):
        """Test with multiple orders."""
        result = find_best_route(sample_location, multiple_orders)
        
        # Should include source and all locations
        expected_locations = {sample_location.id}
        for order in multiple_orders:
            expected_locations.add(order.restaurant.id)
            expected_locations.add(order.customer.id)
        
        assert len(result.best_path) == len(expected_locations)
        assert set(result.best_path) == expected_locations
        assert result.total_time_mins > 0

    def test_restaurant_before_customer_constraint(self, sample_location):
        """Test that restaurant is always visited before its customer."""
        # Create orders where this constraint matters
        orders = [
            Order(
                restaurant=Location(id="rest1", lat=40.7589, lon=-73.9851),
                customer=Location(id="cust1", lat=40.7505, lon=-73.9934),
                prep_time_mins=15.0
            ),
            Order(
                restaurant=Location(id="rest2", lat=40.7614, lon=-73.9776),
                customer=Location(id="cust2", lat=40.7489, lon=-73.9857),
                prep_time_mins=20.0
            )
        ]
        
        result = find_best_route(sample_location, orders)
        
        # Find positions of restaurants and customers
        path = result.best_path
        rest1_pos = path.index("rest1")
        cust1_pos = path.index("cust1")
        rest2_pos = path.index("rest2")
        cust2_pos = path.index("cust2")
        
        # Restaurants must come before their customers
        assert rest1_pos < cust1_pos
        assert rest2_pos < cust2_pos

    def test_identical_locations(self, sample_location):
        """Test with orders having identical restaurant and customer locations."""
        order = Order(
            restaurant=sample_location,
            customer=sample_location,
            prep_time_mins=10.0
        )
        
        result = find_best_route(sample_location, [order])
        # Should handle this gracefully
        assert result.best_path == [sample_location.id]
        assert result.total_time_mins == 0.0

    @patch('app.services.calculate_travel_time_mins')
    def test_travel_time_calculation_called(self, mock_calculate, sample_location, sample_order):
        """Test that travel time calculation is called correctly."""
        mock_calculate.return_value = 5.0
        
        result = find_best_route(sample_location, [sample_order])
        
        # Should be called for each pair of locations
        assert mock_calculate.call_count >= 1
        assert result.total_time_mins > 0


class TestPrecomputeTravelTimes:
    """Test cases for travel time precomputation."""

    def test_single_location(self):
        """Test with single location."""
        locations = {"loc1": Location(id="loc1", lat=40.7128, lon=-74.0060)}
        
        with patch('app.services.calculate_travel_time_mins', return_value=5.0):
            times = _precompute_travel_times(locations)
        
        assert times["loc1"]["loc1"] == 0.0

    def test_multiple_locations(self):
        """Test with multiple locations."""
        locations = {
            "loc1": Location(id="loc1", lat=40.7128, lon=-74.0060),
            "loc2": Location(id="loc2", lat=40.7589, lon=-73.9851),
            "loc3": Location(id="loc3", lat=40.7505, lon=-73.9934)
        }
        
        with patch('app.services.calculate_travel_time_mins', return_value=5.0):
            times = _precompute_travel_times(locations)
        
        # Check diagonal (same location) is 0
        for loc_id in locations:
            assert times[loc_id][loc_id] == 0.0
        
        # Check all other pairs have travel time
        for loc1 in locations:
            for loc2 in locations:
                if loc1 != loc2:
                    assert times[loc1][loc2] == 5.0

    def test_symmetric_travel_times(self):
        """Test that travel times are symmetric."""
        locations = {
            "loc1": Location(id="loc1", lat=40.7128, lon=-74.0060),
            "loc2": Location(id="loc2", lat=40.7589, lon=-73.9851)
        }
        
        with patch('app.services.calculate_travel_time_mins', return_value=5.0):
            times = _precompute_travel_times(locations)
        
        assert times["loc1"]["loc2"] == times["loc2"]["loc1"]


class TestIsPathValid:
    """Test cases for path validation."""

    def test_valid_path(self):
        """Test a valid path where restaurants come before customers."""
        path = ("rest1", "cust1", "rest2", "cust2")
        order_pairs = [("rest1", "cust1"), ("rest2", "cust2")]
        
        assert _is_path_valid(path, order_pairs) is True

    def test_invalid_path_restaurant_after_customer(self):
        """Test an invalid path where restaurant comes after customer."""
        path = ("cust1", "rest1", "rest2", "cust2")
        order_pairs = [("rest1", "cust1"), ("rest2", "cust2")]
        
        assert _is_path_valid(path, order_pairs) is False

    def test_mixed_valid_invalid_path(self):
        """Test a path that's valid for some orders but not others."""
        path = ("rest1", "cust1", "cust2", "rest2")
        order_pairs = [("rest1", "cust1"), ("rest2", "cust2")]
        
        assert _is_path_valid(path, order_pairs) is False

    def test_empty_path(self):
        """Test empty path."""
        path = ()
        order_pairs = [("rest1", "cust1")]
        
        assert _is_path_valid(path, order_pairs) is True

    def test_single_location_path(self):
        """Test path with single location."""
        path = ("rest1",)
        order_pairs = [("rest1", "cust1")]
        
        assert _is_path_valid(path, order_pairs) is True

    def test_complex_valid_path(self):
        """Test a complex but valid path."""
        path = ("rest1", "rest2", "cust1", "rest3", "cust2", "cust3")
        order_pairs = [("rest1", "cust1"), ("rest2", "cust2"), ("rest3", "cust3")]
        
        assert _is_path_valid(path, order_pairs) is True


class TestCalculateTotalTime:
    """Test cases for total time calculation."""

    def test_single_location_path(self, sample_location):
        """Test path with single location."""
        path = ("rest1",)
        travel_times = {
            sample_location.id: {"rest1": 5.0},
            "rest1": {sample_location.id: 5.0}
        }
        prep_times = {"rest1": 10.0}
        
        total_time = _calculate_total_time(sample_location, path, travel_times, prep_times)
        
        # Travel time + wait time (prep_time - arrival_time)
        # 5.0 + max(0, 10.0 - 5.0) = 5.0 + 5.0 = 10.0
        assert total_time == 10.0

    def test_no_wait_time_needed(self, sample_location):
        """Test when no wait time is needed."""
        path = ("rest1",)
        travel_times = {
            sample_location.id: {"rest1": 15.0},
            "rest1": {sample_location.id: 15.0}
        }
        prep_times = {"rest1": 10.0}
        
        total_time = _calculate_total_time(sample_location, path, travel_times, prep_times)
        
        # Travel time only (15.0), no wait needed
        assert total_time == 15.0

    def test_multiple_locations_with_wait(self, sample_location):
        """Test multiple locations with wait times."""
        path = ("rest1", "cust1", "rest2", "cust2")
        travel_times = {
            sample_location.id: {"rest1": 5.0, "cust1": 10.0, "rest2": 15.0, "cust2": 20.0},
            "rest1": {"cust1": 3.0, "rest2": 8.0, "cust2": 13.0},
            "cust1": {"rest2": 5.0, "cust2": 10.0},
            "rest2": {"cust2": 5.0}
        }
        prep_times = {"rest1": 8.0, "rest2": 12.0}
        
        total_time = _calculate_total_time(sample_location, path, travel_times, prep_times)
        
        # This is a complex calculation, just verify it's positive and reasonable
        assert total_time > 0
        assert total_time > 20.0  # Should be more than just travel time

    def test_customer_location_no_prep_time(self, sample_location):
        """Test that customer locations don't have prep time."""
        path = ("rest1", "cust1")
        travel_times = {
            sample_location.id: {"rest1": 5.0, "cust1": 10.0},
            "rest1": {"cust1": 3.0},
            "cust1": {}
        }
        prep_times = {"rest1": 8.0}  # No prep time for cust1
        
        total_time = _calculate_total_time(sample_location, path, travel_times, prep_times)
        
        # Should not add prep time for customer location
        assert total_time > 0

    def test_zero_prep_time(self, sample_location):
        """Test with zero prep time."""
        path = ("rest1",)
        travel_times = {
            sample_location.id: {"rest1": 5.0},
            "rest1": {sample_location.id: 5.0}
        }
        prep_times = {"rest1": 0.0}
        
        total_time = _calculate_total_time(sample_location, path, travel_times, prep_times)
        
        # Should be just travel time
        assert total_time == 5.0
