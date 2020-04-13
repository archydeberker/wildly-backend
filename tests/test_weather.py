import weather
import pandas as pd
from tests.fixtures import location_dict


def test_darksky_class_returns_df():

    ds = weather.DarkSky()
    df = ds.df_template()

    assert isinstance(df, pd.DataFrame)


def test_get_past_week_darksky_returns_df(location_dict):

    ds = weather.DarkSky()
    df = ds.get_nextweek_darksky(location_dict)

    assert isinstance(df, pd.DataFrame)
