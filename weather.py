import datetime
import re

import pandas as pd
import requests

import constants
from constants import DARKSKY_API_KEY

camel_case_pattern = re.compile(r'(?<!^)(?=[A-Z])')
name_mapper = lambda x: camel_case_pattern.sub('_', x).lower()


class DarkSky:

    columns = [
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
    def get_forecast_tomorrow(self, longitude: str, latitude: str):
        df = self.df_template()
        r = requests.get(
            f"https://api.darksky.net/forecast/{DARKSKY_API_KEY}/{latitude},{longitude}?exclude=[currently, minutely]",
            params={"units": "si"},
        )
        j = r.json()
        for h in j["hourly"]["data"]:
            df = df.append(h, ignore_index=True)

        df = self.post_process(df)
        df = self._filter_for_tomorrow(df)

        return df


class WeatherWindowFinder:
    def __init__(self,
                 start_hour: int = 7,
                 end_hour: int = 19,
                 weightings: dict = constants.DEFAULT_WEIGHTINGS):

        self.weightings = weightings
        self.possible_window_start = start_hour
        self.possible_window_end = end_hour

    def filter_for_latest_forecasts(self, df: pd.DataFrame):
        latest_forecast = df['recorded_timestamp'].max()
        return df.loc[df['recorded_timestamp'] == latest_forecast]

    def filter_for_working_day(self, df: pd.DataFrame):
        df['hours'] = df['weather_timestamp'].apply(lambda x: x.hour)
        return df.loc[(df['hours'] > self.possible_window_start) &
                    (df['hours'] < self.possible_window_end)]

    def get_weather_window_for_forecast(self, df: pd.DataFrame):

        df = self.filter_for_latest_forecasts(df)
        df = self.filter_for_working_day(df)

        for columns_to_score, weight in self.weightings.items():
            df[columns_to_score + '_score'] = df[columns_to_score]*weight

        df['total_score'] = df.filter(like='_score').sum(axis=1)

        return df.loc[df['total_score'].idxmax()]


if __name__ == "__main__":
    location = dict(place="Rumney NH", latitude=45.5017, longitude=-73.5673)
    forecast = DarkSky()
    df = forecast.get_forecast_tomorrow(location['longitude'], location['latitude'])

    print(df)
