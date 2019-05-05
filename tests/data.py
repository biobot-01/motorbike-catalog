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


def main():
    for name in manufacturers:
        manufacturer = Manufacturer(name=name)
        session.add(manufacturer)
    session.commit()


if __name__ == '__main__':
    main()
