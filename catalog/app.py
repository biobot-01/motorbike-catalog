#!/usr/bin/env python3

import json
import os
from secrets import token_urlsafe

from flask import (Flask, render_template, request, redirect, url_for,
                   session as login_session, make_response)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from slugify import slugify
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import requests

from models import Base, User, Manufacturer, Motorbike
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

scopes = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


def create_user(login_session):
    user = User(
        name=login_session['name'],
        email=login_session['email'],
        picture=login_session['picture'],
    )
    session.add(user)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).first()
    return user.id


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


@app.route('/oauth/<provider>')
def oauth(provider):
    state = login_session['state']
    if request.args.get('state') != state:
        response = make_response(
            json.dumps('Invalid state parameter.'),
            401,
        )
        response.headers['Content-type'] = 'application/json'
        return response
    if provider == 'google':
        flow = Flow.from_client_secrets_file(
            google_secrets_file,
            scopes=scopes,
            state=state,
        )
        flow.redirect_uri = g_redirect_uri
        auth_url, state = flow.authorization_url(
            state=state,
            access_type='offline',
            prompt='consent',
        )
        return redirect(auth_url)


@app.route('/oauth2callback')
def oauth2callback():
    state = login_session['state']
    if request.args.get('error'):
        response = make_response(
            json.dumps(request.args.get('error') + ': You did not '
                       'approve the access request'),
            401,
        )
    flow = Flow.from_client_secrets_file(
        google_secrets_file,
        scopes=scopes,
        state=state,
    )
    flow.redirect_uri = g_redirect_uri
    auth_resp = request.url
    flow.fetch_token(authorization_response=auth_resp)
    credentials = flow.credentials
    credentials_info = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'id_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }
    access_token = credentials.token
    auth_url = 'https://www.googleapis.com/oauth2/v2/tokeninfo'
    params = {'access_token': access_token}
    result = requests.get(auth_url, params=params)
    data = result.json()
    if data.get('error') is not None:
        response = make_response(
            json.dumps(data['error']),
            500,
        )
        response.headers['Content-type'] = 'application/json'
        return response
    google_issued = data['issued_to']
    if g_client_id != google_issued:
        response = make_response(
            json.dumps("Token's client ID doesn't match app's ID"),
            401,
        )
        response.headers['Content-type'] = 'application/json'
        return response
    google_id = data['user_id']
    stored_credentials = login_session.get('credentials')
    stored_google_id = login_session.get('google_id')
    if stored_credentials is not None and google_id == stored_google_id:
        response = make_response(
            json.dumps('Current user is already connected'),
            200,
        )
        response.headers['Content-type'] = 'application/json'
        return response
    login_session['credentials'] = credentials_info
    login_session['google_id'] = google_id
    userinfo_url = 'https://www.googleapis.com/userinfo/v2/me'
    params = {
        'access_token': access_token,
        'alt': 'json',
    }
    user_request = requests.get(userinfo_url, params=params)
    user_data = user_request.json()
    if user_data['id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID"),
            401,
        )
        response.headers['Content-type'] = 'application/json'
        return response
    login_session['provider'] = 'google'
    login_session['name'] = user_data['name']
    login_session['picture'] = user_data['picture']
    login_session['email'] = user_data['email']
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if 'credentials' not in login_session:
        response = make_response(
            json.dumps('Current user not connected'),
            401,
        )
        response.headers['Content-type'] = 'application/json'
        return response
    credentials = Credentials(**login_session['credentials'])
    access_token = credentials.token
    revoke_url = 'https://accounts.google.com/o/oauth2/revoke'
    params = {'token': access_token}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    revoke_request = requests.post(revoke_url, params=params, headers=headers)
    status_code = revoke_request.status_code
    if status_code == 200:
        del login_session['credentials']
        del login_session['google_id']
        del login_session['name']
        del login_session['picture']
        del login_session['email']
        del login_session['provider']
        del login_session['user_id']
        response = make_response(
            json.dumps('Successfully disconnected'),
            200,
        )
        response.headers['Content-type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user'),
            400,
        )
        response.headers['Content-type'] = 'application/json'
        return response


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
        user_id = login_session['user_id']
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
                user_id=user_id,
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
