from .database import Game, session, User
import os

class IntegrityError(Exception):
    pass


def validate(user):

    user = session.query(User).filter_by(username=username).first()
    if user:
      raise IntegrityError("That username or email has already been taken")
    else:
      return user