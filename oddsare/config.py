import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI =  os.environ["DATABASE_URL"]
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "hehe")
    
class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:thinkful@localhost:5432/odssare-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
    
