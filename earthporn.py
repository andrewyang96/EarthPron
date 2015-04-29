#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
from subreddits import known
from config import GOOGLE_API_KEY, IMGUR_API_KEY
import praw
import pyimgur
import HTMLParser
import urllib, urllib2, urlparse
from alchemyapi import AlchemyAPI
import json
import urllib2
from bs4 import BeautifulSoup
import os

r = praw.Reddit(user_agent="earthporn_maps")
h = HTMLParser.HTMLParser()
imgur = pyimgur.Imgur(IMGUR_API_KEY)
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
    params = {"address" : location, "key" : GOOGLE_API_KEY}

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
            try:
                print unicode(search_query).encode("utf-8"), "has coords at", coords
                imgurl = get_url(post.url)
                html = ("<h3><a target='_blank' href='{0}'>{2}</a></h3>" +
                        "<div><a target='_blank' href='http://www.reddit.com/r/{3}'>/r/{3}</a></div>" +
                        "<img alt='{4}' src='{1}' class='featured-img'>").format(post.url, imgurl,
                                                                                 unicode(post.title).encode("ascii", "xmlcharrefreplace"),
                                                                                 post.subreddit.__str__(),
                                                                                 unicode(search_query).encode("ascii", "xmlcharrefreplace"))
                append.append(html)
                append.append(coords["lat"])
                append.append(coords["lng"])
                ret.append(append)
            except Exception as e:
                print "Error fetching coordinates. Error printed below:"
                print e
        else:
            print "Cannot find coords for search query", search_query
        print ""
    print "Finished fetching Reddit posts"
    return {"data": ret, "timestamp": datetime.datetime.utcnow().__str__() + "+0000"}

def get_url(url):
    urlcomponents = urlparse.urlparse(url)
    netloc = urlcomponents[1]
    if netloc == "www.flickr.com":
        print "The URL is a Flickr URL. Changing..."
        connection = urllib2.urlopen(url)
        soup = BeautifulSoup(connection)
        connection.close()
        # Find #image-src tag and take its href attribute
        return soup.find(id="image-src")["href"] # NOTE: sometimes there's a TypeError
    elif netloc == "imgur.com":
        old_path = urlcomponents[2]
        if "a/" in old_path:
            print "The URL is an Imgur album URL. Changing..."
            pathcomponents = old_path.split('/')
            album = imgur.get_album(pathcomponents[-1])
            return album.images[0].link
        else:
            print "The URL is a plain Imgur URL. Changing..."
            # Change netloc to "i.imgur.com" and append ".jpg" to path
            urlcomponents = urlcomponents._replace(netloc="i.imgur.com")
            urlcomponents = urlcomponents._replace(path=old_path+".jpg")
            return urlparse.urlunparse(urlcomponents)
    else:
        return url

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
