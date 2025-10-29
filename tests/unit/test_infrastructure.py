"""Unit tests for infrastructure layer components."""

import pytest
import math
from app.infrastructure.distance.haversine_calculator import HaversineDistance
from app.infrastructure.distance.speed_config import ConstantSpeedEstimator
from app.core.domain.entities import Location


class TestHaversineDistance:
    """Test cases for HaversineDistance calculator."""

    def test_same_location_distance(self):
        """Test that distance between same location is zero."""
        loc = Location(id="test", lat=40.7128, lon=-74.0060)
        calculator = HaversineDistance()
        distance = calculator.distance_km(loc, loc)
        assert distance == 0.0

    def test_known_distance(self):
        """Test with known distance calculation."""
        # NYC to LA (approximately 3944 km)
        nyc = Location(id="nyc", lat=40.7128, lon=-74.0060)
        la = Location(id="la", lat=34.0522, lon=-118.2437)
        
        calculator = HaversineDistance()
        distance = calculator.distance_km(nyc, la)
        
        # Allow 5% tolerance for floating point precision
        assert 3700 <= distance <= 4200

    def test_custom_earth_radius(self):
        """Test with custom earth radius."""
        loc1 = Location(id="test1", lat=40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=40.7589, lon=-73.9851)
        
        # Use half the earth radius
        calculator = HaversineDistance(earth_radius_km=3185.5)
        distance = calculator.distance_km(loc1, loc2)
        
        # Should be half the normal distance
        normal_calculator = HaversineDistance()
        normal_distance = normal_calculator.distance_km(loc1, loc2)
        
        assert abs(distance - normal_distance / 2) < 0.1

    def test_short_distance(self):
        """Test with short distance (Manhattan to Brooklyn)."""
        manhattan = Location(id="manhattan", lat=40.7589, lon=-73.9851)
        brooklyn = Location(id="brooklyn", lat=40.6782, lon=-73.9442)
        
        calculator = HaversineDistance()
        distance = calculator.distance_km(manhattan, brooklyn)
        
        # Should be around 8-12 km
        assert 8 <= distance <= 12

    def test_antipodal_points(self):
        """Test distance between antipodal points."""
        north_pole = Location(id="north", lat=90.0, lon=0.0)
        south_pole = Location(id="south", lat=-90.0, lon=0.0)
        
        calculator = HaversineDistance()
        distance = calculator.distance_km(north_pole, south_pole)
        
        # Earth's circumference is approximately 40000 km, so antipodal distance is ~20000 km
        assert 19000 <= distance <= 21000

    def test_equator_circumference(self):
        """Test distance along equator."""
        point1 = Location(id="p1", lat=0.0, lon=0.0)
        point2 = Location(id="p2", lat=0.0, lon=180.0)
        
        calculator = HaversineDistance()
        distance = calculator.distance_km(point1, point2)
        
        # Half the Earth's circumference
        assert 19000 <= distance <= 21000

    def test_negative_coordinates(self):
        """Test with negative latitude and longitude."""
        loc1 = Location(id="test1", lat=-40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=-34.0522, lon=-118.2437)
        
        calculator = HaversineDistance()
        distance = calculator.distance_km(loc1, loc2)
        
        assert distance > 0

    def test_extreme_coordinates(self):
        """Test with extreme coordinate values."""
        loc1 = Location(id="test1", lat=89.0, lon=179.0)
        loc2 = Location(id="test2", lat=-89.0, lon=-179.0)
        
        calculator = HaversineDistance()
        distance = calculator.distance_km(loc1, loc2)
        
        assert distance > 0

    def test_symmetric_distance(self):
        """Test that distance is symmetric."""
        loc1 = Location(id="test1", lat=40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=40.7589, lon=-73.9851)
        
        calculator = HaversineDistance()
        distance1 = calculator.distance_km(loc1, loc2)
        distance2 = calculator.distance_km(loc2, loc1)
        
        assert abs(distance1 - distance2) < 0.001

    def test_precision_consistency(self):
        """Test that the same calculation gives consistent results."""
        loc1 = Location(id="test1", lat=40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=40.7589, lon=-73.9851)
        
        calculator = HaversineDistance()
        distance1 = calculator.distance_km(loc1, loc2)
        distance2 = calculator.distance_km(loc1, loc2)
        
        assert distance1 == distance2


class TestConstantSpeedEstimator:
    """Test cases for ConstantSpeedEstimator."""

    def test_zero_distance(self):
        """Test with zero distance."""
        estimator = ConstantSpeedEstimator()
        time = estimator.minutes(0.0)
        assert time == 0.0

    def test_known_distance_calculation(self):
        """Test with known distance calculation."""
        # At 20 km/h, 1 km should take 3 minutes
        estimator = ConstantSpeedEstimator(kmph=20.0)
        time = estimator.minutes(1.0)
        assert time == 3.0

    def test_custom_speed(self):
        """Test with custom speed."""
        # At 60 km/h, 1 km should take 1 minute
        estimator = ConstantSpeedEstimator(kmph=60.0)
        time = estimator.minutes(1.0)
        assert time == 1.0

    def test_long_distance(self):
        """Test with longer distance."""
        # At 20 km/h, 100 km should take 300 minutes (5 hours)
        estimator = ConstantSpeedEstimator(kmph=20.0)
        time = estimator.minutes(100.0)
        assert time == 300.0

    def test_fractional_distance(self):
        """Test with fractional distance."""
        # At 20 km/h, 0.5 km should take 1.5 minutes
        estimator = ConstantSpeedEstimator(kmph=20.0)
        time = estimator.minutes(0.5)
        assert time == 1.5

    def test_very_small_distance(self):
        """Test with very small distance."""
        # At 20 km/h, 0.001 km should take 0.003 minutes
        estimator = ConstantSpeedEstimator(kmph=20.0)
        time = estimator.minutes(0.001)
        assert time == 0.003

    def test_very_large_distance(self):
        """Test with very large distance."""
        # At 20 km/h, 10000 km should take 30000 minutes (500 hours)
        estimator = ConstantSpeedEstimator(kmph=20.0)
        time = estimator.minutes(10000.0)
        assert time == 30000.0

    def test_negative_distance(self):
        """Test with negative distance (should handle gracefully)."""
        estimator = ConstantSpeedEstimator(kmph=20.0)
        time = estimator.minutes(-1.0)
        assert time == -3.0  # Negative time for negative distance

    def test_different_speeds(self):
        """Test with different speed values."""
        # Test various speeds
        speeds = [10.0, 30.0, 50.0, 100.0]
        distance = 60.0  # 60 km
        
        for speed in speeds:
            estimator = ConstantSpeedEstimator(kmph=speed)
            time = estimator.minutes(distance)
            expected_time = (distance / speed) * 60.0
            assert abs(time - expected_time) < 0.001

    def test_precision_consistency(self):
        """Test that the same calculation gives consistent results."""
        estimator = ConstantSpeedEstimator(kmph=20.0)
        time1 = estimator.minutes(5.0)
        time2 = estimator.minutes(5.0)
        assert time1 == time2

    def test_linear_relationship(self):
        """Test that time is linearly related to distance."""
        estimator = ConstantSpeedEstimator(kmph=20.0)
        
        # Test that doubling distance doubles time
        time1 = estimator.minutes(10.0)
        time2 = estimator.minutes(20.0)
        
        assert abs(time2 - 2 * time1) < 0.001
