from flask import Flask
from database import db_session
app = Flask(__name__)

from controllers import *


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
