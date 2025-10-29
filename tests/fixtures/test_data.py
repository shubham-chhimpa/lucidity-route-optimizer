"""Static test data for use in tests."""

from app.core.domain.entities import Location, Order
from app.schemas.route import RouteRequest, RouteResponse


# Real-world NYC locations for realistic testing
NYC_LOCATIONS = {
    "times_square": Location(id="times_square", lat=40.7580, lon=-73.9855),
    "central_park": Location(id="central_park", lat=40.7829, lon=-73.9654),
    "brooklyn_bridge": Location(id="brooklyn_bridge", lat=40.7061, lon=-73.9969),
    "statue_of_liberty": Location(id="statue_of_liberty", lat=40.6892, lon=-74.0445),
    "jfk_airport": Location(id="jfk_airport", lat=40.6413, lon=-73.7781),
    "lga_airport": Location(id="lga_airport", lat=40.7769, lon=-73.8740),
    "yankee_stadium": Location(id="yankee_stadium", lat=40.8296, lon=-73.9262),
    "coney_island": Location(id="coney_island", lat=40.5749, lon=-73.9857),
    "wall_street": Location(id="wall_street", lat=40.7074, lon=-74.0113),
    "high_line": Location(id="high_line", lat=40.7480, lon=-74.0048),
}

# Sample restaurants in NYC
NYC_RESTAURANTS = {
    "pizza_place_1": Location(id="pizza_1", lat=40.7589, lon=-73.9851),
    "pizza_place_2": Location(id="pizza_2", lat=40.7614, lon=-73.9776),
    "burger_joint": Location(id="burger_1", lat=40.7505, lon=-73.9934),
    "sushi_bar": Location(id="sushi_1", lat=40.7489, lon=-73.9857),
    "italian_restaurant": Location(id="italian_1", lat=40.7128, lon=-74.0060),
}

# Sample customer locations in NYC
NYC_CUSTOMERS = {
    "apartment_1": Location(id="apt_1", lat=40.7505, lon=-73.9934),
    "apartment_2": Location(id="apt_2", lat=40.7489, lon=-73.9857),
    "office_1": Location(id="office_1", lat=40.7128, lon=-74.0060),
    "office_2": Location(id="office_2", lat=40.7580, lon=-73.9855),
    "house_1": Location(id="house_1", lat=40.6782, lon=-73.9442),
}

# Sample orders with realistic prep times
SAMPLE_ORDERS = [
    Order(
        restaurant=NYC_RESTAURANTS["pizza_place_1"],
        customer=NYC_CUSTOMERS["apartment_1"],
        prep_time_mins=15.0
    ),
    Order(
        restaurant=NYC_RESTAURANTS["burger_joint"],
        customer=NYC_CUSTOMERS["office_1"],
        prep_time_mins=10.0
    ),
    Order(
        restaurant=NYC_RESTAURANTS["sushi_bar"],
        customer=NYC_CUSTOMERS["apartment_2"],
        prep_time_mins=25.0
    ),
    Order(
        restaurant=NYC_RESTAURANTS["italian_restaurant"],
        customer=NYC_CUSTOMERS["house_1"],
        prep_time_mins=20.0
    ),
]

# Sample route requests
SAMPLE_ROUTE_REQUESTS = {
    "single_order": RouteRequest(
        source=NYC_LOCATIONS["times_square"],
        orders=[SAMPLE_ORDERS[0]]
    ),
    "multiple_orders": RouteRequest(
        source=NYC_LOCATIONS["central_park"],
        orders=SAMPLE_ORDERS[:3]
    ),
    "empty_orders": RouteRequest(
        source=NYC_LOCATIONS["brooklyn_bridge"],
        orders=[]
    ),
    "large_request": RouteRequest(
        source=NYC_LOCATIONS["jfk_airport"],
        orders=SAMPLE_ORDERS
    ),
}

# Edge case test data
EDGE_CASE_ORDERS = [
    # Same location order
    Order(
        restaurant=NYC_LOCATIONS["times_square"],
        customer=NYC_LOCATIONS["times_square"],
        prep_time_mins=5.0
    ),
    # Zero prep time
    Order(
        restaurant=NYC_RESTAURANTS["pizza_place_1"],
        customer=NYC_CUSTOMERS["apartment_1"],
        prep_time_mins=0.0
    ),
    # Very long prep time
    Order(
        restaurant=NYC_RESTAURANTS["sushi_bar"],
        customer=NYC_CUSTOMERS["office_2"],
        prep_time_mins=120.0
    ),
    # Very short prep time
    Order(
        restaurant=NYC_RESTAURANTS["burger_joint"],
        customer=NYC_CUSTOMERS["house_1"],
        prep_time_mins=0.1
    ),
]

# Performance test data
PERFORMANCE_TEST_DATA = {
    "small": {
        "orders": SAMPLE_ORDERS[:2],
        "expected_max_time": 1.0
    },
    "medium": {
        "orders": SAMPLE_ORDERS,
        "expected_max_time": 2.0
    },
    "large": {
        "orders": SAMPLE_ORDERS * 3,  # 12 orders
        "expected_max_time": 10.0
    },
}

# Geographic test data for distance calculations
GEOGRAPHIC_TEST_DATA = {
    "short_distance": {
        "loc1": Location(id="loc1", lat=40.7128, lon=-74.0060),
        "loc2": Location(id="loc2", lat=40.7130, lon=-74.0062),
        "expected_distance_km": 0.2
    },
    "medium_distance": {
        "loc1": Location(id="loc1", lat=40.7128, lon=-74.0060),
        "loc2": Location(id="loc2", lat=40.7589, lon=-73.9851),
        "expected_distance_km": 8.0
    },
    "long_distance": {
        "loc1": Location(id="nyc", lat=40.7128, lon=-74.0060),
        "loc2": Location(id="la", lat=34.0522, lon=-118.2437),
        "expected_distance_km": 3944.0
    },
    "antipodal": {
        "loc1": Location(id="north_pole", lat=90.0, lon=0.0),
        "loc2": Location(id="south_pole", lat=-90.0, lon=0.0),
        "expected_distance_km": 20015.0
    },
}

# Validation test data
VALIDATION_TEST_DATA = {
    "valid_coordinates": [
        {"lat": 0.0, "lon": 0.0},
        {"lat": 90.0, "lon": 180.0},
        {"lat": -90.0, "lon": -180.0},
        {"lat": 40.7128, "lon": -74.0060},
    ],
    "invalid_coordinates": [
        {"lat": 91.0, "lon": 0.0},  # Latitude too high
        {"lat": -91.0, "lon": 0.0},  # Latitude too low
        {"lat": 0.0, "lon": 181.0},  # Longitude too high
        {"lat": 0.0, "lon": -181.0},  # Longitude too low
        {"lat": "invalid", "lon": 0.0},  # Non-numeric latitude
        {"lat": 0.0, "lon": "invalid"},  # Non-numeric longitude
    ],
    "valid_prep_times": [0.0, 5.0, 15.0, 30.0, 60.0, 120.0],
    "invalid_prep_times": [-1.0, -10.0, "invalid", None],
}

# Mock response data for testing
MOCK_RESPONSES = {
    "single_order_success": RouteResponse(
        best_path=["source", "rest1", "cust1"],
        total_time_mins=25.5
    ),
    "multiple_orders_success": RouteResponse(
        best_path=["source", "rest1", "rest2", "cust1", "cust2"],
        total_time_mins=45.2
    ),
    "empty_orders_success": RouteResponse(
        best_path=["source"],
        total_time_mins=0.0
    ),
    "error_response": {
        "detail": "Invalid request payload",
        "errors": [
            {
                "loc": ["body", "source", "lat"],
                "msg": "value is not a valid float",
                "type": "type_error.float"
            }
        ]
    }
}

# Test scenarios for different business cases
BUSINESS_SCENARIOS = {
    "rush_hour": {
        "description": "High traffic scenario with longer travel times",
        "orders": SAMPLE_ORDERS[:2],
        "prep_times": [5.0, 8.0],  # Faster prep times
        "expected_behavior": "Should prioritize orders with shorter prep times"
    },
    "off_peak": {
        "description": "Low traffic scenario with normal travel times",
        "orders": SAMPLE_ORDERS,
        "prep_times": [15.0, 20.0, 25.0, 30.0],
        "expected_behavior": "Should optimize for shortest total route"
    },
    "mixed_prep_times": {
        "description": "Mix of fast and slow prep times",
        "orders": SAMPLE_ORDERS,
        "prep_times": [5.0, 60.0, 10.0, 45.0],
        "expected_behavior": "Should balance prep times with travel efficiency"
    },
    "same_area_delivery": {
        "description": "All locations in same neighborhood",
        "orders": [
            Order(
                restaurant=Location(id="rest1", lat=40.7589, lon=-73.9851),
                customer=Location(id="cust1", lat=40.7590, lon=-73.9852),
                prep_time_mins=15.0
            ),
            Order(
                restaurant=Location(id="rest2", lat=40.7591, lon=-73.9853),
                customer=Location(id="cust2", lat=40.7592, lon=-73.9854),
                prep_time_mins=20.0
            )
        ],
        "expected_behavior": "Should minimize travel between nearby locations"
    }
}
