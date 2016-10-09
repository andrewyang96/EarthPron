"""Entry point for EarthPron app."""

import sqlite3
import time
from datetime import datetime

from flask import Flask
from flask import g
from flask import jsonify
from flask import render_template
from flask import url_for

app = Flask(__name__)
DATABASE = 'earthpron.db'
ONE_WEEK = 604800


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


def get_current_time():
    return int(time.mktime(datetime.utcnow().timetuple()))


@app.route('/')
def index():
    return render_template('index.html',
                           stylesheet=url_for('static', filename='style.css'),
                           script=url_for('static', filename='script.js'))


@app.route('/data')
def data():
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
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
