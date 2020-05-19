import pytest

import constants
import weather
import pandas as pd
from pathlib import Path

test_dir = Path(__file__).parent.absolute()

from tests.fixtures import test_locations


def test_darksky_class_returns_df():

    ds = weather.DarkSky()
    df = ds.df_template()

    assert isinstance(df, pd.DataFrame)


@pytest.mark.parametrize('location', test_locations)
def test_get_past_week_darksky_returns_df(location):

    ds = weather.DarkSky()
    df = ds.get_forecast_tomorrow(location.lon,
                                  location.lat)

    assert isinstance(df, pd.DataFrame)


@pytest.fixture(scope='module')
def example_forecast():
    return pd.read_csv(test_dir / 'data' / 'weather_forecast.csv',
                       parse_dates=['weather_timestamp', 'recorded_timestamp'])


class TestWeatherWindows:

    @pytest.mark.parametrize("preference,expected", [('cool', 9), ('neutral', 10), ('hot', 11)])
    def test_weather_window_differs_based_on_temperature(self, preference, expected, example_forecast):
        df = example_forecast
        preferences = weather.Preferences(temperature=preference, temperature_weighting=constants.TEMPERATURE_WEIGHTINGS,
                                              weightings=constants.DEFAULT_WEIGHTINGS)
        window_finder = weather.WeatherWindowFinder(preferences)

        window = window_finder.get_weather_window_for_forecast(df)

        assert window['weather_timestamp'].hour == expected

    @pytest.mark.skip('Incomplete implementation')
    def test_weather_window_never_exceeds_user_preference(self):
        assert False