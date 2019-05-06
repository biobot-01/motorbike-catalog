#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Manufacturer, Motorbike

# Connect to database
engine = create_engine('sqlite:///../motorbike_catalog.db')
# Bind engine to metadata of Base class to access through DBSession
Base.metadata.bind = engine
# Create a DBSession instance
DBSession = sessionmaker(bind=engine)
# Create a session for the database
session = DBSession()

manufacturers = [
    'Aprilia',
    'BMW',
    'Ducati',
    'Harley-Davidson',
    'Honda',
    'Kawasaki',
    'KTM',
    'MV Agusta',
    'Royal Enfield',
    'Suzuki',
    'Triumph',
    'Yamaha'
]


def add_manufacturers(list_of_names):
    for name in list_of_names:
        manufacturer = Manufacturer(name=name)
        session.add(manufacturer)
    session.commit()


def main():
    add_manufacturers(manufacturers)


if __name__ == '__main__':
    main()
