"""Script to update hot posts in the database."""

import datetime
import sqlite3

from earthpron import get_hot_posts
from earthpron import process_post

DATABASE_NAME = 'earthpron.db'
POST_LIMIT = 25


if __name__ == '__main__':
    print 'Time of execution (UTC):', datetime.datetime.utcnow()
    print 'Limit:', POST_LIMIT
    print 'Fetching Reddit posts...'

    hot_posts = get_hot_posts(POST_LIMIT)
    num_new_posts = 0
    print 'Found', len(hot_posts), 'potential posts to add'

    db = sqlite3.connect(DATABASE_NAME)
    c = db.cursor()
    print 'Opened database connection'

    for post in hot_posts:
        # first try to find if the post exists
        print 'Processing', post
        exists = c.execute(
            '''SELECT EXISTS(
                SELECT 1 FROM hot_posts WHERE url==? AND created_utc==?
            )''', (post.url, post.created_utc)).fetchall()[0][0]
        if exists:
            print 'Already exists, will not insert into database'
        else:
            print 'Inserting into database'
            post_obj = process_post(post)
            if post_obj is None:
                print 'Could not fetch all necessary information'
                print 'Aborted insert'
            else:
                num_new_posts += 1
                print post_obj
                # add to database only if the post is not None
                c.executemany('''
                INSERT INTO hot_posts
                (url, image_url, title, subreddit,
                    query, created_utc, lat, lng)
                VALUES
                (:url, :image_url, :title, :subreddit,
                    :query, :created_utc, :lat, :lng)
                ''', (post_obj,))
                print 'Insert command executed'

    db.commit()
    print 'Everything committed to database. Added', num_new_posts, 'new posts'

    c.close()
    db.close()
    print 'Database update successful'
    print
