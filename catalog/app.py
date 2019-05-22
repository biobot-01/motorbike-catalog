#!/usr/bin/env python3

import json
import os
from secrets import token_urlsafe

from flask import (Flask, render_template, request, redirect, url_for,
                   session as login_session, make_response)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from slugify import slugify
from requests_oauthlib import OAuth2Session

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

google_secrets_file = 'google_secrets.json'
with open(google_secrets_file) as f:
    google_secrets = json.load(f)

g_client_id = google_secrets['web']['client_id']
g_client_secret = google_secrets['web']['client_secret']
g_auth_uri = google_secrets['web']['auth_uri']
g_token_uri = google_secrets['web']['token_uri']
g_redirect_uri = google_secrets['web']['redirect_uris'][1]

scope = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


@app.route('/oauth/<provider>')
def oauth(provider):
    state = login_session['state']
    if provider == 'google':
        if request.args.get('state') != state:
            response = make_response(
                json.dumps('Invalid state parameter.'),
                401,
            )
            response.headers['Content-type'] = 'application/json'
            return response
        google = OAuth2Session(
            client_id=g_client_id,
            redirect_uri=g_redirect_uri,
            scope=scope,
            state=state,
        )
        auth_url, state = google.authorization_url(
            g_auth_uri,
            state=state,
            access_type='offline',
            prompt='consent',
        )
        return redirect(auth_url)


@app.route('/oauth2callback')
def oauth2callback():
    state = login_session['state']
    google = OAuth2Session(
        client_id=g_client_id,
        redirect_uri=g_redirect_uri,
        scope=scope,
        state=state,
    )
    auth_resp = request.url
    google.fetch_token(
        g_token_uri,
        authorization_response=auth_resp,
        client_secret=g_client_secret,
    )
    resp = google.get('https://www.googleapis.com/userinfo/v2/me')
    data = resp.json()
    return json.dumps(data)
    return redirect(url_for('index'))


@app.route('/')
def index():
    state = token_urlsafe(32)
    login_session['state'] = state
    manufacturers = session.query(Manufacturer).order_by(
        Manufacturer.slug).all()
    latest_motorbikes = session.query(Motorbike).order_by(
        Motorbike.created_on.desc()).limit(10).all()
    return render_template(
        'home.html',
        manufacturers=manufacturers,
        motorbikes=latest_motorbikes,
        STATE=state,
        CLIENT_ID=g_client_id,
    )


@app.route('/motorbikes/<manufacturer_slug>')
def motorbikes(manufacturer_slug):
    manufacturers = session.query(Manufacturer).order_by(
        Manufacturer.slug).all()
    manufacturer = session.query(Manufacturer).filter_by(
        slug=manufacturer_slug).first()
    motorbikes = session.query(
        Motorbike.model,
        Motorbike.year,
        Motorbike.slug,
    ).filter_by(manufacturer_id=manufacturer.id).order_by(
        Motorbike.slug, Motorbike.year).all()
    count = session.query(Motorbike).filter_by(
        manufacturer_id=manufacturer.id).count()
    return render_template(
        'motorbikes.html',
        manufacturers=manufacturers,
        manufacturer=manufacturer,
        motorbikes=motorbikes,
        count=count,
    )


@app.route('/motorbikes/<manufacturer_slug>/models/<motorbike_slug>')
def motorbike(manufacturer_slug, motorbike_slug):
    motorbike = session.query(Motorbike).filter_by(
            slug=motorbike_slug).first()
    return render_template('motorbike.html', motorbike=motorbike)


@app.route(
    '/motorbikes/<manufacturer_slug>/models/new',
    methods=['GET', 'POST'])
def new_motorbike(manufacturer_slug):
    manufacturer = session.query(Manufacturer).filter_by(
        slug=manufacturer_slug).first()
    if request.method == 'POST':
        model = request.form['model']
        year = request.form['year']
        engine = request.form['engine']
        displacement = request.form['displacement']
        max_power = request.form['max_power']
        max_torque = request.form['max_torque']
        fuel_capacity = request.form['fuel_capacity']
        curb_mass = request.form['curb_mass']
        image = request.form['image']
        slug = slugify(model + '-' + year)
        manufacturer_id = manufacturer.id
        if not image:
            image = '/static/img/default-bike.png'
        if (model and year and engine and displacement and
                max_power and max_torque and fuel_capacity and
                curb_mass and image and slug):
            motorbike = Motorbike(
                slug=slug,
                model=model,
                year=year,
                engine=engine,
                displacement=displacement,
                curb_mass=curb_mass,
                fuel_capacity=fuel_capacity,
                max_power=max_power,
                max_torque=max_torque,
                image=image,
                manufacturer_id=manufacturer_id,
            )
            session.add(motorbike)
            session.commit()
        return redirect(url_for(
            'motorbikes', manufacturer_slug=manufacturer_slug))
    return render_template('new-motorbike.html', manufacturer=manufacturer)


@app.route(
    '/motorbikes/<manufacturer_slug>/models/<motorbike_slug>/edit',
    methods=['GET', 'POST'])
def edit_motorbike(manufacturer_slug, motorbike_slug):
    motorbike = session.query(Motorbike).filter_by(
        slug=motorbike_slug).first()
    if request.method == 'POST':
        model = request.form['model']
        year = request.form['year']
        engine = request.form['engine']
        displacement = request.form['displacement']
        max_power = request.form['max_power']
        max_torque = request.form['max_torque']
        fuel_capacity = request.form['fuel_capacity']
        curb_mass = request.form['curb_mass']
        image = request.form['image']
        if model:
            motorbike.model = model
        if year:
            motorbike.year = year
        if model and year:
            motorbike.slug = slugify(model + '-' + year)
        elif model and not year:
            motorbike.slug = slugify(model + '-' + motorbike.year)
        elif not model and year:
            motorbike.slug = slugify(motorbike.model + '-' + year)
        else:
            motorbike.slug = slugify(motorbike.model + '-' + motorbike.year)
        if engine:
            motorbike.engine = engine
        if displacement:
            motorbike.displacement = displacement
        if max_power:
            motorbike.max_power = max_power
        if max_torque:
            motorbike.max_torque = max_torque
        if fuel_capacity:
            motorbike.fuel_capacity = fuel_capacity
        if curb_mass:
            motorbike.curb_mass = curb_mass
        if image:
            motorbike.image = image
        session.add(motorbike)
        session.commit()
        return redirect(url_for(
            'motorbike',
            manufacturer_slug=manufacturer_slug,
            motorbike_slug=motorbike.slug,
        ))
    return render_template('edit-motorbike.html', motorbike=motorbike)


@app.route(
    '/motorbikes/<manufacturer_slug>/models/<motorbike_slug>/delete',
    methods=['GET', 'POST'])
def delete_motorbike(manufacturer_slug, motorbike_slug):
    motorbike = session.query(Motorbike).filter_by(
        slug=motorbike_slug).first()
    if request.method == 'POST':
        session.delete(motorbike)
        session.commit()
        return redirect(url_for(
            'motorbikes',
            manufacturer_slug=manufacturer_slug))
    return render_template(
        'delete-motorbike.html',
        motorbike=motorbike)


def main():
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000, threaded=False)


if __name__ == '__main__':
    main()
