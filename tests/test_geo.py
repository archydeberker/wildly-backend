import geo
import numpy as np
from tests.fixtures import test_locations, TestLocation
import pytest


@pytest.mark.parametrize('location', test_locations)
def test_geocoding_returns_correct_city(location: TestLocation):
    location_result = geo.call_geocoding_api(location.place)
    assert location_result['results'][0]['address_components'][3]['long_name'] == location.city


@pytest.mark.parametrize('location', test_locations)
def test_geocoding_returns_correct_lat_lon(location: TestLocation):
    lat, lon = geo.get_lat_lon_for_place(location.place)
    np.testing.assert_almost_equal([lat, lon], [location.lat, location.lon], decimal=1)

