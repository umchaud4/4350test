import os
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from database import db_session
app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'evander kane'
basedir = os.path.abspath(os.path.dirname(__file__))
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'users/login'
open_id = OpenID(app, os.path.join(basedir, 'tmp'))


from controllers import *
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
