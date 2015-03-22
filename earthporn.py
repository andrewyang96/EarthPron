#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import praw
import HTMLParser
import urllib, urllib2, urlparse
import json
from bs4 import BeautifulSoup
r = praw.Reddit(user_agent="example")
h = HTMLParser.HTMLParser()
API_KEY = "AIzaSyDBOe7KSp2n0VAd8XONeS60KcVLeHeuBRk"

def get_hot_posts(LIMIT=10):
    ret = []
    hot_submissions = r.get_multireddit("theyangmaster", "earthporns").get_hot(limit=LIMIT)
    for item in hot_submissions:
        item.title = h.unescape(item.title)
        ret.append(item)
    return ret


def get_nlp(phrase):
    URL = "http://nlp.stanford.edu:8080/ner/process"
    params = {"classifier": "english.muc.7class.distsim.crf.ser.gz",
              "outputFormat": "inlineXML", "preserveSpacing": "true",
              "input": phrase, "Process": "Submit Query"}

    url_parts = list(urlparse.urlparse(URL))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    for k, v in query.iteritems():
        query[k] = unicode(v).encode("utf-8")
    url_parts[4] = urllib.urlencode(query)
    URL = urlparse.urlunparse(url_parts)

    connection = urllib2.urlopen(URL)
    html = connection.read()
    connection.close()

    start = html.find("&lt;")
    end = html.find('<div id="Footer">')
    return BeautifulSoup("<xml>" + h.unescape(html[start:end]).rstrip() + "</xml>", "html.parser")

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
    return j["results"][0]["geometry"]["location"]

def get_data(limit):
    print "Execution time:", datetime.datetime.now()
    print "Limit:", limit
    ret = []
    print "Fetching Reddit posts"
    for post in get_hot_posts(limit):
        print "Processing:", post.title, ("-- from /r/" + post.subreddit.__str__())
        append = []
        nlp = get_nlp(post.title)
        location = " ".join([e.string for e in nlp.find_all(["organization", "location"])])
        # TODO: insert country based on subreddit
        coords = get_coordinates(location)
        if coords is not None:
            print location, "has coords at", coords
            html = ("<h3><a href='{0}'>{1}</a></h3>" +
                    "<div><a href='http://www.reddit.com/r/{2}'>/r/{2}</a></div>" +
                    "<img alt='{3}' src='{0}' class='featured-img'>").format(post.url,
                                                                             unicode(post.title).encode("ascii", "xmlcharrefreplace"),
                                                                             post.subreddit.__str__(),
                                                                             unicode(location).encode("ascii", "xmlcharrefreplace"))
            append.append(html)
            append.append(coords["lat"])
            append.append(coords["lng"])
            ret.append(append)
        else:
            print "Cannot find coords for search query", location
    print "Finished fetching Reddit posts"
    return ret

def test():
    for post in get_hot_posts():
        nlp = get_nlp(post.title)
        print "Title:", post.title
        print "Location Query:", get_locations(nlp)
        print "URL: ", post.url
        print get_coordinates(get_locations(nlp))
        print ""
