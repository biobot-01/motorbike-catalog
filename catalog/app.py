#!/usr/bin/env python3

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Manufacturer, Motorbike
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
    manufacturers = session.query(Manufacturer).all()
    latest_models = session.query(Motorbike).order_by(
        Motorbike.created_on.desc()).limit(10).all()
    return render_template(
        'home.html',
        manufacturers=manufacturers,
        models=latest_models
    )


@app.route('/bikes/<manufacturer_slug>')
def bikes(manufacturer_slug):
    manufacturers = session.query(Manufacturer).all()
    manufacturer = session.query(Manufacturer).filter_by(
        slug=manufacturer_slug).first()
    manufacturer_models = session.query(
        Motorbike.model,
        Motorbike.year,
        Motorbike.slug,
    ).filter_by(manufacturer_id=manufacturer.id).all()
    return render_template(
        'bikes.html',
        manufacturers=manufacturers,
        manufacturer=manufacturer,
        models=manufacturer_models,
    )


@app.route('/models/<manufacturer_slug>/<motorbike_slug>')
def model(manufacturer_slug, motorbike_slug):
    manufacturer_model = session.query(Motorbike).filter_by(
            slug=motorbike_slug).first()
    return render_template('model.html', model=manufacturer_model)


@app.route('/models/<manufacturer_slug>/new', methods=['GET', 'POST'])
def new_model(manufacturer_slug):
    manufacturer = session.query(Manufacturer).filter_by(
        slug=manufacturer_slug).first()
    return render_template('new-model.html', manufacturer=manufacturer)


@app.route(
    '/models/<manufacturer_slug>/<motorbike_slug>/edit',
    methods=['GET', 'POST'])
def edit_model(manufacturer_slug, motorbike_slug):
    manufacturer_model = session.query(Motorbike).filter_by(
        slug=motorbike_slug).first()
    return render_template('edit-model.html', model=manufacturer_model)


def main():
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000, threaded=False)


if __name__ == '__main__':
    main()
