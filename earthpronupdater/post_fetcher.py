"""Script to fetch and process hot Reddit posts."""

from alchemyapi import AlchemyAPI
import json
import praw
import pyimgur

from earthpron.alchemy import get_entity_words
from earthpron.geocode import get_coordinates
from earthpron.hot_post import HotPost
from earthpron.image_url_parser import extract_image_url

with open('config.json', 'r') as f:
    _config = json.load(f)
    GOOGLE_API_KEY = _config['GOOGLE_API_KEY']
    IMGUR_CLIENT_ID = _config['IMGUR_CLIENT_ID']
    IMGUR_CLIENT_SECRET = _config['IMGUR_CLIENT_SECRET']
    REDDIT_CLIENT_ID = _config['REDDIT_CLIENT_ID']
    REDDIT_CLIENT_SECRET = _config['REDDIT_CLIENT_SECRET']

REDDIT_CLIENT = praw.Reddit(
    client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET,
    user_agent='earthpron_rocks')
IMGUR_CLIENT = pyimgur.Imgur(
    client_id=IMGUR_CLIENT_ID, client_secret=IMGUR_CLIENT_SECRET)
ALCHEMY_API_CLIENT = AlchemyAPI()

MULTIREDDIT_USER = 'theyangmaster'
MULTIREDDIT_NAME = 'earthporns'


def _process_post(post):
    print('Processing', post.post_title, '-- from /r/' + str(post.subreddit))

    keywords = get_entity_words(
        post, ALCHEMY_API_CLIENT, str(post.subreddit))
    if keywords is None:
        return None
    post.keywords = keywords

    coords = get_coordinates(keywords, GOOGLE_API_KEY)
    if coords is None:
        return None
    post.lat, post.lng = coords

    post.image_url = extract_image_url(post, IMGUR_CLIENT)
    return post


def fetch_and_process_posts(limit=25):
    """Fetch and process posts."""
    multireddit = REDDIT_CLIENT.multireddit('theyangmaster', 'earthporns')
    hot_posts = HotPost.fetch_hot_posts_from_multireddit(
        multireddit, limit=limit)
    processed_posts = [_process_post(post) for post in hot_posts]
    return filter(None, processed_posts)


if __name__ == '__main__':
    posts = fetch_and_process_posts()
