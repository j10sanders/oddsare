from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from oddsare import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base, engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask.ext.login import UserMixin

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    dare = Column(String(128))
    odds = Column(Integer())
    move1 = Column(Integer())
    move2 = Column(Integer())
    rebound = Column(Integer())
    move3 = Column(Integer())
    move4 = Column(Integer())
    player1 = Column(Integer, ForeignKey('users.id'))
    player2 = Column(Integer, ForeignKey('users.id'))
    #player1id= relationship("User", uselist=False, backref="player1")

class User(Base, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    email = Column(String(128), unique=True)
    password = Column(String(128))

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)