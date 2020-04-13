import requests
from constants import GOOGLE_API_KEY
import datetime


def call_timezone_api(lat, lon):
    req = f"https://maps.googleapis.com/maps/api/timezone/json?location={lat},{lon}&key={GOOGLE_API_KEY}&timestamp=" \
          f"{datetime.datetime.now().timestamp()}"

    response = requests.get(req)
    return response.json()


def call_geocoding_api(postcode):
    req = f"https://maps.googleapis.com/maps/api/geocode/json?components=postal_code:{postcode}&key={GOOGLE_API_KEY}"
    response = requests.get(req)
    print(response.json())
    return response.json()


def get_lat_lon_for_postcode(postcode: str):
    response = call_geocoding_api(postcode)
    location = response['results'][0]['geometry']['location']
    lat, lon = location['lat'], location['lng']

    return lat, lon


if __name__ == '__main__':
    lat, lon = get_lat_lon_for_postcode('H2S 3C2')
    resp = call_timezone_api(lat, lon)

    print(resp)