"""Class definition for a hot post."""


class HotPost(object):
    """A representation of a hot post."""

    def __init__(self, post_url, post_title, subreddit, created_utc):
        """Constructor for HotPost."""
        self.post_url = post_url
        self.post_title = post_title
        self.subreddit = subreddit
        self.created_utc = created_utc

    @classmethod
    def fetch_hot_posts_from_multireddit(cls, multireddit, limit=25):
        """Fetch hot posts from given multireddit."""
        hot_submissions = multireddit.hot(limit=limit)
        return [
            HotPost(item.url, item.title, str(item.subreddit),
                    int(item.created_utc))
            for item in hot_submissions
        ]

    def commit_to_db(self, cur, keywords, lat, lng, image_url=None):
        """Insert self into given cursor's database.

        Returns False if there was conflict, else True.
        """
        cur.execute('''
            INSERT INTO hot_posts
            (url, image_url, title, subreddit, query, created_utc, lat, lng)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING''', (
            self.post_url, image_url, self.post_title, self.subreddit,
            keywords, self.created_utc, lat, lng))
        return cur.rowcount
