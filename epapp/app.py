"""Entry point for EarthPron app."""
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    print 'Hello world'
