#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
from subreddits import known
import praw
import HTMLParser
import urllib, urllib2, urlparse
from alchemyapi import AlchemyAPI
import json

r = praw.Reddit(user_agent="earthporn_maps")
h = HTMLParser.HTMLParser()
API_KEY = "AIzaSyDBOe7KSp2n0VAd8XONeS60KcVLeHeuBRk"
alchemyapi = AlchemyAPI()
ACCEPTED_ENTITY_TYPES = [
    "City",
    "Company",
    "Continent",
    "Country",
    "GeographicFeature",
    "Organization",
    "Region",
    "StateOrCounty"
]

def get_hot_posts(LIMIT=10):
    ret = []
    hot_submissions = r.get_multireddit("theyangmaster", "earthporns").get_hot(limit=LIMIT)
    for item in hot_submissions:
        item.title = h.unescape(item.title)
        ret.append(item)
    return ret

def get_entities(phrase):
    res = alchemyapi.entities("text", phrase)
    ret = []
    for entity in res['entities']:
        if entity['type'] in ACCEPTED_ENTITY_TYPES:
            ret.append(entity)
    return ret

def parse_search_query(entity_list):
    ret = []
    for entity in entity_list:
        if 'disambiguation' in entity.keys():
            ret.append(entity['disambiguation']['name'])
        else:
            ret.append(entity['text'])
    return ret

def get_coordinates(location):
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address" : location, "key" : API_KEY}

    url_parts = list(urlparse.urlparse(URL))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    for k, v in query.iteritems():
        query[k] = unicode(v).encode("utf-8")
    url_parts[4] = urllib.urlencode(query)
    URL = urlparse.urlunparse(url_parts)
    
    connection = urllib2.urlopen(URL)
    stuff = connection.read()
    connection.close()
    j = json.loads(stuff)
    if (j["status"] == "ZERO_RESULTS"):
        return None
    # print j # POSSIBLE IndexError
    return j["results"][0]["geometry"]["location"]

def get_data(limit):
    print "Time of execution:", datetime.datetime.now()
    print "Limit:", limit
    ret = []
    print "Fetching Reddit posts"
    print "-"*80
    for post in get_hot_posts(limit):
        print "Processing:", unicode(post.title).encode("utf-8"), ("-- from /r/" + post.subreddit.__str__())
        append = []
        entity_list = get_entities(post.title)
        entities = parse_search_query(entity_list)
        # append country name if necessary
        if post.subreddit.__str__() in known:
            country = post.subreddit.__str__()
            print "Found a country-related subreddit:", country
            if country in entities:
                print "Not necessary to add country to location string"
            else:
                print "Adding country to location string"
                entities.append(known[country])
        search_query = " ".join(entities)
        # find coords or else calls Google Reverse Geocoding API
        coords = None
        for entity in entity_list:
            if 'disambiguation' in entity.keys() and 'geo' in entity['disambiguation'].keys():
                coords = entity['disambiguation'].split(' ')
                coords = {"lat": coords[0], "lng": coords[1]}
                print "Geographics coords found with Alchemy API:", coords
            else:
                coords = get_coordinates(search_query)
        if coords is not None:
            print unicode(search_query).encode("utf-8"), "has coords at", coords
            # TODO: manipulate URL based on domain so that they always link to images
            html = ("<h3><a target='_blank' href='{0}'>{1}</a></h3>" +
                    "<div><a target='_blank' href='http://www.reddit.com/r/{2}'>/r/{2}</a></div>" +
                    "<img alt='{3}' src='{0}' class='featured-img'>").format(post.url,
                                                                             unicode(post.title).encode("ascii", "xmlcharrefreplace"),
                                                                             post.subreddit.__str__(),
                                                                             unicode(search_query).encode("ascii", "xmlcharrefreplace"))
            append.append(html)
            append.append(coords["lat"])
            append.append(coords["lng"])
            ret.append(append)
        else:
            print "Cannot find coords for search query", search_query
        print ""
    print "Finished fetching Reddit posts"
    return {"data": ret, "timestamp": datetime.datetime.utcnow().__str__() + "+0000"}

def test():
    for post in get_hot_posts():
        entity_list = get_entities(post.title)
        entities = parse_search_query(entity_list)
        if post.subreddit.__str__() in known:
            country = post.subreddit.__str__()
            print "Found a country-related subreddit:", country
            if country in entities:
                print "Not necessary to add country to location string"
            else:
                print "Adding country to location string"
                entities.append(known[country])
        search_query = " ".join(entities)
        print "Title:", post.title
        print "URL:", post.url
        print "Subreddit:", post.subreddit
        print "Search Query:", search_query
        print ""
