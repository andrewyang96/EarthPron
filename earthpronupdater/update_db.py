"""Script to upsert hot posts into the database."""

from datetime import datetime
import psycopg2
import time

from post_fetcher import fetch_and_process_posts

DB_NAME = 'earthpron'
DB_USERNAME = 'postgres'
POST_LIMIT = 25


def get_current_time():
    """Get current UTC timestamp."""
    return int(time.mktime(datetime.utcnow().timetuple()))


def update_db():
    """Upsert hot posts into the database."""
    print('Time of execution:', datetime.utcnow())
    print('Limit:', POST_LIMIT)

    hot_posts = fetch_and_process_posts(limit=POST_LIMIT)
    print('Found', len(hot_posts), 'submissions with location info')

    db = psycopg2.connect(
        'dbname={0} user={1} password={2}'.format(DB_NAME, DB_USERNAME, '')
    )
    cur = db.cursor()

    num_new_posts = 0
    for post in hot_posts:
        num_new_posts += post.commit_to_db(cur)

    curr_time = get_current_time()
    cur.execute(
        'INSERT INTO update_history (timestamp, posts_added) VALUES (?, ?)',
        (curr_time, num_new_posts))
    db.commit()
    print('Committed', num_new_posts,
          'new posts to database at timestamp', curr_time)

    cur.close()
    db.close()
    print()


if __name__ == '__main__':
    update_db()
