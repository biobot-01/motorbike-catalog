# Item Catalog Project
Flask web application that lists motorbikes by their manufacturer.

## Contents
* [Project Overview](#project-overview)
* [Requirements](#requirements)
* [Project Setup](#project-setup)
* [Setting up Google OAuth 2.0](#setting-up-google-oauth-20)
* [Setting up Github OAuth 2.0](#setting-up-github-oauth-20)

## Project Overview
This project is about developing a web application that provides a list of items(bikes) within a variety of categories(manufacturers), & integrates third party user registration & authentication.
Authenticated users have the ability to post, edit & delete their own items.
Implements RESTful architecture for API endpoints that return JSON data of the items & categories.

## Requirements
In order to run this project, you will need to have the following:
* Python >= 3.6
* Flask >= 1.0.3
* google-auth >= 1.6.3
* google-auth-httplib2 >= 0.0.3
* google-auth-oauthlib >= 0.3.0
* httplib2 >= 0.13.0
* oauthlib >= 3.0.1
* python-slugify >= 3.0.2
* requests >= 2.22.0
* requests-oauthlib >= 1.2.0
* SQLAlchemy >= 1.3.4

## Project Setup
1. Clone the git repo `$ git clone git@github.com:biobot-01/motorbike-catalog.git`
1. Change directory `$ cd motorbike-catalog`
1. Setup [Google Client ID](#setting-up-google-oauth-20)
1. Setup [Github Client ID](#setting-up-github-oauth-20)
1. Setup Python virtual environment [(venv)](https://docs.python.org/3.6/library/venv.html) `$ python3 -m venv .venv/flask`
1. Activate Python venv `$ source .venv/flask/bin/activate`
1. Update pip `$ pip install -U pip`
1. Install requirements `$ pip install -r requirements.txt`
1. Create the database `$ python catalog/models.py`
1. Add dummy data to database `$ python database_setup.py`
1. Run the application `$ python catalog/app.py`
1. Open browser & go to `http://localhost:8000`

## Setting up Google OAuth 2.0
This is required to authenticate users signing into the application. You can refer to [Google Oauth 2.0](https://developers.google.com/identity/protocols/OAuth2) for further information.
To create an OAuth 2.0 client ID in the console:
1. Go to [Google Developers Console](https://console.developers.google.com).
1. From the project list, create a new one.
1. If the APIs & Services page isn't already open, open the console left side menu and select __APIs & Services__.
1. On the left, click __Credentials__.
1. Click __Create Credentials__, then select __OAuth client ID__.
1. Click __Configure consent screen__.
1. Enter the __Application name__ Motorbike Catalog and click __Save__ at the bottom
1. Select Application type to __Web application__.
1. Add a name for your client id, __not__ the name of your app.
1. Add __Authorized JavaScript origins__ URI type http://localhost:8000 and press Enter.
1. Add __Authorized redirect URIs__ type http://localhost:8000 and press Enter, repeat for http://localhost:8000/google/callback.
1. Click __Create__.
1. You will now see your new client ID created, at the very right click download json, download this file to your project root directory (motorbike-catalog) and rename it __google_secrets.json__.

## Setting up Github OAuth 2.0
This is required to authenticate users signing into the application. You can refer to [Github Oauth 2.0](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/) for further information.
The link is a step-by-step guide which you can follow.
1. Set __Homepage URL__ to http://localhost:8000.
1. The __User authorization callback URL__ must be http://localhost:8000/github/callback.
1. Once you have registered the app, it will give you the __Client ID__ and __Client Secret__.
1. In the project root directory there is a file called github_secrets_example.json. Rename this file to github_secrets.json.
1. Enter the __Client ID__ and __Client Secret__ int this file.
