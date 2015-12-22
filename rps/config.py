import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/rps"
    DEBUG = True
    SECRET_KEY = "Not secret"
    
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/rps-test"
    DEBUG = False
    SECRET_KEY = "Not secret"