"""EarthPron utility functions."""

import HTMLParser
import json
import urllib
import urllib2
import urlparse

from alchemyapi import AlchemyAPI

from bs4 import BeautifulSoup

import praw

import pyimgur

from subreddits import known_subreddits

with open('config.json', 'r') as f:
    config = json.load(f)
    GOOGLE_API_KEY = config['GOOGLE_API_KEY']
    IMGUR_API_KEY = config['IMGUR_API_KEY']

r = praw.Reddit(user_agent='earthpron_rocks')
h = HTMLParser.HTMLParser()
imgur = pyimgur.Imgur(IMGUR_API_KEY)
alchemyapi = AlchemyAPI()
ACCEPTED_ENTITY_TYPES = [
    'City',
    'Company',
    'Continent',
    'Country',
    'GeographicFeature',
    'Organization',
    'Region',
    'StateOrCounty'
]


def get_hot_posts(limit=10):
    """Fetch the hottest posts. Limit defaults to 10."""
    multireddit = r.get_multireddit('theyangmaster', 'earthporns')
    hot_submissions = list(multireddit.get_hot(limit=limit))
    for item in hot_submissions:
        item.title = h.unescape(item.title)
    return hot_submissions


def get_entities_from_phrase(phrase):
    """Fetch entity objects from phrase via AlchemyAPI."""
    res = alchemyapi.entities('text', phrase)
    if res['status'] == 'ERROR':
        print 'There has been an error. Printing response here:'
        print res
        return []
    return filter(lambda entity: entity['type'] in ACCEPTED_ENTITY_TYPES,
                  res['entities'])


def transform_entities_to_words(entity_list):
    """Transform entity objects into words."""
    ret = []
    for entity in entity_list:
        if 'disambiguation' in entity.keys():
            ret.append(entity['disambiguation']['name'])
        else:
            ret.append(entity['text'])
    return ret


def get_coordinates(location):
    """Fetch coordinates from a phrase of entity words."""
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': location, 'key': GOOGLE_API_KEY}

    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    for k, v in query.iteritems():
        query[k] = unicode(v).encode("utf-8")
    url_parts[4] = urllib.urlencode(query)
    url = urlparse.urlunparse(url_parts)

    connection = urllib2.urlopen(url)
    stuff = connection.read()
    connection.close()
    j = json.loads(stuff)
    if (j["status"] == "ZERO_RESULTS"):
        return None
    # print j # POSSIBLE IndexError
    return j["results"][0]["geometry"]["location"]


def extract_image_url(url):
    """Try to extract image URL from URL."""
    urlcomponents = urlparse.urlparse(url)
    netloc = urlcomponents[1]
    if netloc == 'www.flickr.com':
        print 'The URL is a Flickr URL. Changing...'
        connection = urllib2.urlopen(url)
        soup = BeautifulSoup(connection, 'html.parser')
        connection.close()
        return soup.find(id='image-src')['href']
        # NOTE: sometimes there's a TypeError
    elif netloc == 'imgur.com':
        old_path = urlcomponents[2]
        if 'a/' in old_path:
            print 'The URL is an Imgur album URL. Changing...'
            pathcomponents = old_path.split('/')
            album = imgur.get_album(pathcomponents[-1])
            return album.images[0].link
        else:
            print 'The URL is a plain Imgur URL. Changing...'
            urlcomponents = urlcomponents._replace(netloc='i.imgur.com')
            urlcomponents = urlcomponents._replace(path=old_path + '.jpg')
            return urlparse.urlunparse(urlcomponents)
    else:
        return url


def process_post(post):
    """Process a post object received from get_hot_posts."""
    print 'Processing:', unicode(post.title).encode('utf-8'), (
        '-- from /r/' + post.subreddit.__str__())
    entity_objs = get_entities_from_phrase(post.title)
    if entity_objs == []:
        return None
    entity_words = transform_entities_to_words(entity_objs)

    # append country name if necessary
    if post.subreddit.__str__() in known_subreddits:
        country = post.subreddit.__str__()
        print 'Found a country-related subreddit:', country
        if country in entity_words:
            print 'Not necessary to add country to location string'
        else:
            print 'Adding country to location string'
            entity_words.append(known_subreddits[country])
    query = ' '.join(entity_words)

    # try to find coords in AlchemyAPI object
    coords = get_coordinates(query)
    if coords is None:
        return None
    else:
        try:
            print unicode(query).encode('utf-8'), 'has coords at', coords
            image_url = extract_image_url(post.url)
            return {
                'url': post.url,
                'image_url': image_url,
                'title': unicode(post.title).encode('ascii',
                                                    'xmlcharrefreplace'),
                'subreddit': post.subreddit.__str__(),
                'query': unicode(query).encode('ascii', 'xmlcharrefreplace'),
                'lat': coords['lat'],
                'lng': coords['lng'],
                'created_utc': int(post.created_utc)
            }
        except Exception as e:
            print 'An error occurred'
            print e
            return None


def test():
    """Dry run method."""
    hot_posts = get_hot_posts()
    results = filter(None, map(process_post, hot_posts))
    return results
