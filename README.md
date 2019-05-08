# Item Catalog Project
Flask web application that lists motorbikes by their manufacturer.
## Project Overview
This project is about developing a web application that provides a list of items(bikes) within a variety of categories(manufacturers), & integrates third party user registration & authentication.
Authenticated users have the ability to post, edit & delete their own items.
Implements RESTful architecture for API endpoints that return JSON data of the items & categories.
## Requirements
In order to run this project, you will need to have the following:
* Python >= 3.6
* Flask >= 1.0.2
* SQLAlchemy >= 1.3.3
* requests >= 2.21.0
## Project Setup
1. Clone the git repo `$ git clone git@github.com:biobot-01/motorbike-catalog.git`
1. Change directory `$ cd motorbike-catalog`
1. Setup Python virtual environment [(venv)](https://docs.python.org/3.6/library/venv.html) `$ python3 -m venv .venv/flask`
1. Activate Python venv `$ source .venv/flask/bin/activate`
1. Update pip `$ pip install -U pip`
1. Install requirements `$ pip install -r requirements.txt`
1. Create the database `$ python catalog/models.py`
1. Add dummy data to database `$ python tests/data.py`
1. Run the application `$ python catalog/app.py`
1. Open browser & go to `http://localhost:8000`
