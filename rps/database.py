from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from rps import app

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base, engine

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    this_game = relationship("Game", backref="player")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    move = Column(String(128))
    player_id = Column(Integer, ForeignKey('players.id'))


Base.metadata.create_all(engine)