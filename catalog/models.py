from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('sqlite:///../motorbike_catalog.db')
Base.metadata.create_all(engine)
