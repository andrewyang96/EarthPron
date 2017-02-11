"""Functions related to parsing image URLs."""

from urllib.parse import urlparse
from urllib.parse import urlunparse
import requests

from bs4 import BeautifulSoup

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif']


def _extract_flickr_url(url):
    print('Detected Flickr URL')
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup.find(id='image-src')['href']


def _extract_imgur_url(url_components, imgur):
    old_path = url_components[2]
    if 'a/' in old_path:
        print('Detected Imgur album URL')
        path_components = old_path.split('/')
        album = imgur.get_album(path_components[-1])
        return album.images[0].link
    else:
        print('Detected Imgur image URL')
        url_components = url_components._replace(
            netloc='i.imgur.com', path=old_path + '.jpg')
        return urlunparse(url_components)


def _extract_gfycat_url(url_components):
    print('Detected Gfycat URL')
    old_path = url_components[2]
    url_components = url_components._replace(
        netloc='thumbs.gfycat.com', path=old_path + '-size_restricted.gif')
    return urlunparse(url_components)


def extract_image_url(post, imgur):
    """Extract image URL from post's URL.

    Return None if no image URL detected.
    """
    url_components = urlparse(post.post_url)
    if any(url_components.path.endswith(ext) for ext in IMAGE_EXTENSIONS):
        print('Detected image extension')
        return post.post_url

    netloc = url_components.netloc
    if netloc == 'www.flickr.com':
        return _extract_flickr_url(post.post_url)
    elif netloc == 'imgur.com':
        return _extract_imgur_url(url_components, imgur)
    elif netloc == 'gfycat.com':
        return _extract_gfycat_url(url_components)
    else:
        print('Did not detect image URL')
        return None
