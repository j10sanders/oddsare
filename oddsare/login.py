from flask.ext.login import LoginManager

from oddsare import app
from .database import session, User
from flask import request, redirect, url_for

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login_get"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(id):
    return session.query(User).get(int(id))
    
@login_manager.unauthorized_handler
def unauthorized_callback():
    if request.path.startswith("/game/"):
        return redirect(url_for("register_get") + "?next=" + request.path)
    else:
        return redirect(url_for(login_manager.login_view) + "?next=" + request.path)