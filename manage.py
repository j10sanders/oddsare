import os
from flask.ext.script import Manager
from oddsare import app
from oddsare.database import Game, session
from oddsare.database import Base

manager = Manager(app)

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    print("https://jps-python-jonsanders-1.c9.io/")
    app.run(host='0.0.0.0', port=port)

class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata


if __name__ == "__main__":
    manager.run()
    
    
