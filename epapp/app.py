"""Entry point for EarthPron app."""
from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           stylesheet=url_for('static', filename='style.css'),
                           script=url_for('static', filename='script.js'))


if __name__ == '__main__':
    app.run(port=5000)
