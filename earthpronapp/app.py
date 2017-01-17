"""Entry point for EarthPron app."""

import psycopg2
import time
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask
from flask import g
from flask import jsonify
from flask import render_template
from flask import url_for

from update_db import update_db

app = Flask(__name__)
app.config['DATABASE'] = DATABASE = 'earthpron'
app.config['USER'] = DB_USERNAME = 'postgres'
ONE_WEEK = 604800


def get_db():
    """Get database object."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(
            'dbname={0} user={1} password={2}'.format(
                app.config['DATABASE'], app.config['USER'], ''
            )
        )
    return db


def get_current_time():
    """Get current UTC timestamp."""
    return int(time.mktime(datetime.utcnow().timetuple()))


@app.route('/')
def index():
    """Index handler."""
    return render_template('index.html',
                           stylesheet=url_for('static', filename='style.css'),
                           script=url_for('static', filename='script.js'))


@app.route('/data')
def data():
    """Data handler."""
    c = get_db().cursor()
    results = c.execute('SELECT * FROM hot_posts WHERE created_utc>? LIMIT 25',
                        (get_current_time() - ONE_WEEK,)).fetchall()
    column_names = tuple(description[0] for description in c.description)
    last_updated = c.execute(
        'SELECT MAX(timestamp) FROM update_history').fetchone()[0]
    c.close()
    return jsonify({
        'results': map(
            lambda result: dict(zip(column_names, result)), results),
        'count': len(results),
        'last_updated': last_updated
    })


@app.teardown_appcontext
def close_connection(exception):
    """Close database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(update_db, 'cron', hour='*')
    try:
        app.run(host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
