#!/usr/bin/env python3

from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime,
                        func)
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(70), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String, nullable=False)


class Manufacturer(Base):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    slug = Column(String(250), index=True, nullable=False)
    name = Column(String(60), nullable=False)


class Motorbike(Base):
    __tablename__ = 'motorbike'

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
    created_at = Column(DateTime, server_default=func.now())
    manufacturer_id = Column(Integer, ForeignKey('manufacturer.id'))
    manufacturer = relationship(Manufacturer)


engine = create_engine('sqlite:///motorbike_catalog.db')
Base.metadata.create_all(engine)
