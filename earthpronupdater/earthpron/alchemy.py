"""Functions related to AlchemyAPI."""


ACCEPTED_ENTITY_TYPES = [
    'City',
    'Company',
    'Continent',
    'Country',
    'GeographicFeature',
    'Organization',
    'Region',
    'StateOrCounty',
]

KNOWN_SUBREDDITS = {
    'AustraliaPics': 'Australia',
    'britpics': 'Great Britain',
    'ChinaPics': 'China',
    'ExplorePakistan': 'Pakistan',
    'fotosmexico': 'Mexico',
    'FrancePics': 'France',
    'GermanyPics': 'Germany',
    'GreecePics': 'Greece',
    'IncredibleIndia': 'India',
    'IrelandPics': 'Ireland',
    'Island': 'Iceland',
    'ItalyPhotos': 'Italy',
    'japanpics': 'Japan',
    'NetherlandsPics': 'Netherlands',
    'NepalPics': 'Nepal',
    'NorwayPics': 'Norway',
    'NZPhotos': 'New Zealand',
    'PeruPics': 'Peru',
    'RussiaPics': 'Russia',
    'schweiz': 'Switzerland',
    'ScottishPhotos': 'Scotland',
    'SouthKoreaPics': 'South Korea',
    'SpainPics': 'Spain',
    'SwedenPics': 'Sweden',
    'TaiwanPics': 'Taiwan',
    'TrueNorthPictures': 'Canada',
    'unitedstatesofamerica': 'USA',
}


def get_entity_words(post, alchemyapi, subreddit):
    """Get entity keywords string from a HotPost object's title via AlchemyAPI.

    If country name is given, it is appended to the end of the string.
    Returns None if AlchemyAPI couldn't find an entity of accepted type.
    """
    res = alchemyapi.entities(
        'text', post.post_title, {'language': 'english'})
    if res['status'] == 'ERROR':
        print('There has been an error:')
        print(res)
        return []

    entity_objs = [
        entity for entity in res['entities']
        if entity['type'] in ACCEPTED_ENTITY_TYPES
    ]
    if len(entity_objs) == 0:
        return None

    entity_words = [
        entity['disambiguation']['name']
        if 'disambiguation' in entity else entity['text']
        for entity in entity_objs
    ]
    if subreddit in KNOWN_SUBREDDITS:
        entity_words.append(KNOWN_SUBREDDITS[subreddit])
    return ' '.join(entity_words)
