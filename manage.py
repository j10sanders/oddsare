import os
from flask.ext.script import Manager
from oddsare import app
from oddsare.database import Game, session, User
from oddsare.database import Base
from getpass import getpass
from werkzeug.security import generate_password_hash

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    print("https://jps-python-jonsanders-1.c9.io/")
    app.run(host='0.0.0.0', port=port)


from flask.ext.migrate import Migrate, MigrateCommand
from oddsare.database import Base

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)


@manager.command
def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    while len(password) < 8 or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
    user = User(username=username, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()
if __name__ == "__main__":
    manager.run()
    
    
