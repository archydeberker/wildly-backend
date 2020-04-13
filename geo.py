import requests
from constants import GOOGLE_API_KEY


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
