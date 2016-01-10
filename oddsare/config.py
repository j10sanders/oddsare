import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/oddsare"
    DEBUG = True
    SECRET_KEY = "Not secret"
    
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/odssare-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
    
