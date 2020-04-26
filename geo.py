import requests
from constants import GOOGLE_API_KEY
import datetime


def call_timezone_api(lat, lon):
    req = f"https://maps.googleapis.com/maps/api/timezone/json?location={lat},{lon}&key={GOOGLE_API_KEY}&timestamp=" \
          f"{datetime.datetime.now().timestamp()}"

    response = requests.get(req)
    return response.json()


def call_geocoding_api(place):
    req = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={GOOGLE_API_KEY}"
    response = requests.get(req)
    print(response.json())
    return response.json()


def get_lat_lon_for_place(place: str):
    response = call_geocoding_api(place)
    location = response['results'][0]['geometry']['location']
    lat, lon = location['lat'], location['lng']

    return lat, lon


def get_timezone_for_lat_lon(lat: str, lon: str):
    j = call_timezone_api(lat, lon)
    return j['timeZoneId']


if __name__ == '__main__':
    lat, lon = get_lat_lon_for_place('Redland, Bristol, UK')
    resp = call_timezone_api(lat, lon)

    print(resp)