# Test Suite Documentation

This directory contains comprehensive tests for the Route Optimization Service, following production best practices.

## Test Structure

```
tests/
├── conftest.py                 # Global test configuration and fixtures
├── fixtures/                   # Test data and factories
│   ├── factories.py           # Factory classes for generating test data
│   └── test_data.py           # Static test data and scenarios
├── integration/               # Integration tests
│   └── test_api_endpoints.py  # API endpoint tests
├── unit/                      # Unit tests
│   ├── test_domain_services.py # Domain service tests
│   ├── test_infrastructure.py  # Infrastructure layer tests
│   ├── test_models.py         # Pydantic model tests
│   ├── test_services.py       # Service layer tests
│   └── test_utils.py          # Utility function tests
└── README.md                  # This file
```

## Test Categories

### Unit Tests (`tests/unit/`)

- **test_utils.py**: Tests for utility functions (Haversine distance, travel time calculation)
- **test_services.py**: Tests for service layer functions (route finding, path validation)
- **test_domain_services.py**: Tests for domain services (RouteOptimizer, PathGenerator, CostCalculator)
- **test_infrastructure.py**: Tests for infrastructure components (HaversineDistance, ConstantSpeedEstimator)
- **test_models.py**: Tests for Pydantic models (validation, serialization)

### Integration Tests (`tests/integration/`)

- **test_api_endpoints.py**: Tests for API endpoints (health checks, route finding, error handling)

## Test Configuration

### Pytest Configuration (`pytest.ini`)

- Test discovery patterns
- Coverage reporting
- Markers for different test types
- Async test support

### Test Markers

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Slow-running tests
- `@pytest.mark.api`: API endpoint tests
- `@pytest.mark.service`: Service layer tests
- `@pytest.mark.domain`: Domain logic tests
- `@pytest.mark.infrastructure`: Infrastructure tests

## Running Tests

### Using the Test Runner Script

```bash
# Run all tests
./run_tests.py

# Run only unit tests
./run_tests.py --type unit

# Run only integration tests
./run_tests.py --type integration

# Run with coverage analysis
./run_tests.py --type coverage

# Run with verbose output
./run_tests.py --verbose

# Skip slow tests
./run_tests.py --fast

# Set custom coverage threshold
./run_tests.py --coverage-threshold 90
```

### Using Pytest Directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_utils.py

# Run tests with specific marker
pytest -m unit

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run tests in parallel
pytest -n auto

# Run only fast tests
pytest -m "not slow"
```

### Using Make (if Makefile exists)

```bash
# Run all tests
make test

# Run unit tests
make test-unit

# Run integration tests
make test-integration

# Run with coverage
make test-coverage

# Run linting
make lint

# Run type checking
make type-check
```

## Test Fixtures

### Global Fixtures (`conftest.py`)

- `client`: FastAPI test client
- `async_client`: Async test client
- `sample_location`: Sample location for testing
- `sample_restaurant`: Sample restaurant location
- `sample_customer`: Sample customer location
- `sample_order`: Sample order
- `sample_route_request`: Sample route request
- `multiple_orders`: Multiple orders for complex scenarios
- `complex_route_request`: Complex route request with multiple orders
- `empty_route_request`: Route request with no orders
- `same_location_order`: Order with same restaurant and customer location
- `zero_prep_time_order`: Order with zero prep time
- `long_prep_time_order`: Order with very long prep time

### Factory Classes (`fixtures/factories.py`)

- `LocationFactory`: Creates Location entities
- `OrderFactory`: Creates Order entities
- `RouteRequestFactory`: Creates RouteRequest objects
- `RouteResponseFactory`: Creates RouteResponse objects
- Specialized factories for different scenarios

### Static Test Data (`fixtures/test_data.py`)

- Real-world NYC locations
- Sample restaurants and customers
- Edge case scenarios
- Performance test data
- Validation test data
- Business scenario data

## Test Coverage

The test suite aims for comprehensive coverage:

- **Unit Tests**: 90%+ coverage of core business logic
- **Integration Tests**: 100% coverage of API endpoints
- **Model Tests**: 100% coverage of Pydantic models
- **Edge Cases**: Comprehensive coverage of edge cases and error conditions

### Coverage Reports

Coverage reports are generated in multiple formats:

- **Terminal**: `--cov-report=term-missing`
- **HTML**: `--cov-report=html:htmlcov` (view in `htmlcov/index.html`)
- **XML**: `--cov-report=xml` (for CI/CD integration)

## Test Data Management

### Using Factories

```python
from tests.fixtures.factories import LocationFactory, OrderFactory

# Create a random location
location = LocationFactory()

# Create a location with specific attributes
location = LocationFactory(id="custom_id", lat=40.7128, lon=-74.0060)

# Create multiple locations
locations = LocationFactory.build_batch(5)

# Create an order
order = OrderFactory()
```

### Using Static Test Data

```python
from tests.fixtures.test_data import NYC_LOCATIONS, SAMPLE_ORDERS

# Use predefined NYC locations
times_square = NYC_LOCATIONS["times_square"]

# Use sample orders
orders = SAMPLE_ORDERS[:3]
```

## Continuous Integration

### GitHub Actions

The project includes GitHub Actions workflows for:

- **Test Suite** (`.github/workflows/test.yml`): Runs tests on multiple Python versions
- **Deploy** (`.github/workflows/deploy.yml`): Builds and deploys the application

### Pre-commit Hooks

Recommended pre-commit hooks:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
      - id: flake8
        name: flake8
        entry: flake8
        language: system
        pass_filenames: true
      - id: mypy
        name: mypy
        entry: mypy
        language: system
        pass_filenames: false
        always_run: true
```

## Best Practices

### Test Organization

1. **One test file per module**: Each module has a corresponding test file
2. **Descriptive test names**: Test names clearly describe what is being tested
3. **Arrange-Act-Assert**: Tests follow the AAA pattern
4. **Single responsibility**: Each test focuses on one specific behavior

### Test Data

1. **Use factories for dynamic data**: Generate test data using factory classes
2. **Use static data for known scenarios**: Use predefined data for specific test cases
3. **Isolate test data**: Each test should be independent and not rely on other tests
4. **Clean up after tests**: Use fixtures to ensure proper cleanup

### Assertions

1. **Specific assertions**: Use specific assertions rather than generic ones
2. **Test edge cases**: Include tests for boundary conditions and error cases
3. **Test both success and failure paths**: Ensure error handling is tested
4. **Use descriptive assertion messages**: Make test failures easy to understand

### Performance

1. **Mark slow tests**: Use `@pytest.mark.slow` for tests that take longer than 1 second
2. **Use fixtures for expensive setup**: Avoid repeating expensive setup in each test
3. **Mock external dependencies**: Use mocks for external services and APIs
4. **Run fast tests first**: Structure tests so fast tests run before slow ones

## Debugging Tests

### Running Specific Tests

```bash
# Run a specific test
pytest tests/unit/test_utils.py::TestHaversineDistance::test_same_location_distance

# Run tests matching a pattern
pytest -k "test_distance"

# Run tests in a specific class
pytest tests/unit/test_utils.py::TestHaversineDistance
```

### Debug Mode

```bash
# Run tests with debug output
pytest -s -v

# Drop into debugger on failure
pytest --pdb

# Run with extra logging
pytest --log-cli-level=DEBUG
```

### Coverage Analysis

```bash
# Generate detailed coverage report
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html

# Check coverage for specific files
pytest --cov=app.services --cov-report=term-missing
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure the app module is in the Python path
2. **Fixture not found**: Check that fixtures are defined in `conftest.py` or imported properly
3. **Async test issues**: Use `pytest-asyncio` and mark async tests with `@pytest.mark.asyncio`
4. **Coverage issues**: Ensure all code paths are tested, including error conditions

### Getting Help

1. Check the pytest documentation: https://docs.pytest.org/
2. Review the FastAPI testing guide: https://fastapi.tiangolo.com/tutorial/testing/
3. Check the factory_boy documentation: https://factoryboy.readthedocs.io/
4. Review the project's test examples in the test files
