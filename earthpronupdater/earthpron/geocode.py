"""Functions related to Google's Geocoding API."""

import json
import requests


def get_coordinates(keywords, google_api_key):
    """Fetch coordinates given an entity keywords string.

    Returns None if Google's Geocoding API couldn't find coordinates.
    Otherwise returns a tuple (lat, lng).
    """
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': keywords, 'key': google_api_key}

    req = requests.get(url, params=params)
    j = json.loads(req.text)
    if j['status'] == 'ZERO_RESULTS':
        return None

    coords = j['results'][0]['geometry']['location']
    if coords is None:
        return None
    return (coords['lat'], coords['lng'])
