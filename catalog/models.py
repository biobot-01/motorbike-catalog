#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime)
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), index=True, nullable=False)
    name = Column(String(70), nullable=False)
    picture = Column(String, nullable=False)


class Manufacturer(Base):
    __tablename__ = 'manufacturers'

    id = Column(Integer, primary_key=True)
    slug = Column(String(250), index=True, nullable=False)
    name = Column(String(60), nullable=False)


class Motorbike(Base):
    __tablename__ = 'motorbikes'

    id = Column(Integer, primary_key=True)
    slug = Column(String(250), index=True, nullable=False)
    model = Column(String(140), nullable=False)
    year = Column(String(4), nullable=False)
    engine = Column(String(140), nullable=False)
    displacement = Column(String(10), nullable=False)
    curb_mass = Column(String(10), nullable=False)
    fuel_capacity = Column(String(10), nullable=False)
    max_power = Column(String(40), nullable=False)
    max_torque = Column(String(40), nullable=False)
    image = Column(String, nullable=False)
    created_on = Column(DateTime, default=datetime.now())
    manufacturer_id = Column(Integer, ForeignKey('manufacturers.id'))
    manufacturer = relationship(Manufacturer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)


engine = create_engine('sqlite:///motorbike_catalog.db')
Base.metadata.create_all(engine)
