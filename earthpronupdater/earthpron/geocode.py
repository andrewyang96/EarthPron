"""Functions related to Google's Geocoding API."""

import json
import requests


def get_coordinates(keywords, api_key):
    """Fetch coordinates given an entity keywords string."""
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': keywords, 'key': api_key}

    req = requests.get(url, params=params)
    j = json.loads(req.text)
    if j['status'] == 'ZERO_RESULTS':
        return None
    return j['results'][0]['geometry']['location']
