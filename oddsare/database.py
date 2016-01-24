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
from datetime import datetime

class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    dare = Column(String(128))
    odds = Column(Integer())
    move1 = Column(Integer())
    move2 = Column(Integer())
    rebound = Column(Integer())
    move3 = Column(Integer())
    move4 = Column(Integer())
    player1 = Column(Integer, ForeignKey('user.id'))
    player2 = Column(Integer, ForeignKey('user.id'))
    #user1= relationship("User", uselist=False, backref="user1", foreign_keys=[player1])    
    #user2= relationship("User", uselist=False, backref="user2", foreign_keys=[player2])
    
class User(Base, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique = True, index = True)
    email = Column(String(128), unique=True)
    password = Column(String(20))
    registered_on = Column('registered_on', DateTime)
    games = relationship('Game', viewonly=True, primaryjoin='or_(User.id == Game.player1, User.id == Game.player2)')
    
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)