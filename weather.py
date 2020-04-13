import datetime
import re

import numpy as np
import pandas as pd
import requests

from constants import DARKSKY_API_KEY

camel_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')
name_mapper = lambda x: camel_case_pattern.sub('_', x).lower()


class DarkSky:
    def __init__(self):

        self.columns = [
            "weather_timestamp",
            "recorded_timestamp",
            "summary",
            "icon",
            "precipIntensity",
            "precipProbability",
            "precipType",
            "temperature",
            "apparentTemperature",
            "dewPoint",
            "humidity",
            "pressure",
            "windSpeed",
            "windGust",
            "windBearing",
            "cloudCover",
            "uvIndex",
            "visibility",
            "ozone",
        ]

    def df_template(self):
        """ Returns basic dataframe with DarkSky columns."""

        return pd.DataFrame(columns=self.columns)

    def post_process(self, df):
        """ Post-process df which comes from a DarkSky API call"""

        df["weather_timestamp"] = df["time"].apply(lambda x: datetime.datetime.fromtimestamp(x))
        df["recorded_timestamp"] = datetime.datetime.now()
        df.sort_values(by=["time"], inplace=True)
        df = df[self.columns]
        df.rename(axis=1, mapper=name_mapper, inplace=True)
        return df

    @staticmethod
    def _filter_for_tomorrow(df: pd.DataFrame):

        today = datetime.datetime.now().date()
        df['weather_date'] = df['weather_timestamp'].apply(lambda x: x.date())

        df = df.loc[df['weather_date'] == today + datetime.timedelta(days=1)]
        df.drop('weather_date', axis=1, inplace=True)
        return df

    #TODO: refactor this to avoid pandas at all, will be faster
    def get_forecast_tomorrow(self, longitude, latitude):
        df = self.df_template()
        r = requests.get(
            "https://api.darksky.net/forecast/%s/%1.4f,%1.4f?exclude=[currently, minutely]" % (DARKSKY_API_KEY, longitude, latitude),
            params={"units": "si"},
        )
        j = r.json()
        for h in j["hourly"]["data"]:
            df = df.append(h, ignore_index=True)

        df = self.post_process(df)
        df = self._filter_for_tomorrow(df)

        return df


def get_weather_window_for_forecast(df, time_now):
    """Get the best weather period for the following day"""




if __name__ == "__main__":
    location = dict(postcode="Rumney NH", latitude=45.5017, longitude=-73.5673)
    forecast = DarkSky()
    df = forecast.get_forecast_tomorrow(location['longitude'], location['latitude'])

    print(df)
