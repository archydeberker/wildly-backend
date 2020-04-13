import pytest

import weather
import pandas as pd
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


