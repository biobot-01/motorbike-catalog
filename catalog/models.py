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


engine = create_engine('sqlite:///../motorbike_catalog.db')
Base.metadata.create_all(engine)
