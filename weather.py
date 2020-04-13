import datetime

import numpy as np
import pandas as pd
import requests

from constants import DARKSKY_API_KEY


class DarkSky:
    def __init__(self):

        self.columns = [
            "location",
            "timezone",
            "time",
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

        df["time"] = df["time"].apply(lambda x: datetime.datetime.fromtimestamp(x))

        df.sort_values(by=["time", "location"], inplace=True)

        p_type = np.array([int(i) for i in (df["precipType"] == "rain").tolist()])

        df = df[self.columns]

        df["precipSigned"] = df.loc[:, "precipIntensity"].copy() * (1 - 2 * p_type)

        return df

    def get_forecast_tomorrow(self, location):
        df = self.df_template()

        lon = location["longitude"]
        lat = location["latitude"]

        r = requests.get(
            "https://api.darksky.net/forecast/%s/%1.4f,%1.4f" % (DARKSKY_API_KEY, lon, lat),
            params={"units": "si"},
        )
        j = r.json()
        for h in j["hourly"]["data"]:
            h["location"] = location["postcode"]
            df = df.append(h, ignore_index=True)

        return self.post_process(df)


if __name__ == "__main__":
    location = dict(postcode="Rumney NH", latitude=45.5017, longitude=-73.5673)
    forecast = DarkSky()
    df = forecast.get_forecast_tomorrow(location)

    print(df)
