import os
from flask.ext.script import Manager
from rps import app
from rps.database import Player1, Player2, session
from rps.database import Base

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    print("https://jps-python-jonsanders-1.c9.io/")
    app.run(host='0.0.0.0', port=port)


from rps.database import Player1, Player2

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata


if __name__ == "__main__":
    manager.run()
    
    
