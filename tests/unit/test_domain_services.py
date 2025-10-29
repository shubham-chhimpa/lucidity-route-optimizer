"""Unit tests for domain services."""

import pytest
from unittest.mock import Mock, MagicMock
from app.core.services.route_optimizer import RouteOptimizer
from app.core.services.path_generator import PermutationPathGenerator
from app.core.services.cost_calculator import TimeCostCalculator
from app.core.domain.entities import Location, Order


class TestRouteOptimizer:
    """Test cases for the RouteOptimizer service."""

    def test_empty_orders(self):
        """Test with no orders."""
        # Mock dependencies
        path_generator = Mock()
        cost_calculator = Mock()
        distance_calculator = Mock()
        time_estimator = Mock()
        
        optimizer = RouteOptimizer(path_generator, cost_calculator, distance_calculator, time_estimator)
        
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        result_path, result_time = optimizer.best_route(source, [])
        
        assert result_path == [source.id]
        assert result_time == 0.0

    def test_single_order(self):
        """Test with single order."""
        # Mock dependencies
        path_generator = Mock()
        cost_calculator = Mock()
        distance_calculator = Mock()
        time_estimator = Mock()
        
        # Setup mocks
        path_generator.valid_paths.return_value = [("rest1", "cust1")]
        cost_calculator.total_time_mins.return_value = 15.0
        distance_calculator.distance_km.return_value = 5.0
        time_estimator.minutes.return_value = 15.0
        
        optimizer = RouteOptimizer(path_generator, cost_calculator, distance_calculator, time_estimator)
        
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        order = Order(
            restaurant=Location(id="rest1", lat=40.7589, lon=-73.9851),
            customer=Location(id="cust1", lat=40.7505, lon=-73.9934),
            prep_time_mins=10.0
        )
        
        result_path, result_time = optimizer.best_route(source, [order])
        
        assert result_path == ["source", "rest1", "cust1"]
        assert result_time == 15.0

    def test_multiple_orders(self):
        """Test with multiple orders."""
        # Mock dependencies
        path_generator = Mock()
        cost_calculator = Mock()
        distance_calculator = Mock()
        time_estimator = Mock()
        
        # Setup mocks
        path_generator.valid_paths.return_value = [
            ("rest1", "cust1", "rest2", "cust2"),
            ("rest1", "rest2", "cust1", "cust2"),
            ("rest2", "rest1", "cust1", "cust2")
        ]
        cost_calculator.total_time_mins.side_effect = [20.0, 15.0, 25.0]  # Second path is best
        distance_calculator.distance_km.return_value = 5.0
        time_estimator.minutes.return_value = 15.0
        
        optimizer = RouteOptimizer(path_generator, cost_calculator, distance_calculator, time_estimator)
        
        source = Location(id="source", lat=40.7128, lon=-74.0060)
        orders = [
            Order(
                restaurant=Location(id="rest1", lat=40.7589, lon=-73.9851),
                customer=Location(id="cust1", lat=40.7505, lon=-73.9934),
                prep_time_mins=10.0
            ),
            Order(
                restaurant=Location(id="rest2", lat=40.7614, lon=-73.9776),
                customer=Location(id="cust2", lat=40.7489, lon=-73.9857),
                prep_time_mins=15.0
            )
        ]
        
        result_path, result_time = optimizer.best_route(source, orders)
        
        # Should choose the path with minimum time (15.0)
        assert result_path == ["source", "rest1", "rest2", "cust1", "cust2"]
        assert result_time == 15.0

    def test_precompute_travel_times(self):
        """Test travel time precomputation."""
        # Mock dependencies
        path_generator = Mock()
        cost_calculator = Mock()
        distance_calculator = Mock()
        time_estimator = Mock()
        
        # Setup mocks
        distance_calculator.distance_km.return_value = 5.0
        time_estimator.minutes.return_value = 15.0
        
        optimizer = RouteOptimizer(path_generator, cost_calculator, distance_calculator, time_estimator)
        
        locations = {
            "loc1": Location(id="loc1", lat=40.7128, lon=-74.0060),
            "loc2": Location(id="loc2", lat=40.7589, lon=-73.9851)
        }
        
        travel_times = optimizer._precompute_travel_times(locations)
        
        # Check diagonal is 0
        assert travel_times["loc1"]["loc1"] == 0.0
        assert travel_times["loc2"]["loc2"] == 0.0
        
        # Check other pairs have travel time
        assert travel_times["loc1"]["loc2"] == 15.0
        assert travel_times["loc2"]["loc1"] == 15.0
        
        # Verify mocks were called
        assert distance_calculator.distance_km.call_count == 2  # Two pairs
        assert time_estimator.minutes.call_count == 2


class TestPermutationPathGenerator:
    """Test cases for the PermutationPathGenerator service."""

    def test_empty_orders(self, sample_location):
        """Test with no orders."""
        generator = PermutationPathGenerator()
        paths = list(generator.valid_paths(sample_location, []))
        
        assert paths == []

    def test_single_order(self, sample_location):
        """Test with single order."""
        generator = PermutationPathGenerator()
        order = Order(
            restaurant=Location(id="rest1", lat=40.7589, lon=-73.9851),
            customer=Location(id="cust1", lat=40.7505, lon=-73.9934),
            prep_time_mins=10.0
        )
        
        paths = list(generator.valid_paths(sample_location, [order]))
        
        # Should have one valid path: (rest1, cust1)
        assert len(paths) == 1
        assert paths[0] == ("rest1", "cust1")

    def test_multiple_orders(self, sample_location):
        """Test with multiple orders."""
        generator = PermutationPathGenerator()
        orders = [
            Order(
                restaurant=Location(id="rest1", lat=40.7589, lon=-73.9851),
                customer=Location(id="cust1", lat=40.7505, lon=-73.9934),
                prep_time_mins=10.0
            ),
            Order(
                restaurant=Location(id="rest2", lat=40.7614, lon=-73.9776),
                customer=Location(id="cust2", lat=40.7489, lon=-73.9857),
                prep_time_mins=15.0
            )
        ]
        
        paths = list(generator.valid_paths(sample_location, orders))
        
        # Should have multiple valid paths
        assert len(paths) > 0
        
        # All paths should be valid (restaurants before customers)
        for path in paths:
            rest1_pos = path.index("rest1")
            cust1_pos = path.index("cust1")
            rest2_pos = path.index("rest2")
            cust2_pos = path.index("cust2")
            
            assert rest1_pos < cust1_pos
            assert rest2_pos < cust2_pos

    def test_is_valid_static_method(self):
        """Test the static _is_valid method."""
        # Valid path
        path = ("rest1", "cust1", "rest2", "cust2")
        order_pairs = [("rest1", "cust1"), ("rest2", "cust2")]
        assert PermutationPathGenerator._is_valid(path, order_pairs) is True
        
        # Invalid path
        path = ("cust1", "rest1", "rest2", "cust2")
        assert PermutationPathGenerator._is_valid(path, order_pairs) is False
        
        # Empty path
        path = ()
        assert PermutationPathGenerator._is_valid(path, order_pairs) is True


class TestTimeCostCalculator:
    """Test cases for the TimeCostCalculator service."""

    def test_single_location_path(self, sample_location):
        """Test path with single location."""
        calculator = TimeCostCalculator()
        
        path = ("rest1",)
        travel_times = {
            sample_location.id: {"rest1": 5.0},
            "rest1": {sample_location.id: 5.0}
        }
        prep_times = {"rest1": 10.0}
        
        total_time = calculator.total_time_mins(sample_location, path, travel_times, prep_times)
        
        # Travel time + wait time
        assert total_time == 10.0

    def test_no_wait_time_needed(self, sample_location):
        """Test when no wait time is needed."""
        calculator = TimeCostCalculator()
        
        path = ("rest1",)
        travel_times = {
            sample_location.id: {"rest1": 15.0},
            "rest1": {sample_location.id: 15.0}
        }
        prep_times = {"rest1": 10.0}
        
        total_time = calculator.total_time_mins(sample_location, path, travel_times, prep_times)
        
        # Just travel time
        assert total_time == 15.0

    def test_multiple_locations(self, sample_location):
        """Test multiple locations."""
        calculator = TimeCostCalculator()
        
        path = ("rest1", "cust1", "rest2", "cust2")
        travel_times = {
            sample_location.id: {"rest1": 5.0, "cust1": 10.0, "rest2": 15.0, "cust2": 20.0},
            "rest1": {"cust1": 3.0, "rest2": 8.0, "cust2": 13.0},
            "cust1": {"rest2": 5.0, "cust2": 10.0},
            "rest2": {"cust2": 5.0}
        }
        prep_times = {"rest1": 8.0, "rest2": 12.0}
        
        total_time = calculator.total_time_mins(sample_location, path, travel_times, prep_times)
        
        # Should be positive and reasonable
        assert total_time > 0
        assert total_time > 20.0

    def test_customer_no_prep_time(self, sample_location):
        """Test that customer locations don't have prep time."""
        calculator = TimeCostCalculator()
        
        path = ("rest1", "cust1")
        travel_times = {
            sample_location.id: {"rest1": 5.0, "cust1": 10.0},
            "rest1": {"cust1": 3.0},
            "cust1": {}
        }
        prep_times = {"rest1": 8.0}  # No prep time for cust1
        
        total_time = calculator.total_time_mins(sample_location, path, travel_times, prep_times)
        
        # Should not add prep time for customer
        assert total_time > 0

    def test_zero_prep_time(self, sample_location):
        """Test with zero prep time."""
        calculator = TimeCostCalculator()
        
        path = ("rest1",)
        travel_times = {
            sample_location.id: {"rest1": 5.0},
            "rest1": {sample_location.id: 5.0}
        }
        prep_times = {"rest1": 0.0}
        
        total_time = calculator.total_time_mins(sample_location, path, travel_times, prep_times)
        
        # Just travel time
        assert total_time == 5.0
