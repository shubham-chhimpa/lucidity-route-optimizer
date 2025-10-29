"""Unit tests for utility functions."""

import pytest
import math
from app.utils import haversine_distance, calculate_travel_time_mins
from app.models import Location


class TestHaversineDistance:
    """Test cases for haversine distance calculation."""

    def test_same_location_distance(self):
        """Test that distance between same location is zero."""
        loc = Location(id="test", lat=40.7128, lon=-74.0060)
        distance = haversine_distance(loc, loc)
        assert distance == 0.0

    def test_known_distance(self):
        """Test with known distance calculation."""
        # NYC to LA (approximately 3944 km)
        nyc = Location(id="nyc", lat=40.7128, lon=-74.0060)
        la = Location(id="la", lat=34.0522, lon=-118.2437)
        
        distance = haversine_distance(nyc, la)
        # Allow 5% tolerance for floating point precision
        assert 3700 <= distance <= 4200

    def test_short_distance(self):
        """Test with short distance (Manhattan to Brooklyn)."""
        manhattan = Location(id="manhattan", lat=40.7589, lon=-73.9851)
        brooklyn = Location(id="brooklyn", lat=40.6782, lon=-73.9442)
        
        distance = haversine_distance(manhattan, brooklyn)
        # Should be around 8-12 km
        assert 8 <= distance <= 12

    def test_antipodal_points(self):
        """Test distance between antipodal points (should be ~20000 km)."""
        north_pole = Location(id="north", lat=90.0, lon=0.0)
        south_pole = Location(id="south", lat=-90.0, lon=0.0)
        
        distance = haversine_distance(north_pole, south_pole)
        # Earth's circumference is approximately 40000 km, so antipodal distance is ~20000 km
        assert 19000 <= distance <= 21000

    def test_equator_circumference(self):
        """Test distance along equator (should be ~40000 km for full circle)."""
        point1 = Location(id="p1", lat=0.0, lon=0.0)
        point2 = Location(id="p2", lat=0.0, lon=180.0)
        
        distance = haversine_distance(point1, point2)
        # Half the Earth's circumference
        assert 19000 <= distance <= 21000

    def test_negative_coordinates(self):
        """Test with negative latitude and longitude."""
        loc1 = Location(id="test1", lat=-40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=-34.0522, lon=-118.2437)
        
        distance = haversine_distance(loc1, loc2)
        assert distance > 0

    def test_extreme_coordinates(self):
        """Test with extreme coordinate values."""
        loc1 = Location(id="test1", lat=89.0, lon=179.0)
        loc2 = Location(id="test2", lat=-89.0, lon=-179.0)
        
        distance = haversine_distance(loc1, loc2)
        assert distance > 0


class TestCalculateTravelTimeMins:
    """Test cases for travel time calculation."""

    def test_same_location_time(self):
        """Test that travel time between same location is zero."""
        loc = Location(id="test", lat=40.7128, lon=-74.0060)
        time = calculate_travel_time_mins(loc, loc)
        assert time == 0.0

    def test_short_distance_time(self):
        """Test travel time for short distance."""
        # ~1.77 km distance should take ~5.3 minutes at 20 km/h
        loc1 = Location(id="test1", lat=40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=40.7128, lon=-73.9850)  # ~1.77km east
        
        time = calculate_travel_time_mins(loc1, loc2)
        # Should be around 5.3 minutes
        assert 5.0 <= time <= 5.6

    def test_long_distance_time(self):
        """Test travel time for longer distance."""
        # NYC to LA (approximately 3944 km)
        nyc = Location(id="nyc", lat=40.7128, lon=-74.0060)
        la = Location(id="la", lat=34.0522, lon=-118.2437)
        
        time = calculate_travel_time_mins(nyc, la)
        # At 20 km/h, should be around 197 hours = 11820 minutes
        expected_time = 3700 * 60 / 20  # Using 3700 km as approximate distance
        assert expected_time * 0.9 <= time <= expected_time * 1.1

    def test_very_short_distance(self):
        """Test with very short distance (meters)."""
        loc1 = Location(id="test1", lat=40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=40.7129, lon=-74.0060)  # ~100m north
        
        time = calculate_travel_time_mins(loc1, loc2)
        # Should be very small (less than 1 minute)
        assert 0 <= time <= 1

    def test_precision_consistency(self):
        """Test that the same calculation gives consistent results."""
        loc1 = Location(id="test1", lat=40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=40.7589, lon=-73.9851)
        
        time1 = calculate_travel_time_mins(loc1, loc2)
        time2 = calculate_travel_time_mins(loc1, loc2)
        
        assert time1 == time2

    def test_commutative_property(self):
        """Test that travel time is the same regardless of direction."""
        loc1 = Location(id="test1", lat=40.7128, lon=-74.0060)
        loc2 = Location(id="test2", lat=40.7589, lon=-73.9851)
        
        time_a_to_b = calculate_travel_time_mins(loc1, loc2)
        time_b_to_a = calculate_travel_time_mins(loc2, loc1)
        
        assert abs(time_a_to_b - time_b_to_a) < 0.001  # Should be identical within floating point precision
