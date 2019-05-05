#!/usr/bin/env python3

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
# Create flask instance
app = Flask(__name__)
# Connect to database
engine = create_engine('sqlite:///../motorbike_catalog.db')
# Bind engine to metadata of Base class to access through DBSession
Base.metadata.bind = engine
# Create a DBSession instance
DBSession = sessionmaker(bind=engine)
# Create a session for the database
session = DBSession()


@app.route('/')
def index():
    return 'Welcome to the index page'


@app.route('/bikes/<manufacturer_slug>')
def bikes(manufacturer_slug):
    return 'Bikes built by {}'.format(manufacturer_slug)


@app.route('/model/<manufacturer_slug>/<motorbike_slug>')
def model(manufacturer_slug, motorbike_slug):
    return '{} {}, year {}'.format(manufacturer_slug, model, year)


def main():
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000, threaded=False)


if __name__ == '__main__':
    main()
