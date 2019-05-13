#!/usr/bin/env python3

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Motorbike
# Create flask instance
app = Flask(__name__)
# Connect to database
engine = create_engine('sqlite:///motorbike_catalog.db')
# Bind engine to metadata of Base class to access through DBSession
Base.metadata.bind = engine
# Create a DBSession instance
DBSession = sessionmaker(bind=engine)
# Create a session for the database
session = DBSession()


@app.route('/')
def index():
    latest_models = session.query(Motorbike).order_by(
        Motorbike.created_on.desc()).limit(7).all()
    return render_template('home.html', models=latest_models)


@app.route('/bikes/<manufacturer_slug>')
def bikes(manufacturer_slug):
    return render_template('bikes.html')


@app.route('/model/<manufacturer_slug>/<motorbike_slug>')
def model(manufacturer_slug, motorbike_slug):
    return render_template('model.html')


def main():
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000, threaded=False)


if __name__ == '__main__':
    main()
