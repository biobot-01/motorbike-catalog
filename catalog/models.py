from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(70), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String)


class Manufacturer(Base):
    __tablename__ = 'manufacturer'

    id = Column(Integer, primary_key=True)
    name = Column(String(60), index=True, nullable=False)


class Motorbike(Base):
    __tablename__ = 'motorbike'

    id = Column(Integer, primary_key=True)
    model = Column(String(70), nullable=False)
    engine = Column(String(140), nullable=False)
    capacity = Column(String(40), nullable=False)


engine = create_engine('sqlite:///../motorbike_catalog.db')
Base.metadata.create_all(engine)
